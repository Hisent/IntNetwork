from fastapi.testclient import TestClient
from app.main import app


def test_trainer_login_ok_and_bad():
    with TestClient(app) as c:
        r = c.post("/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"})
        assert r.status_code == 200
        assert r.json()["access_token"]

        bad = c.post("/api/trainer/login", json={"email": "trainer@test.de", "password": "wrong"})
        assert bad.status_code == 401
