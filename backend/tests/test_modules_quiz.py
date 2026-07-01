from fastapi.testclient import TestClient
from app.main import app


def _participant_token(c):
    h = {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}
    code = c.post("/api/courses", json={"name": "QuizKurs"}, headers=h).json()["join_code"]
    return c.post("/api/join", json={"code": code, "name": "Bob"}).json()["access_token"]


def test_module_delivery_hides_answers_and_grades():
    with TestClient(app) as c:
        tok = _participant_token(c)
        h = {"Authorization": f"Bearer {tok}"}

        mod = c.get("/api/modules/vlan", headers=h).json()
        for q in mod["quiz"]["questions"]:
            assert "answer" not in q

        good = {"v1": 1, "v2": 1, "v3": [0, 1, 3], "v4": 20}
        r = c.post("/api/modules/vlan/quiz", json={"answers": good}, headers=h).json()
        assert r["score"] == 4 and r["total"] == 4 and r["passed"] is True

        me = c.get("/api/me", headers=h).json()
        vlan = next(p for p in me["progress"] if p["module_key"] == "vlan")
        assert vlan["done"] is True and vlan["best"] == 100

        c.post("/api/modules/vlan/quiz", json={"answers": {"v1": 0}}, headers=h)
        me2 = c.get("/api/me", headers=h).json()
        assert next(p for p in me2["progress"] if p["module_key"] == "vlan")["best"] == 100

        assert c.get("/api/modules/nope", headers=h).status_code == 404
