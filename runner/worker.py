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

Trennung der Läufe vom Worker (Stand 2026-10-13): Der Worker läuft als uid 0
mit genau fünf Capabilities, jeder Lauf unter einer eigenen, exklusiv
vergebenen uid ohne jede Capability (JOB_UIDS). Ein Lauf kommt damit weder an
/queue noch an den Worker-Prozess noch an fremde Arbeitsverzeichnisse. Siehe
Abschnitt "Trennung der Läufe" weiter unten und docs/lab-sicherheit.md.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
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


# Die Ausgabe eines Laufs ist fremdbestimmt. ANSI-Sequenzen (CSI, OSC, 2-Byte)
# fallen weg, alle übrigen C0-/C1-Steuerzeichen außer \n und \t werden sichtbar
# ersetzt: kein NUL, kein Rücklauf, der eine Zeile im Terminal oder Log
# überschreibt, keine Escape-Folge, die ein Betrachter interpretieren könnte.
_ANSI = re.compile(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07\x1b]*(?:\x07|\x1b\\)?|[@-Z\\-_])")
_STEUERZEICHEN = re.compile(r"[\x00-\x08\x0b-\x1f\x7f-\x9f]")


def _bereinigen(text: str) -> str:
    text = _ANSI.sub("", text).replace("\r\n", "\n").replace("\r", "\n")
    return _STEUERZEICHEN.sub("�", text)


def _clip(text: str) -> tuple[str, bool]:
    text = _bereinigen(text)
    roh = text.encode("utf-8", "replace")
    if len(roh) <= MAX_OUTPUT_BYTES:
        return text, False
    return roh[:MAX_OUTPUT_BYTES].decode("utf-8", "ignore") + "\n\n[Ausgabe gekürzt]", True


# ---------------------------------------------------------------------------
# Trennung der Läufe (docs/lab-sicherheit.md, "Trennung der Läufe per uid").
# ---------------------------------------------------------------------------
#
# Ein Playbook ist beliebiger Code. Lief es unter der uid des Workers, konnte
# es /queue lesen und beschreiben (fremde Aufträge, Ergebnis-Token), den Worker
# beenden und dessen Speicher lesen. Deshalb:
#   - Worker = uid 0 mit CHOWN, DAC_OVERRIDE, SETUID, SETGID, KILL (compose).
#     Ein unprivilegierter Worker kann keine uid wechseln: setuid-Hilfsprogramme
#     und Datei-Capabilities sind durch "no-new-privileges" wirkungslos, und
#     Docker gibt einem Nicht-root-Benutzer keine Capabilities aus cap_add.
#   - Jeder Lauf = eine uid aus JOB_UIDS, exklusiv für die Dauer des Laufs,
#     ohne Gruppen, ohne Capabilities. Eine uid je Slot statt EINER Job-uid:
#     sonst könnten gleichzeitige Läufe einander lesen und beenden.
#   - /queue gehört root:QUEUE_GID (0750, in/ und out/ 0770): Worker und
#     Backend ja, Läufe nein.
# Standard ist die Trennung. Kann sie nicht eingerichtet werden, bleibt die Art
# "ansible" gesperrt (fail-closed, _ansible_sperrgrund).
ISOLATION_UNSICHER = "aus-unsicher"
# UNSICHER, nur für lokale Entwicklung/Tests ohne root (macOS, Windows, CI-Job
# "runner"): RUNNER_ISOLATION=aus-unsicher lässt Playbooks unter der uid des
# Workers laufen. Nie im Container setzen - als uid 0 wird der Wert verweigert.
ISOLATION = os.getenv("RUNNER_ISOLATION", "uid")
# = Benutzer labjob10002..labjob10009 in runner/Dockerfile. Mehr gleichzeitige
# Läufe als uids gibt es nicht: ein Lauf wartet dann auf einen freien Slot.
JOB_UIDS = tuple(range(10002, 10010))
# Gruppe des Backend-Containers (backend/Dockerfile: useradd --uid 10001).
QUEUE_GID = int(os.getenv("RUNNER_QUEUE_GID", "10001"))
# Für alle beschreibbare Orte im Container; was ein Lauf dort hinterlässt,
# wird nach dem Lauf entfernt (sonst erbte es der nächste Lauf im selben Slot).
GEMEINSAME_SCHREIBORTE = (Path("/tmp"), Path("/dev/shm"))
KILL_RUNDEN = 40
SYSCTL_FS = Path("/proc/sys/fs")

_slots = threading.Condition()
_freie_uids: list[int] = []
_belegte_arbeitsplaetze: set[Path] = set()
_gesperrte_arbeitsplaetze: set[Path] = set()
_isolation_aktiv = False
_isolation_fehler = "Die Startprüfung der Trennung ist nicht gelaufen."

# Läuft unter der Job-uid und meldet, was ein Lauf tatsächlich an Rechten hat.
_PROBE = (
    "import os,time;"
    "s=dict(z.split(':\\t',1) for z in open('/proc/self/status').read().splitlines() if ':\\t' in z);"
    "print(os.getuid(),os.getgid(),os.getgroups(),int(s['CapPrm'],16)|int(s['CapEff'],16),"
    "s.get('NoNewPrivs'),flush=True);time.sleep(30)"
)


def _eigene_uid() -> int:
    return os.getuid() if hasattr(os, "getuid") else -1  # Windows: nur Tests


def _isolation_probe(uid: int) -> str | None:
    """Probiert ECHT aus, was die Trennung braucht, statt Capability-Bits zu
    lesen: eine fehlende Capability zeigt sich genau an dem Schritt, der sie
    braucht. Liefert die Ursache als Text oder None, wenn alles stimmt."""
    schritt = "Probeverzeichnis anlegen"
    verzeichnis = proc = None
    try:
        verzeichnis = Path(tempfile.mkdtemp(prefix="probe-"))
        schritt = "chown an die Job-uid (CAP_CHOWN)"
        os.chown(verzeichnis, uid, uid)
        schritt = "Schreiben in ein fremdes 0700-Verzeichnis (CAP_DAC_OVERRIDE)"
        (verzeichnis / "probe").write_text("", encoding="utf-8")
        schritt = "Prozess unter der Job-uid starten (CAP_SETUID/CAP_SETGID)"
        proc = subprocess.Popen([sys.executable, "-c", _PROBE], stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, text=True, user=uid, group=uid,
                                extra_groups=[])
        zeile = proc.stdout.readline().strip()
        schritt = "Prozess der Job-uid beenden (CAP_KILL)"
        os.kill(proc.pid, signal.SIGKILL)
        proc.wait()
    except (OSError, subprocess.SubprocessError) as fehler:
        return f"{schritt} fehlgeschlagen: {fehler}"
    finally:
        if proc is not None:
            proc.stdout.close()
        if verzeichnis is not None:
            shutil.rmtree(verzeichnis, ignore_errors=True)
    erwartet = f"{uid} {uid} [] 0 1"
    if zeile != erwartet:
        return (f"Ein Lauf hätte nicht die erwarteten Rechte (uid gid Gruppen Capabilities "
                f"NoNewPrivs): {zeile!r} statt {erwartet!r} - fehlt "
                f"security_opt no-new-privileges?")
    return None


