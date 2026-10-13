"""Tests fuer die Trennung der Laeufe per uid (worker._job und Umfeld).

Hier steht alles, was sich OHNE root pruefen laesst: Slot-Vergabe, Rechte- und
Pfadberechnung, Umgebung des Laufs, fail-closed-Startpruefung und die
Kill-Logik mit eingesetzten Systemaufrufen. Ob die Trennung im Container
wirklich haelt (setuid, Capabilities, /queue-Rechte, /proc), prueft
runner/tests/isolation_check.py im CI-Job "runner-isolation".
"""
from __future__ import annotations

import os
import signal
import sys
import threading
from pathlib import Path

import pytest

import worker

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="uid-Trennung gibt es nur unter POSIX")


def ino(pfad) -> int:
    return os.lstat(pfad).st_ino


@pytest.fixture
def aktiv(monkeypatch, tmp_path):
    """Trennung "aktiv" ohne root: chown wird aufgezeichnet statt ausgefuehrt,
    Prozesse einer Job-uid gibt es keine. Aufzeichnung: (Name, uid, gid) fuer
    chown ueber dir_fd, (inode, uid, gid) fuer fchown."""
    aufrufe: list[tuple] = []
    monkeypatch.setattr(worker, "_isolation_aktiv", True)
    monkeypatch.setattr(worker, "_freie_uids", [10002, 10003])
    monkeypatch.setattr(worker, "_belegte_arbeitsplaetze", set())
    monkeypatch.setattr(worker, "WORKSPACE_ROOT", tmp_path / "ws")
    monkeypatch.setattr(worker, "GEMEINSAME_SCHREIBORTE", ())
    monkeypatch.setattr(worker, "_prozesse_der_uid", lambda uid: [])
    monkeypatch.setattr(worker, "_job_prozesse_beenden", lambda uid, **kw: True)

    def chown(pfad, uid, gid, **kw):
        assert kw.get("follow_symlinks") is False, "chown darf keinem Symlink folgen"
        aufrufe.append((str(pfad), uid, gid))

    monkeypatch.setattr(worker.os, "chown", chown)
    monkeypatch.setattr(worker.os, "fchown",
                        lambda fd, uid, gid: aufrufe.append((os.fstat(fd).st_ino, uid, gid)))
    return aufrufe


# --- Slot-Vergabe ------------------------------------------------------------

def test_ohne_trennung_gibt_es_keine_uid(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "WORKSPACE_ROOT", tmp_path)
    with worker._job("anna") as (arbeitsplatz, laufverzeichnis, uid):
        assert uid is None and arbeitsplatz == tmp_path / "anna"
        assert laufverzeichnis.is_dir()
    assert not laufverzeichnis.exists()


def test_gleichzeitige_laeufe_bekommen_verschiedene_uids_und_geben_sie_zurueck(aktiv):
    with worker._job("anna") as (platz_a, lauf_a, uid_a), worker._job("bernd") as (platz_b, lauf_b, uid_b):
        assert uid_a != uid_b and {uid_a, uid_b} == {10002, 10003}
        assert platz_a != platz_b and lauf_a != lauf_b
        assert worker._freie_uids == []
        assert worker._belegte_arbeitsplaetze == {platz_a, platz_b}
    assert sorted(worker._freie_uids) == [10002, 10003]
    assert worker._belegte_arbeitsplaetze == set()
    assert not lauf_a.exists() and not lauf_b.exists()


