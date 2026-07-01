from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _course(c, h, name):
    return c.post("/api/courses", json={"name": name}, headers=h).json()["join_code"]


def _join(c, code, name):
    return {"Authorization": "Bearer " + c.post(
        "/api/join", json={"code": code, "name": name}).json()["access_token"]}


def test_participant_comment_flow():
    with TestClient(app) as c:
        h = _trainer(c)
        code_a = _course(c, h, "KursA")
        code_b = _course(c, h, "KursB")
        a1 = _join(c, code_a, "A1")
        a2 = _join(c, code_a, "A2")
        b1 = _join(c, code_b, "B1")

        r = c.post("/api/modules/switching/comments",
                   json={"block_index": 0, "body": "Guter Abschnitt"}, headers=a1)
        assert r.status_code == 200
        cid = r.json()["id"]

        assert c.get("/api/modules/switching/comments", headers=a1).json()[0]["own"] is True
        assert c.get("/api/modules/switching/comments", headers=a2).json()[0]["own"] is False
        assert c.get("/api/modules/switching/comments", headers=b1).json() == []

        assert c.post("/api/modules/switching/comments",
                      json={"block_index": 0, "body": "   "}, headers=a1).status_code == 400
        assert c.delete(f"/api/comments/{cid}", headers=a2).status_code == 403
        assert c.delete(f"/api/comments/{cid}", headers=a1).status_code == 200
        assert c.delete(f"/api/comments/{cid}", headers=a1).status_code == 404


def test_comments_gated_by_feature():
    with TestClient(app) as c:
        h = _trainer(c)
        code = _course(c, h, "KursGate")
        p = _join(c, code, "P1")
        c.put("/api/trainer/features", json={"comments": False}, headers=h)
        assert c.get("/api/modules/switching/comments", headers=p).status_code == 403
        assert c.post("/api/modules/switching/comments",
                      json={"block_index": 0, "body": "x"}, headers=p).status_code == 403
        c.put("/api/trainer/features", json={"comments": True}, headers=h)
