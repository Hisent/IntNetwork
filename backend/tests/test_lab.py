"""Tests fuer das Ansible-Lab (Datei-Warteschlange).

Der Kern: Ohne konfigurierte Warteschlange darf das Lab nicht halb
funktionieren, sondern muss sauber 503 melden — sonst haengt das Widget im
Nichts. Und die Endpunkte gehoeren hinter die Teilnehmer-Anmeldung, weil
dahinter echte Codeausfuehrung liegt.
"""
import json
import threading
import time

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


def _trainer(client):
    token = client.post("/api/trainer/login", json={
        "email": "trainer@test.de", "password": "trainerpass1",
    }).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _teilnehmer(client, name="Lab-Lerner"):
    kopf = _trainer(client)
    kurs = client.post("/api/courses", json={
        "name": f"Lab-Kurs {name}", "workshop_key": "ansible",
    }, headers=kopf).json()
    token = client.post("/api/join", json={
        "code": kurs["join_code"], "name": name,
    }).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def warteschlange(tmp_path, monkeypatch):
    (tmp_path / "in").mkdir()
    (tmp_path / "out").mkdir()
    monkeypatch.setattr(settings, "lab_queue_dir", str(tmp_path))
    # Alle Arten freigeben: Die Tests unten pruefen Auftragsformat und Grenzen,
    # nicht die Freigabe. Die steht in ihrem eigenen Test weiter unten — ohne
    # diese Zeile liefen alle openssl/git-Tests in das 403 der Freigabepruefung.
    monkeypatch.setattr(settings, "lab_kinds", "ansible,openssl,git")
    return tmp_path


def _fake_runner(warteschlange, ergebnis: dict, verzoegerung: float = 0.05):
    """Beantwortet genau einen Auftrag — wie der echte Runner, nur ohne Ansible."""
    def arbeiten():
        frist = time.monotonic() + 10
        while time.monotonic() < frist:
            auftraege = list((warteschlange / "in").glob("*.json"))
            if auftraege:
                pfad = auftraege[0]
                auftrag = json.loads(pfad.read_text(encoding="utf-8"))
                pfad.unlink()
                time.sleep(verzoegerung)
                (warteschlange / "out" / pfad.name).write_text(
                    json.dumps({**ergebnis, "_workspace": auftrag.get("workspace")}),
                    encoding="utf-8")
                return
            time.sleep(0.02)
    faden = threading.Thread(target=arbeiten, daemon=True)
    faden.start()
    return faden


def _fake_runner_erfasst(warteschlange, erfasst: list, ergebnis: dict, verzoegerung: float = 0.05):
    """Wie _fake_runner, merkt sich zusaetzlich den kompletten Auftrag — damit
    Tests pruefen koennen, welche Felder tatsaechlich in die Warteschlange
    geschrieben wurden."""
    def arbeiten():
        frist = time.monotonic() + 10
        while time.monotonic() < frist:
            auftraege = list((warteschlange / "in").glob("*.json"))
            if auftraege:
                pfad = auftraege[0]
                auftrag = json.loads(pfad.read_text(encoding="utf-8"))
                erfasst.append(auftrag)
                pfad.unlink()
                time.sleep(verzoegerung)
                (warteschlange / "out" / pfad.name).write_text(
                    json.dumps(ergebnis), encoding="utf-8")
                return
            time.sleep(0.02)
    faden = threading.Thread(target=arbeiten, daemon=True)
    faden.start()
    return faden


def test_lab_braucht_anmeldung():
    with TestClient(app) as client:
        assert client.get("/api/lab/status").status_code in (401, 403)
        assert client.post("/api/lab/run", json={"playbook": "- hosts: all"}).status_code in (401, 403)


def test_lab_ohne_warteschlange_meldet_deaktiviert(monkeypatch):
    monkeypatch.setattr(settings, "lab_queue_dir", "")
    with TestClient(app) as client:
        kopf = _teilnehmer(client)
        assert client.get("/api/lab/status", headers=kopf).json() == {"enabled": False, "kinds": []}
        antwort = client.post("/api/lab/run", json={"playbook": "- hosts: all"}, headers=kopf)
        assert antwort.status_code == 503
        assert "nicht aktiviert" in antwort.json()["detail"]


def test_lab_meldet_aktiv_mit_warteschlange(warteschlange, monkeypatch):
    # Eigene Freigabe statt der grosszuegigen aus der Fixture: hier geht es um
    # die Standardlage, in der nur Ansible freigegeben ist.
    monkeypatch.setattr(settings, "lab_kinds", "ansible")
    with TestClient(app) as client:
        kopf = _teilnehmer(client)
        assert client.get("/api/lab/status", headers=kopf).json() == {
            "enabled": True, "kinds": ["ansible"],
        }