def test_arbeitsverzeichnis_geht_an_die_uid_und_danach_zurueck_an_root(aktiv):
    with worker._job("anna") as (arbeitsplatz, laufverzeichnis, uid):
        (arbeitsplatz / "stand.txt").write_text("x")
        assert aktiv[:4] == [(ino(worker.WORKSPACE_ROOT), 0, 0), (ino(arbeitsplatz), 0, 0),
                             (ino(arbeitsplatz), uid, uid), (ino(laufverzeichnis), 0, 0)]
        aktiv.clear()
    # In Ruhe: Verzeichnis root, Inhalt weiter bei der Job-uid (nichts darin gehoert root).
    assert [a for a in aktiv if a[0] == ino(arbeitsplatz)][-1] == (ino(arbeitsplatz), 0, 0)
    assert ("stand.txt", uid, uid) in aktiv and ("stand.txt", 0, 0) not in aktiv
    assert arbeitsplatz.stat().st_mode & 0o777 == 0o700
    assert (worker.WORKSPACE_ROOT.stat().st_mode & 0o777) == 0o711  # nicht auflistbar
    assert not laufverzeichnis.exists()


def test_kein_freier_slot_ist_ein_fehler_und_kein_lauf_ohne_trennung(aktiv, monkeypatch):
    monkeypatch.setattr(worker, "_freie_uids", [])
    monkeypatch.setattr(worker, "TIMEOUT_SECONDS", -9.9)  # Wartezeit 0,1 s
    with pytest.raises(RuntimeError, match="Kein freier Job-Slot"), worker._job("anna"):
        pytest.fail("Lauf ohne uid gestartet")


def test_zweiter_lauf_im_selben_arbeitsverzeichnis_wartet(aktiv):
    reihenfolge: list[str] = []
    drin = threading.Event()

    def zweiter():
        drin.wait()
        with worker._job("anna"):
            reihenfolge.append("zweiter")

    faden = threading.Thread(target=zweiter)
    faden.start()
    with worker._job("anna"):
        drin.set()
        faden.join(timeout=0.3)
        assert faden.is_alive(), "zweiter Lauf lief trotz belegtem Arbeitsverzeichnis"
        reihenfolge.append("erster")
    faden.join(timeout=5)
    assert reihenfolge == ["erster", "zweiter"]


def test_slot_kommt_zurueck_wenn_schon_das_laufverzeichnis_scheitert(aktiv, monkeypatch):
    def voll(**kw):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(worker.tempfile, "mkdtemp", voll)
    with pytest.raises(OSError), worker._job("anna"):
        pytest.fail("Lauf ohne Laufverzeichnis gestartet")
    assert sorted(worker._freie_uids) == [10002, 10003] and worker._belegte_arbeitsplaetze == set()


def test_slot_bleibt_gesperrt_wenn_prozesse_ueberleben(aktiv, monkeypatch):
    monkeypatch.setattr(worker, "_job_prozesse_beenden", lambda uid, **kw: False)
    with worker._job("anna") as (arbeitsplatz, laufverzeichnis, uid):
        aktiv.clear()
    assert uid not in worker._freie_uids
    assert arbeitsplatz in worker._belegte_arbeitsplaetze
    assert aktiv == []  # kein chown mehr: das Verzeichnis bleibt, wie es ist
    assert laufverzeichnis.exists()  # nicht anfassen, solange Prozesse der uid leben
    laufverzeichnis.rmdir()


def test_aufraeumen_entfernt_nur_hinterlassenschaften_der_eigenen_uid(aktiv, monkeypatch, tmp_path):
    ort = tmp_path / "tmp"
    ort.mkdir()
    (ort / "rest.txt").write_text("x")
    (ort / "restordner").mkdir()
    (ort / "restordner" / "y").write_text("y")
    aussen = tmp_path / "queue"
    aussen.mkdir()
    (aussen / "auftrag.json").write_text("{}")
    (ort / "link").symlink_to(aussen)
    os.mkfifo(ort / "fifo")
    monkeypatch.setattr(worker, "GEMEINSAME_SCHREIBORTE", (ort, tmp_path / "gibt-es-nicht"))
    platz, lauf = tmp_path / "platz", tmp_path / "lauf"
    platz.mkdir()
    lauf.mkdir()

    assert worker._slot_aufraeumen(platz, lauf, os.getuid() + 1) is True
    assert len(list(ort.iterdir())) == 4  # fremde uid: nichts angefasst
    assert not lauf.exists()
    assert worker._slot_aufraeumen(platz, lauf, os.getuid()) is True
    assert list(ort.iterdir()) == []
    assert (aussen / "auftrag.json").read_text() == "{}"  # Symlink entfernt, Ziel unberuehrt


