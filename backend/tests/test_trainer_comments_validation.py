from fastapi.testclient import TestClient

from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_trainer_comments_require_existing_course_module_and_block():
    with TestClient(app) as c:
        h = _trainer(c)
        course = c.post("/api/courses", json={"name": "TrainerKommentar"}, headers=h).json()
        url = f"/api/trainer/courses/{course['id']}/modules/switching/comments"

        assert c.post(url, json={"block_index": 0, "body": "Hinweis"}, headers=h).status_code == 200
        assert c.post(url, json={"block_index": -1, "body": "Hinweis"}, headers=h).status_code == 422
        assert c.post(f"/api/trainer/courses/{course['id']}/modules/nein/comments",
                      json={"block_index": 0, "body": "Hinweis"}, headers=h).status_code == 404
        assert c.post("/api/trainer/courses/99999/modules/switching/comments",
                      json={"block_index": 0, "body": "Hinweis"}, headers=h).status_code == 404
        assert c.get("/api/trainer/courses/99999/comments", headers=h).status_code == 404