def _isolation_einrichten() -> None:
    """Startprüfung. Danach gilt genau einer von drei Zuständen: Trennung aktiv
    (Slots vergeben), ausdrücklich unsicher (nur Nicht-root) oder gesperrt."""
    global _isolation_aktiv, _isolation_fehler
    uid = _eigene_uid()
    if ISOLATION == ISOLATION_UNSICHER and uid != 0:
        log("WARNUNG: RUNNER_ISOLATION=aus-unsicher - Läufe sind NICHT vom Worker getrennt "
            "und können /queue lesen und schreiben. Nur für lokale Entwicklung.")
        return
    if ISOLATION == ISOLATION_UNSICHER:
        fehler = "RUNNER_ISOLATION=aus-unsicher bei einem Worker mit uid 0 - Playbooks liefen als root."
    elif uid != 0:
        fehler = (f"Der Worker läuft als uid {uid} statt 0 und kann keine uid wechseln "
                  f"(docker-compose.yml, Dienst runner: user \"0:0\" und cap_add).")
    else:
        fehler = _isolation_probe(JOB_UIDS[0])
    if fehler is None:
        with _slots:
            _freie_uids[:] = JOB_UIDS
        _isolation_aktiv = True
        log(f"Trennung aktiv: Läufe unter uid {JOB_UIDS[0]}-{JOB_UIDS[-1]}, ohne Capabilities.")
        # Nur Hinweis, kein Sperrgrund: der Worker folgt selbst keinem Symlink
        # und fasst mehrfach verlinkte Dateien nicht an (_uebergeben). Die beiden
        # Kernel-Schalter sind die zweite Schicht dahinter.
        for schalter in ("protected_hardlinks", "protected_symlinks"):
            try:
                wert = (SYSCTL_FS / schalter).read_text(encoding="ascii").strip()
            except OSError:
                wert = "unlesbar"
            if wert != "1":
                log(f"WARNUNG: fs.{schalter}={wert} auf dem Host (erwartet 1) - "
                    f"siehe docs/lab-sicherheit.md, Restrisiken.")
    else:
        _isolation_fehler = fehler
        log(f"ANSIBLE-LAB DEAKTIVIERT (fail-closed): {fehler} Playbooks werden abgelehnt, "
            f"bis die Trennung steht. openssl/git laufen weiter unter uid {uid} - sie führen "
            f"keinen Teilnehmer-Code aus (Argumentprüfung). Siehe docs/lab-sicherheit.md.")


def _ansible_sperrgrund() -> str | None:
    if _isolation_aktiv or (ISOLATION == ISOLATION_UNSICHER and _eigene_uid() != 0):
        return None
    return _isolation_fehler


def _verzeichnis_sichern(pfad: Path, uid: int, gid: int, modus: int) -> None:
    """chown + chmod über einen Deskriptor, der NUR ein echtes Verzeichnis
    öffnet. `os.chown(pfad)`/`os.chmod(pfad)` folgten einem Symlink - der
    root-Worker würde das Ziel umhängen. Erst chown, dann chmod: ohne
    CAP_FOWNER darf auch root die Rechte nur an eigenen Dateien ändern."""
    fd = os.open(pfad, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fchown(fd, uid, gid)
        os.fchmod(fd, modus)
    finally:
        os.close(fd)


def _sonderbits_loeschen(name: str, dir_fd: int) -> None:
    """Nimmt setuid/setgid/sticky weg. Über einen O_NOFOLLOW-Deskriptor, weil
    chmod(2) Symlinks folgt; vorher an root, weil nur der Eigentümer chmod darf.
    (Linux löscht setuid bei chown auf Dateien ohnehin, auch für root - darauf
    verlässt sich hier nichts.)"""
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=dir_fd)
    try:
        os.fchown(fd, 0, 0)
        os.fchmod(fd, os.fstat(fd).st_mode & 0o777)
    finally:
        os.close(fd)


def _eintrag_uebergeben(name: str, dir_fd: int, uid: int) -> int:
    """Ein Eintrag aus _uebergeben. Liefert 1, wenn er entfernt wurde, sonst 0."""
    st = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    art = stat.S_IFMT(st.st_mode)
    if art not in (stat.S_IFREG, stat.S_IFDIR, stat.S_IFLNK) or (
            art == stat.S_IFREG and st.st_nlink > 1):
        os.unlink(name, dir_fd=dir_fd)
        return 1
    if art != stat.S_IFLNK and st.st_mode & 0o7000:
        _sonderbits_loeschen(name, dir_fd)
    os.chown(name, uid, uid, dir_fd=dir_fd, follow_symlinks=False)
    return 0


