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
        ids = [q["id"] for q in mod["quiz"]["questions"]]
        for q in mod["quiz"]["questions"]:
            assert "answer" not in q

        # Reihenfolge/Antworten entsprechen dem Content in app/content/vlan.py:
        # v1 single->1, v2 single->1, v3 multi->[0,1,3], v4 number->20
        good = {ids[0]: 1, ids[1]: 1, ids[2]: [0, 1, 3], ids[3]: 20}
        r = c.post("/api/modules/vlan/quiz", json={"answers": good}, headers=h).json()
        assert r["score"] == 4 and r["total"] == 4 and r["passed"] is True

        me = c.get("/api/me", headers=h).json()
        vlan = next(p for p in me["progress"] if p["module_key"] == "vlan")
        assert vlan["done"] is True and vlan["best"] == 100

        c.post("/api/modules/vlan/quiz", json={"answers": {ids[0]: 0}}, headers=h)
        me2 = c.get("/api/me", headers=h).json()
        assert next(p for p in me2["progress"] if p["module_key"] == "vlan")["best"] == 100

        assert c.get("/api/modules/nope", headers=h).status_code == 404


def test_get_module_resolves_participant_language():
    with TestClient(app) as c:
        tok = _participant_token(c)
        h = {"Authorization": f"Bearer {tok}"}

        de = c.get("/api/modules/switching", headers=h).json()
        c.patch("/api/me/language", json={"language": "en"}, headers=h)
        en = c.get("/api/modules/switching", headers=h).json()
        assert de["scenario"] != en["scenario"]

        de_list = c.get("/api/modules", headers=h).json()
        assert all("title_en" in m for m in de_list)
