"""Echte Pruefung der Trennung der Laeufe - gegen einen LAUFENDEN Runner.

Kein pytest-Test (laeuft nicht in `pytest runner/tests`): Das Skript spielt das
Backend. Es legt echte Auftraege in die Warteschlange, wartet auf die
Ergebnisse und prueft, was ein boesartiges Playbook im Runner NICHT kann.
Nur Standardbibliothek, lauffaehig mit dem Python des Backend-Images.

Aufruf (Einzelheiten in docs/lab-sicherheit.md, "Trennung nachpruefen"):
  bash ops/lab-isolation-test.sh                       # eigenes Compose-Projekt, wie in der CI
  docker exec -i <backend-container> python - < runner/tests/isolation_check.py   # laufendes System

Muss unter der uid/gid des Backends laufen (sonst kein Zugriff auf /queue) und
braucht RUNNER_KINDS=ansible,openssl,git beim Runner (sonst --arten anpassen).
Ende mit 0, wenn alles stimmt; sonst 1 und je Befund eine Zeile "FEHLER ...".
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import secrets
import sys
import threading
import time
import uuid
from pathlib import Path

JOB_UIDS = range(10002, 10010)  # = worker.JOB_UIDS
WORKSPACE_ROOT = "/tmp/lab-workspaces"  # = worker.WORKSPACE_ROOT im Container

fehler: list[str] = []


def pruefe(name: str, bedingung: object, detail: object = "") -> bool:
    if bedingung:
        print(f"OK      {name}", flush=True)
    else:
        fehler.append(name)
        print(f"FEHLER  {name}" + (f"\n        {str(detail)[:3000]}" if detail != "" else ""), flush=True)
    return bool(bedingung)


class Warteschlange:
    def __init__(self, pfad: Path, frist: float) -> None:
        self.pfad, self.frist = pfad, frist

    def auftrag(self, name: str, **felder: object) -> dict:
        """Wie backend/app/routers/lab.py: atomar ablegen, auf out/ warten,
        Token pruefen. Liefert immer ein dict (bei Ausfall rc=-1)."""
        auftrags_id, token = uuid.uuid4().hex, secrets.token_urlsafe(32)
        eingang = self.pfad / "in" / f"{auftrags_id}.json"
        ausgang = self.pfad / "out" / f"{auftrags_id}.json"
        try:
            vorlaeufig = eingang.with_suffix(".json.tmp")
            vorlaeufig.write_text(json.dumps({**felder, "token": token}), encoding="utf-8")
            os.replace(vorlaeufig, eingang)
        except OSError as err:
            pruefe(f"{name}: Auftrag ablegen", False, f"{err!r} (uid {os.getuid()}, gid {os.getgid()})")
            return {"rc": -1, "output": ""}
        ende = time.monotonic() + self.frist
        while time.monotonic() < ende:
            try:
                ergebnis = json.loads(ausgang.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                time.sleep(0.15)
                continue
            ausgang.unlink(missing_ok=True)
            pruefe(f"{name}: Ergebnis traegt das Token des Auftrags", ergebnis.get("token") == token)
            pruefe(f"{name}: Auftragsdatei wurde beim Beanspruchen entfernt", not eingang.exists())
            return ergebnis
        eingang.unlink(missing_ok=True)
        pruefe(f"{name}: Ergebnis innerhalb von {self.frist:.0f}s", False,
               "kein out/<id>.json - laeuft der Runner? (docker logs <runner-container>)")
        return {"rc": -1, "output": ""}


def playbook(tasks: list, fakten: bool = False) -> str:
    # JSON ist gueltiges YAML - spart das Einruecken von Hand.
    return json.dumps([{"hosts": "all", "gather_facts": fakten, "tasks": tasks}])


def skript_tasks(skript: str, argument: dict) -> list:
    """Legt `skript` ins Arbeitsverzeichnis und fuehrt es mit python3 aus.
    Die Skripte unten enthalten bewusst keine doppelten geschweiften Klammern
    (Ansible wuerde sie als Jinja-Ausdruck lesen)."""
    return [
        {"copy": {"content": skript, "dest": "{{ lab_dir }}/pruefskript.py"}},
        {"command": {"argv": ["python3", "{{ lab_dir }}/pruefskript.py", json.dumps(argument)]},
         "register": "lauf", "failed_when": False},
        {"debug": {"var": "lauf.stdout_lines"}},
        {"debug": {"var": "lauf.stderr_lines"}},
    ]


# Laeuft IM Runner unter der Job-uid. Jede Zeile "PROBE <name> DICHT <Fehlerart>"
# heisst: der Zugriff wurde abgelehnt. "LECK" heisst: er ging durch.
ANGRIFF = r'''
import json, os, signal, sys, time
arg = json.loads(sys.argv[1])
ich = os.getuid()

def versuch(name, zugriff):
    try:
        wert = zugriff()
    except OSError as err:
        print("PROBE", name, "DICHT", type(err).__name__)
    else:
        print("PROBE", name, "LECK", repr(wert)[:120])

def lesen(pfad):
    with open(pfad, "rb") as datei:
        return datei.read(64)

def schreiben(pfad):
    with open(pfad, "w") as datei:
        datei.write("gefaelscht")
    return "geschrieben"

def uids(pid):
    try:
        with open("/proc/%s/status" % pid) as datei:
            for zeile in datei:
                if zeile.startswith("Uid:"):
                    return [int(u) for u in zeile.split()[1:]]
    except OSError:
        pass
    return []

status = dict(z.split(":\t", 1) for z in open("/proc/self/status").read().splitlines() if ":\t" in z)
print("INFO uid=%d gid=%d gruppen=%s capeff=%s capprm=%s nnp=%s" % (
    ich, os.getgid(), os.getgroups(), status["CapEff"], status["CapPrm"], status.get("NoNewPrivs")))

q = arg["queue"]
for ordner in ("", "/in", "/out"):
    versuch("queue_auflisten" + ordner, lambda: os.listdir(q + ordner))
versuch("queue_in_schreiben", lambda: schreiben(q + "/in/gefaelscht.json"))
versuch("queue_out_schreiben", lambda: schreiben(q + "/out/gefaelscht.json"))
versuch("queue_in_lesen", lambda: lesen(arg["koeder_in"]))
versuch("queue_out_lesen", lambda: lesen(arg["koeder_out"]))
versuch("queue_out_loeschen", lambda: os.unlink(arg["koeder_out"]))

versuch("arbeitsverzeichnisse_auflisten", lambda: os.listdir(arg["workspace_root"]))
for name, pfad in (("ruhend", arg["fremd_ruhend"]), ("aktiv", arg["fremd_aktiv"])):
    versuch("fremdes_verzeichnis_%s_auflisten" % name, lambda: os.listdir(pfad))
    versuch("fremdes_verzeichnis_%s_lesen" % name, lambda: lesen(pfad + "/geheim.txt"))
    versuch("fremdes_verzeichnis_%s_schreiben" % name, lambda: schreiben(pfad + "/untergeschoben.txt"))

# Der Worker: alle Prozesse mit uid 0 (im Container PID 1).
for pid in sorted(int(p) for p in os.listdir("/proc") if p.isdigit()):
    if uids(pid)[:1] != [0]:
        continue
    basis = "/proc/%d/" % pid
    versuch("worker_pid%d_environ" % pid, lambda: lesen(basis + "environ"))
    versuch("worker_pid%d_mem" % pid, lambda: lesen(basis + "mem"))
    versuch("worker_pid%d_cwd" % pid, lambda: os.readlink(basis + "cwd"))
    versuch("worker_pid%d_fd" % pid, lambda: os.listdir(basis + "fd"))
    versuch("worker_pid%d_signal0" % pid, lambda: os.kill(pid, 0))
    versuch("worker_pid%d_sigkill" % pid, lambda: os.kill(pid, signal.SIGKILL))

# Der gleichzeitig laufende fremde Lauf: andere Job-uid.
fremde = []
ende = time.time() + arg["warten"]
while not fremde and time.time() < ende:
    fremde = [int(p) for p in os.listdir("/proc") if p.isdigit()
              and any(u != ich and arg["uid_von"] <= u <= arg["uid_bis"] for u in uids(p))]
    if not fremde:
        time.sleep(0.2)
print("INFO fremde_prozesse=%d" % len(fremde))
for pid in fremde[:3]:
    basis = "/proc/%d/" % pid
    versuch("fremder_lauf_environ", lambda: lesen(basis + "environ"))
    versuch("fremder_lauf_mem", lambda: lesen(basis + "mem"))
    versuch("fremder_lauf_cwd", lambda: os.readlink(basis + "cwd"))
    versuch("fremder_lauf_signal0", lambda: os.kill(pid, 0))
    versuch("fremder_lauf_sigkill", lambda: os.kill(pid, signal.SIGKILL))
# Hardlink auf eine fremde Datei desselben Dateisystems (liegt fuer alle les-
# und schreibbar in /tmp): gaebe der Worker den Link spaeter per chown an uns,
# gehoerte uns die fremde Datei.
hier = os.path.dirname(os.path.abspath(__file__))
ende = time.time() + 5
while not os.path.exists(arg["opfer_tmp"]) and time.time() < ende:
    time.sleep(0.2)
try:
    os.link(arg["opfer_tmp"], hier + "/hart")
    print("INFO hardlink=angelegt")
except OSError as err:
    print("INFO hardlink=abgelehnt:" + type(err).__name__)
print("INFO angriff_fertig")
'''

# Ueberlebt die Zeitgrenze, wenn der Worker nur die Prozessgruppe beendet: ein
# Kind verlaesst Sitzung und Gruppe (setsid), ein weiteres bleibt drin.
ENDLOS = r'''
import os, sys, time
if os.fork() == 0:
    os.setsid()
    if os.fork() == 0:
        time.sleep(3600)
    time.sleep(3600)
if os.fork() == 0:
    time.sleep(3600)
print("INFO endlos_gestartet uid=%d" % os.getuid(), flush=True)
while True:
    time.sleep(1)
'''

# Sucht nach dem Timeout-Lauf nach dessen Ueberresten (cmdline ist fuer alle lesbar).
NACHSCHAU = r'''
import os, sys
reste = []
for pid in os.listdir("/proc"):
    if pid.isdigit() and int(pid) != os.getpid():
        try:
            with open("/proc/%s/cmdline" % pid, "rb") as datei:
                zeile = datei.read().replace(b"\0", b" ").decode("utf-8", "replace")
        except OSError:
            continue
        if "pruefskript.py" in zeile:
            reste.append(pid + ":" + zeile[:80])
print("INFO reste=%d %s" % (len(reste), reste))
hier = os.path.dirname(os.path.abspath(__file__))
print("INFO hart=%s" % ("vorhanden" if os.path.lexists(hier + "/hart") else "fehlt"))
'''

# Hinterlaesst im Arbeitsverzeichnis und an den gemeinsamen Schreiborten alles,
# womit ein Lauf den root-Worker beim Aufraeumen oder den naechsten Lauf
# hereinlegen koennte.
HINTERLASSEN = r'''
import json, os, socket, sys
arg = json.loads(sys.argv[1])
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def tue(name, aktion):
    try:
        aktion()
        print("INFO %s=angelegt" % name)
    except OSError as err:
        print("INFO %s=abgelehnt:%s" % (name, type(err).__name__))

def datei(pfad, inhalt="x", modus=None):
    with open(pfad, "w") as d:
        d.write(inhalt)
    if modus is not None:
        os.chmod(pfad, modus)

def klebrig():
    os.mkdir("klebrig")
    datei("klebrig/drin")
    os.mkfifo("klebrig/fifo-drin")
    os.chmod("klebrig", 0o3777)

def sockel():
    s = socket.socket(socket.AF_UNIX)
    s.bind("sock")

def doppelt():
    datei("original")
    os.link("original", "zweitname")

def gemeinsam(ort):
    basis = ort + "/" + arg["praefix"]
    datei(basis + "-datei", "GEHEIM-GEMEINSAM", 0o644)
    os.symlink(arg["queue"] + "/in", basis + "-link")
    os.makedirs(basis + "-baum/a/b")
    datei(basis + "-baum/a/b/datei")
    os.mkfifo(basis + "-baum/a/fifo")
    os.symlink(arg["queue"], basis + "-baum/a/b/link")
    os.chmod(basis + "-baum/a", 0o1777)

tue("symlink_queue", lambda: os.symlink(arg["queue"] + "/in/evil.json", "ziel"))
tue("symlink_passwd", lambda: os.symlink("/etc/passwd", "passwd-link"))
tue("sonderbit_datei", lambda: datei("suid-datei", "#!/bin/sh\n", 0o6755))
tue("sonderbit_verzeichnis", klebrig)
tue("fifo", lambda: os.mkfifo("fifo"))
tue("socket", sockel)
tue("hardlink_eigen", doppelt)
tue("gemeinsam_tmp", lambda: gemeinsam("/tmp"))
tue("gemeinsam_shm", lambda: gemeinsam("/dev/shm"))
print("INFO uid=%d" % os.getuid())
'''

# Schaut zwei Laeufe spaeter nach, was davon uebrig ist.
NACHHER = r'''
import json, os, stat, sys
arg = json.loads(sys.argv[1])
hier = os.path.dirname(os.path.abspath(__file__))

def art(pfad):
    try:
        modus = os.lstat(pfad).st_mode
    except OSError:
        return "fehlt"
    for name, test in (("symlink", stat.S_ISLNK), ("regulaer", stat.S_ISREG), ("verzeichnis", stat.S_ISDIR)):
        if test(modus):
            return name
    return "spezial"

for name in ("ziel", "passwd-link", "fifo"):
    inhalt = "-"
    if art(hier + "/" + name) == "regulaer":
        with open(hier + "/" + name) as d:
            inhalt = d.read().strip()
    print("INFO %s_art=%s %s_inhalt=%s" % (name, art(hier + "/" + name), name, inhalt))
with open("/etc/passwd") as d:
    passwd = d.read()
print("INFO passwd=%s" % ("unveraendert" if passwd.startswith("root:") and "LAB-INHALT" not in passwd else "VERAENDERT"))

sonder, root, spezial, mehrfach, fremd = [], [], [], [], []
for wurzel, ordner, dateien in os.walk(hier):
    for name in ordner + dateien:
        st = os.lstat(os.path.join(wurzel, name))
        if not stat.S_ISLNK(st.st_mode) and st.st_mode & 0o7000:
            sonder.append(name)
        if st.st_uid == 0:
            root.append(name)
        if st.st_uid != os.getuid():
            fremd.append(name)
        if art(os.path.join(wurzel, name)) == "spezial":
            spezial.append(name)
        if stat.S_ISREG(st.st_mode) and st.st_nlink > 1:
            mehrfach.append(name)
for name, liste in (("sonderbits", sonder), ("root_eintraege", root), ("fremde_eintraege", fremd),
                    ("spezialdateien", spezial), ("mehrfach_verlinkt", mehrfach)):
    print("INFO %s=%d %s" % (name, len(liste), liste))
st = os.lstat(hier + "/klebrig")
print("INFO klebrig_modus=%o" % (st.st_mode & 0o7777))
reste = [ort + "/" + name for ort in ("/tmp", "/dev/shm") for name in os.listdir(ort)
         if name.startswith(arg["praefix"])]
print("INFO reste_gemeinsam=%d %s" % (len(reste), reste))
print("INFO uid=%d" % os.getuid())
'''

# 1 MB mit ANSI-Sequenzen, NUL, BEL, Backspace, ungueltigem UTF-8, Ruecklauf.
FLUT_BYTES = b"\x1b[31mROT\x1b[0m" + b"\x00\x07\x08" + b"\xff\xfe" + b"\x1b]0;titel\x07" + b"\r\n"
# Fuer das Playbook ohne die ungueltigen UTF-8-Bytes: Ansible lehnt eine
# Modul-Ausgabe damit selbst ab ("Refusing to deserialize an invalid UTF8 string").
FLUT = r'''
import sys
stueck = b"\x1b[31mROT\x1b[0m" + b"\x00\x07\x08" + b"\x1b]0;titel\x07" + b"\r\n"
sys.stdout.buffer.write(stueck * (1024 * 1024 // len(stueck) + 1))
'''

# Kursvorlagen: Abschrift aus frontend/src/widgets/opensslab/templates.ts und
# frontend/src/widgets/gitlab/templates.ts (id in Klammern).
LIEFERSCHEIN = {"lieferschein.txt": "Lieferschein 4711: 12 Paletten nach Hamburg\n",
                "lieferschein-manipuliert.txt": "Lieferschein 4711: 13 Paletten nach Hamburg\n"}
OPENSSL_VORLAGEN = [
    ("schluessel-csr", {}, [
        "genrsa -out server.key 2048",
        ("req -new -key server.key -out server.csr -subj /CN=www.nordwind-logistik.de"
         " -addext subjectAltName=DNS:www.nordwind-logistik.de"),
        "req -in server.csr -noout -text"], 0, "Certificate Request"),
    ("signieren-pruefen", LIEFERSCHEIN, [
        "genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out sign.key",
        "pkey -in sign.key -pubout -out sign.pub",
        "dgst -sha256 -sign sign.key -out lieferschein.sig lieferschein.txt",
        "dgst -sha256 -verify sign.pub -signature lieferschein.sig lieferschein.txt"], 0, "Verified OK"),
    # Braucht OpenSSL >= 3.5 (ML-KEM/ML-DSA) - belegt die Mindestversion praktisch.
    ("pqc-schluessel", {}, [
        "genpkey -algorithm ML-KEM-768 -out mlkem.key",
        "pkey -in mlkem.key -pubout",
        "genpkey -algorithm ML-DSA-65 -out mldsa.key",
        "req -x509 -key mldsa.key -out mldsa.pem -days 30 -subj /CN=pq-test.nordwind-logistik.de",
        "x509 -in mldsa.pem -noout -text"], 0, "ML-DSA-65"),
]
GIT_VORLAGEN = [
    ("init-commit", {"README.md": "# Kurs-Repo\n"}, ["init", "add .", "commit -m start"], 0, "start"),
    # Zweiter Lauf derselben Vorlage, in aller Regel unter einer ANDEREN Job-uid:
    # scheitert die Uebergabe des Arbeitsverzeichnisses, meldet git hier
    # "dubious ownership" statt "nothing to commit".
    ("init-commit (2. Lauf)", {"README.md": "# Kurs-Repo\n"}, ["init", "add .", "commit -m start"],
     1, "nothing to commit"),
    ("worktree", {}, ["init", "commit --allow-empty -m base", "worktree add wt-feature -b feature-wt",
                      "worktree list"], 0, "wt-feature"),
]


def info(ausgabe: str, schluessel: str) -> str | None:
    treffer = re.search(rf"INFO [^\n\"]*\b{schluessel}=([^\s\"\\]+)", ausgabe)
    return treffer.group(1) if treffer else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--queue", default=os.getenv("LAB_QUEUE_DIR") or "/queue")
    parser.add_argument("--arten", default="ansible,openssl,git",
                        help="was der Runner freigegeben hat (RUNNER_KINDS)")
    parser.add_argument("--zeitgrenze", type=float, default=float(os.getenv("RUNNER_TIMEOUT") or 30),
                        help="RUNNER_TIMEOUT des Runners in Sekunden")
    parser.add_argument("--modus", choices=["voll", "failclosed"], default="voll",
                        help="failclosed: der Runner laeuft OHNE Trennung und muss Ansible ablehnen")
    optionen = parser.parse_args()
    arten = {teil.strip() for teil in optionen.arten.split(",") if teil.strip()}
    queue = Path(optionen.queue)
    ws = Warteschlange(queue, optionen.zeitgrenze + 45)
    lauf = secrets.token_hex(4)
    kennung = {name: f"pruefung{lauf}{name}" for name in ("a", "b", "c", "s", "w")}
    print(f"Pruefung {lauf}: Warteschlange {queue}, als uid {os.getuid()} gid {os.getgid()}, "
          f"Arten {sorted(arten)}, Zeitgrenze {optionen.zeitgrenze:.0f}s", flush=True)

    # --- Rechte der Warteschlange, vom Backend aus gesehen ---------------------
    for ordner, modus in (("", 0o750), ("in", 0o770), ("out", 0o770)) if optionen.modus == "voll" else ():
        try:
            st = (queue / ordner).stat()
            pruefe(f"/queue/{ordner} gehoert root, Gruppe des Backends, Modus {modus:o}",
                   (st.st_uid, st.st_gid, st.st_mode & 0o777) == (0, os.getgid(), modus),
                   f"uid {st.st_uid}, gid {st.st_gid}, Modus {st.st_mode & 0o777:o}")
        except OSError as err:
            pruefe(f"/queue/{ordner} ist fuer das Backend erreichbar", False, repr(err))

    if optionen.modus == "failclosed":
        failclosed_pruefen(ws, kennung)
        print(f"\n{len(fehler)} Fehler" + ("" if not fehler else ":\n  - " + "\n  - ".join(fehler)), flush=True)
        return 1 if fehler else 0
    if "ansible" in arten:
        ansible_pruefen(ws, queue, kennung, optionen.zeitgrenze)
        hinterlassenschaften_pruefen(ws, queue, kennung, arten)
    flut_pruefen(ws, kennung, arten)
    for art, vorlagen in (("openssl", OPENSSL_VORLAGEN), ("git", GIT_VORLAGEN)):
        if art not in arten:
            continue
        for vorlage, dateien, befehle, rc, erwartet in vorlagen:
            ergebnis = ws.auftrag(f"(d) {art} {vorlage}", kind=art, workspace=kennung["w"] + art,
                                  commands=befehle, **({"files": dateien} if dateien else {}))
            pruefe(f"(d) {art}-Vorlage {vorlage}: rc={rc} und {erwartet!r} in der Ausgabe",
                   ergebnis.get("rc") == rc and erwartet in ergebnis.get("output", ""),
                   f"rc={ergebnis.get('rc')}\n{ergebnis.get('output')}")

    print(f"\n{len(fehler)} Fehler" + ("" if not fehler else ":\n  - " + "\n  - ".join(fehler)), flush=True)
    return 1 if fehler else 0


def failclosed_pruefen(ws: Warteschlange, kennung: dict) -> None:
    """(8) Runner ohne user 0:0/cap_add: Ansible muss mit Klartext abgelehnt
    werden, openssl muss laufen."""
    ansible = ws.auftrag("(8) Ansible ohne Trennung", kind="ansible", workspace=kennung["a"],
                         playbook=playbook([{"command": "id -u"}]))
    pruefe("(8) fail-closed: Ansible-Auftrag wird mit Klartext abgelehnt (rc=2, 'deaktiviert')",
           ansible.get("rc") == 2 and "deaktiviert" in ansible.get("output", "")
           and "PLAY" not in ansible.get("output", ""),
           f"rc={ansible.get('rc')}\n{ansible.get('output')}")
    _vorlage, _dateien, befehle, rc, erwartet = OPENSSL_VORLAGEN[0]
    openssl = ws.auftrag("(8) openssl ohne Trennung", kind="openssl", workspace=kennung["w"], commands=befehle)
    pruefe("(8) fail-closed: openssl-Auftrag laeuft weiter (rc=0)",
           openssl.get("rc") == rc and erwartet in openssl.get("output", ""),
           f"rc={openssl.get('rc')}\n{openssl.get('output')}")


def hinterlassenschaften_pruefen(ws: Warteschlange, queue: Path, kennung: dict, arten: set) -> None:
    """(1), (3), (4), (6): Lauf A hinterlaesst Fallen, Lauf B schreibt Lab-Dateien
    gleichen Namens, Lauf C sieht nach."""
    argument = {"queue": str(queue), "praefix": kennung["s"]}
    erster = ws.auftrag("(1) Fallen legen", kind="ansible", workspace=kennung["s"],
                        playbook=playbook(skript_tasks(HINTERLASSEN, argument)))
    ausgabe = erster.get("output", "")
    angelegt = ["symlink_queue", "symlink_passwd", "sonderbit_datei", "sonderbit_verzeichnis", "fifo",
                "socket", "hardlink_eigen", "gemeinsam_tmp", "gemeinsam_shm"]
    if not pruefe("(1) Lauf A hat alle Fallen angelegt (Symlinks, Sonderbits, FIFO, Socket, Hardlink, /tmp, /dev/shm)",
                  erster.get("rc") == 0 and all(info(ausgabe, name) == "angelegt" for name in angelegt),
                  f"rc={erster.get('rc')}\n{ausgabe}"):
        return

    werkzeug = next((art for art in ("openssl", "git") if art in arten), None)
    if werkzeug:
        befehle = {"openssl": ["dgst -sha256 ziel passwd-link fifo"],
                   "git": ["init", "add ziel passwd-link fifo"]}[werkzeug]
        zweiter = ws.auftrag("(1) Lab-Dateien gleichen Namens", kind=werkzeug, workspace=kennung["s"],
                             commands=befehle, files={name: "LAB-INHALT\n" for name in ("ziel", "passwd-link", "fifo")})
        pruefe(f"(1)+(4) {werkzeug}-Lauf B schreibt ziel/passwd-link/fifo und kommt zurueck (rc=0, kein Haenger)",
               zweiter.get("rc") == 0 and not zweiter.get("timed_out"),
               f"rc={zweiter.get('rc')}\n{zweiter.get('output')}")
    pruefe("(1) /queue/in/evil.json existiert nicht", not os.path.lexists(queue / "in" / "evil.json"))
    (queue / "in" / "evil.json").unlink(missing_ok=True)
    pruefe("(6) /queue/in und /queue/out sind weiter echte Verzeichnisse",
           all((queue / o).is_dir() and not (queue / o).is_symlink() for o in ("in", "out")))

    dritter = ws.auftrag("(3) Nachsehen", kind="ansible", workspace=kennung["s"],
                         playbook=playbook(skript_tasks(NACHHER, argument)))
    ausgabe = dritter.get("output", "")
    if not pruefe("(4) Lauf C nach FIFO/Socket im Arbeitsverzeichnis kommt zurueck (rc=0)",
                  dritter.get("rc") == 0 and "INFO uid=" in ausgabe, f"rc={dritter.get('rc')}\n{ausgabe}"):
        return
    if werkzeug:
        for name in ("ziel", "passwd-link", "fifo"):
            pruefe(f"(1) {name} ist jetzt eine regulaere Datei mit dem Lab-Inhalt",
                   info(ausgabe, f"{name}_art") == "regulaer" and info(ausgabe, f"{name}_inhalt") == "LAB-INHALT",
                   f"{info(ausgabe, f'{name}_art')} / {info(ausgabe, f'{name}_inhalt')}")
    pruefe("(1) /etc/passwd unveraendert", info(ausgabe, "passwd") == "unveraendert", ausgabe)
    for name, text in (("sonderbits", "(3) kein Eintrag mit setuid/setgid/sticky im Arbeitsverzeichnis"),
                       ("root_eintraege", "(3) nichts im Arbeitsverzeichnis gehoert root"),
                       ("fremde_eintraege", "(3) alles im Arbeitsverzeichnis gehoert der uid des laufenden Laufs"),
                       ("spezialdateien", "(4) keine FIFOs/Sockets mehr im Arbeitsverzeichnis"),
                       ("mehrfach_verlinkt", "(2) keine mehrfach verlinkte Datei mehr im Arbeitsverzeichnis"),
                       ("reste_gemeinsam", "(6) nichts von Lauf A in /tmp und /dev/shm, zweiter Lauf sieht nichts")):
        pruefe(text, info(ausgabe, name) == "0", re.findall(rf"INFO {name}=[^\"\n]*", ausgabe))
    pruefe("(3) Sticky-/setgid-Verzeichnis ist entschaerft (Modus 777)", info(ausgabe, "klebrig_modus") == "777",
           info(ausgabe, "klebrig_modus"))
    pruefe("(6) der nachsehende Lauf hatte eine andere uid als Lauf A",
           info(ausgabe, "uid") != info(erster.get("output", ""), "uid"),
           f"{info(erster.get('output', ''), 'uid')} / {info(ausgabe, 'uid')}")


def sauber_und_begrenzt(name: str, ergebnis: dict, rc: int) -> None:
    ausgabe = ergebnis.get("output", "")
    steuerzeichen = sorted({f"U+{ord(z):04X}" for z in ausgabe if (ord(z) < 32 and z not in "\n\t") or 127 <= ord(z) < 160})
    pruefe(f"(5) {name}: Ergebnis kommt (rc={rc}), ist gekuerzt und begrenzt",
           ergebnis.get("rc") == rc and ergebnis.get("truncated") is True
           and "[Ausgabe gekürzt]" in ausgabe and len(ausgabe.encode("utf-8")) < 70_000 and "ROT" in ausgabe,
           f"rc={ergebnis.get('rc')} truncated={ergebnis.get('truncated')} "
           f"bytes={len(ausgabe.encode('utf-8'))} ROT={'ROT' in ausgabe}\n{ausgabe[:400]!r}")
    pruefe(f"(5) {name}: Ausgabe ohne Steuerzeichen (kein ESC, NUL, BEL, CR, C1)", not steuerzeichen, steuerzeichen)


def flut_pruefen(ws: Warteschlange, kennung: dict, arten: set) -> None:
    """(5) Ausgabeflut. Ansible gibt Modul-Ausgaben JSON-kodiert weiter - rohe
    Steuerzeichen erreichen das Ergebnis nur ueber ein Werkzeug, das selbst
    nach stdout schreibt. Deshalb beide Wege."""
    if not arten & {"ansible", "openssl"}:
        return
    if "ansible" in arten:
        flut = ws.auftrag("(5) Playbook mit 1 MB Ausgabe", kind="ansible", workspace=kennung["s"],
                          playbook=playbook(skript_tasks(FLUT, {})))
        sauber_und_begrenzt("Playbook mit 1 MB Ausgabe", flut, 0)
    if "openssl" in arten:
        # 23 kB je Befehl, sechsmal: 138 kB rohe Bytes direkt nach stdout.
        b64 = base64.b64encode(FLUT_BYTES * (23_000 // len(FLUT_BYTES))).decode("ascii")
        datei = "\n".join(b64[i:i + 64] for i in range(0, len(b64), 64)) + "\n"
        flut = ws.auftrag("(5) openssl mit rohen Steuerzeichen", kind="openssl", workspace=kennung["s"],
                          files={"flut.b64": datei}, commands=["enc -d -base64 -in flut.b64"] * 6)
        sauber_und_begrenzt("openssl mit rohen Steuerzeichen", flut, 0)
    danach = ws.auftrag("(5) Lauf nach der Flut", kind="ansible" if "ansible" in arten else "openssl",
                        workspace=kennung["s"], playbook=playbook([{"debug": {"msg": "INFO danach=ok"}}]),
                        commands=["rand -hex 4"])
    pruefe("(5) Worker lebt und der Slot ist frei: der naechste Lauf im selben Arbeitsverzeichnis laeuft",
           danach.get("rc") == 0, f"rc={danach.get('rc')}\n{danach.get('output')}")


def ansible_pruefen(ws: Warteschlange, queue: Path, kennung: dict, zeitgrenze: float) -> None:
    # --- (a) normales Playbook, zweimal: Ergebnis, Job-uid, Idempotenz ---------
    tasks = [
        {"command": "id -u", "register": "wer", "changed_when": False},
        {"command": "openssl version", "register": "ssl", "changed_when": False},
        {"debug": {"msg": "INFO uid={{ wer.stdout }} benutzer={{ ansible_user_id }} "
                          "openssl={{ ssl.stdout.split()[1] }}"}},
        {"copy": {"content": "GEHEIM-A-RUHEND", "dest": "{{ lab_dir }}/geheim.txt"}},
    ]
    erster = ws.auftrag("(a) Playbook", kind="ansible", workspace=kennung["a"],
                        playbook=playbook(tasks, fakten=True))
    ausgabe = erster.get("output", "")
    if not pruefe("(a) normales Playbook laeuft (rc=0, changed=1)",
                  erster.get("rc") == 0 and "changed=1" in ausgabe, f"rc={erster.get('rc')}\n{ausgabe}"):
        if "deaktiviert" in ausgabe:
            print("        -> Der Runner hat die Trennung nicht einrichten koennen (fail-closed). "
                  "Ursache steht oben und im Runner-Log.", flush=True)
        return
    uid_a = int(info(ausgabe, "uid") or -1)
    pruefe("(a) Playbook laeuft unter einer Job-uid, nicht unter der des Workers",
           uid_a in JOB_UIDS, f"uid={uid_a}")
    pruefe("(a) Job-uid hat einen Benutzernamen (Ansible-Fakten)",
           info(ausgabe, "benutzer") == f"labjob{uid_a}", info(ausgabe, "benutzer"))
    version = info(ausgabe, "openssl") or "0.0"
    pruefe(f"(d) openssl version >= 3.5 (gefunden: {version})",
           tuple(int(t) for t in re.findall(r"\d+", version)[:2]) >= (3, 5))
    zweiter = ws.auftrag("(a) Playbook, 2. Lauf", kind="ansible", workspace=kennung["a"],
                         playbook=playbook(tasks, fakten=True))
    pruefe("(a) zweiter Lauf: Arbeitsverzeichnis erhalten und idempotent (changed=0)",
           zweiter.get("rc") == 0 and "changed=0" in zweiter.get("output", ""),
           f"rc={zweiter.get('rc')}\n{zweiter.get('output')}")

    # --- (b) + (e) boesartiges Playbook, waehrend ein fremder Lauf laeuft ------
    koeder_in, koeder_out = queue / "in" / f"koeder-{uuid.uuid4().hex}.txt", \
        queue / "out" / f"koeder-{uuid.uuid4().hex}.txt"
    for koeder in (koeder_in, koeder_out):
        koeder.write_text("GEHEIM-QUEUE", encoding="utf-8")
        os.chmod(koeder, 0o666)  # lesbar fuer alle: nur die Verzeichnisrechte duerfen schuetzen
    opfer: dict = {}
    opfer_tmp = f"/tmp/{kennung['b']}-opfer.txt"
    opfer_faden = threading.Thread(target=lambda: opfer.update(ws.auftrag(
        "(e) Opfer-Lauf", kind="ansible", workspace=kennung["b"], playbook=playbook([
            {"copy": {"content": "GEHEIM-B-AKTIV", "dest": "{{ lab_dir }}/geheim.txt", "mode": "0644"}},
            {"copy": {"content": "OPFER-TMP", "dest": opfer_tmp, "mode": "0666"}},
            {"command": "id -u", "register": "wer"},
            {"debug": {"msg": "INFO uid={{ wer.stdout }}"}},
            {"command": f"sleep {max(6, int(zeitgrenze * 0.4))}"},
            {"command": {"argv": ["python3", "-c", ("import os, sys; st = os.stat(sys.argv[1]); "
                                  "print('%d:%d:%s' % (st.st_uid, st.st_nlink, open(sys.argv[1]).read()))"),
                                  opfer_tmp]}, "register": "st"},
            {"debug": {"msg": "INFO opfer_tmp={{ st.stdout }}"}},
        ]))))
    opfer_faden.start()
    time.sleep(1)
    argument = {"queue": str(queue), "koeder_in": str(koeder_in), "koeder_out": str(koeder_out),
                "workspace_root": WORKSPACE_ROOT, "fremd_ruhend": f"{WORKSPACE_ROOT}/{kennung['a']}",
                "fremd_aktiv": f"{WORKSPACE_ROOT}/{kennung['b']}", "uid_von": JOB_UIDS[0],
                "uid_bis": JOB_UIDS[-1], "warten": max(5, int(zeitgrenze * 0.5)), "opfer_tmp": opfer_tmp}
    angriff = ws.auftrag("(b) Angriff", kind="ansible", workspace=kennung["c"],
                         playbook=playbook(skript_tasks(ANGRIFF, argument)))
    opfer_faden.join()
    for koeder in (koeder_in, koeder_out):
        pruefe(f"(b) Koeder {koeder.parent.name}/ ist unveraendert noch da",
               koeder.exists() and koeder.read_text(encoding="utf-8") == "GEHEIM-QUEUE")
        koeder.unlink(missing_ok=True)
    for ordner in ("in", "out"):
        pruefe(f"(b) keine untergeschobene Datei in /queue/{ordner}",
               not (queue / ordner / "gefaelscht.json").exists())
        (queue / ordner / "gefaelscht.json").unlink(missing_ok=True)

    ausgabe = angriff.get("output", "")
    if not pruefe("(b) Angriffs-Playbook ist bis zum Ende gelaufen",
                  angriff.get("rc") == 0 and "INFO angriff_fertig" in ausgabe,
                  f"rc={angriff.get('rc')}\n{ausgabe}"):
        return
    proben = dict(re.findall(r"PROBE (\S+) ((?:DICHT|LECK) [^\"\n]*)", ausgabe))
    pruefe("(b) Lauf ohne Gruppen, ohne Capabilities, mit no-new-privileges",
           info(ausgabe, "gruppen") == "[]" and info(ausgabe, "nnp") == "1"
           and set(info(ausgabe, "capeff") or "x") == {"0"} and set(info(ausgabe, "capprm") or "x") == {"0"},
           re.findall(r"INFO uid=[^\"\n]*", ausgabe))
    erwartet = [
        "queue_auflisten", "queue_auflisten/in", "queue_auflisten/out", "queue_in_schreiben",
        "queue_out_schreiben", "queue_in_lesen", "queue_out_lesen", "queue_out_loeschen",
        "arbeitsverzeichnisse_auflisten",
        "fremdes_verzeichnis_ruhend_auflisten", "fremdes_verzeichnis_ruhend_lesen",
        "fremdes_verzeichnis_ruhend_schreiben",
        "worker_pid1_environ", "worker_pid1_mem", "worker_pid1_cwd", "worker_pid1_fd",
        "worker_pid1_signal0", "worker_pid1_sigkill",
    ]
    gleichzeitig = int(info(ausgabe, "fremde_prozesse") or 0) >= 1
    pruefe("(e) Angriff und Opfer liefen wirklich gleichzeitig (fremder Job-Prozess gesehen)",
           gleichzeitig, "Zeitablauf passt nicht - Pruefung (e) ist so nicht aussagekraeftig.\n" + ausgabe)
    if gleichzeitig:
        erwartet += ["fremdes_verzeichnis_aktiv_auflisten", "fremdes_verzeichnis_aktiv_lesen",
                     "fremdes_verzeichnis_aktiv_schreiben", "fremder_lauf_environ", "fremder_lauf_mem",
                     "fremder_lauf_cwd", "fremder_lauf_signal0", "fremder_lauf_sigkill"]
    for name in erwartet:
        abschnitt = "(e)" if "aktiv" in name or "fremder_lauf" in name else "(b)"
        pruefe(f"{abschnitt} abgelehnt: {name}", proben.get(name, "").startswith("DICHT PermissionError"),
               proben.get(name, "Probe fehlt in der Ausgabe"))
    lecks = sorted(name for name, wert in proben.items() if wert.startswith("LECK"))
    pruefe("(b) keine einzige Probe ging durch", not lecks, lecks)
    pruefe("(b) kein Geheimnis in der Ausgabe des Angreifers",
           not re.search(r"GEHEIM-(QUEUE|A-RUHEND|B-AKTIV)", ausgabe), ausgabe)
    pruefe("(e) Opfer-Lauf blieb unbehelligt (rc=0)", opfer.get("rc") == 0,
           f"rc={opfer.get('rc')}\n{opfer.get('output')}")
    uid_opfer, uid_angriff = info(opfer.get("output", ""), "uid"), info(ausgabe, "uid")
    pruefe(f"(e) gleichzeitige Laeufe haben verschiedene uids ({uid_opfer} / {uid_angriff})",
           uid_opfer and uid_angriff and uid_opfer != uid_angriff)

    # --- (c) Endlosschleife: Zeitgrenze, danach keine Reste --------------------
    endlos = ws.auftrag("(c) Endlos-Lauf", kind="ansible", workspace=kennung["c"],
                        playbook=playbook(skript_tasks(ENDLOS, {})))
    pruefe("(c) Endlos-Playbook wird an der Zeitgrenze abgebrochen (rc=124, timed_out)",
           endlos.get("rc") == 124 and endlos.get("timed_out") is True
           and zeitgrenze * 1000 <= endlos.get("duration_ms", 0) <= (zeitgrenze + 15) * 1000,
           {k: v for k, v in endlos.items() if k != "token"})
    nachschau = ws.auftrag("(c) Nachschau", kind="ansible", workspace=kennung["c"],
                           playbook=playbook(skript_tasks(NACHSCHAU, {})))
    pruefe("(c) nach dem Abbruch laeuft kein Prozess des Endlos-Laufs mehr (auch kein setsid-Kind)",
           nachschau.get("rc") == 0 and info(nachschau.get("output", ""), "reste") == "0",
           f"rc={nachschau.get('rc')}\n{nachschau.get('output')}")

    # --- (2) Hardlink auf die fremde Datei des Opfers ---------------------------
    hardlink = info(ausgabe, "hardlink") or "Probe fehlt"
    opfer_stand = info(opfer.get("output", ""), "opfer_tmp")
    pruefe(f"(2) Hardlink auf fremde Datei: abgelehnt oder folgenlos (Versuch: {hardlink}, "
           f"Opfer-Datei danach uid:links:inhalt = {opfer_stand})",
           hardlink == "abgelehnt:PermissionError"
           or (hardlink == "angelegt" and opfer_stand == f"{uid_opfer}:1:OPFER-TMP"
               and info(nachschau.get("output", ""), "hart") == "fehlt"),
           f"{ausgabe}\n{opfer.get('output')}\n{nachschau.get('output')}")


if __name__ == "__main__":
    sys.exit(main())
