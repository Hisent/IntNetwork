import hashlib
import uuid

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.api_token import TrainerApiToken
from app.models.audit_log import AuditLog
from app.models.workshop import Workshop
from app.services.api_tokens import resolve_token


def _login(c, email, password):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": email, "password": password}).json()["access_token"]}


def _admin(c):
    return _login(c, "trainer@test.de", "trainerpass1")


def _new_trainer(c, admin):
    email = f"tok-{uuid.uuid4().hex[:8]}@test.de"
    r = c.post("/api/trainer/accounts", json={"email": email, "name": email, "password": "pass1234"},
               headers=admin)
    assert r.status_code == 200
    return r.json()["id"], email, _login(c, email, "pass1234")


def test_token_wird_einmal_im_klartext_geliefert_und_gehasht_gespeichert():
    with TestClient(app) as c:
        admin = _admin(c)
        tid, email, h = _new_trainer(c, admin)
        assert c.post("/api/trainer/api-tokens", json={"name": ""}, headers=h).status_code == 422
        assert c.post("/api/trainer/api-tokens", json={"name": "x" * 61}, headers=h).status_code == 422

        r = c.post("/api/trainer/api-tokens", json={"name": "Laptop"}, headers=h)
        assert r.status_code == 200, r.text
        body = r.json()
        token = body["token"]
        assert token.startswith("lgt_") and body["prefix"] == token[:8] and body["name"] == "Laptop"

        listed = c.get("/api/trainer/api-tokens", headers=h).json()
        assert len(listed) == 1 and "token" not in listed[0]
        assert set(listed[0]) == {"id", "name", "prefix", "created_at", "last_used_at"}
        assert listed[0]["last_used_at"] is None
        # Fremde Tokens tauchen nicht in der eigenen Liste auf.
        assert all(t["id"] != body["id"] for t in c.get("/api/trainer/api-tokens", headers=admin).json())

        with SessionLocal() as db:
            row = db.get(TrainerApiToken, body["id"])
            assert row.token_hash == hashlib.sha256(token.encode()).hexdigest()
            assert token not in (row.token_hash, row.prefix)
            # Klartext landet nie im Audit.
            audits = db.query(AuditLog).filter(AuditLog.action == "api_token.create").all()
            assert audits and all(token not in f"{a.target} {a.detail}" for a in audits)

            who = resolve_token(db, token)
            assert who["trainer_id"] == tid and who["sub"] == email and who["role"] == "trainer"
            assert who["is_admin"] is False and who["token_name"] == "Laptop"
            assert resolve_token(db, "lgt_unbekannt") is None
            assert resolve_token(db, "") is None

        assert c.get("/api/trainer/api-tokens", headers=h).json()[0]["last_used_at"] is not None


def test_fremdes_token_nicht_loeschbar():
    with TestClient(app) as c:
        admin = _admin(c)
        _, _, h1 = _new_trainer(c, admin)
        _, _, h2 = _new_trainer(c, admin)
        tok = c.post("/api/trainer/api-tokens", json={"name": "A"}, headers=h1).json()
        # Auch ein Admin löscht fremde Tokens nicht über diesen Endpunkt.
        assert c.delete(f"/api/trainer/api-tokens/{tok['id']}", headers=h2).status_code == 404
        assert c.delete(f"/api/trainer/api-tokens/{tok['id']}", headers=admin).status_code == 404
        assert c.delete(f"/api/trainer/api-tokens/{tok['id']}", headers=h1).status_code == 200
        assert c.get("/api/trainer/api-tokens", headers=h1).json() == []
        with SessionLocal() as db:
            assert resolve_token(db, tok["token"]) is None


def test_admin_widerruft_alle_tokens():
    with TestClient(app) as c:
        admin = _admin(c)
        tid, _, h = _new_trainer(c, admin)
        toks = [c.post("/api/trainer/api-tokens", json={"name": n}, headers=h).json()["token"] for n in "AB"]
        # Nur Admins.
        assert c.delete(f"/api/trainer/accounts/{tid}/api-tokens", headers=h).status_code == 403
        r = c.delete(f"/api/trainer/accounts/{tid}/api-tokens", headers=admin)
        assert r.status_code == 200 and r.json() == {"deleted": 2}
        assert c.get("/api/trainer/api-tokens", headers=h).json() == []
        with SessionLocal() as db:
            assert all(resolve_token(db, t) is None for t in toks)
            assert db.query(AuditLog).filter(AuditLog.action == "api_token.revoke_all",
                                             AuditLog.target == f"trainer:{tid}").count() == 1


def test_api_token_gilt_nicht_an_trainer_rest():
    with TestClient(app) as c:
        _, _, h = _new_trainer(c, _admin(c))
        token = c.post("/api/trainer/api-tokens", json={"name": "MCP"}, headers=h).json()["token"]
        r = c.get("/api/trainer/accounts", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 401


def test_trainer_loeschen_entfernt_tokens_und_gibt_lehrgaenge_frei():
    with TestClient(app) as c:
        admin = _admin(c)
        tid, _, h = _new_trainer(c, admin)
        token = c.post("/api/trainer/api-tokens", json={"name": "A"}, headers=h).json()["token"]
        key = f"ws-{uuid.uuid4().hex[:8]}"
        with SessionLocal() as db:
            db.add(Workshop(key=key, title_de="E", title_en="E", summary_de="S", summary_en="S",
                            theme="network", sections=[], context=None, status="draft", owner_trainer_id=tid))
            db.commit()

        assert c.delete(f"/api/trainer/accounts/{tid}", headers=admin).status_code == 200

        with SessionLocal() as db:
            assert db.query(TrainerApiToken).filter(TrainerApiToken.trainer_id == tid).count() == 0
            assert resolve_token(db, token) is None
            assert db.get(Workshop, key).owner_trainer_id is None