# --- Rechte und Pfade --------------------------------------------------------

def test_uebergeben_folgt_keinem_symlink(aktiv, tmp_path):
    fremd = tmp_path / "queue"
    fremd.mkdir()
    (fremd / "auftrag.json").write_text("{}")
    platz = tmp_path / "platz"
    (platz / "unter").mkdir(parents=True)
    (platz / "unter" / "datei").write_text("x")
    (platz / "falle").symlink_to(fremd)

    worker._uebergeben(platz, 10002)

    assert platz.stat().st_mode & 0o777 == 0o700
    # Oberstes Verzeichnis ueber den Deskriptor: erst root (nur der Eigentuemer
    # darf chmod), dann die uid.
    assert aktiv[:2] == [(ino(platz), 0, 0), (ino(platz), 10002, 10002)]
    assert sorted(aktiv[2:]) == sorted([("unter", 10002, 10002), ("falle", 10002, 10002),
                                        ("datei", 10002, 10002)])
    assert not any(eintrag[0] in ("auftrag.json", ino(fremd)) for eintrag in aktiv)


def test_uebergeben_auf_einen_symlink_fasst_das_ziel_nicht_an(aktiv, tmp_path):
    ziel = tmp_path / "queue"
    ziel.mkdir(mode=0o755)
    (tmp_path / "lauf").symlink_to(ziel)

    worker._uebergeben(tmp_path / "lauf", 0)

    assert aktiv == [(str(tmp_path / "lauf"), 0, 0)]  # nur der Link selbst (lchown)
    assert ziel.stat().st_mode & 0o777 == 0o755


def test_uebergeben_entschaerft_hinterlassenschaften(aktiv, tmp_path, capsys):
    fremd = tmp_path / "fremde-datei"
    fremd.write_text("gehoert jemand anderem")
    platz = tmp_path / "platz"
    platz.mkdir()
    os.link(fremd, platz / "hardlink")          # L4: chown gaebe die fremde Datei dem Lauf
    os.mkfifo(platz / "fifo")                   # wuerde ein open() anhalten
    (platz / "suid").write_text("#!/bin/sh\n")
    os.chmod(platz / "suid", 0o6755)
    (platz / "klebrig").mkdir()
    os.chmod(platz / "klebrig", 0o3777)
    (platz / "normal").write_text("bleibt")

    worker._uebergeben(platz, 10002, oben=0)

    assert sorted(p.name for p in platz.iterdir()) == ["klebrig", "normal", "suid"]
    assert fremd.read_text() == "gehoert jemand anderem" and ino(fremd) not in [a[0] for a in aktiv]
    assert "hardlink" not in [a[0] for a in aktiv]
    assert (platz / "suid").stat().st_mode & 0o7777 == 0o755
    assert (platz / "klebrig").stat().st_mode & 0o7777 == 0o777
    assert [a for a in aktiv if a[0] == ino(platz)][-1] == (ino(platz), 0, 0)  # Ruecknahme: oben root
    assert ("normal", 10002, 10002) in aktiv and ("suid", 10002, 10002) in aktiv
    assert "2 Einträge entfernt" in capsys.readouterr().err


def test_uebergeben_ohne_uid_tut_nichts(aktiv, tmp_path):
    worker._uebergeben(tmp_path, None)
    assert aktiv == []


