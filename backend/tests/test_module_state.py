"""Serverseitiger Übungs-/Lesestand je Modul: Rundreise, PUT ersetzt den Stand,
Größengrenze, nur eigene und freigeschaltete Module."""
from fastapi.testclient import TestClient

from app.main import app
from app.routers.modules import STATE_MAX_BYTES


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}).json()["access_token"]}


def _join(c, h, name):
    course = c.post("/api/courses", json={"name": f"State-{name}", "workshop_key": "network"}, headers=h).json()
    tok = c.post("/api/join", json={"code": course["join_code"], "name": name}).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}, course["id"]


def test_state_roundtrip_last_write_wins_and_isolation():
    with TestClient(app) as c:
        h = _trainer(c)
        p, cid = _join(c, h, "Sven")
        other, _ = _join(c, h, "Sina")
        assert c.get("/api/modules/vlan/state", headers=p).json() == {"read": [], "exercises": {}, "updated_at": None}

        blob = {"read": [0, 3], "exercises": {"cloze-1": {"v": "12.345", "s": {"vals": ["a"]}, "done": False}}}
        first = c.put("/api/modules/vlan/state", json=blob, headers=p).json()["updated_at"]
        got = c.get("/api/modules/vlan/state", headers=p).json()
        assert {k: got[k] for k in ("read", "exercises")} == blob and got["updated_at"] == first

        # zweites Gerät schreibt später -> ersetzt den ganzen Stand
        newer = {"read": [1], "exercises": {}}
        second = c.put("/api/modules/vlan/state", json=newer, headers=p).json()["updated_at"]
        got = c.get("/api/modules/vlan/state", headers=p).json()
        assert got["read"] == [1] and got["exercises"] == {}
        # updated_at ist die Basisversion des Clients (moduleStateSync.ts): GET liefert
        # exakt den String der PUT-Antwort, jeder PUT einen neuen.
        assert got["updated_at"] == second != first

        # anderer Teilnehmer sieht nichts davon
        assert c.get("/api/modules/vlan/state", headers=other).json()["updated_at"] is None
        # abgewähltes und unbekanntes Modul: 404, Trainer-Token: 403
        c.put(f"/api/courses/{cid}/modules", json={"module_key": "vlan", "active": False}, headers=h)
        assert c.get("/api/modules/vlan/state", headers=p).status_code == 404
        assert c.put("/api/modules/vlan/state", json=newer, headers=p).status_code == 404
        assert c.put("/api/modules/gibtsnicht/state", json=newer, headers=p).status_code == 404
        assert c.get("/api/modules/vlan/state", headers=h).status_code == 403


def test_state_is_validated_and_capped():
    with TestClient(app) as c:
        p, _ = _join(c, _trainer(c), "Gross")
        too_big = {"read": [], "exercises": {"x": {"s": "a" * STATE_MAX_BYTES}}}
        assert c.put("/api/modules/vlan/state", json=too_big, headers=p).status_code == 422
        assert c.put("/api/modules/vlan/state", json={"read": ["x"]}, headers=p).status_code == 422
        assert c.put("/api/modules/vlan/state", json={"read": [-1]}, headers=p).status_code == 422
        assert c.put("/api/modules/vlan/state", json={"exercises": {"k" * 201: 1}}, headers=p).status_code == 422
        assert c.put("/api/modules/vlan/state", json={"read": list(range(1001))}, headers=p).status_code == 422
        assert c.get("/api/modules/vlan/state", headers=p).json()["updated_at"] is None
