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


@pytest.fixture
def aktiv(monkeypatch, tmp_path):
    """Trennung "aktiv" ohne root: chown wird aufgezeichnet statt ausgefuehrt,
    Prozesse einer Job-uid gibt es keine."""
    aufrufe: list[tuple] = []
    monkeypatch.setattr(worker, "_isolation_aktiv", True)
    monkeypatch.setattr(worker, "_freie_uids", [10002, 10003])
    monkeypatch.setattr(worker, "_belegte_arbeitsplaetze", set())
    monkeypatch.setattr(worker, "WORKSPACE_ROOT", tmp_path / "ws")
    monkeypatch.setattr(worker, "GEMEINSAME_SCHREIBORTE", ())
    monkeypatch.setattr(worker, "_prozesse_der_uid", lambda uid: [])
    monkeypatch.setattr(worker, "_job_prozesse_beenden", lambda uid, **kw: True)
    monkeypatch.setattr(worker.os, "chown",
                        lambda pfad, uid, gid, **kw: aufrufe.append((str(pfad), uid, gid, kw)))
    monkeypatch.setattr(worker.os, "fchown", lambda fd, uid, gid: aufrufe.append(("fd", uid, gid, {})))
    return aufrufe


# --- Slot-Vergabe ------------------------------------------------------------

def test_ohne_trennung_gibt_es_keine_uid(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "WORKSPACE_ROOT", tmp_path)
    with worker._job("anna") as (arbeitsplatz, uid):
        assert uid is None and arbeitsplatz == tmp_path / "anna"


def test_gleichzeitige_laeufe_bekommen_verschiedene_uids_und_geben_sie_zurueck(aktiv):
    with worker._job("anna") as (platz_a, uid_a), worker._job("bernd") as (platz_b, uid_b):
        assert uid_a != uid_b and {uid_a, uid_b} == {10002, 10003}
        assert platz_a != platz_b
        assert worker._freie_uids == []
        assert worker._belegte_arbeitsplaetze == {platz_a, platz_b}
    assert sorted(worker._freie_uids) == [10002, 10003]
    assert worker._belegte_arbeitsplaetze == set()


def test_arbeitsverzeichnis_geht_an_die_uid_und_danach_zurueck_an_root(aktiv):
    with worker._job("anna") as (arbeitsplatz, uid):
        assert (str(arbeitsplatz), uid, uid, {"follow_symlinks": False}) in aktiv
        aktiv.clear()
    assert aktiv == [(str(arbeitsplatz), 0, 0, {"follow_symlinks": False})]
    assert arbeitsplatz.stat().st_mode & 0o777 == 0o700
    assert (worker.WORKSPACE_ROOT.stat().st_mode & 0o777) == 0o711  # nicht auflistbar


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


def test_slot_bleibt_gesperrt_wenn_prozesse_ueberleben(aktiv, monkeypatch):
    monkeypatch.setattr(worker, "_job_prozesse_beenden", lambda uid, **kw: False)
    with worker._job("anna") as (arbeitsplatz, uid):
        aktiv.clear()
    assert uid not in worker._freie_uids
    assert arbeitsplatz in worker._belegte_arbeitsplaetze
    assert aktiv == []  # kein chown mehr: das Verzeichnis bleibt, wie es ist


def test_aufraeumen_entfernt_nur_hinterlassenschaften_der_eigenen_uid(aktiv, monkeypatch, tmp_path):
    ort = tmp_path / "tmp"
    ort.mkdir()
    (ort / "rest.txt").write_text("x")
    (ort / "restordner").mkdir()
    (ort / "restordner" / "y").write_text("y")
    monkeypatch.setattr(worker, "GEMEINSAME_SCHREIBORTE", (ort, tmp_path / "gibt-es-nicht"))
    platz = tmp_path / "platz"
    platz.mkdir()

    assert worker._slot_aufraeumen(platz, os.getuid() + 1) is True
    assert sorted(p.name for p in ort.iterdir()) == ["rest.txt", "restordner"]  # fremde uid
    assert worker._slot_aufraeumen(platz, os.getuid()) is True
    assert list(ort.iterdir()) == []


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
    # Erst an root (nur der Eigentuemer darf chmod), dann an die uid.
    assert [(pfad, uid) for pfad, uid, *_ in aktiv[:2]] == [(str(platz), 0), (str(platz), 10002)]
    namen = [pfad for pfad, *_ in aktiv[1:]]
    assert sorted(namen) == sorted([str(platz), "unter", "falle", "datei"])
    assert "auftrag.json" not in namen  # nicht in den Symlink hineingelaufen
    assert all(kw["follow_symlinks"] is False for *_, kw in aktiv)
    assert all("dir_fd" in kw for pfad, *_, kw in aktiv if pfad != str(platz))


def test_uebergeben_ohne_uid_tut_nichts(aktiv, tmp_path):
    worker._uebergeben(tmp_path, None)
    assert aktiv == []


def test_datei_schreiben_ueberschreibt_kein_symlink_ziel(aktiv, tmp_path):
    ziel_ausserhalb = tmp_path / "queue-in.json"
    ziel_ausserhalb.write_text("original")
    platz = tmp_path / "platz"
    platz.mkdir()
    (platz / "ca.cnf").symlink_to(ziel_ausserhalb)

    worker._datei_schreiben(platz / "ca.cnf", "vom Teilnehmer", 10002)

    assert ziel_ausserhalb.read_text() == "original"
    assert not (platz / "ca.cnf").is_symlink()
    assert (platz / "ca.cnf").read_text() == "vom Teilnehmer"
    assert ("fd", 10002, 10002, {}) in aktiv