def test_datei_schreiben_ueberschreibt_kein_symlink_ziel(aktiv, tmp_path):
    ziel_ausserhalb = tmp_path / "queue-in.json"
    ziel_ausserhalb.write_text("original")
    platz = tmp_path / "platz"
    platz.mkdir()
    (platz / "ca.cnf").symlink_to(ziel_ausserhalb)
    os.mkfifo(platz / "fifo")

    worker._datei_schreiben(platz / "ca.cnf", "vom Teilnehmer", 10002)
    worker._datei_schreiben(platz / "fifo", "haengt nicht", 10002)

    assert ziel_ausserhalb.read_text() == "original"
    assert not (platz / "ca.cnf").is_symlink()
    assert (platz / "ca.cnf").read_text() == "vom Teilnehmer"
    assert (platz / "fifo").read_text() == "haengt nicht"
    assert (ino(platz / "ca.cnf"), 10002, 10002) in aktiv


def test_warteschlange_ist_fuer_andere_geschlossen(aktiv, monkeypatch, tmp_path):
    queue = tmp_path / "queue"
    monkeypatch.setattr(worker, "QUEUE", queue)
    (queue / "in").mkdir(parents=True)
    os.chmod(queue / "in", 0o777)  # Volume einer aelteren Fassung

    assert worker._warteschlange_vorbereiten() is True

    assert queue.stat().st_mode & 0o777 == 0o750
    assert (queue / "in").stat().st_mode & 0o777 == 0o770
    assert (queue / "out").stat().st_mode & 0o777 == 0o770
    assert set(aktiv) == {(ino(queue), 0, worker.QUEUE_GID), (ino(queue / "in"), 0, worker.QUEUE_GID),
                          (ino(queue / "out"), 0, worker.QUEUE_GID)}


def test_warteschlange_folgt_keinem_symlink_aus_einem_bestands_volume(aktiv, monkeypatch, tmp_path, capsys):
    """M1: Ein frueherer Lauf hat in/ durch einen Symlink ersetzt. Das Ziel
    darf weder root:10001 bekommen noch 0770."""
    queue, ziel = tmp_path / "queue", tmp_path / "ziel"
    monkeypatch.setattr(worker, "QUEUE", queue)
    queue.mkdir()
    ziel.mkdir(mode=0o755)
    (queue / "in").symlink_to(ziel)
    (queue / "out").write_text("eine Datei statt eines Verzeichnisses")

    assert worker._warteschlange_vorbereiten() is True

    assert not (queue / "in").is_symlink() and (queue / "in").is_dir()
    assert (queue / "out").is_dir()
    assert ziel.stat().st_mode & 0o777 == 0o755
    assert ino(ziel) not in [a[0] for a in aktiv]
    assert "wird ersetzt" in capsys.readouterr().err


def test_verzeichnis_sichern_verweigert_symlinks(tmp_path):
    ziel = tmp_path / "ziel"
    ziel.mkdir(mode=0o755)
    (tmp_path / "link").symlink_to(ziel)
    with pytest.raises(OSError):
        worker._verzeichnis_sichern(tmp_path / "link", os.getuid(), os.getgid(), 0o700)
    assert ziel.stat().st_mode & 0o777 == 0o755


def test_warteschlange_bleibt_nicht_still_offen(aktiv, monkeypatch, tmp_path, capsys):
    def kein_chown(*a, **kw):
        raise PermissionError(1, "Operation not permitted")

    monkeypatch.setattr(worker, "QUEUE", tmp_path / "queue")
    monkeypatch.setattr(worker.os, "fchown", kein_chown)
    assert worker._warteschlange_vorbereiten() is False  # main() versucht es weiter, statt zu laufen
    assert "nicht für Läufe schließen" in capsys.readouterr().err


def test_ergebnis_ist_fuer_das_backend_lesbar(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "QUEUE", tmp_path)
    (tmp_path / "out").mkdir()
    fremd = tmp_path / "fremd.json"
    fremd.write_text("original")
    (tmp_path / "out" / "abc.json.tmp").symlink_to(fremd)  # hinterlegt von einem frueheren Lauf
    alte_umask = os.umask(0o077)
    try:
        worker._antwort_schreiben("abc", {"rc": 0})
    finally:
        os.umask(alte_umask)
    assert (tmp_path / "out" / "abc.json").stat().st_mode & 0o777 == 0o644
    assert fremd.read_text() == "original"


