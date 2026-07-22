import jwt
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from app.services.security import ALGORITHM


def _trainer_token(c, email="trainer@test.de", password="trainerpass1"):
    return c.post("/api/trainer/login", json={"email": email, "password": password}).json()["access_token"]


def _headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_password_change_requires_correct_old_password():
    with TestClient(app) as c:
        token = _trainer_token(c)
        r = c.post("/api/trainer/password",
                   json={"old_password": "wrongpass", "new_password": "newpass123"},
                   headers=_headers(token))
        assert r.status_code == 401
        # Fehlversuch bumpt token_version nicht -> derselbe Token funktioniert weiter.
        assert c.get("/api/trainer/modules", headers=_headers(token)).status_code == 200


def test_password_change_invalidates_old_token_and_updates_password():
    with TestClient(app) as c:
        # Eigenen Trainer anlegen, damit dieser Test den geteilten Standard-
        # Trainer (trainer@test.de) nicht für andere Testdateien verändert.
        h = _headers(_trainer_token(c))
        created = c.post("/api/trainer/accounts",
                         json={"email": "pwchange@test.de", "name": "PW", "password": "oldpass123"},
                         headers=h).json()
        old_token = c.post("/api/trainer/login",
                           json={"email": "pwchange@test.de", "password": "oldpass123"}).json()["access_token"]
        old_headers = _headers(old_token)
        assert c.get("/api/trainer/modules", headers=old_headers).status_code == 200

        r = c.post("/api/trainer/password",
                   json={"old_password": "oldpass123", "new_password": "newpass456"},
                   headers=old_headers)
        assert r.status_code == 200
        new_token = r.json()["access_token"]

        # Der zum Wechsel benutzte (alte) Token ist jetzt tot ...
        assert c.get("/api/trainer/modules", headers=old_headers).status_code == 401
        # ... der frisch zurückgegebene Token der Antwort funktioniert weiter ...
        assert c.get("/api/trainer/modules", headers=_headers(new_token)).status_code == 200
        # ... Login mit dem alten Passwort klappt nicht mehr, mit dem neuen schon.
        assert c.post("/api/trainer/login",
                      json={"email": "pwchange@test.de", "password": "oldpass123"}).status_code == 401
        relogged = c.post("/api/trainer/login",
                          json={"email": "pwchange@test.de", "password": "newpass456"})
        assert relogged.status_code == 200
        assert c.get("/api/trainer/modules",
                     headers=_headers(relogged.json()["access_token"])).status_code == 200

        c.delete(f"/api/trainer/accounts/{created['id']}", headers=h)


def test_password_change_rejects_short_new_password():
    with TestClient(app) as c:
        h = _headers(_trainer_token(c))
        created = c.post("/api/trainer/accounts",
                         json={"email": "shortpw@test.de", "name": "S", "password": "oldpass123"},
                         headers=h).json()
        token = c.post("/api/trainer/login",
                       json={"email": "shortpw@test.de", "password": "oldpass123"}).json()["access_token"]
        r = c.post("/api/trainer/password",
                   json={"old_password": "oldpass123", "new_password": "short"},
                   headers=_headers(token))
        assert r.status_code == 422
        # Weiterhin gültig, da Fehlschlag vor dem token_version-Bump passiert.
        assert c.get("/api/trainer/modules", headers=_headers(token)).status_code == 200
        c.delete(f"/api/trainer/accounts/{created['id']}", headers=h)


def test_password_change_requires_auth():
    with TestClient(app) as c:
        r = c.post("/api/trainer/password", json={"old_password": "x", "new_password": "newpass123"})
        assert r.status_code in (401, 403)


def test_trainer_legacy_token_without_token_version_claim_still_works():
    """Alt-Tokens von vor dieser Änderung haben kein token_version-Claim ->
    muss weiterhin funktionieren, solange die DB (frisch) bei 0 steht."""
    with TestClient(app) as c:
        token = _trainer_token(c)
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        del payload["token_version"]
        legacy = jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)
        assert c.get("/api/trainer/modules", headers=_headers(legacy)).status_code == 200
