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

import json
import os
import shutil
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
ANSIBLE_BIN = os.getenv("ANSIBLE_PLAYBOOK_BIN", "ansible-playbook")
POLL_SECONDS = float(os.getenv("RUNNER_POLL_SECONDS", "0.2"))

WORKSPACE_ROOT = Path(os.getenv("RUNNER_WORKSPACE_ROOT", "/tmp/lab-workspaces"))
WORKSPACE_MAX_AGE_SECONDS = float(os.getenv("RUNNER_WORKSPACE_MAX_AGE", str(12 * 3600)))
# Aufträge, die niemand mehr abholt (Backend neu gestartet), sollen nicht ewig
# liegen bleiben und Arbeit erzeugen.
JOB_MAX_AGE_SECONDS = float(os.getenv("RUNNER_JOB_MAX_AGE", "300"))

DEFAULT_INVENTORY = "[lab]\nlabhost ansible_connection=local\n"


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
    sicher = "".join(z for z in kennung if z.isalnum() or z in "_-")[:64] or "gast"
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


def _ausfuehren(auftrag: dict) -> dict:
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
            # Nur Interpreter-Rauschen unterdrücken; Ansibles eigene Meldungen
            # bleiben sichtbar, sie sind Lernstoff.
            "PYTHONWARNINGS": "ignore::SyntaxWarning",
        }

        try:
            fertig = subprocess.run(argumente, cwd=laufverzeichnis, env=umgebung,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    timeout=TIMEOUT_SECONDS)
            rc = fertig.returncode
            text = fertig.stdout.decode("utf-8", "replace")
        except subprocess.TimeoutExpired as zeit:
            abgebrochen = True
            rc = 124
            teil = (zeit.stdout or b"").decode("utf-8", "replace")
            text = (teil + f"\n\nAbgebrochen: Der Lauf hat die Zeitgrenze von "
                           f"{TIMEOUT_SECONDS:.0f} Sekunden überschritten.")

        text, gekappt = _clip(text)
        return {"rc": rc, "output": text, "truncated": gekappt,
                "duration_ms": int((time.monotonic() - begonnen) * 1000),
                "timed_out": abgebrochen}
    finally:
        shutil.rmtree(laufverzeichnis, ignore_errors=True)


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


def main() -> None:
    for ordner in ("in", "out"):
        (QUEUE / ordner).mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(QUEUE / ordner, 0o777)  # Backend und Runner laufen als verschiedene Nutzer
        except OSError:
            pass
    log(f"Lab-Runner bereit. Warteschlange: {QUEUE}, parallel: {MAX_PARALLEL}, "
        f"Zeitgrenze: {TIMEOUT_SECONDS:.0f}s, Netzwerk: keines")

    letzte_reinigung = 0.0
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL) as pool:
        while True:
            auftraege = [b for b in (_uebernehmen(p) for p in sorted((QUEUE / "in").glob("*.json"))) if b]
            if auftraege:
                for pfad in auftraege:
                    pool.submit(_bearbeiten, pfad)
            else:
                time.sleep(POLL_SECONDS)
            if time.monotonic() - letzte_reinigung > 60:
                _aufraeumen()
                letzte_reinigung = time.monotonic()


if __name__ == "__main__":
    main()