@pytest.mark.parametrize("anlegen", [
    lambda pfad, ziel: pfad.symlink_to(ziel),   # Symlink auf einen gueltigen Auftrag
    lambda pfad, ziel: os.mkfifo(pfad),         # read() auf ein FIFO haelt den Worker an
    lambda pfad, ziel: pfad.mkdir(),            # unlink() auf ein Verzeichnis wirft
], ids=["symlink", "fifo", "verzeichnis"])
def test_auftrag_lesen_nimmt_nur_regulaere_dateien(tmp_path, anlegen):
    ziel = tmp_path / "echt.json"
    ziel.write_text('{"kind": "ansible"}')
    pfad = tmp_path / "abc.claimed"
    anlegen(pfad, ziel)

    assert worker._auftrag_lesen(pfad) is None
    assert not os.path.lexists(pfad)
    assert ziel.read_text() == '{"kind": "ansible"}'


def test_auftrag_lesen_liest_regulaere_datei(tmp_path):
    pfad = tmp_path / "abc.claimed"
    pfad.write_text('{"kind": "git"}')
    assert worker._auftrag_lesen(pfad) == ("abc", {"kind": "git"})
    assert not pfad.exists()


# --- Ausgabe -----------------------------------------------------------------

@pytest.mark.parametrize("roh,sauber", [
    ("\x1b[31mROT\x1b[0m normal", "ROT normal"),                 # CSI-Farben
    ("\x1b]0;Fenstertitel\x07danach", "danach"),                 # OSC bis BEL
    ("\x1b]8;;http://x\x1b\\Link", "Link"),                      # OSC bis ST
    ("a\r\nb\rc", "a\nb\nc"),                                    # kein Ruecklauf, der Zeilen ueberschreibt
    ("NUL\x00 BEL\x07 BS\x08 DEL\x7f C1\x9b", "NUL� BEL� BS� DEL� C1�"),
    ("allein\x1b", "allein�"),
    ("Tab\tund\nZeile äöü €", "Tab\tund\nZeile äöü €"),
])
def test_ausgabe_ohne_steuerzeichen(roh, sauber):
    assert worker._bereinigen(roh) == sauber
    assert worker._clip(roh) == (sauber, False)


def test_ausgabeflut_bleibt_begrenzt_und_sauber(monkeypatch):
    monkeypatch.setattr(worker, "MAX_OUTPUT_BYTES", 1000)
    flut = (b"\x1b[31mROT\x1b[0m\x00\x07\xff\xfe\r\n" * 5000).decode("utf-8", "replace")
    text, gekappt = worker._clip(flut)
    assert gekappt and "ROT" in text and len(text.encode()) < 1100
    assert not worker._STEUERZEICHEN.search(text) and "\x1b" not in text


# --- Umgebung des Laufs ------------------------------------------------------

def _popen_kwargs(monkeypatch, tmp_path, uid):
    gesehen: dict = {}
    echtes_popen = worker.subprocess.Popen

    def popen(argv, **kw):
        gesehen.update(kw)
        for schluessel in ("user", "group", "extra_groups", "umask"):
            kw.pop(schluessel, None)  # ohne root nicht ausfuehrbar
        return echtes_popen(argv, **kw)

    monkeypatch.setattr(worker.subprocess, "Popen", popen)
    rc, _, _ = worker._mit_zeitgrenze_ausfuehren([sys.executable, "-c", "pass"], tmp_path, {}, 10, uid)
    assert rc == 0
    return gesehen


def test_lauf_startet_unter_der_job_uid_ohne_gruppen(monkeypatch, tmp_path):
    kw = _popen_kwargs(monkeypatch, tmp_path, 10004)
    assert (kw["user"], kw["group"], kw["extra_groups"], kw["umask"]) == (10004, 10004, [], 0o077)
    assert kw["start_new_session"] is True
    assert kw["stdin"] == worker.subprocess.DEVNULL  # L2: nicht fd 0 des Workers erben


