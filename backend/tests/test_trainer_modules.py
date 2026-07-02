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


def test_quiz_stats_aggregate_per_question():
    with TestClient(app) as c:
        h = _trainer(c)
        # eigenen Kurs + Teilnehmer anlegen, der einmal gut und einmal schlecht abgibt
        code = c.post("/api/courses", json={"name": "StatsKurs"}, headers=h).json()["join_code"]
        ph = {"Authorization": "Bearer " + c.post(
            "/api/join", json={"code": code, "name": "Statistik-Susi"}).json()["access_token"]}
        mod = c.get("/api/modules/vlan", headers=ph).json()
        ids = [q["id"] for q in mod["quiz"]["questions"]]
        good = {ids[0]: 1, ids[1]: 1, ids[2]: [0, 1, 3], ids[3]: 20}
        c.post("/api/modules/vlan/quiz", json={"answers": good}, headers=ph)
        c.post("/api/modules/vlan/quiz", json={"answers": {ids[0]: 1}}, headers=ph)

        r = c.get("/api/trainer/modules/vlan/quiz-stats", headers=h)
        assert r.status_code == 200
        data = r.json()
        assert data["submissions"] >= 2
        by_id = {q["id"]: q for q in data["questions"]}
        # Frage 1 in beiden Abgaben richtig, Frage 2 nur in der guten
        assert by_id[ids[0]]["correct"] >= 2
        assert by_id[ids[1]]["correct"] >= 1
        assert all(q["prompt"] for q in data["questions"])
        assert all(q["attempts"] == data["submissions"] for q in data["questions"])

        assert c.get("/api/trainer/modules/nope/quiz-stats", headers=h).status_code == 404
        assert c.get("/api/trainer/modules/vlan/quiz-stats").status_code in (401, 403)


def test_quiz_stats_filters_by_course():
    with TestClient(app) as c:
        h = _trainer(c)
        # Kurs A: eine perfekte Abgabe; Kurs B: eine leere Abgabe
        outer = {}
        for name, answers_kind in (("KursA", "good"), ("KursB", "empty")):
            code = c.post("/api/courses", json={"name": name}, headers=h).json()["join_code"]
            cid = next(k["id"] for k in c.get("/api/courses", headers=h).json() if k["name"] == name)
            ph = {"Authorization": "Bearer " + c.post(
                "/api/join", json={"code": code, "name": f"P-{name}"}).json()["access_token"]}
            mod = c.get("/api/modules/vlan", headers=ph).json()
            ids = [q["id"] for q in mod["quiz"]["questions"]]
            answers = {ids[0]: 1, ids[1]: 1, ids[2]: [0, 1, 3], ids[3]: 20} if answers_kind == "good" else {}
            c.post("/api/modules/vlan/quiz", json={"answers": answers}, headers=ph)
            outer[name] = cid

        a = c.get(f"/api/trainer/modules/vlan/quiz-stats?course_id={outer['KursA']}", headers=h).json()
        b = c.get(f"/api/trainer/modules/vlan/quiz-stats?course_id={outer['KursB']}", headers=h).json()
        assert a["submissions"] == 1
        assert b["submissions"] == 1
        assert all(q["correct"] == 1 for q in a["questions"])
        assert all(q["correct"] == 0 for q in b["questions"])
        # ohne Filter: mindestens beide zusammen
        alle = c.get("/api/trainer/modules/vlan/quiz-stats", headers=h).json()
        assert alle["submissions"] >= 2