def _uebergeben(pfad: Path, uid: int | None, oben: int | None = None) -> None:
    """Gibt `pfad` samt Inhalt der uid (Verzeichnis: 0700). Ohne Trennung nichts.
    `oben` weicht nur bei der Rücknahme ab: der Inhalt bleibt bei der Job-uid,
    das Verzeichnis selbst geht an root.

    Der Worker ist root und fasst hier Dateien an, die ein Lauf angelegt hat.
    Deshalb durchgehend über Deskriptoren (os.fwalk, dir_fd) und nie einem
    Symlink nach. Unterwegs wird entschärft, was ein Lauf hinterlassen kann:
      - FIFOs, Sockets, Geräte: entfernt (nichts im Lab braucht sie);
      - Dateien mit mehr als einem Hardlink: entfernt statt übergeben - der
        zweite Name kann auf eine fremde Datei desselben Dateisystems zeigen,
        ein chown gäbe sie dem Lauf (Hardlinks überleben einen Lauf also nicht);
      - setuid/setgid/sticky: gelöscht;
      - alles, was sich trotzdem nicht übergeben lässt: entfernt und geloggt.
    Nur wenn auch das Entfernen scheitert, wirft die Funktion.
    """
    if uid is None:
        return
    oben = uid if oben is None else oben
    try:
        wurzel = os.open(pfad, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError:
        os.chown(pfad, oben, oben, follow_symlinks=False)  # Datei, Symlink, FIFO: nur der Eintrag
        return
    entfernt = 0
    try:
        os.fchown(wurzel, 0, 0)
        os.fchmod(wurzel, 0o700)
        os.fchown(wurzel, oben, oben)
        for _wurzel, ordner, dateien, fd in os.fwalk(".", dir_fd=wurzel):
            for name in ordner + dateien:
                try:
                    entfernt += _eintrag_uebergeben(name, fd, uid)
                except OSError as fehler:
                    # Was sich nicht übergeben lässt, kommt weg - ein Lauf darf den
                    # Worker mit keiner Hinterlassenschaft am Aufräumen hindern.
                    # Bekannter Fall (CI-Lauf vom 13.10.2026, EPERM): root OHNE
                    # CAP_FOWNER kann eine setuid-Datei nicht per chown übernehmen,
                    # weil der Kernel dabei die Bits löscht und dafür
                    # Eigentümerrechte verlangt.
                    try:
                        os.unlink(name, dir_fd=fd)
                    except OSError:
                        raise OSError(fehler.errno, f"{name!r}: {fehler.strerror}") from None
                    log(f"{pfad.name}: {name!r} nicht übergebbar ({fehler.strerror}) - entfernt.")
    finally:
        os.close(wurzel)
    if entfernt:
        log(f"{pfad.name}: {entfernt} Einträge entfernt (Spezialdatei oder mehrfach verlinkt).")


def _loeschen(pfad: Path) -> None:
    if _isolation_aktiv:
        try:
            # Erst an root: in einem Sticky-Verzeichnis eines Laufs dürfte sonst
            # auch root (ohne CAP_FOWNER) nichts löschen.
            _uebergeben(pfad, 0)
        except OSError:
            pass
    if pfad.is_dir() and not pfad.is_symlink():
        shutil.rmtree(pfad, ignore_errors=True)
    else:
        try:
            pfad.unlink(missing_ok=True)
        except OSError:
            pass


def _uids_von(pid: int | str) -> list[str]:
    """Reale, effektive, gespeicherte und Dateisystem-uid eines Prozesses.

    Aus /proc/<pid>/status und nicht aus dem Eigentümer von /proc/<pid>: der
    gehört root, sobald ein Prozess sich mit prctl(PR_SET_DUMPABLE, 0)
    versteckt."""
    try:
        status = Path("/proc", str(pid), "status").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []  # inzwischen beendet
    for zeile in status.splitlines():
        if zeile.startswith("Uid:"):
            return zeile.split()[1:]
    return []


def _prozesse_der_uid(uid: int) -> list[int]:
    """Alle Prozesse der uid. Zombies zählen mit - ein beendeter
    Thread-Gruppenführer steht als Zombie da, während seine Threads weiterlaufen."""
    return [int(eintrag) for eintrag in os.listdir("/proc")
            if eintrag.isdigit() and str(uid) in _uids_von(eintrag)]


def _signal_an_uid(pid: int, signalnummer: int, uid: int) -> None:
    """Signal an `pid`, aber nur solange der Prozess wirklich der uid gehört.

    Zwischen Zählen und Signal kann die pid neu vergeben sein - an den Worker
    selbst oder einen fremden Lauf. Das pidfd hält den Prozess fest: erst
    öffnen, DANN die uid noch einmal lesen, dann über das pidfd senden. Stirbt
    der Prozess dazwischen, geht das Signal ins Leere statt an den Nachfolger.
    """
    try:
        fd = os.pidfd_open(pid)
    except (AttributeError, OSError) as fehler:
        if isinstance(fehler, ProcessLookupError):
            raise
        # Kein pidfd (kein Linux, Kernel < 5.3, vom seccomp-Profil gesperrt):
        # ponytail: dann bleibt das Mikrosekunden-Fenster der pid-Wiederverwendung.
        os.kill(pid, signalnummer)
        return
    try:
        if str(uid) in _uids_von(pid):
            signal.pidfd_send_signal(fd, signalnummer)
    finally:
        os.close(fd)


def _job_prozesse_beenden(uid: int | None, *, finden=_prozesse_der_uid, senden=None,
                          ernten=None, warten=time.sleep) -> bool:
    """Beendet ALLE Prozesse der Job-uid, auch solche, die ihre Prozessgruppe
    mit setsid() verlassen haben. True, wenn danach keiner mehr existiert.

    Je Runde erst SIGSTOP an alle, dann SIGKILL: ein angehaltener Prozess kann
    nicht mehr forken, ein Wettlauf "schneller forken als der Worker zählt"
    endet damit nach wenigen Runden. Verwaiste Kinder hängen am Worker (PID 1
    im Container) und werden hier geerntet, sonst blieben sie als Zombies
    stehen und zählten gegen das pids-Limit.
    """
    if uid is None:
        return True
    ernten = ernten or os.waitpid
    senden = senden or (lambda pid, signalnummer: _signal_an_uid(pid, signalnummer, uid))
    for _ in range(KILL_RUNDEN):
        pids = finden(uid)
        if not pids:
            return True
        for signalnummer in (signal.SIGSTOP, signal.SIGKILL):
            for pid in pids:
                try:
                    senden(pid, signalnummer)
                except ProcessLookupError:
                    pass
        for pid in pids:
            try:
                ernten(pid, os.WNOHANG)
            except ChildProcessError:
                pass  # nicht unser Kind: erntet ein anderer (z. B. tini)
        warten(0.05)
    return not finden(uid)


def _slot_aufraeumen(arbeitsplatz: Path, laufverzeichnis: Path | None, uid: int) -> bool:
    """Nach dem Lauf: Prozesse der uid beenden, Arbeitsverzeichnis zurück an
    root (in Ruhe kommt keine Job-uid hinein - auch nicht der nächste Lauf im
    selben Slot), Hinterlassenschaften an gemeinsamen Orten entfernen.

    Zustand in Ruhe: das Verzeichnis selbst gehört root (0700), sein Inhalt
    weiter der letzten Job-uid - ohne Sonderbits, ohne Spezialdateien. Root
    gehört darin nichts; der nächste Lauf bekommt alles an seine uid.

    False (Slot bleibt gesperrt) gibt es nur noch, wenn sich Prozesse nicht
    beenden lassen oder ein Arbeitsverzeichnis weder zurückzunehmen noch zu
    löschen ist. Was ein Lauf im Arbeitsverzeichnis hinterlässt, darf den Slot
    nicht kosten: acht präparierte Läufe legten sonst das Lab für alle still.
    """
    try:
        if not _job_prozesse_beenden(uid):
            raise OSError("Prozesse der uid lassen sich nicht beenden")
    except OSError as fehler:
        log(f"Job-Slot uid {uid} GESPERRT, Aufräumen fehlgeschlagen: {fehler}. Der Slot und "
            f"{arbeitsplatz.name} bleiben bis zum Neustart des Runners außer Betrieb.")
        return False
    sauber = True
    try:
        _uebergeben(arbeitsplatz, uid, oben=0)
    except OSError as fehler:
        log(f"Arbeitsverzeichnis {arbeitsplatz.name} lässt sich nicht zurücknehmen ({fehler}) - "
            f"es wird verworfen, der nächste Lauf beginnt leer.")
        _loeschen(arbeitsplatz)
        if os.path.lexists(arbeitsplatz):
            log(f"Job-Slot uid {uid} GESPERRT: {arbeitsplatz.name} lässt sich auch nicht löschen. "
                f"Slot und Arbeitsverzeichnis bleiben bis zum Neustart außer Betrieb.")
            sauber = False
    # Erst jetzt: solange ein Prozess der uid lebt, könnte er das ihm gehörende
    # Laufverzeichnis im Sticky-/tmp gegen einen Symlink tauschen.
    if laufverzeichnis is not None:
        _loeschen(laufverzeichnis)
    for ort in GEMEINSAME_SCHREIBORTE:
        try:
            eintraege = list(os.scandir(ort))
        except OSError:
            continue  # gibt es hier nicht
        for eintrag in eintraege:
            try:
                eigen = eintrag.stat(follow_symlinks=False).st_uid == uid
            except OSError:
                continue  # ein anderer Lauf hat ihn gerade entfernt
            if eigen:
                _loeschen(Path(eintrag.path))
    return sauber


@contextmanager
def _job(kennung: str):
    """Belegt für einen Lauf das Arbeitsverzeichnis, ein frisches
    Laufverzeichnis (HOME/TMPDIR des Laufs, danach gelöscht) und - mit Trennung
    - eine Job-uid. Liefert (arbeitsplatz, laufverzeichnis, uid); uid ist None
    ohne Trennung.

    Ein Arbeitsverzeichnis hat höchstens EINEN Lauf gleichzeitig: sonst würde
    der zweite es dem ersten per chown unter den Füßen wegnehmen.
    """
    arbeitsplatz = _workspace(kennung)
    if not _isolation_aktiv:
        laufverzeichnis = Path(tempfile.mkdtemp(prefix="lauf-"))
        try:
            yield arbeitsplatz, laufverzeichnis, None
        finally:
            shutil.rmtree(laufverzeichnis, ignore_errors=True)
        return
    with _slots:
        frei = _slots.wait_for(
            lambda: arbeitsplatz in _gesperrte_arbeitsplaetze
            or (_freie_uids and arbeitsplatz not in _belegte_arbeitsplaetze),
            timeout=TIMEOUT_SECONDS + 10)
        if arbeitsplatz in _gesperrte_arbeitsplaetze:
            # Sofort, nicht erst nach der Wartezeit: es wird nicht mehr frei.
            raise RuntimeError("Das Arbeitsverzeichnis ist bis zum Neustart des Runners gesperrt.")
        if not frei:
            raise RuntimeError("Kein freier Job-Slot (alle belegt oder gesperrt).")
        # Vorn nehmen, hinten zurückgeben: die uids rotieren, ein Arbeitsverzeichnis
        # hängt nie an einer bestimmten uid.
        uid = _freie_uids.pop(0)
        _belegte_arbeitsplaetze.add(arbeitsplatz)
    laufverzeichnis = None
    try:
        # Im try: scheitert schon das Anlegen (tmpfs voll), muss der Slot zurück.
        laufverzeichnis = Path(tempfile.mkdtemp(prefix="lauf-"))
        arbeitsplatz.mkdir(exist_ok=True)  # falls der letzte Lauf es verwerfen musste
        _uebergeben(arbeitsplatz, uid)
        _uebergeben(laufverzeichnis, uid)
        yield arbeitsplatz, laufverzeichnis, uid
    finally:
        frei = _slot_aufraeumen(arbeitsplatz, laufverzeichnis, uid)
        with _slots:
            if frei:
                _freie_uids.append(uid)
                _belegte_arbeitsplaetze.discard(arbeitsplatz)
            else:
                _gesperrte_arbeitsplaetze.add(arbeitsplatz)  # uid und Verzeichnis bleiben weg
            _slots.notify_all()


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
    if _isolation_aktiv:
        # Läufe dürfen hindurch, aber nichts auflisten. Scheitert an einem
        # Symlink - dann gibt es keinen Lauf.
        _verzeichnis_sichern(WORKSPACE_ROOT, 0, 0, 0o711)
    jetzt = time.time()
    for eintrag in WORKSPACE_ROOT.iterdir():
        try:
            if (eintrag.is_dir() and eintrag not in _belegte_arbeitsplaetze
                    and jetzt - eintrag.stat().st_mtime > WORKSPACE_MAX_AGE_SECONDS):
                _loeschen(eintrag)
        except OSError:
            pass
    verzeichnis = WORKSPACE_ROOT / sicher
    verzeichnis.mkdir(parents=True, exist_ok=True)
    return verzeichnis


def _mit_zeitgrenze_ausfuehren(argv: list[str], cwd: Path, env: dict[str, str],
                                zeitgrenze: float, uid: int | None = None) -> tuple[int, bytes, bool]:
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

    Die Ausgabe geht in eine temporaere Datei statt in eine PIPE. Das begrenzt
    den Speicherverbrauch des Workers auch dann, wenn ein Auftrag sehr viel
    schreibt. Wichtig fuer den Timeout-Fall: ein Kind kann seine Prozessgruppe
    mit setsid() verlassen und dabei einen geerbten Pipe-Deskriptor offen
    halten. communicate() wuerde dann trotz beendetem Elternprozess haengen.
    Auf eine Datei zu warten ist nicht noetig; wir warten nur auf den direkt
    gestarteten Prozess und lesen danach hoechstens die Ergebnisgrenze ein.

    Rueckgabe: (rc, stdout_bytes, timed_out). Bei Abbruch ist rc IMMER 124,
    stdout_bytes enthaelt die bis zum Abbruch angefallene Teilausgabe.

    `uid` (Trennung der Laeufe): der Prozess startet unter dieser uid/gid, ohne
    Zusatzgruppen; der Wechsel weg von uid 0 leert seine Capabilities. Wer der
    Prozessgruppe entkommt, wird danach von _job_prozesse_beenden erfasst.
    """
    posix = sys.platform != "win32"
    trennung = {} if uid is None else {"user": uid, "group": uid, "extra_groups": [],
                                       "umask": 0o077}
    with tempfile.TemporaryFile(mode="w+b", dir=cwd) as ausgabe:
        # stdin ausdrücklich leer: sonst erbte der Lauf fd 0 des Workers (PID 1).
        proc = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                stdout=ausgabe, stderr=subprocess.STDOUT,
                                start_new_session=posix, **trennung)
        try:
            proc.wait(timeout=zeitgrenze)
            timed_out = False
        except subprocess.TimeoutExpired:
            if posix:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except ProcessLookupError:
                    pass  # zwischen Timeout und Signal bereits beendet
            else:
                proc.kill()
            # Nie communicate(): ein entkommenes Kind kann eine geerbte PIPE
            # offenhalten. Nach SIGKILL muss der direkte Elternprozess enden;
            # falls nicht, geben wir trotzdem zeitnah an den Worker zurueck.
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
            timed_out = True

        ausgabe.seek(0)
        # Ein Byte mehr reicht als Signal fuer _clip; die spaetere Antwort
        # bleibt damit auch bei mehreren Werkzeug-Kommandos klein.
        roh = ausgabe.read(MAX_OUTPUT_BYTES + 1)
        return (124 if timed_out else proc.returncode), roh, timed_out


def _run_ansible(auftrag: dict) -> dict:
    playbook = str(auftrag.get("playbook", ""))[:16_000]
    inventar = auftrag.get("inventory") or DEFAULT_INVENTORY
    extra_vars = auftrag.get("extra_vars")
    check = bool(auftrag.get("check"))
    with _job(str(auftrag.get("workspace", "gast"))) as (arbeitsplatz, laufverzeichnis, uid):
        return _run_ansible_im_slot(playbook, inventar, extra_vars, check, arbeitsplatz,
                                    laufverzeichnis, uid)


def _run_ansible_im_slot(playbook: str, inventar: object, extra_vars: object, check: bool,
                         arbeitsplatz: Path, laufverzeichnis: Path, uid: int | None) -> dict:
    begonnen = time.monotonic()
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

    # Playbook und Inventar hat root geschrieben: mit übergeben. HOME, TMPDIR
    # und die Ansible-Temp-Verzeichnisse liegen alle hier; gelöscht wird das
    # Laufverzeichnis von _job, nachdem alle Prozesse des Laufs beendet sind.
    _uebergeben(laufverzeichnis, uid)
    rc, roh, abgebrochen = _mit_zeitgrenze_ausfuehren(
        argumente, laufverzeichnis, umgebung, TIMEOUT_SECONDS, uid)
    text = roh.decode("utf-8", "replace")
    if abgebrochen:
        text += (f"\n\nAbgebrochen: Der Lauf hat die Zeitgrenze von "
                 f"{TIMEOUT_SECONDS:.0f} Sekunden überschritten.")

    text, gekappt = _clip(text)
    return {"rc": rc, "output": text, "truncated": gekappt,
            "duration_ms": int((time.monotonic() - begonnen) * 1000),
            "timed_out": abgebrochen}


# ---------------------------------------------------------------------------
# Änderung 2/3: gemeinsame Ausführung für openssl und git.
# ---------------------------------------------------------------------------
#
# P0-Sicherheitslücke (2026-07-22): _argv_bauen zerlegt die Lernenden-
# Kommandozeile zwar OHNE Shell, hängt die Tokens aber bis hierher ungefiltert
# hinter das Programm. Über den git-eigenen Transport "ext::" ließ sich damit
# TROTZ network_mode: none beliebiger Shell-Code im Container ausführen:
#   -c protocol.ext.allow=always clone ext::sh -c 'beliebiger_befehl' /tmp/x
# Die Zusage in docs/lab-sicherheit.md, dass git/openssl "keinen frei
# geschriebenen Code ausführen", galt nur mit der folgenden Sperre.
#
# Zwei Schichten, ALLOWLIST statt Blockliste (eine Blockliste einzelner Flags
# wäre eine Einladung, sie zu umgehen):
#   1. Das erste Nicht-Options-Token muss eines der hier je Art freigegebenen
#      Unterkommandos sein. Netz- oder codeausführende Unterkommandos wie
#      "clone"/"fetch"/"push"/"pull"/"remote"/"submodule" (git) oder
#      "s_client"/"s_server" (openssl) stehen bewusst NICHT auf der Liste.
#   2. Unabhängig von der Position: bestimmte Flags/Muster sind IMMER
#      verboten, weil sie einen Transport oder Codepfad außerhalb des
#      Unterkommandos öffnen ("-c" für git-Konfigurationsinjektion, "ext::"
#      für den shell-ausführenden git-Transport, "-engine" für das Nachladen
#      einer beliebigen openssl-Engine-Bibliothek, ...).
#
# Bewusst eine Allowlist: Ein neues Unterkommando muss hier ausdrücklich
# aufgenommen werden, damit es läuft - keine Blockliste, die ein cleverer
# Teilnehmer umgehen könnte. Wer eine neue Lab-Vorlage mit einem weiteren,
# lokalen und ungefährlichen Unterkommando braucht, erweitert diese Liste
# bewusst.
GIT_ERLAUBTE_SUBBEFEHLE = {
    "init", "status", "add", "commit", "log", "diff", "branch", "checkout",
    "switch", "merge", "rebase", "reset", "restore", "show", "tag", "stash",
    "worktree", "mv",
}
# "config" bewusst NICHT dabei: `git config alias.status '!sh -c ...'` legt
# einen Alias an, der bei einem SPÄTEREN, für sich harmlos aussehenden Aufruf
# wie "status" anstelle des echten Unterkommandos beliebigen Shell-Code
# ausführt - das Subcommand-Token bliebe dabei aus Sicht dieser Allowlist
# unverändert "status", die Prüfung allein fängt das nicht ab. Keine der
# Lab-Vorlagen (frontend/src/widgets/gitlab/templates.ts) braucht
# `git config`.

OPENSSL_ERLAUBTE_SUBBEFEHLE = {
    "genrsa", "genpkey", "rsa", "pkey", "req", "x509", "ca", "verify",
    "dgst", "enc", "rand",
}
# Kein "s_client"/"s_server": beide bauen eine Netzverbindung auf.

ERLAUBTE_SUBBEFEHLE = {"git": GIT_ERLAUBTE_SUBBEFEHLE, "openssl": OPENSSL_ERLAUBTE_SUBBEFEHLE}

GIT_VERBOTENE_FLAGS = {
    "-c", "--config-env", "--exec", "--exec-path", "-C", "--upload-pack",
    "--receive-pack", "-u", "--git-dir", "--work-tree",
    "--template", "--separate-git-dir",
}
# "-c name=wert"/"--config-env name=ENV" injizieren Konfiguration, die bei einem
# SPÄTEREN, harmlos aussehenden Unterkommando Code ausführt (core.hooksPath,
# core.sshCommand, core.fsmonitor, core.editor/pager, diff.external, alias.*);
# "--exec-path" setzt das git-Programmverzeichnis, "-C" wechselt vor dem Lauf
# das Verzeichnis (Ausbruch). "init --template=<dir>" kopiert <dir>/hooks/* ins
# neue Repository (Code beim nächsten commit), "--separate-git-dir"/"--git-dir"/
# "--work-tree" verlegen Repository bzw. Arbeitsbaum - alle drei passierten den
# Pfadfilter mit einem RELATIVEN Pfad. Keine Lab-Vorlage braucht eines davon.
# git nimmt lange Optionen auch eindeutig ABGEKÜRZT an ("--templ=x"): geprüft
# wird deshalb jeder Präfix einer verbotenen langen Option.
# Argument-Substrings, die einen shell-ausführenden bzw. entfernten Transport
# adressieren - unabhängig davon, in welchem Token sie stehen (shlex kann
# "ext::sh -c evil" durch Anführungszeichen in EIN Token packen).
GIT_VERBOTENE_MUSTER = ("ext::", "fd::", "file://")

OPENSSL_VERBOTENE_FLAGS = {"-engine", "-provider", "-provider-path", "-config", "-exec"}
# Fuer openssl prueft _openssl_pfadargumente_pruefen diese Liste zusaetzlich in
# normalisierter Form: openssl nimmt auch "--config x" und "-config=x" an.

VERBOTENE_FLAGS = {"git": GIT_VERBOTENE_FLAGS, "openssl": OPENSSL_VERBOTENE_FLAGS}
VERBOTENE_MUSTER = {"git": GIT_VERBOTENE_MUSTER, "openssl": ()}


def _werkzeug_argv_pruefen(tokens: list[str], art: str) -> str | None:
    """Allowlist-Prüfung für die Auftragsarten "git"/"openssl" (siehe
    Kommentar oben). `tokens` ist argv OHNE das Programm selbst (also
    argv[1:] aus _argv_bauen). Liefert bei einem Verstoß eine deutsche
    Fehlermeldung, die das abgelehnte Token nennt - sonst None.

    Für nicht gelistete Arten (aktuell nur "ansible", das seine eigene, feste
    Kommandozeile baut und nie über diese Funktion läuft) greift die Prüfung
    nicht - `VERBOTENE_FLAGS.get(art)` liefert dann None.

    DRITTE Schicht (P0, 2026-07-22, zweite Fassung): Schicht 1 (Subcommand-
    Allowlist) und Schicht 2 (verbotene Flags/Muster) prüften bisher nur, OB
    ein Unterkommando/Flag vorkommen darf - nicht die WERTE der dabei
    mitgegebenen Pfad-Argumente. Damit ließ sich trotz beider Schichten
    beliebiger Dateiinhalt aus dem Container lesen (`openssl enc -base64 -in
    /etc/passwd` - "enc" ist erlaubt, "-in" war ungeprüft) oder beliebig
    schreiben, auch in das mit dem Backend GETEILTE, nicht-readonly
    `/queue`-Volume (`git diff --output=/queue/x`, `openssl req -out
    /queue/x`). Siehe `_git_pfadargumente_pruefen`/`_openssl_pfadargumente_pruefen`
    weiter unten: git prüft die WERTE bekannter pfadwertiger Flags (reiner
    Dateiname, `_dateiname_gueltig`), openssl prüft fail-closed JEDES Token.
    """
    verbotene_flags = VERBOTENE_FLAGS.get(art)
    if verbotene_flags is None:
        return None

    verbotene_muster = VERBOTENE_MUSTER.get(art, ())
    for token in tokens:
        name = token.split("=", 1)[0]
        for flag in verbotene_flags:
            if token == flag or (flag.startswith("--") and len(name) > 2 and name.startswith("--")
                                 and (art == "git" and flag.startswith(name) or name == flag)):
                return (f"Unzulässiges Flag {token!r} für {art} abgelehnt "
                         f"(Allowlist statt Blockliste, siehe docs/lab-sicherheit.md).")
        for muster in verbotene_muster:
            if muster in token:
                return (f"Unzulässiges Muster {muster!r} im Argument {token!r} "
                         f"für {art} abgelehnt.")

    erlaubt = ERLAUBTE_SUBBEFEHLE.get(art, set())
    subbefehl = next((token for token in tokens if not token.startswith("-")), None)
    if subbefehl is None or subbefehl not in erlaubt:
        freigegeben = ", ".join(sorted(erlaubt)) or "(keine)"
        return (f"Unterkommando {subbefehl!r} für {art} nicht freigegeben "
                 f"(erlaubt: {freigegeben}).")

    pfad_pruefung = PFADARGUMENTE_PRUEFEN.get(art)
    if pfad_pruefung is not None:
        fehlermeldung = pfad_pruefung(tokens)
        if fehlermeldung:
            return fehlermeldung
    return None


# ---------------------------------------------------------------------------
# Dritte Schicht: Werte pfadwertiger Flags auf das Arbeitsverzeichnis
# beschränken (siehe Docstring von _werkzeug_argv_pruefen oben).
#
# git UND openssl: fail-closed über ALLE Tokens statt einer (lückenhaften)
# Liste bekannter Pfad-Flags. git erlaubt dabei relative Unterpfade mit "/"
# (Zweignamen "feature/x", "add src/app.py"), openssl verbietet "/" ganz
# (siehe OPENSSL_FREITEXT_MUSTER unten). Code-/Transport-öffnende Optionen
# fängt in beiden Fällen GIT_/OPENSSL_VERBOTENE_FLAGS in Schicht 2 ab.
# ---------------------------------------------------------------------------

# openssl: FAIL-CLOSED statt einer Liste "bekannter Pfad-Flags" (2026-10-12).
# Die frühere Liste (-in, -out, -CA, ...) war unvollständig: -CAserial,
# -writerand, -untrusted, -CApath, -kfile, -sign, -keyfile, -outdir, die
# Positionsargumente von dgst/verify u.v.m. kamen ungeprüft durch. Außerdem
# nimmt openssl (apps/lib/opt.c) JEDE Option auch als "--flag" und als
# "-flag=wert" an - "--out /queue/x" und "--config=x.cnf" umgingen damit Pfad-
# UND Flag-Sperre. Jetzt gilt für JEDES Token: kein Pfadtrenner, kein "..",
# kein Steuerzeichen - egal zu welcher Option es gehört. Was dann noch ein
# Dateiname ist, liegt zwangsläufig im Arbeitsverzeichnis.
#
# Einzige Ausnahme sind die Werte der folgenden Freitext-Optionen, die "/"
# brauchen (-subj /CN=..., -addext ...=URI:http://...). Ihre FORM ist so
# eingeschränkt, dass der Wert auch dann kein Ausbruchspfad ist, wenn openssl
# ihn anders liest als wir (z.B. "dgst -out -subj /queue/x": dort ist "-subj"
# der Wert von -out und "/queue/x" eine Eingabedatei): bei -subj muss jedes
# "/"-Segment "typ=wert" sein, -addext muss mit "name=" beginnen (also relativ)
# und darf kein ".." und keine Datei-/Abschnittsreferenz enthalten.
OPENSSL_FREITEXT_MUSTER = {
    "-subj": re.compile(r"(/[A-Za-z0-9.]+=[^/]*)+"),
    # Defensiv (nicht ausnutzbar, -config ist gesperrt): kein "file:"-URI, kein
    # "@abschnitt"-Verweis in eine Konfigurationsdatei (am Wertanfang oder nach
    # , : ; Leerzeichen - "email:a@b.de" bleibt erlaubt), kein "dirName:abschnitt".
    "-addext": re.compile(r"[A-Za-z0-9.]+ ?=(?!.*\.\.)(?!(?:.*[,:;\s])?@)(?!.*(?i:file:|dirname:)).*"),
}
# Wert ist eine Passwort-QUELLE: "pass:wert" (inline, erlaubt), "file:pfad"/
# "env:name"/"fd:n" (Datei- bzw. Umgebungszugriff, verboten). Keine der
# Lab-Vorlagen braucht diese Flags.
OPENSSL_PASSWORT_FLAGS = {"-passin", "-passout", "-pass"}


def _openssl_passwort_wert_pruefen(wert: str | None, flag: str) -> str | None:
    if wert is None or wert.startswith("pass:"):
        return None
    return (f"Unzulässige Passwort-Quelle {wert!r} für {flag!r} abgelehnt "
            f"(nur 'pass:...' erlaubt, keine Datei- oder Umgebungsquelle).")


def _bricht_aus_arbeitsverzeichnis_aus(wert: str) -> bool:
    """Lexikalisch (ohne Dateisystem): verlässt `wert` als POSIX-Pfad das
    Arbeitsverzeichnis? Absolut, ein ausbrechendes ".."-Segment, "\\" oder ein
    Steuerzeichen => True. Reine Unterpfade wie "src/app.py" oder "feature/x"
    bleiben drin => False. Symlink-Ausbrüche sind lexikalisch nicht erkennbar
    (dokumentierte Grenze; git kann im Arbeitsverzeichnis Symlinks anlegen)."""
    if any(ord(zeichen) < 32 for zeichen in wert):
        return True
    if "\\" in wert:
        return True
    if wert.startswith("/") or (len(wert) >= 2 and wert[1] == ":"):
        return True  # absolut (POSIX "/..." bzw. Windows "C:\...")
    tiefe = 0
    for segment in wert.split("/"):
        if segment == "..":
            tiefe -= 1
            if tiefe < 0:
                return True
        elif segment and segment != ".":
            tiefe += 1
    return False


def _git_pfadargumente_pruefen(tokens: list[str]) -> str | None:
    """Fail-closed: JEDES Token (Positionsargument ODER der Wert einer
    "--opt=wert"-Option) muss im Arbeitsverzeichnis bleiben. Werte in der Form
    "--opt wert" werden als eigenes Token in der nächsten Runde geprüft -
    deshalb braucht es hier keine Paarung von Option und Wert. Reine Optionen
    ohne Wert ("-b", "--allow-empty") prüft Schicht 2 (verbotene Flags)."""
    for token in tokens:
        if token.startswith("-"):
            if "=" not in token:
                continue
            wert = token.split("=", 1)[1]
        else:
            wert = token
        if _bricht_aus_arbeitsverzeichnis_aus(wert):
            return (f"Unzulässiger Pfad {wert!r} für git abgelehnt (erlaubt sind nur "
                    f"Pfade im Arbeitsverzeichnis: kein absoluter Pfad, kein '..', "
                    f"kein '\\', keine Steuerzeichen).")
    return None


def _openssl_pfadargumente_pruefen(tokens: list[str]) -> str | None:
    """Fail-closed, siehe Kommentar über OPENSSL_FREITEXT_MUSTER."""
    i = 0
    while i < len(tokens):
        token = tokens[i]
        i += 1
        if any(ord(zeichen) < 32 for zeichen in token):
            return f"Steuerzeichen im Argument {token!r} abgelehnt."
        flag, wert = None, token
        if token.startswith("-"):
            name, gleich, inline = token.partition("=")
            flag = "-" + name.lstrip("-")  # "--out" ist für openssl dasselbe wie "-out"
            if flag in OPENSSL_VERBOTENE_FLAGS:
                return (f"Unzulässiges Flag {token!r} für openssl abgelehnt "
                        f"(Allowlist statt Blockliste, siehe docs/lab-sicherheit.md).")
            if flag in OPENSSL_FREITEXT_MUSTER or flag in OPENSSL_PASSWORT_FLAGS:
                if gleich:
                    wert = inline
                else:
                    wert = tokens[i] if i < len(tokens) else ""
                    i += 1
        if flag in OPENSSL_PASSWORT_FLAGS:
            fehlermeldung = _openssl_passwort_wert_pruefen(wert, flag)
            if fehlermeldung:
                return fehlermeldung
        elif flag in OPENSSL_FREITEXT_MUSTER:
            if not OPENSSL_FREITEXT_MUSTER[flag].fullmatch(wert):
                return f"Unzulässiger Wert {wert!r} für {flag!r} abgelehnt."
        elif "/" in token or "\\" in token or ".." in token:
            vorher = tokens[i - 2] if i >= 2 else "openssl"
            return (f"Unzulässiger Pfad {token!r} nach {vorher!r} abgelehnt (erlaubt sind "
                    f"nur Dateinamen im Arbeitsverzeichnis: kein Pfadtrenner, kein '..', "
                    f"kein absoluter Pfad).")
    return None


PFADARGUMENTE_PRUEFEN = {
    "git": _git_pfadargumente_pruefen,
    "openssl": _openssl_pfadargumente_pruefen,
}


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

    Das allein reicht NICHT: Ohne weitere Prüfung könnte ein Argument wie
    `ext::sh -c evil` das Werkzeug selbst (git) dazu bringen, Code auszuführen
    (git-eigener "ext"-Transport). Die zurückgegebenen Tokens durchlaufen
    deshalb in `_run_werkzeug` zusätzlich `_werkzeug_argv_pruefen` (Allowlist
    der Unterkommandos je Art, siehe dort) - diese Funktion zerlegt nur, sie
    entscheidet nicht, ob das Ergebnis erlaubt ist.
    """
    tokens = shlex.split(befehl)
    if not tokens:
        return None
    if tokens[0] == art:
        tokens = tokens[1:]
    return [binaer] + tokens


def _exklusiv_schreiben(ziel: Path, inhalt: str, modus: int, uid: int | None = None) -> None:
    """Legt `ziel` NEU an, statt in Vorhandenes zu schreiben, und folgt dabei
    keinem Symlink (O_EXCL|O_NOFOLLOW). Der Worker schreibt als root an Orte,
    an denen ein Lauf - auch ein früherer - einen Symlink oder ein FIFO
    gleichen Namens hinterlegt haben kann: `ziel -> /queue/in/x.json` brächte
    ihn sonst dazu, einen fremden Auftrag zu schreiben."""
    ziel.unlink(missing_ok=True)
    fd = os.open(ziel, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), modus)
    with os.fdopen(fd, "w", encoding="utf-8") as datei:
        datei.write(inhalt)
        if hasattr(os, "fchmod"):  # unabhängig von der umask; Windows: nur Tests
            os.fchmod(fd, modus)
        if uid is not None:
            os.fchown(fd, uid, uid)