def test_ohne_trennung_kein_uid_wechsel(monkeypatch, tmp_path):
    assert not {"user", "group", "extra_groups"} & _popen_kwargs(monkeypatch, tmp_path, None).keys()


def test_ansible_umgebung_liegt_im_laufverzeichnis_und_nie_in_der_queue(aktiv, monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "QUEUE", tmp_path / "queue")
    gesehen: dict = {}

    def ausfuehren(argv, cwd, env, zeitgrenze, uid=None):
        gesehen.update(argv=argv, cwd=cwd, env=env, uid=uid,
                       eigentuemer=[a for a in aktiv if a[0] == ino(cwd)],
                       dateien=[a for a in aktiv if a[0] in ("playbook.yml", "inventory.ini")])
        return 0, b"ok", False

    monkeypatch.setattr(worker, "_mit_zeitgrenze_ausfuehren", ausfuehren)
    ergebnis = worker._run_ansible({"playbook": "- hosts: all\n", "workspace": "anna"})

    assert ergebnis["rc"] == 0
    cwd, env, uid = gesehen["cwd"], gesehen["env"], gesehen["uid"]
    assert uid in (10002, 10003)
    assert gesehen["eigentuemer"][-1][1:] == (uid, uid)
    assert sorted(gesehen["dateien"])[-2:] == [("inventory.ini", uid, uid), ("playbook.yml", uid, uid)]
    for name in ("HOME", "TMPDIR", "ANSIBLE_LOCAL_TEMP", "ANSIBLE_REMOTE_TEMP"):
        assert Path(env[name]).is_relative_to(cwd), name
    assert not any(str(worker.QUEUE) in wert for wert in list(env.values()) + gesehen["argv"])
    assert not cwd.exists()  # Laufverzeichnis nach dem Lauf entfernt


def test_werkzeug_laeuft_ebenfalls_unter_der_job_uid(aktiv, monkeypatch):
    gesehen: list = []

    def ausfuehren(argv, cwd, env, zeitgrenze, uid=None):
        gesehen.append((uid, cwd, env, Path(env["TMPDIR"]).is_dir(), ino(cwd / "a.txt")))
        return 0, b"", False

    monkeypatch.setattr(worker, "RUNNER_KINDS", {"git"})
    monkeypatch.setattr(worker, "_mit_zeitgrenze_ausfuehren", ausfuehren)
    ergebnis = worker._ausfuehren({"kind": "git", "commands": ["status"], "files": {"a.txt": "x"},
                                   "workspace": "anna"})
    uid, cwd, env, tmp_war_da, datei = gesehen[0]
    assert ergebnis["rc"] == 0 and uid in (10002, 10003)
    assert (datei, uid, uid) in aktiv  # mitgeschickte Datei gehoert dem Lauf
    # L1: eigenes TMPDIR des Laufs - nicht das gemeinsame /tmp, nicht im
    # Arbeitsverzeichnis (git status), danach entfernt.
    tmpdir = Path(env["TMPDIR"])
    assert tmp_war_da and not tmpdir.exists()
    assert tmpdir.name.startswith("lauf-") and not tmpdir.is_relative_to(cwd)
    assert (ino(cwd), uid, uid) in aktiv and env["HOME"] == str(cwd)


# --- Startpruefung: fail-closed ---------------------------------------------

@pytest.fixture
def startzustand(monkeypatch):
    monkeypatch.setattr(worker, "_isolation_aktiv", False)
    monkeypatch.setattr(worker, "_isolation_fehler", "nicht gelaufen")
    monkeypatch.setattr(worker, "_freie_uids", [])
    monkeypatch.setattr(worker, "RUNNER_KINDS", {"ansible", "openssl"})
    monkeypatch.setattr(worker, "HANDLER", {"ansible": lambda a: {"rc": 0, "output": "lief"},
                                            "openssl": lambda a: {"rc": 0, "output": "lief"}})

    def stellen(schalter, uid, probe=None):
        monkeypatch.setattr(worker, "ISOLATION", schalter)
        monkeypatch.setattr(worker, "_eigene_uid", lambda: uid)
        monkeypatch.setattr(worker, "_isolation_probe", lambda job_uid: probe)
        worker._isolation_einrichten()

    return stellen


