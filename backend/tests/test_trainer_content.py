from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _minimal_module(order=99):
    return {
        "title_de": "Test DE", "title_en": "Test EN", "order": order,
        "pass_threshold": 0.7, "prerequisites": [], "goals": [],
        "scenario_de": "Szenario DE", "scenario_en": "Scenario EN",
        "blocks": [{"type": "text", "value_de": "Text DE", "value_en": "Text EN"}],
        "quiz": [{"qtype": "single", "prompt_de": "Frage?", "prompt_en": "Question?",
                  "options_de": ["A", "B"], "options_en": ["A", "B"], "answer": 1}],
    }


def test_content_endpoints_require_trainer():
    with TestClient(app) as c:
        assert c.get("/api/trainer/content/modules").status_code in (401, 403)
        assert c.get("/api/trainer/content/modules/vlan").status_code in (401, 403)
        assert c.post("/api/trainer/content/modules", json={"key": "x", "title_de": "X"}).status_code in (401, 403)
        assert c.put("/api/trainer/content/modules/vlan", json=_minimal_module()).status_code in (401, 403)


def test_create_get_update_round_trip():
    with TestClient(app) as c:
        h = _trainer(c)
        created = c.post("/api/trainer/content/modules", json={"key": "testmod", "title_de": "Testmodul"}, headers=h)
        assert created.status_code == 200
        assert created.json()["key"] == "testmod"

        got = c.get("/api/trainer/content/modules/testmod", headers=h)
        assert got.status_code == 200
        assert got.json()["blocks"] == []
        assert got.json()["quiz"] == []

        updated = c.put("/api/trainer/content/modules/testmod", json=_minimal_module(order=99), headers=h)
        assert updated.status_code == 200

        got2 = c.get("/api/trainer/content/modules/testmod", headers=h).json()
        assert got2["title_de"] == "Test DE"
        assert len(got2["blocks"]) == 1 and got2["blocks"][0]["value_de"] == "Text DE"
        assert len(got2["quiz"]) == 1 and got2["quiz"][0]["answer"] == 1

        listed = c.get("/api/trainer/content/modules", headers=h).json()
        assert any(m["key"] == "testmod" for m in listed)


def test_create_rejects_bad_key_and_duplicate():
    with TestClient(app) as c:
        h = _trainer(c)
        assert c.post("/api/trainer/content/modules", json={"key": "Bad Key!", "title_de": "X"}, headers=h).status_code == 422
        c.post("/api/trainer/content/modules", json={"key": "dupmod", "title_de": "X"}, headers=h)
        assert c.post("/api/trainer/content/modules", json={"key": "dupmod", "title_de": "Y"}, headers=h).status_code == 422


def test_update_rejects_unknown_module():
    with TestClient(app) as c:
        h = _trainer(c)
        assert c.put("/api/trainer/content/modules/does-not-exist", json=_minimal_module(), headers=h).status_code == 404


def test_update_rejects_invalid_widget_id():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "widgetmod", "title_de": "X"}, headers=h)
        body = _minimal_module()
        body["blocks"] = [{"type": "widget", "widget_id": "nope-demo"}]
        assert c.put("/api/trainer/content/modules/widgetmod", json=body, headers=h).status_code == 422


def test_update_rejects_self_and_unknown_prerequisite():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "premod", "title_de": "X"}, headers=h)
        body = _minimal_module()
        body["prerequisites"] = ["premod"]
        assert c.put("/api/trainer/content/modules/premod", json=body, headers=h).status_code == 422
        body["prerequisites"] = ["nope"]
        assert c.put("/api/trainer/content/modules/premod", json=body, headers=h).status_code == 422


def test_update_rejects_out_of_range_answer_index():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "answermod", "title_de": "X"}, headers=h)
        body = _minimal_module()
        body["quiz"] = [{"qtype": "single", "prompt_de": "F?", "prompt_en": "Q?",
                         "options_de": ["A", "B"], "options_en": ["A", "B"], "answer": 5}]
        assert c.put("/api/trainer/content/modules/answermod", json=body, headers=h).status_code == 422


def test_update_accepts_number_question_without_options():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "nummod", "title_de": "X"}, headers=h)
        body = _minimal_module()
        body["quiz"] = [{"qtype": "number", "prompt_de": "Wie viel?", "prompt_en": "How much?", "answer": 42}]
        assert c.put("/api/trainer/content/modules/nummod", json=body, headers=h).status_code == 200
        got = c.get("/api/trainer/content/modules/nummod", headers=h).json()
        assert got["quiz"][0]["answer"] == 42
        assert got["quiz"][0]["options_de"] is None
