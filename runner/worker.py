"""Ansible-Lab-Runner als Datei-Arbeiter — ohne jede Netzwerkschnittstelle.

Warum kein HTTP mehr (Stand 2026-07-21):
Der Runner lief zuerst als HTTP-Dienst in einem eigenen internen Netz. Auf dem
Zielsystem (Coolify) hängt aber jeder Dienst zusätzlich im Projekt-Netz, und das
ist NICHT intern: Aus dem Runner heraus waren das Internet (HTTPS) sowie
Datenbank und Backend erreichbar. Die Zusage „kein Zugriff auf Daten, kein Weg
nach draußen" war damit falsch.

Jetzt läuft der Container mit `network_mode: none`. Er hat keine Adresse, keine
Namensauflösung, keinen Socket nach außen — ein Playbook kann per Netz nichts
erreichen, weil kein Netz existiert. Das ist eine strukturelle Grenze und keine
Firewall-Regel, die jemand später versehentlich entfernt.

Auftrag und Ergebnis laufen über ein gemeinsames Volume:
  <queue>/in/<id>.json    vom Backend geschrieben (atomar per rename)
  <queue>/out/<id>.json   vom Runner geschrieben (atomar per rename)

Was das NICHT löst: Ein Playbook kann weiterhin im Runner-Container Rechenzeit
verbrauchen und in dessen Dateisystem schreiben. Dafür gelten weiter Zeitgrenze,
Parallelitätsgrenze, tmpfs und die Container-Limits.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

QUEUE = Path(os.getenv("RUNNER_QUEUE_DIR", "/queue"))
TIMEOUT_SECONDS = float(os.getenv("RUNNER_TIMEOUT", "30"))
MAX_OUTPUT_BYTES = int(os.getenv("RUNNER_MAX_OUTPUT", "65536"))
MAX_PARALLEL = int(os.getenv("RUNNER_MAX_PARALLEL", "2"))
# Wie viele Auftraege der Runner hoechstens gleichzeitig BEANSPRUCHT hat
# (laufend + im Executor wartend) - nicht zu verwechseln mit MAX_PARALLEL,
# das nur begrenzt, wie viele davon GLEICHZEITIG laufen. Siehe _runde().
MAX_QUEUE_DEPTH = int(os.getenv("RUNNER_MAX_QUEUE_DEPTH", str(MAX_PARALLEL * 2)))
ANSIBLE_BIN = os.getenv("ANSIBLE_PLAYBOOK_BIN", "ansible-playbook")
POLL_SECONDS = float(os.getenv("RUNNER_POLL_SECONDS", "0.2"))

WORKSPACE_ROOT = Path(os.getenv("RUNNER_WORKSPACE_ROOT", "/tmp/lab-workspaces"))
WORKSPACE_MAX_AGE_SECONDS = float(os.getenv("RUNNER_WORKSPACE_MAX_AGE", str(12 * 3600)))
# Aufträge, die niemand mehr abholt (Backend neu gestartet), sollen nicht ewig
# liegen bleiben und Arbeit erzeugen.
JOB_MAX_AGE_SECONDS = float(os.getenv("RUNNER_JOB_MAX_AGE", "300"))

DEFAULT_INVENTORY = "[lab]\nlabhost ansible_connection=local\n"

# Änderung 1 (docs/ideen/2026-07-22-lab-erweiterung.md): Auftragsarten jenseits
# von Ansible. Ohne Konfiguration ändert sich nichts — Standard ist genau die
# eine Art, die es bisher gab.
RUNNER_KINDS = {
    teil.strip() for teil in os.getenv("RUNNER_KINDS", "ansible").split(",") if teil.strip()
}

OPENSSL_BIN = os.getenv("OPENSSL_BIN", "openssl")
GIT_BIN = os.getenv("GIT_BIN", "git")
# Eigene, kurze Zeitgrenzen je Werkzeug: openssl/git sind schnell, eine knappe
# Grenze schützt die Parallelitätsgrenze (siehe Änderung 2/3 im Entwurf).
OPENSSL_TIMEOUT_SECONDS = float(os.getenv("RUNNER_OPENSSL_TIMEOUT", "10"))
GIT_TIMEOUT_SECONDS = float(os.getenv("RUNNER_GIT_TIMEOUT", "15"))

MAX_TOOL_FILES = 10
MAX_TOOL_FILE_BYTES = 32_768
MAX_TOOL_COMMANDS = 6
MAX_TOOL_COMMAND_CHARS = 512
DATEINAME_MUSTER = re.compile(r"^[A-Za-z0-9._-]{1,64}$")

# Fest statt "jetzt": sonst ist der Commit-Hash bei jedem Lauf ein anderer und
# Aufgabenstellungen können sich nicht auf einen bestimmten Hash beziehen.
GIT_FIXED_DATE = "2024-01-01T00:00:00+00:00"


def log(*teile: object) -> None:
    print(*teile, file=sys.stderr, flush=True)


def _clip(text: str) -> tuple[str, bool]:
    roh = text.encode("utf-8", "replace")
    if len(roh) <= MAX_OUTPUT_BYTES:
        return text, False
    return roh[:MAX_OUTPUT_BYTES].decode("utf-8", "ignore") + "\n\n[Ausgabe gekürzt]", True


def _workspace(kennung: str) -> Path:
    """Dauerhaftes Arbeitsverzeichnis je Teilnehmer (siehe lab_dir im Playbook).

    Ohne diese Trennung erbte der zweite Mensch den Zustand des ersten und die
    Idempotenz-Übung wäre wertlos.
    """
    sicher = "".join(z for z in kennung if z.isalnum() or z in "_-")[:64]
    if not sicher:
        # Rohwerte, die der Filter komplett auffrisst (nur Punkte, Pfadtrenner,
        # Leerzeichen), liefen vorher alle auf denselben Ordner "gast" und haetten
        # sich damit ein Arbeitsverzeichnis geteilt. Das Backend schickt zwar immer
        # einen HMAC-Hexwert, der das nie ausloest — aber die Trennung der
        # Teilnehmenden soll nicht davon abhaengen, dass die Eingabe wohlgeformt
        # ist. Ein Hash des Rohwerts bleibt eindeutig UND ueber Laeufe stabil.
        sicher = "x" + hashlib.sha256(kennung.encode("utf-8")).hexdigest()[:16]
    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)
    jetzt = time.time()
    for eintrag in WORKSPACE_ROOT.iterdir():
        try:
            if eintrag.is_dir() and jetzt - eintrag.stat().st_mtime > WORKSPACE_MAX_AGE_SECONDS:
                shutil.rmtree(eintrag, ignore_errors=True)
        except OSError:
            pass
    verzeichnis = WORKSPACE_ROOT / sicher
    verzeichnis.mkdir(parents=True, exist_ok=True)
    return verzeichnis


def _mit_zeitgrenze_ausfuehren(argv: list[str], cwd: Path, env: dict[str, str],
                                zeitgrenze: float) -> tuple[int, bytes, bool]:
    """Wie `subprocess.run(argv, ..., timeout=zeitgrenze)`, beendet bei
    Zeitueberschreitung aber die GESAMTE Prozessgruppe des gestarteten
    Prozesses statt nur ihn selbst.

    Hintergrund (docs/lab-sicherheit.md, "Harte Zeitgrenze je Lauf"): Ein
    Playbook mit z.B. `shell: sleep 9999 &` startet einen eigenen
    Kindprozess. `subprocess.run(...)` ruft beim Abbruch `kill()` nur auf
    den direkt gestarteten Prozess (hier: ansible-playbook) - was DER
    seinerseits gestartet hat, lief bisher unbeeindruckt weiter und
    unterlief damit die Zusage einer harten Zeitgrenze je Lauf.

    POSIX (Produktion - der Runner faehrt ausschliesslich im Linux-
    Container): `start_new_session=True` macht den gestarteten Prozess zur
    Sitzungs- UND Gruppenfuehrerin einer neuen Prozessgruppe. Alles, was er
    selbst startet, erbt diese Gruppe (sofern es sie nicht explizit
    verlaesst) - `os.killpg` trifft deshalb auch Kinder, die der Prozess
    selbst hervorgebracht hat.

    Windows (nur die Entwicklungsmaschine - dort laufen ausschliesslich die
    Tests, niemals die Produktion): POSIX-Prozessgruppen gibt es dort nicht.
    `proc.kill()` bleibt auf den direkten Kindprozess beschraenkt; ein von
    ihm gestarteter Enkelprozess ueberlebt den Abbruch weiterhin. Das ist
    ein bewusst hingenommener, dokumentierter Unterschied - keine
    vorgetaeuschte Gleichwertigkeit zum POSIX-Verhalten.

    Rueckgabe: (rc, stdout_bytes, timed_out). Bei Abbruch ist rc IMMER 124,
    stdout_bytes enthaelt die bis zum Abbruch angefallene Teilausgabe.
    """
    posix = sys.platform != "win32"
    proc = subprocess.Popen(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, start_new_session=posix)
    try:
        roh, _ = proc.communicate(timeout=zeitgrenze)
        return proc.returncode, roh, False
    except subprocess.TimeoutExpired:
        if posix:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except ProcessLookupError:
                pass  # zwischen Timeout und Signal bereits beendet
        else:
            proc.kill()
        # Nach dem Signal erneut abholen: liefert die bis zum Abbruch
        # angefallene Teilausgabe und vermeidet einen Zombie-Prozess. Der
        # kurze Nachlauf hier ist die Ausnahme - ein totes/gekilltes
        # Prozessbaum-Ende raeumt sich in aller Regel sofort auf.
        try:
            roh, _ = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            roh, _ = proc.communicate()
        return 124, roh, True


def _run_ansible(auftrag: dict) -> dict:
    playbook = str(auftrag.get("playbook", ""))[:16_000]
    inventar = auftrag.get("inventory") or DEFAULT_INVENTORY
    extra_vars = auftrag.get("extra_vars")
    check = bool(auftrag.get("check"))
    arbeitsplatz = _workspace(str(auftrag.get("workspace", "gast")))

    laufverzeichnis = Path(tempfile.mkdtemp(prefix="lauf-"))
    begonnen = time.monotonic()
    abgebrochen = False
    try:
        (laufverzeichnis / "playbook.yml").write_text(playbook, encoding="utf-8")
        (laufverzeichnis / "inventory.ini").write_text(str(inventar)[:4_000], encoding="utf-8")

        argumente = [ANSIBLE_BIN, "-i", "inventory.ini", "playbook.yml",
                     "--extra-vars", f"lab_dir={arbeitsplatz}"]
        if check:
            argumente.append("--check")
        if extra_vars:
            # Nach lab_dir: eigene Angaben der Teilnehmenden gewinnen.
            argumente += ["--extra-vars", str(extra_vars)[:1_000]]

        umgebung = {
            "PATH": os.getenv("PATH", "/usr/local/bin:/usr/bin:/bin"),
            "HOME": str(laufverzeichnis),
            "TMPDIR": str(laufverzeichnis),
            "LANG": "C.UTF-8",
            "ANSIBLE_LOCAL_TEMP": str(laufverzeichnis / ".ansible-tmp"),
            "ANSIBLE_REMOTE_TEMP": str(laufverzeichnis / ".ansible-tmp"),
            "ANSIBLE_RETRY_FILES_ENABLED": "0",
            "ANSIBLE_NOCOLOR": "1",
            "ANSIBLE_DEPRECATION_WARNINGS": "0",
            "ANSIBLE_SYSTEM_WARNINGS": "0",
            # Ohne das steht ueber JEDEM Lauf eine Warnung, dass der
            # Python-Interpreter automatisch gefunden wurde. Im Container ist
            # genau ein Interpreter installiert, die Warnung hat also keinen
            # Erkenntniswert und lenkt von der eigentlichen Ausgabe ab.
            # "auto_silent" behaelt die automatische Erkennung und schweigt nur.
            "ANSIBLE_PYTHON_INTERPRETER": "auto_silent",
            # Nur Interpreter-Rauschen unterdrücken; Ansibles eigene Meldungen
            # bleiben sichtbar, sie sind Lernstoff.
            "PYTHONWARNINGS": "ignore::SyntaxWarning",
        }
        # Testbarkeit auf der Windows-Entwicklungsmaschine (runner/tests):
        # Ohne SystemRoot kann ein Windows-Kindprozess seine kryptografische
        # Zufallsquelle nicht initialisieren und stuerzt sofort ab (CPython
        # _Py_HashRandomization_Init). Betroffen ist JEDER Unterprozess, nicht
        # nur ansible-playbook - das hat die Zeitgrenzen-Tests zunaechst zum
        # Absturz statt zum Timeout gebracht. In Produktion laeuft der Runner
        # ausschliesslich im Linux-Container, wo SystemRoot nicht existiert;
        # dieser Zweig hat dort keine Wirkung.
        if sys.platform == "win32":
            systemroot = os.getenv("SystemRoot")
            if systemroot:
                umgebung["SystemRoot"] = systemroot

        rc, roh, abgebrochen = _mit_zeitgrenze_ausfuehren(
            argumente, laufverzeichnis, umgebung, TIMEOUT_SECONDS)
        text = roh.decode("utf-8", "replace")
        if abgebrochen:
            text += (f"\n\nAbgebrochen: Der Lauf hat die Zeitgrenze von "
                     f"{TIMEOUT_SECONDS:.0f} Sekunden überschritten.")

        text, gekappt = _clip(text)
        return {"rc": rc, "output": text, "truncated": gekappt,
                "duration_ms": int((time.monotonic() - begonnen) * 1000),
                "timed_out": abgebrochen}
    finally:
        shutil.rmtree(laufverzeichnis, ignore_errors=True)


# ---------------------------------------------------------------------------
# Änderung 2/3: gemeinsame Ausführung für openssl und git.
# ---------------------------------------------------------------------------

def _dateiname_gueltig(name: object) -> bool:
    if not isinstance(name, str):
        return False
    if not DATEINAME_MUSTER.match(name):
        return False
    # ".." besteht nur aus erlaubten Zeichen, ist als Pfadsegment aber ein
    # Verzeichniswechsel nach oben - das Muster allein fängt das nicht ab.
    return name not in (".", "..")


def _dateien_pruefen(dateien: object) -> str | None:
    if not isinstance(dateien, dict):
        return "„files“ muss ein Objekt aus Dateiname -> Inhalt sein."
    if len(dateien) > MAX_TOOL_FILES:
        return f"Zu viele Dateien: {len(dateien)} (höchstens {MAX_TOOL_FILES})."
    for name, inhalt in dateien.items():
        if not _dateiname_gueltig(name):
            return (f"Unzulässiger Dateiname: {name!r} (erlaubt sind Buchstaben, "
                     f"Ziffern, '.', '_', '-', höchstens 64 Zeichen, kein Pfadtrenner).")
        umfang = len(str(inhalt).encode("utf-8", "replace"))
        if umfang > MAX_TOOL_FILE_BYTES:
            return f"Datei {name!r} ist zu groß: {umfang} Bytes (höchstens {MAX_TOOL_FILE_BYTES})."
    return None


def _befehle_pruefen(befehle: object) -> str | None:
    if not isinstance(befehle, list) or not befehle:
        return "„commands“ muss eine nichtleere Liste von Befehlszeilen sein."
    if len(befehle) > MAX_TOOL_COMMANDS:
        return f"Zu viele Befehle: {len(befehle)} (höchstens {MAX_TOOL_COMMANDS})."
    for befehl in befehle:
        if not isinstance(befehl, str) or not befehl.strip():
            return "Leerer Befehl abgelehnt."
        if len(befehl) > MAX_TOOL_COMMAND_CHARS:
            return f"Befehl zu lang: {len(befehl)} Zeichen (höchstens {MAX_TOOL_COMMAND_CHARS})."
    return None


def _argv_bauen(befehl: str, art: str, binaer: str) -> list[str] | None:
    """Zerlegt eine Lernenden-Kommandozeile ohne Shell.

    `shlex.split`, dann wird ein führendes Token gleich der Art (z.B. "git")
    entfernt - Lernende tippen mal `git status`, mal nur `status`, beides soll
    zum selben argv führen. `argv[0]` ist danach IMMER das konfigurierte
    Binärprogramm; ein fremder erster Tokenname (z.B. `sh`) wird nicht als
    Programmname behandelt, sondern landet als ganz normales Argument beim
    konfigurierten Werkzeug - es gibt keinen Weg, darüber ein anderes Programm
    zu starten (kein shell=True, keine Pipes, keine Umleitungen).
    """
    tokens = shlex.split(befehl)
    if not tokens:
        return None
    if tokens[0] == art:
        tokens = tokens[1:]
    return [binaer] + tokens


def _run_werkzeug(auftrag: dict, art: str, binaer: str, zeitgrenze: float,
                   zusatz_umgebung: dict[str, str] | None = None) -> dict:
    """Führt eine kurze Folge von Befehlen für ein Kommandozeilen-Werkzeug aus.

    `cwd` ist bewusst das DAUERHAFTE Arbeitsverzeichnis der Teilnehmerin
    (`_workspace`), nicht ein frisches Lauf-Verzeichnis wie bei Ansible: eine in
    Aufgabe 1 erzeugte CA muss bis Aufgabe 3 überleben (Änderung 2 im Entwurf).
    """
    begonnen = time.monotonic()

    def _ergebnis(rc: int, text: str, timed_out: bool = False) -> dict:
        text_gekuerzt, gekappt = _clip(text)
        return {"rc": rc, "output": text_gekuerzt, "truncated": gekappt,
                "duration_ms": int((time.monotonic() - begonnen) * 1000),
                "timed_out": timed_out}

    dateien = auftrag.get("files") or {}
    fehler = _dateien_pruefen(dateien)
    if fehler:
        return _ergebnis(2, fehler)

    befehle = auftrag.get("commands") or []
    fehler = _befehle_pruefen(befehle)
    if fehler:
        return _ergebnis(2, fehler)

    arbeitsplatz = _workspace(str(auftrag.get("workspace", "gast")))
    for name, inhalt in dateien.items():
        (arbeitsplatz / name).write_text(str(inhalt), encoding="utf-8")

    umgebung = {
        "PATH": os.getenv("PATH", "/usr/local/bin:/usr/bin:/bin"),
        "HOME": str(arbeitsplatz),
        "LANG": "C.UTF-8",
    }
    if zusatz_umgebung:
        umgebung.update(zusatz_umgebung)
    # Siehe Kommentar im Ansible-Zweig weiter oben: nur für die Windows-
    # Entwicklungsmaschine relevant, in Produktion (Linux-Container) wirkungslos.
    if sys.platform == "win32":
        systemroot = os.getenv("SystemRoot")
        if systemroot:
            umgebung["SystemRoot"] = systemroot

    ausgabe_teile: list[str] = []
    rc = 0
    abgebrochen = False
    # Die Zeitgrenze gilt für den GESAMTEN Lauf, nicht je Befehl - sonst könnte
    # ein Auftrag mit 6 Befehlen bis zu 6-mal so lange laufen und würde damit
    # die Parallelitätsgrenze unterlaufen.
    frist = begonnen + zeitgrenze
    for befehl in befehle:
        argv = _argv_bauen(befehl, art, binaer)
        if argv is None:
            rc = 2
            ausgabe_teile.append(f"$ {befehl}\nLeere Befehlszeile abgelehnt.")
            break
        anzeige = " ".join([art] + argv[1:])
        ausgabe_teile.append(f"$ {anzeige}")

        verbleibend = frist - time.monotonic()
        if verbleibend <= 0:
            abgebrochen = True
            rc = 124
            ausgabe_teile.append(f"Abgebrochen: Der Lauf hat die Zeitgrenze von "
                                  f"{zeitgrenze:.0f} Sekunden überschritten.")
            break
        try:
            rc, roh, befehl_abgebrochen = _mit_zeitgrenze_ausfuehren(
                argv, arbeitsplatz, umgebung, verbleibend)
        except OSError as fehler:
            rc = 2
            ausgabe_teile.append(f"Werkzeug nicht ausführbar: {fehler}")
            break
        ausgabe_teile.append(roh.decode("utf-8", "replace"))
        if befehl_abgebrochen:
            abgebrochen = True
            ausgabe_teile.append(f"Abgebrochen: Der Lauf hat die Zeitgrenze von "
                                  f"{zeitgrenze:.0f} Sekunden überschritten.")
            break
        if rc != 0:
            break

    return _ergebnis(rc, "\n".join(ausgabe_teile), timed_out=abgebrochen)


def _run_openssl(auftrag: dict) -> dict:
    return _run_werkzeug(auftrag, "openssl", OPENSSL_BIN, OPENSSL_TIMEOUT_SECONDS)


def _run_git(auftrag: dict) -> dict:
    zusatz_umgebung = {
        "GIT_AUTHOR_NAME": "Lab-Teilnehmerin",
        "GIT_AUTHOR_EMAIL": "lab@lab.invalid",
        "GIT_COMMITTER_NAME": "Lab-Teilnehmerin",
        "GIT_COMMITTER_EMAIL": "lab@lab.invalid",
        "GIT_AUTHOR_DATE": GIT_FIXED_DATE,
        "GIT_COMMITTER_DATE": GIT_FIXED_DATE,
        # Keine Konfiguration von außerhalb des Containers soll hereinwirken.
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
    }
    return _run_werkzeug(auftrag, "git", GIT_BIN, GIT_TIMEOUT_SECONDS, zusatz_umgebung)


HANDLER = {"ansible": _run_ansible, "openssl": _run_openssl, "git": _run_git}


def _ausfuehren(auftrag: dict) -> dict:
    """Wählt anhand von `kind` die Ausführung. Fehlt `kind`, gilt `"ansible"`
    (Verträge, die schon in der Warteschlange liegen, laufen unverändert
    weiter). Eine unbekannte oder nicht freigegebene Art stürzt den Arbeiter
    nicht ab - sie liefert ein reguläres Ergebnis mit `rc=2`."""
    art = auftrag.get("kind") or "ansible"
    art = str(art)

    handler = HANDLER.get(art)
    if handler is None:
        return {"rc": 2, "output": f"Unbekannte Auftragsart {art!r}.",
                "truncated": False, "duration_ms": 0, "timed_out": False}
    if art not in RUNNER_KINDS:
        freigegeben = ", ".join(sorted(RUNNER_KINDS)) or "(keine)"
        return {"rc": 2,
                "output": (f"Auftragsart {art!r} ist auf diesem Runner nicht freigegeben "
                           f"(RUNNER_KINDS={freigegeben})."),
                "truncated": False, "duration_ms": 0, "timed_out": False}
    return handler(auftrag)


def _antwort_schreiben(auftrags_id: str, ergebnis: dict) -> None:
    ziel = QUEUE / "out" / f"{auftrags_id}.json"
    vorlaeufig = ziel.with_suffix(".json.tmp")
    vorlaeufig.write_text(json.dumps(ergebnis), encoding="utf-8")
    os.replace(vorlaeufig, ziel)  # atomar: das Backend sieht nie eine halbe Datei
    try:
        os.chmod(ziel, 0o666)
    except OSError:
        pass


def _uebernehmen(pfad: Path) -> Path | None:
    """Beansprucht einen Auftrag exklusiv, bevor er in den Pool geht.

    Ohne das würde die Schleife denselben Auftrag mehrfach einreihen, solange
    der Arbeiter ihn noch nicht gelöscht hat — das Playbook liefe doppelt.
    os.replace ist atomar: Nur der erste Versuch gewinnt.
    """
    beansprucht = pfad.with_suffix(".claimed")
    try:
        os.replace(pfad, beansprucht)
        return beansprucht
    except OSError:
        return None


def _bearbeiten(pfad: Path) -> None:
    auftrags_id = pfad.name.removesuffix(".claimed").removesuffix(".json")
    try:
        auftrag = json.loads(pfad.read_text(encoding="utf-8"))
    except (OSError, ValueError) as fehler:
        log("Auftrag unlesbar:", pfad.name, fehler)
        pfad.unlink(missing_ok=True)
        return
    pfad.unlink(missing_ok=True)  # nur einmal ausführen, auch wenn danach etwas schiefgeht
    try:
        ergebnis = _ausfuehren(auftrag)
    except Exception as fehler:  # noqa: BLE001 - der Arbeiter darf nie sterben
        log("Lauf fehlgeschlagen:", fehler)
        ergebnis = {"rc": 1, "output": f"Interner Fehler im Lab-Runner: {fehler}",
                    "truncated": False, "duration_ms": 0, "timed_out": False}
    _antwort_schreiben(auftrags_id, ergebnis)


def _aufraeumen() -> None:
    jetzt = time.time()
    for ordner in ("in", "out"):
        for eintrag in list((QUEUE / ordner).glob("*.json")) + list((QUEUE / ordner).glob("*.claimed")):
            try:
                if jetzt - eintrag.stat().st_mtime > JOB_MAX_AGE_SECONDS:
                    eintrag.unlink(missing_ok=True)
            except OSError:
                pass


def _warteschlange_vorbereiten() -> bool:
    """Legt in/ und out/ an. Gibt False zurück, wenn die Rechte fehlen.

    Bewusst kein Absturz: Ein Container, der beim Start sofort stirbt, landet in
    einer Neustartschleife und die eigentliche Ursache scrollt aus dem Log. Wir
    melden sie stattdessen deutlich und versuchen es weiter — sobald die Rechte
    stimmen, arbeitet der Runner ohne Eingriff weiter.
    """
    for ordner in ("in", "out"):
        try:
            (QUEUE / ordner).mkdir(parents=True, exist_ok=True)
        except OSError as fehler:
            log(f"Warteschlange {QUEUE / ordner} nicht nutzbar: {fehler}. "
                f"Erwartet wird ein Volume, in das der Runner-Benutzer (uid "
                f"{os.getuid()}) schreiben darf — siehe runner/Dockerfile und "
                f"docs/lab-sicherheit.md.")
            return False
        try:
            os.chmod(QUEUE / ordner, 0o777)  # Backend und Runner laufen als verschiedene Nutzer
        except OSError:
            pass  # Rechte reichen bereits, sonst waere das mkdir gescheitert
    return True


def _runde(pool: ThreadPoolExecutor, offene: list) -> tuple[list, int]:
    """Eine Runde: fertige Futures aussortieren, dann so viele neue Auftraege
    beanspruchen und an den Pool geben, wie zusammen mit den noch offenen
    (laufenden + im Executor wartenden) Futures MAX_QUEUE_DEPTH nicht
    ueberschreiten.

    Ohne diese Grenze uebernahm die Schleife JEDEN Durchlauf ALLE wartenden
    Auftragsdateien auf einmal (sie sind durch _uebernehmen ja schon aus
    'in/' umbenannt, fuer den naechsten Durchlauf also unsichtbar) und reichte
    sie an den Executor weiter. MAX_PARALLEL begrenzte dabei nur, wie viele
    GLEICHZEITIG laufen - nicht, wie viele bereits beansprucht in der
    Warteschlange des Executors auf ihre Ausfuehrung warten. Bei vielen
    Auftraegen wuchs diese Warteschlange unbegrenzt; und weil ein beanspruchter
    Auftrag fuer das Backend nicht mehr als "noch wartend" erkennbar ist, lief
    das Backend nach TIMEOUT_SECONDS + 15s bereits in seinen eigenen 504 -
    der Auftrag wurde trotzdem noch ausgefuehrt, nur schaute niemand mehr hin.

    Nicht beanspruchte Auftragsdateien bleiben ABSICHTLICH in 'in/' liegen -
    das ist kein Leck, das noch geschlossen werden muss: Das Backend raeumt
    seinen eigenen (getimeouteten) Auftrag beim 504 selbst weg, und
    _aufraeumen() entfernt liegengebliebene Dateien nach JOB_MAX_AGE_SECONDS.
    Wer hier "vorsichtshalber sofort alles beanspruchen" nachruestet, stellt
    genau den Fehler wieder her, den diese Funktion beheben soll.

    Gibt (aktualisierte Liste offener Futures, Anzahl in dieser Runde frisch
    beanspruchter Auftraege) zurueck.
    """
    offene = [future for future in offene if not future.done()]
    frei = MAX_QUEUE_DEPTH - len(offene)
    beansprucht = 0
    if frei > 0:
        for pfad in sorted((QUEUE / "in").glob("*.json"))[:frei]:
            ziel = _uebernehmen(pfad)
            if ziel is not None:
                offene.append(pool.submit(_bearbeiten, ziel))
                beansprucht += 1
    return offene, beansprucht


def main() -> None:
    while not _warteschlange_vorbereiten():
        time.sleep(5)
    log(f"Lab-Runner bereit. Warteschlange: {QUEUE}, parallel: {MAX_PARALLEL}, "
        f"Warteschlangentiefe: {MAX_QUEUE_DEPTH}, "
        f"Zeitgrenze: {TIMEOUT_SECONDS:.0f}s, Netzwerk: keines, "
        f"Arten: {', '.join(sorted(RUNNER_KINDS)) or '(keine)'}")

    letzte_reinigung = 0.0
    offene: list = []
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL) as pool:
        while True:
            offene, beansprucht = _runde(pool, offene)
            if beansprucht == 0:
                time.sleep(POLL_SECONDS)
            if time.monotonic() - letzte_reinigung > 60:
                _aufraeumen()
                letzte_reinigung = time.monotonic()


if __name__ == "__main__":
    main()
