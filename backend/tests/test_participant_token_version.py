import jwt
from fastapi.testclient import TestClient

from app.config import settings
from app.database import SessionLocal
from app.main import app
from app.models.participant import Participant
from app.services.security import ALGORITHM


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_token_with_stale_token_version_rejected():
    """Ein Token, dessen token_version-Claim nicht mehr zum DB-Wert passt (z.B.
    weil der Trainer zwischenzeitlich den Code zurückgesetzt hat), muss 401
    liefern statt akzeptiert zu werden."""
    with TestClient(app) as c:
        h = _trainer(c)
        code = c.post("/api/courses", json={"name": "TVKurs"}, headers=h).json()["join_code"]
        joined = c.post("/api/join", json={"code": code, "name": "Tina"}).json()
        auth = {"Authorization": f"Bearer {joined['access_token']}"}
        assert c.get("/api/me", headers=auth).status_code == 200

        db = SessionLocal()
        try:
            p = db.query(Participant).filter(Participant.name == "Tina").first()
            p.token_version += 1
            db.commit()
        finally:
            db.close()

        assert c.get("/api/me", headers=auth).status_code == 401


def test_token_without_token_version_claim_treated_as_zero():
    """Alt-Tokens von vor dieser Änderung haben kein token_version-Claim ->
    muss weiterhin funktionieren, solange die DB (frisch) bei 0 steht."""
    with TestClient(app) as c:
        h = _trainer(c)
        code = c.post("/api/courses", json={"name": "LegacyTVKurs"}, headers=h).json()["join_code"]
        joined = c.post("/api/join", json={"code": code, "name": "Lena"}).json()
        db = SessionLocal()
        try:
            pid = db.query(Participant).filter(Participant.name == "Lena").first().id
        finally:
            db.close()
        legacy_payload = jwt.decode(joined["access_token"], settings.secret_key, algorithms=[ALGORITHM])
        del legacy_payload["token_version"]
        legacy_token = jwt.encode(legacy_payload, settings.secret_key, algorithm=ALGORITHM)

        assert c.get("/api/me", headers={"Authorization": f"Bearer {legacy_token}"}).status_code == 200


def test_reset_code_invalidates_running_token():
    """Der Trainer-Reset des Wiederaufnahme-Codes muss auch die laufende
    JWT-Sitzung beenden, nicht nur den alten Code sperren."""
    with TestClient(app) as c:
        h = _trainer(c)
        course = c.post("/api/courses", json={"name": "ResetTVKurs"}, headers=h).json()
        joined = c.post("/api/join", json={"code": course["join_code"], "name": "Ronja"}).json()
        auth = {"Authorization": f"Bearer {joined['access_token']}"}
        assert c.get("/api/me", headers=auth).status_code == 200

        db = SessionLocal()
        try:
            pid = db.query(Participant).filter(Participant.name == "Ronja").first().id
        finally:
            db.close()

        reset = c.post(f"/api/courses/{course['id']}/participants/{pid}/reset-code", headers=h)
        assert reset.status_code == 200

        # Alte Sitzung ist tot ...
        assert c.get("/api/me", headers=auth).status_code == 401
        # ... neuer Join mit dem neuen Code klappt und liefert einen frischen Token.
        rejoin = c.post("/api/join", json={
            "code": course["join_code"], "name": "Ronja", "resume_code": reset.json()["resume_code"]})
        assert rejoin.status_code == 200
        new_auth = {"Authorization": f"Bearer {rejoin.json()['access_token']}"}
        assert c.get("/api/me", headers=new_auth).status_code == 200