def test_root_mit_bestandener_probe_schaltet_die_trennung_ein(startzustand, monkeypatch, tmp_path, capsys):
    (tmp_path / "protected_hardlinks").write_text("0\n")
    (tmp_path / "protected_symlinks").write_text("1\n")
    monkeypatch.setattr(worker, "SYSCTL_FS", tmp_path)
    startzustand("uid", 0)
    log = capsys.readouterr().err
    assert "WARNUNG: fs.protected_hardlinks=0" in log and "protected_symlinks" not in log
    assert worker._isolation_aktiv is True
    assert worker._freie_uids == list(worker.JOB_UIDS) == list(range(10002, 10010))
    assert worker._ausfuehren({"kind": "ansible"})["output"] == "lief"


@pytest.mark.parametrize("schalter,uid,probe,teil", [
    ("uid", 10001, None, "uid 10001 statt 0"),                     # altes Compose, kein user 0:0
    ("uid", 0, "Prozess der Job-uid beenden (CAP_KILL) fehlgeschlagen", "CAP_KILL"),  # cap_add fehlt
    ("aus-unsicher", 0, None, "Playbooks liefen als root"),        # Schalter im Container
    ("irgendwas", 501, None, "uid 501 statt 0"),                   # Tippfehler ist nicht "aus"
])
def test_ohne_trennung_ist_ansible_gesperrt_und_openssl_laeuft_weiter(
        startzustand, capsys, schalter, uid, probe, teil):
    startzustand(schalter, uid, probe)

    assert worker._isolation_aktiv is False and worker._freie_uids == []
    ergebnis = worker._ausfuehren({"kind": "ansible", "playbook": "x"})
    assert ergebnis["rc"] == 2 and "deaktiviert" in ergebnis["output"] and teil in ergebnis["output"]
    assert worker._ausfuehren({"kind": "openssl"})["output"] == "lief"
    assert "ANSIBLE-LAB DEAKTIVIERT (fail-closed)" in capsys.readouterr().err


def test_unsicherer_schalter_gilt_nur_ohne_root_und_warnt(startzustand, capsys):
    startzustand("aus-unsicher", 501)
    assert worker._isolation_aktiv is False
    assert worker._ausfuehren({"kind": "ansible"})["output"] == "lief"
    assert "NICHT vom Worker getrennt" in capsys.readouterr().err


def test_ohne_startpruefung_ist_ansible_gesperrt(monkeypatch):
    monkeypatch.setattr(worker, "ISOLATION", "uid")
    monkeypatch.setattr(worker, "_isolation_aktiv", False)
    assert worker._ausfuehren({"kind": "ansible", "playbook": "x"})["rc"] == 2


def test_probe_meldet_den_schritt_der_scheitert(monkeypatch):
    def kein_chown(*a, **kw):
        raise PermissionError(1, "Operation not permitted")

    monkeypatch.setattr(worker.os, "chown", kein_chown)
    assert "CAP_CHOWN" in worker._isolation_probe(10002)


# --- Kill-Logik --------------------------------------------------------------

def test_beenden_haelt_erst_an_und_toetet_dann_bis_niemand_mehr_da_ist():
    funde = [[11, 12], [13], []]  # 13 ist waehrend der ersten Runde entstanden
    signale: list[tuple[int, int]] = []
    geerntet: list[int] = []

    def senden(pid, sig):
        signale.append((pid, sig))
        if pid == 12:
            raise ProcessLookupError  # schon weg: kein Fehler

    def ernten(pid, option):
        geerntet.append(pid)
        if pid == 11:
            raise ChildProcessError  # nicht unser Kind

    assert worker._job_prozesse_beenden(10002, finden=lambda uid: funde.pop(0), senden=senden,
                                        ernten=ernten, warten=lambda s: None) is True
    assert signale == [(11, signal.SIGSTOP), (12, signal.SIGSTOP), (11, signal.SIGKILL),
                       (12, signal.SIGKILL), (13, signal.SIGSTOP), (13, signal.SIGKILL)]
    assert geerntet == [11, 12, 13]


