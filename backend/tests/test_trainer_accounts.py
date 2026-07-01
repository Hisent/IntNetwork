from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models.trainer import Trainer


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_accounts_require_trainer():
    with TestClient(app) as c:
        assert c.get("/api/trainer/accounts").status_code in (401, 403)
        assert c.post("/api/trainer/accounts", json={"email": "x@x.de", "name": "X", "password": "pass1234"}).status_code in (401, 403)
        assert c.delete("/api/trainer/accounts/1").status_code in (401, 403)


def test_create_and_list_trainer():
    with TestClient(app) as c:
        h = _trainer(c)
        r = c.post("/api/trainer/accounts", json={"email": "Second@Test.de", "name": "Second", "password": "pass1234"}, headers=h)
        assert r.status_code == 200
        assert r.json()["email"] == "second@test.de"

        listed = c.get("/api/trainer/accounts", headers=h).json()
        assert any(t["email"] == "second@test.de" for t in listed)


def test_create_rejects_duplicate_email():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/accounts", json={"email": "dup@test.de", "name": "D", "password": "pass1234"}, headers=h)
        r = c.post("/api/trainer/accounts", json={"email": "dup@test.de", "name": "D2", "password": "pass1234"}, headers=h)
        assert r.status_code == 422


def test_create_rejects_short_password():
    with TestClient(app) as c:
        h = _trainer(c)
        r = c.post("/api/trainer/accounts", json={"email": "short@test.de", "name": "S", "password": "abc"}, headers=h)
        assert r.status_code == 422


def test_create_rejects_bad_email():
    with TestClient(app) as c:
        h = _trainer(c)
        r = c.post("/api/trainer/accounts", json={"email": "not-an-email", "name": "X", "password": "pass1234"}, headers=h)
        assert r.status_code == 422


def test_new_trainer_can_login_and_use_trainer_endpoints():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/accounts", json={"email": "newlogin@test.de", "name": "New", "password": "pass1234"}, headers=h)

        login = c.post("/api/trainer/login", json={"email": "newlogin@test.de", "password": "pass1234"})
        assert login.status_code == 200
        new_h = {"Authorization": f"Bearer {login.json()['access_token']}"}

        assert c.get("/api/trainer/modules", headers=new_h).status_code == 200

        wrong = c.post("/api/trainer/login", json={"email": "newlogin@test.de", "password": "wrongpass"})
        assert wrong.status_code == 401


def test_delete_trainer():
    with TestClient(app) as c:
        h = _trainer(c)
        created = c.post("/api/trainer/accounts", json={"email": "todelete@test.de", "name": "D", "password": "pass1234"}, headers=h).json()
        r = c.delete(f"/api/trainer/accounts/{created['id']}", headers=h)
        assert r.status_code == 200
        listed = c.get("/api/trainer/accounts", headers=h).json()
        assert not any(t["id"] == created["id"] for t in listed)


def test_delete_last_trainer_blocked():
    """Reduziert die trainer-Tabelle temporär auf 1 Zeile (DB wird über den
    ganzen Testlauf geteilt, u.a. mit dem geseedeten trainer@test.de) und
    stellt den Ausgangszustand danach exakt wieder her, damit spätere Tests
    (inkl. anderer Dateien) nicht auf einen gelöschten Trainer treffen."""
    with TestClient(app) as c:
        h = _trainer(c)
        db = SessionLocal()
        try:
            all_trainers = db.query(Trainer).all()
            others = all_trainers[1:]
            backup = [(t.id, t.email, t.name, t.password_hash, t.created_at) for t in others]
            for t in others:
                db.delete(t)
            db.commit()
        finally:
            db.close()

        remaining = c.get("/api/trainer/accounts", headers=h).json()
        assert len(remaining) == 1
        r = c.delete(f"/api/trainer/accounts/{remaining[0]['id']}", headers=h)
        assert r.status_code == 422

        db = SessionLocal()
        try:
            for tid, email, name, pw_hash, created_at in backup:
                db.add(Trainer(id=tid, email=email, name=name, password_hash=pw_hash, created_at=created_at))
            db.commit()
        finally:
            db.close()


def test_delete_unknown_trainer_404():
    with TestClient(app) as c:
        h = _trainer(c)
        assert c.delete("/api/trainer/accounts/999999", headers=h).status_code == 404


def test_deleted_trainer_token_immediately_rejected():
    with TestClient(app) as c:
        h = _trainer(c)
        created = c.post("/api/trainer/accounts", json={"email": "revoke@test.de", "name": "R", "password": "pass1234"}, headers=h).json()
        login = c.post("/api/trainer/login", json={"email": "revoke@test.de", "password": "pass1234"})
        revoked_h = {"Authorization": f"Bearer {login.json()['access_token']}"}
        assert c.get("/api/trainer/modules", headers=revoked_h).status_code == 200

        c.delete(f"/api/trainer/accounts/{created['id']}", headers=h)

        assert c.get("/api/trainer/modules", headers=revoked_h).status_code == 401
