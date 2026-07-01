from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_features_default_on_and_toggle():
    with TestClient(app) as c:
        assert c.get("/api/features").json() == {"comments": True}
        h = _trainer(c)
        assert c.put("/api/trainer/features", json={"comments": False}, headers=h).json() == {"comments": False}
        assert c.get("/api/features").json() == {"comments": False}
        c.put("/api/trainer/features", json={"comments": True}, headers=h)


def test_toggle_requires_trainer():
    with TestClient(app) as c:
        assert c.put("/api/trainer/features", json={"comments": False}).status_code in (401, 403)
