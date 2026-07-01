from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_trainer_module_requires_trainer():
    with TestClient(app) as c:
        assert c.get("/api/trainer/modules/switching").status_code in (401, 403)


def test_trainer_module_returns_notes_answers_goals():
    with TestClient(app) as c:
        h = _trainer(c)
        r = c.get("/api/trainer/modules/switching", headers=h)
        assert r.status_code == 200
        data = r.json()
        assert data["goals"]
        assert any("note" in b for b in data["blocks"])
        assert data["quiz"]["questions"][0]["answer"]
        assert c.get("/api/trainer/modules", headers=h).status_code == 200
        assert c.get("/api/trainer/modules/nope", headers=h).status_code == 404