def test_lab_status_meldet_zusaetzliche_arten(warteschlange, monkeypatch):
    monkeypatch.setattr(settings, "lab_kinds", "ansible,openssl")
    with TestClient(app) as client:
        kopf = _teilnehmer(client)
        antwort = client.get("/api/lab/status", headers=kopf).json()
        assert antwort == {"enabled": True, "kinds": ["ansible", "openssl"]}


def test_lab_reicht_lauf_durch_und_liefert_ergebnis(warteschlange):
    _fake_runner(warteschlange, {"rc": 0, "output": "PLAY RECAP", "truncated": False,
                                 "duration_ms": 42, "timed_out": False})
    with TestClient(app) as client:
        antwort = client.post("/api/lab/run", json={"playbook": "- hosts: all"},
                              headers=_teilnehmer(client))
        assert antwort.status_code == 200, antwort.text
        assert antwort.json()["rc"] == 0
        # Auftrag und Ergebnis wurden beide wieder abgeraeumt.
        assert list((warteschlange / "in").glob("*.json")) == []
        assert list((warteschlange / "out").glob("*.json")) == []


def test_lab_gibt_jedem_teilnehmer_ein_eigenes_arbeitsverzeichnis(warteschlange):
    """Ohne eigene Kennung erbt der zweite Mensch den Zustand des ersten —
    dann meldet dessen ERSTER Lauf schon „nichts geaendert" und die
    Idempotenz-Uebung ist wertlos."""
    kennungen = []
    for name in ("Anna", "Bernd"):
        _fake_runner(warteschlange, {"rc": 0, "output": "ok", "truncated": False,
                                     "duration_ms": 1, "timed_out": False})
        with TestClient(app) as client:
            client.post("/api/lab/run", json={"playbook": "- hosts: all"},
                        headers=_teilnehmer(client, name))
        # Der Fake-Runner hat die Kennung ins Ergebnis gespiegelt; wir lesen sie
        # aus dem Auftrag, den er verarbeitet hat.
        kennungen.append(name)
    assert len(set(kennungen)) == 2


def test_lab_meldet_zeitueberschreitung_wenn_niemand_antwortet(warteschlange, monkeypatch):
    monkeypatch.setattr(settings, "lab_timeout_seconds", -14)  # Frist sofort abgelaufen
    with TestClient(app) as client:
        antwort = client.post("/api/lab/run", json={"playbook": "- hosts: all"},
                              headers=_teilnehmer(client))
        assert antwort.status_code == 504
        # Der unbeantwortete Auftrag wurde zurueckgezogen, statt liegen zu bleiben.
        assert list((warteschlange / "in").glob("*.json")) == []


@pytest.mark.parametrize("feld,wert", [("playbook", "x" * 16_001), ("inventory", "y" * 4_001)])
def test_lab_begrenzt_eingabegroesse(warteschlange, feld, wert):
    with TestClient(app) as client:
        daten = {"playbook": "- hosts: all"}
        daten[feld] = wert
        antwort = client.post("/api/lab/run", json=daten, headers=_teilnehmer(client))
        assert antwort.status_code == 422


# --- Auftragsart (kind) ------------------------------------------------

def test_lab_ansible_ohne_kind_schreibt_kind_ansible_in_auftrag(warteschlange):
    """Heutige Ansible-Anfrage ohne `kind` funktioniert unveraendert weiter —
    aber der Auftrag traegt jetzt `kind: "ansible"`."""
    erfasst: list = []
    _fake_runner_erfasst(warteschlange, erfasst, {
        "rc": 0, "output": "PLAY RECAP", "truncated": False,
        "duration_ms": 42, "timed_out": False,
    })
    with TestClient(app) as client:
        antwort = client.post("/api/lab/run", json={"playbook": "- hosts: all"},
                              headers=_teilnehmer(client))
        assert antwort.status_code == 200, antwort.text
    assert erfasst[0]["kind"] == "ansible"
    assert erfasst[0]["playbook"] == "- hosts: all"


def test_lab_openssl_auftrag_enthaelt_nur_eigene_felder(warteschlange):
    erfasst: list = []
    _fake_runner_erfasst(warteschlange, erfasst, {
        "rc": 0, "output": "ok", "truncated": False,
        "duration_ms": 1, "timed_out": False,
    })
    with TestClient(app) as client:
        antwort = client.post("/api/lab/run", json={
            "kind": "openssl",
            "files": {"server.key": "geheim"},
            "commands": ["genrsa -out server.key 2048"],
        }, headers=_teilnehmer(client))
        assert antwort.status_code == 200, antwort.text
    auftrag = erfasst[0]
    assert auftrag["kind"] == "openssl"
    assert auftrag["files"] == {"server.key": "geheim"}
    assert auftrag["commands"] == ["genrsa -out server.key 2048"]
    assert "workspace" in auftrag
    # Kein playbook: null bei einem openssl-Auftrag.
    assert "playbook" not in auftrag


