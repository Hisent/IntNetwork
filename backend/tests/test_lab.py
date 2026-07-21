"""Tests fuer das Ansible-Lab.

Der Kern: Ohne konfigurierten Runner darf das Lab nicht halb funktionieren,
sondern muss sauber 503 melden — sonst haengt das Widget im Nichts. Und die
Endpunkte gehoeren hinter die Teilnehmer-Anmeldung, weil dahinter echte
Codeausfuehrung liegt.
"""
import httpx
import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


def _trainer(client):
    token = client.post("/api/trainer/login", json={
        "email": "trainer@test.de", "password": "trainerpass1",
    }).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _teilnehmer(client):
    kopf = _trainer(client)
    kurs = client.post("/api/courses", json={
        "name": "Lab-Kurs", "workshop_key": "ansible",
    }, headers=kopf).json()
    token = client.post("/api/join", json={
        "code": kurs["join_code"], "name": "Lab-Lerner",
    }).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_lab_braucht_anmeldung():
    with TestClient(app) as client:
        assert client.get("/api/lab/status").status_code in (401, 403)
        assert client.post("/api/lab/run", json={"playbook": "- hosts: all"}).status_code in (401, 403)


def test_lab_ohne_runner_meldet_deaktiviert():
    with TestClient(app) as client:
        kopf = _teilnehmer(client)
        status = client.get("/api/lab/status", headers=kopf)
        assert status.status_code == 200
        assert status.json() == {"enabled": False}

        lauf = client.post("/api/lab/run", json={"playbook": "- hosts: all"}, headers=kopf)
        assert lauf.status_code == 503
        assert "nicht aktiviert" in lauf.json()["detail"]


def test_lab_reicht_lauf_an_runner_weiter(monkeypatch):
    """Mit konfiguriertem Runner wird weitergereicht — inklusive Token-Kopf."""
    gesehen = {}

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def post(self, url, json, headers):
            gesehen["url"] = url
            gesehen["playbook"] = json["playbook"]
            gesehen["token"] = headers["X-Runner-Token"]
            return httpx.Response(200, json={
                "rc": 0, "output": "PLAY RECAP", "truncated": False,
                "duration_ms": 42, "timed_out": False,
            })

    monkeypatch.setattr(settings, "lab_runner_url", "http://runner:8080")
    monkeypatch.setattr(settings, "lab_runner_token", "geheim")
    monkeypatch.setattr(httpx, "AsyncClient", FakeClient)

    with TestClient(app) as client:
        kopf = _teilnehmer(client)
        antwort = client.post("/api/lab/run", json={"playbook": "- hosts: all"}, headers=kopf)
        assert antwort.status_code == 200, antwort.text
        assert antwort.json()["rc"] == 0
        assert gesehen["url"] == "http://runner:8080/run"
        assert gesehen["token"] == "geheim"


def test_lab_meldet_nicht_erreichbaren_runner(monkeypatch):
    class FailingClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def post(self, *args, **kwargs):
            raise httpx.ConnectError("keine Verbindung")

    monkeypatch.setattr(settings, "lab_runner_url", "http://runner:8080")
    monkeypatch.setattr(settings, "lab_runner_token", "geheim")
    monkeypatch.setattr(httpx, "AsyncClient", FailingClient)

    with TestClient(app) as client:
        antwort = client.post("/api/lab/run", json={"playbook": "- hosts: all"},
                              headers=_teilnehmer(client))
        assert antwort.status_code == 502


@pytest.mark.parametrize("feld,wert", [("playbook", "x" * 16_001), ("inventory", "y" * 4_001)])
def test_lab_begrenzt_eingabegroesse(feld, wert):
    with TestClient(app) as client:
        daten = {"playbook": "- hosts: all"}
        daten[feld] = wert
        antwort = client.post("/api/lab/run", json=daten, headers=_teilnehmer(client))
        assert antwort.status_code == 422