def test_warteschlange_ist_fuer_andere_geschlossen(aktiv, monkeypatch, tmp_path):
    queue = tmp_path / "queue"
    monkeypatch.setattr(worker, "QUEUE", queue)
    (queue / "in").mkdir(parents=True)
    os.chmod(queue / "in", 0o777)  # Volume einer aelteren Fassung

    assert worker._warteschlange_vorbereiten() is True

    assert queue.stat().st_mode & 0o777 == 0o750
    assert (queue / "in").stat().st_mode & 0o777 == 0o770
    assert (queue / "out").stat().st_mode & 0o777 == 0o770
    assert {(pfad, uid, gid) for pfad, uid, gid, _ in aktiv} == {
        (str(queue), 0, worker.QUEUE_GID), (str(queue / "in"), 0, worker.QUEUE_GID),
        (str(queue / "out"), 0, worker.QUEUE_GID)}


def test_warteschlange_bleibt_nicht_still_offen(aktiv, monkeypatch, tmp_path, capsys):
    def kein_chown(*a, **kw):
        raise PermissionError(1, "Operation not permitted")

    monkeypatch.setattr(worker, "QUEUE", tmp_path / "queue")
    monkeypatch.setattr(worker.os, "chown", kein_chown)
    assert worker._warteschlange_vorbereiten() is False  # main() versucht es weiter, statt zu laufen
    assert "nicht für Läufe schließen" in capsys.readouterr().err


def test_ergebnis_ist_fuer_das_backend_lesbar(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "QUEUE", tmp_path)
    (tmp_path / "out").mkdir()
    alte_umask = os.umask(0o077)
    try:
        worker._antwort_schreiben("abc", {"rc": 0})
    finally:
        os.umask(alte_umask)
    assert (tmp_path / "out" / "abc.json").stat().st_mode & 0o777 == 0o644


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


def test_ohne_trennung_kein_uid_wechsel(monkeypatch, tmp_path):
    assert not {"user", "group", "extra_groups"} & _popen_kwargs(monkeypatch, tmp_path, None).keys()


def test_ansible_umgebung_liegt_im_laufverzeichnis_und_nie_in_der_queue(aktiv, monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "QUEUE", tmp_path / "queue")
    gesehen: dict = {}

    def ausfuehren(argv, cwd, env, zeitgrenze, uid=None):
        gesehen.update(argv=argv, cwd=cwd, env=env, uid=uid,
                       eigentuemer=[a for a in aktiv if a[0] == str(cwd)])
        return 0, b"ok", False

    monkeypatch.setattr(worker, "_mit_zeitgrenze_ausfuehren", ausfuehren)
    ergebnis = worker._run_ansible({"playbook": "- hosts: all\n", "workspace": "anna"})

    assert ergebnis["rc"] == 0
    cwd, env, uid = gesehen["cwd"], gesehen["env"], gesehen["uid"]
    assert uid in (10002, 10003)
    assert gesehen["eigentuemer"][-1] == (str(cwd), uid, uid, {"follow_symlinks": False})
    for name in ("HOME", "TMPDIR", "ANSIBLE_LOCAL_TEMP", "ANSIBLE_REMOTE_TEMP"):
        assert Path(env[name]).is_relative_to(cwd), name
    assert not any(str(worker.QUEUE) in wert for wert in list(env.values()) + gesehen["argv"])
    assert not cwd.exists()  # Laufverzeichnis nach dem Lauf entfernt


def test_werkzeug_laeuft_ebenfalls_unter_der_job_uid(aktiv, monkeypatch):
    uids: list = []
    monkeypatch.setattr(worker, "RUNNER_KINDS", {"git"})
    monkeypatch.setattr(worker, "_mit_zeitgrenze_ausfuehren",
                        lambda argv, cwd, env, zeitgrenze, uid=None: (uids.append(uid), (0, b"", False))[1])
    ergebnis = worker._ausfuehren({"kind": "git", "commands": ["status"], "files": {"a.txt": "x"},
                                   "workspace": "anna"})
    assert ergebnis["rc"] == 0 and uids[0] in (10002, 10003)
    assert ("fd", uids[0], uids[0], {}) in aktiv  # mitgeschickte Datei gehoert dem Lauf


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


def test_root_mit_bestandener_probe_schaltet_die_trennung_ein(startzustand):
    startzustand("uid", 0)
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


def test_beenden_ohne_uid_fasst_keinen_prozess_an():
    def nie(*a):
        raise AssertionError("ohne Trennung darf nichts gesucht oder beendet werden")

    assert worker._job_prozesse_beenden(None, finden=nie, senden=nie) is True


@pytest.mark.skipif(not Path("/proc/self/status").exists(), reason="braucht Linux-/proc")
def test_prozesse_der_uid_findet_den_eigenen_prozess():
    assert os.getpid() in worker._prozesse_der_uid(os.getuid())
    assert worker._prozesse_der_uid(2 ** 31 - 7) == []