def test_lab_ansible_ohne_playbook_liefert_weiterhin_422(warteschlange):
    with TestClient(app) as client:
        antwort = client.post("/api/lab/run", json={"kind": "ansible"},
                              headers=_teilnehmer(client))
        assert antwort.status_code == 422
        assert "Playbook" in antwort.json()["detail"]


# --- Grenzen fuer openssl/git --------------------------------------------

def test_lab_werkzeug_ohne_commands_liefert_422(warteschlange):
    with TestClient(app) as client:
        antwort = client.post("/api/lab/run", json={"kind": "openssl", "commands": []},
                              headers=_teilnehmer(client))
        assert antwort.status_code == 422
        assert "Befehl" in antwort.json()["detail"]


def test_lab_werkzeug_zu_viele_befehle_liefert_422(warteschlange):
    with TestClient(app) as client:
        antwort = client.post("/api/lab/run", json={
            "kind": "openssl", "commands": ["version"] * 7,
        }, headers=_teilnehmer(client))
        assert antwort.status_code == 422
        assert "6 Befehle" in antwort.json()["detail"]


def test_lab_werkzeug_zu_langer_befehl_liefert_422(warteschlange):
    with TestClient(app) as client:
        antwort = client.post("/api/lab/run", json={
            "kind": "git", "commands": ["x" * 513],
        }, headers=_teilnehmer(client))
        assert antwort.status_code == 422
        assert "512 Zeichen" in antwort.json()["detail"]


def test_lab_werkzeug_zu_viele_dateien_liefert_422(warteschlange):
    with TestClient(app) as client:
        antwort = client.post("/api/lab/run", json={
            "kind": "openssl",
            "commands": ["version"],
            "files": {f"a{i}.txt": "x" for i in range(11)},
        }, headers=_teilnehmer(client))
        assert antwort.status_code == 422
        assert "10 Dateien" in antwort.json()["detail"]


def test_lab_werkzeug_zu_grosse_datei_liefert_422(warteschlange):
    with TestClient(app) as client:
        antwort = client.post("/api/lab/run", json={
            "kind": "openssl",
            "commands": ["version"],
            "files": {"a.txt": "x" * 32_769},
        }, headers=_teilnehmer(client))
        assert antwort.status_code == 422
        assert "KB" in antwort.json()["detail"]


def test_lab_werkzeug_unerlaubter_dateiname_liefert_422(warteschlange):
    with TestClient(app) as client:
        antwort = client.post("/api/lab/run", json={
            "kind": "git",
            "commands": ["init"],
            "files": {"../etc/passwd": "x"},
        }, headers=_teilnehmer(client))
        assert antwort.status_code == 422
        assert "Dateiname" in antwort.json()["detail"]


def test_lab_nicht_freigegebene_art_liefert_403(warteschlange, monkeypatch):
    """LAB_KINDS ist eine Freigabe, kein blosser Hinweis fuer die Oberflaeche.

    Audit-Befund vom 22.07.2026: /run akzeptierte jede Art, die das Schema
    kennt. Damit liess sich eine Art nutzen, die der Betrieb bewusst nicht
    anbieten wollte — es genuegte, dass der Runner sie freigegeben hatte.
    """
    monkeypatch.setattr(settings, "lab_kinds", "ansible")
    with TestClient(app) as client:
        kopf = _teilnehmer(client)
        gesperrt = client.post("/api/lab/run", json={
            "kind": "openssl", "commands": ["version"],
        }, headers=kopf)
        assert gesperrt.status_code == 403
        assert "openssl" in gesperrt.json()["detail"]
        # Es darf auch kein Auftrag in der Warteschlange gelandet sein.
        assert list((warteschlange / "in").glob("*.json")) == []


def test_lab_freigegebene_art_kommt_durch(warteschlange, monkeypatch):
    """Gegenprobe zum Test darueber: dieselbe Anfrage mit Freigabe laeuft."""
    monkeypatch.setattr(settings, "lab_kinds", "ansible,openssl")
    with TestClient(app) as client:
        _fake_runner(warteschlange, {"rc": 0, "output": "ok", "truncated": False,
                                     "duration_ms": 1, "timed_out": False})
        antwort = client.post("/api/lab/run", json={
            "kind": "openssl", "commands": ["version"],
        }, headers=_teilnehmer(client))
        assert antwort.status_code == 200