def _datei_schreiben(ziel: Path, inhalt: str, uid: int | None) -> None:
    """Legt eine mitgeschickte Datei im Arbeitsverzeichnis an (gehört dem Lauf)."""
    _exklusiv_schreiben(ziel, inhalt, 0o644 if uid is None else 0o600, uid)


def _regulaer_lesen(pfad: Path, hoechstens: int = 1_000_000) -> str:
    """Liest NUR eine reguläre Datei: kein Symlink (O_NOFOLLOW), und ein FIFO
    hält den Worker nicht an (O_NONBLOCK, dann Typprüfung am Deskriptor)."""
    fd = os.open(pfad, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(fd, "rb") as datei:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise OSError(f"{pfad.name} ist keine reguläre Datei")
        return datei.read(hoechstens).decode("utf-8")


def _werkzeug_ergebnis(begonnen: float, rc: int, text: str, timed_out: bool = False) -> dict:
    text_gekuerzt, gekappt = _clip(text)
    return {"rc": rc, "output": text_gekuerzt, "truncated": gekappt,
            "duration_ms": int((time.monotonic() - begonnen) * 1000),
            "timed_out": timed_out}


def _run_werkzeug(auftrag: dict, art: str, binaer: str, zeitgrenze: float,
                   zusatz_umgebung: dict[str, str] | None = None) -> dict:
    """Führt eine kurze Folge von Befehlen für ein Kommandozeilen-Werkzeug aus.

    `cwd` ist bewusst das DAUERHAFTE Arbeitsverzeichnis der Teilnehmerin
    (`_workspace`), nicht ein frisches Lauf-Verzeichnis wie bei Ansible: eine in
    Aufgabe 1 erzeugte CA muss bis Aufgabe 3 überleben (Änderung 2 im Entwurf).
    """
    begonnen = time.monotonic()

    dateien = auftrag.get("files") or {}
    fehler = _dateien_pruefen(dateien)
    if fehler:
        return _werkzeug_ergebnis(begonnen, 2, fehler)

    befehle = auftrag.get("commands") or []
    fehler = _befehle_pruefen(befehle)
    if fehler:
        return _werkzeug_ergebnis(begonnen, 2, fehler)

    # Auch openssl/git laufen im Slot unter der Job-uid: git führt Hooks aus,
    # die ein früheres Playbook im selben Arbeitsverzeichnis hinterlegt haben kann.
    with _job(str(auftrag.get("workspace", "gast"))) as (arbeitsplatz, laufverzeichnis, uid):
        return _run_werkzeug_im_slot(dateien, befehle, art, binaer, zeitgrenze, zusatz_umgebung,
                                     arbeitsplatz, laufverzeichnis, uid, begonnen)


def _run_werkzeug_im_slot(dateien: dict, befehle: list, art: str, binaer: str,
                          zeitgrenze: float, zusatz_umgebung: dict[str, str] | None,
                          arbeitsplatz: Path, laufverzeichnis: Path, uid: int | None,
                          begonnen: float) -> dict:
    for name, inhalt in dateien.items():
        _datei_schreiben(arbeitsplatz / name, str(inhalt), uid)

    umgebung = {
        "PATH": os.getenv("PATH", "/usr/local/bin:/usr/bin:/bin"),
        "HOME": str(arbeitsplatz),
        # Eigenes Temp-Verzeichnis des Laufs statt des gemeinsamen /tmp - und
        # nicht im Arbeitsverzeichnis, wo `git status` es anzeigen würde.
        "TMPDIR": str(laufverzeichnis),
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
    # Ab hier, nicht ab Auftragsbeginn: Warten auf einen Slot zählt nicht mit.
    frist = time.monotonic() + zeitgrenze
    for befehl in befehle:
        argv = _argv_bauen(befehl, art, binaer)
        if argv is None:
            rc = 2
            ausgabe_teile.append(f"$ {befehl}\nLeere Befehlszeile abgelehnt.")
            break
        anzeige = " ".join([art] + argv[1:])
        ausgabe_teile.append(f"$ {anzeige}")

        fehlermeldung = _werkzeug_argv_pruefen(argv[1:], art)
        if fehlermeldung:
            rc = 2
            ausgabe_teile.append(fehlermeldung)
            break

        verbleibend = frist - time.monotonic()
        if verbleibend <= 0:
            abgebrochen = True
            rc = 124
            ausgabe_teile.append(f"Abgebrochen: Der Lauf hat die Zeitgrenze von "
                                  f"{zeitgrenze:.0f} Sekunden überschritten.")
            break
        try:
            rc, roh, befehl_abgebrochen = _mit_zeitgrenze_ausfuehren(
                argv, arbeitsplatz, umgebung, verbleibend, uid)
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

    return _werkzeug_ergebnis(begonnen, rc, "\n".join(ausgabe_teile), timed_out=abgebrochen)


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
        # Zweite Verteidigungsebene zu _werkzeug_argv_pruefen oben: blockt
        # Netztransporte (ext/ssh/http/git/...) auf Umgebungsebene. Ergänzt
        # die Allowlist-Prüfung, ersetzt sie nicht.
        "GIT_ALLOW_PROTOCOL": "file",
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
    # Fail-closed: ohne Trennung kein Teilnehmer-Code. openssl/git bleiben
    # nutzbar - sie führen keinen frei geschriebenen Code aus.
    sperrgrund = _ansible_sperrgrund() if art == "ansible" else None
    if sperrgrund:
        return {"rc": 2,
                "output": ("Das Ansible-Lab ist auf diesem Server deaktiviert, weil Läufe nicht "
                           f"vom Lab-Dienst getrennt werden können: {sperrgrund}"),
                "truncated": False, "duration_ms": 0, "timed_out": False}
    return handler(auftrag)


def _antwort_schreiben(auftrags_id: str, ergebnis: dict) -> None:
    ziel = QUEUE / "out" / f"{auftrags_id}.json"
    vorlaeufig = ziel.with_suffix(".json.tmp")
    # 0644: lesbar für das Backend (andere uid). Den Schutz vor Läufen leisten die
    # Verzeichnisrechte von /queue (_warteschlange_vorbereiten), nicht dieser Modus.
    _exklusiv_schreiben(vorlaeufig, json.dumps(ergebnis), 0o644)
    os.replace(vorlaeufig, ziel)  # atomar: das Backend sieht nie eine halbe Datei


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


def _auftrag_lesen(pfad: Path) -> tuple[str, dict] | None:
    """Liest einen beanspruchten Auftrag und löscht die Datei SOFORT.

    Passiert direkt beim Beanspruchen (in _runde), nicht erst wenn ein Thread
    frei wird: Der Auftrag trägt ein Ergebnis-Token des Backends, und solange
    die Datei im Volume liegt, könnte ein Teilnehmer-Playbook sie lesen, falls
    die Trennung per uid einmal nicht greift (zweite Schicht). Danach existiert
    das Token nur noch im Speicher dieses Prozesses. Siehe docs/lab-sicherheit.md.
    """
    auftrags_id = pfad.name.removesuffix(".claimed").removesuffix(".json")
    try:
        # In einem Bestands-Volume kann ein früherer Lauf Symlinks, FIFOs oder
        # Verzeichnisse mit passendem Namen hinterlassen haben.
        auftrag = json.loads(_regulaer_lesen(pfad))
        if not isinstance(auftrag, dict):
            raise ValueError("kein JSON-Objekt")
    except (OSError, ValueError) as fehler:
        log("Auftrag unlesbar:", pfad.name, fehler)
        _loeschen(pfad)
        return None
    pfad.unlink(missing_ok=True)  # nur einmal ausführen, auch wenn danach etwas schiefgeht
    return auftrags_id, auftrag


def _bearbeiten(auftrags_id: str, auftrag: dict) -> None:
    # Token nicht an die Handler weiterreichen — es gehört nur ins Ergebnis.
    token = auftrag.pop("token", None)
    try:
        ergebnis = _ausfuehren(auftrag)
    except Exception as fehler:  # noqa: BLE001 - der Arbeiter darf nie sterben
        log("Lauf fehlgeschlagen:", auftrags_id, fehler)
        ergebnis = {"rc": 1, "output": f"Interner Fehler im Lab-Runner: {fehler}",
                    "truncated": False, "duration_ms": 0, "timed_out": False}
    if token is not None:
        ergebnis = {**ergebnis, "token": token}
    _antwort_schreiben(auftrags_id, ergebnis)


def _aufraeumen() -> None:
    jetzt = time.time()
    for ordner in ("in", "out"):
        for eintrag in list((QUEUE / ordner).glob("*.json")) + list((QUEUE / ordner).glob("*.claimed")):
            try:
                if jetzt - eintrag.lstat().st_mtime > JOB_MAX_AGE_SECONDS:
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
        pfad = QUEUE / ordner
        try:
            if os.path.lexists(pfad) and (pfad.is_symlink() or not pfad.is_dir()):
                # Bestands-Volume (früher 0777, Läufe als Eigentümer): ein Lauf kann
                # in/ oder out/ durch einen Symlink ersetzt haben. Nicht folgen -
                # den Eintrag entfernen und ein echtes Verzeichnis anlegen.
                log(f"Warteschlange {pfad} ist kein Verzeichnis (Symlink oder Datei) - wird ersetzt.")
                pfad.unlink()
            pfad.mkdir(parents=True, exist_ok=True)
        except OSError as fehler:
            log(f"Warteschlange {pfad} nicht nutzbar: {fehler}. "
                f"Erwartet wird ein Volume, in das der Runner-Benutzer (uid "
                f"{_eigene_uid()}) schreiben darf — siehe runner/Dockerfile und "
                f"docs/lab-sicherheit.md.")
            return False
    # root:QUEUE_GID, kein Zugriff für andere: Worker (Eigentümer) und Backend
    # (Gruppe) ja, Läufe nein. Korrigiert auch ein Volume einer älteren Fassung
    # (uid 10001, 0777) beim ersten Start.
    for pfad, modus in ((QUEUE, 0o750), (QUEUE / "in", 0o770), (QUEUE / "out", 0o770)):
        try:
            if _isolation_aktiv:
                _verzeichnis_sichern(pfad, 0, QUEUE_GID, modus)
            else:
                os.chmod(pfad, modus)
        except OSError as fehler:
            if _isolation_aktiv:
                # Fail-closed: mit offener Warteschlange wäre die Trennung wertlos.
                log(f"Warteschlange {pfad} lässt sich nicht für Läufe schließen: {fehler}.")
                return False
            # ohne Trennung nicht Eigentümer: Rechte bleiben, wie sie sind
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
                gelesen = _auftrag_lesen(ziel)
                if gelesen is not None:
                    offene.append(pool.submit(_bearbeiten, *gelesen))
                beansprucht += 1
    return offene, beansprucht


def main() -> None:
    _isolation_einrichten()  # vor der Warteschlange: deren Rechte hängen davon ab
    while not _warteschlange_vorbereiten():
        time.sleep(5)
    log(f"Lab-Runner bereit. Warteschlange: {QUEUE}, parallel: {MAX_PARALLEL}, "
        f"Warteschlangentiefe: {MAX_QUEUE_DEPTH}, "
        f"Zeitgrenze: {TIMEOUT_SECONDS:.0f}s, Netzwerk: keines, "
        f"Arten: {', '.join(sorted(RUNNER_KINDS)) or '(keine)'}, "
        f"Trennung: {'uid je Lauf' if _isolation_aktiv else 'KEINE'}")

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