def test_beenden_gibt_auf_und_meldet_es(monkeypatch):
    monkeypatch.setattr(worker, "KILL_RUNDEN", 3)
    runden: list[int] = []
    assert worker._job_prozesse_beenden(10002, finden=lambda uid: [99],
                                        senden=lambda pid, sig: runden.append(sig),
                                        ernten=lambda pid, o: None, warten=lambda s: None) is False
    assert len(runden) == 6


@pytest.mark.parametrize("uids_jetzt,erwartet", [
    (["10002", "10002", "10002", "10002"], [(77, 9)]),  # gehoert noch dem Lauf
    (["0", "0", "0", "0"], []),                         # pid inzwischen neu vergeben (Worker!)
    ([], []),                                           # inzwischen beendet
])
def test_signal_geht_nur_an_einen_prozess_der_noch_der_uid_gehoert(monkeypatch, uids_jetzt, erwartet):
    """L3: pidfd oeffnen, DANN uid erneut lesen, dann ueber das pidfd senden."""
    ablauf: list = []
    monkeypatch.setattr(worker.os, "pidfd_open", lambda pid: ablauf.append(("auf", pid)) or 77,
                        raising=False)
    monkeypatch.setattr(worker.signal, "pidfd_send_signal",
                        lambda fd, sig: ablauf.append((fd, int(sig))), raising=False)
    monkeypatch.setattr(worker, "_uids_von", lambda pid: ablauf.append(("uid", pid)) or uids_jetzt)
    monkeypatch.setattr(worker.os, "close", lambda fd: ablauf.append(("zu", fd)))

    worker._signal_an_uid(4711, signal.SIGKILL, 10002)

    assert ablauf[:2] == [("auf", 4711), ("uid", 4711)] and ablauf[-1] == ("zu", 77)
    assert ablauf[2:-1] == erwartet


def test_signal_ohne_pidfd_faellt_auf_kill_zurueck(monkeypatch):
    gesendet: list = []
    monkeypatch.setattr(worker.os, "kill", lambda pid, sig: gesendet.append((pid, sig)))
    monkeypatch.delattr(worker.os, "pidfd_open", raising=False)  # kein Linux
    worker._signal_an_uid(4711, signal.SIGSTOP, 10002)

    def gesperrt(pid):
        raise PermissionError(1, "seccomp")

    monkeypatch.setattr(worker.os, "pidfd_open", gesperrt, raising=False)
    worker._signal_an_uid(4711, signal.SIGKILL, 10002)
    assert gesendet == [(4711, signal.SIGSTOP), (4711, signal.SIGKILL)]

    def weg(pid):
        raise ProcessLookupError(3, "No such process")

    monkeypatch.setattr(worker.os, "pidfd_open", weg, raising=False)
    with pytest.raises(ProcessLookupError):  # _job_prozesse_beenden faengt das ab
        worker._signal_an_uid(4711, signal.SIGKILL, 10002)
    assert len(gesendet) == 2


def test_beenden_ohne_uid_fasst_keinen_prozess_an():
    def nie(*a):
        raise AssertionError("ohne Trennung darf nichts gesucht oder beendet werden")

    assert worker._job_prozesse_beenden(None, finden=nie, senden=nie) is True


@pytest.mark.skipif(not Path("/proc/self/status").exists(), reason="braucht Linux-/proc")
def test_prozesse_der_uid_findet_den_eigenen_prozess():
    assert os.getpid() in worker._prozesse_der_uid(os.getuid())
    assert worker._prozesse_der_uid(2 ** 31 - 7) == []
