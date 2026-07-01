from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _join(c, code, name):
    return {"Authorization": "Bearer " + c.post(
        "/api/join", json={"code": code, "name": name}).json()["access_token"]}


def test_trainer_comment_flow():
    with TestClient(app) as c:
        h = _trainer(c)
        course = c.post("/api/courses", json={"name": "KursT"}, headers=h).json()
        cid = next(x["id"] for x in c.get("/api/courses", headers=h).json()
                   if x["join_code"] == course["join_code"])
        p = _join(c, course["join_code"], "P1")

        c.post("/api/modules/vlan/comments", json={"block_index": 1, "body": "Frage dazu"}, headers=p)
        r = c.post(f"/api/trainer/courses/{cid}/modules/vlan/comments",
                   json={"block_index": 1, "body": "Antwort vom Trainer"}, headers=h)
        assert r.status_code == 200 and r.json()["author_kind"] == "trainer"
        tid = r.json()["id"]

        allc = c.get(f"/api/trainer/courses/{cid}/comments", headers=h).json()
        assert len(allc) == 2
        assert all("module_key" in x for x in allc)

        part_id = next(x["id"] for x in allc if x["author_kind"] == "participant")
        assert c.delete(f"/api/trainer/comments/{part_id}", headers=h).status_code == 200
        assert c.delete(f"/api/trainer/comments/{tid}", headers=h).status_code == 200
        assert c.delete(f"/api/trainer/comments/{tid}", headers=h).status_code == 404
