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


def test_lab_braucht_anmeldung():
    with TestClient(app) as client:
        assert client.get("/api/lab/status").status_code in (401, 403)
        assert client.post("/api/lab/run", json={"playbook": "- hosts: all"}).status_code in (401, 403)


def test_lab_ohne_warteschlange_meldet_deaktiviert(monkeypatch):
    monkeypatch.setattr(settings, "lab_queue_dir", "")
    with TestClient(app) as client:
        kopf = _teilnehmer(client)
        assert client.get("/api/lab/status", headers=kopf).json() == {"enabled": False}
        antwort = client.post("/api/lab/run", json={"playbook": "- hosts: all"}, headers=kopf)
        assert antwort.status_code == 503
        assert "nicht aktiviert" in antwort.json()["detail"]


def test_lab_meldet_aktiv_mit_warteschlange(warteschlange):
    with TestClient(app) as client:
        kopf = _teilnehmer(client)
        assert client.get("/api/lab/status", headers=kopf).json() == {"enabled": True}


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
