from fastapi.testclient import TestClient
from app.main import app
from app.services import ratelimit


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


def test_comment_body_length_capped():
    with TestClient(app) as c:
        h = _trainer(c)
        code = _course(c, h, "KursLang2")
        p = _join(c, code, "P9")
        assert c.post("/api/modules/switching/comments",
                      json={"block_index": 0, "body": "x" * 2001}, headers=p).status_code == 422
        assert c.post("/api/modules/switching/comments",
                      json={"block_index": 0, "body": "x" * 2000}, headers=p).status_code == 200


def test_comments_require_a_visible_module_and_existing_block():
    with TestClient(app) as c:
        h = _trainer(c)
        code = _course(c, h, "KursZiel")
        p = _join(c, code, "P10")

        assert c.get("/api/modules/gibt-es-nicht/comments", headers=p).status_code == 404
        assert c.post("/api/modules/gibt-es-nicht/comments",
                      json={"block_index": 0, "body": "x"}, headers=p).status_code == 404
        assert c.post("/api/modules/switching/comments",
                      json={"block_index": -1, "body": "x"}, headers=p).status_code == 422
        assert c.post("/api/modules/switching/comments",
                      json={"block_index": 9999, "body": "x"}, headers=p).status_code == 422

        course = c.get("/api/courses", headers=h).json()[0]
        assert c.put(f"/api/courses/{course['id']}/modules",
                     json={"module_key": "switching", "active": False}, headers=h).status_code == 200
        assert c.post("/api/modules/switching/comments",
                      json={"block_index": 0, "body": "x"}, headers=p).status_code == 404


def test_add_comment_is_rate_limited(monkeypatch):
    monkeypatch.setattr(ratelimit, "_ENABLED", True)
    monkeypatch.setattr(ratelimit, "_HITS", ratelimit.defaultdict(ratelimit.deque))
    with TestClient(app) as c:
        h = _trainer(c)
        code = _course(c, h, "KursRate")
        p = _join(c, code, "RateP")
        for _ in range(30):  # Limit aus comments.py: 30 Kommentare / 60s
            assert c.post("/api/modules/switching/comments",
                          json={"block_index": 0, "body": "hi"}, headers=p).status_code == 200
        blocked = c.post("/api/modules/switching/comments",
                         json={"block_index": 0, "body": "hi"}, headers=p)
        assert blocked.status_code == 429


def test_list_comments_supports_limit_and_offset():
    with TestClient(app) as c:
        h = _trainer(c)
        code = _course(c, h, "KursPage")
        p = _join(c, code, "PagerP")
        for i in range(5):
            assert c.post("/api/modules/switching/comments",
                          json={"block_index": 0, "body": f"Kommentar {i}"}, headers=p).status_code == 200

        default = c.get("/api/modules/switching/comments", headers=p).json()
        assert len(default) == 5  # großzügiger Default schneidet nichts ab

        page1 = c.get("/api/modules/switching/comments?limit=2&offset=0", headers=p).json()
        page2 = c.get("/api/modules/switching/comments?limit=2&offset=2", headers=p).json()
        assert [x["body"] for x in page1] == ["Kommentar 0", "Kommentar 1"]
        assert [x["body"] for x in page2] == ["Kommentar 2", "Kommentar 3"]

        assert c.get("/api/modules/switching/comments?limit=0", headers=p).status_code == 422
        assert c.get("/api/modules/switching/comments?offset=-1", headers=p).status_code == 422


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
