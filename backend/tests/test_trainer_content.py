from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _minimal_module(order=99):
    return {
        "title_de": "Test DE", "title_en": "Test EN", "order": order,
        "prerequisites": [], "goals": [],
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


def test_update_rejects_inconsistent_quiz_translations_and_answer_types():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "quizval", "title_de": "X"}, headers=h)
        url = "/api/trainer/content/modules/quizval"

        body = _minimal_module()
        body["quiz"][0]["options_en"] = ["A"]
        assert c.put(url, json=body, headers=h).status_code == 422

        body = _minimal_module()
        body["quiz"][0]["answer"] = [1]
        assert c.put(url, json=body, headers=h).status_code == 422

        body = _minimal_module()
        body["quiz"][0]["qtype"] = "multi"
        body["quiz"][0]["answer"] = []
        assert c.put(url, json=body, headers=h).status_code == 422

        body = _minimal_module()
        body["quiz"] = [{"qtype": "number", "prompt_de": "F?", "prompt_en": "Q?", "answer": [42]}]
        assert c.put(url, json=body, headers=h).status_code == 422


def test_concurrent_create_same_key_never_500s():
    """Zwei gleichzeitige Create-Requests mit demselben Key (z.B. Doppelklick)
    duerfen nie mit 500 crashen -> genau einer gewinnt (200), der Rest 422."""
    with TestClient(app, raise_server_exceptions=False) as c:
        h = _trainer(c)
        results = []

        def create():
            r = c.post("/api/trainer/content/modules", json={"key": "racemod", "title_de": "X"}, headers=h)
            results.append(r.status_code)

        with ThreadPoolExecutor(max_workers=8) as ex:
            list(ex.map(lambda _: create(), range(8)))

        assert results.count(500) == 0
        assert results.count(200) == 1
        assert results.count(422) == 7


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


def test_check_and_reveal_blocks_round_trip_and_delivery():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "checkmod", "title_de": "X"}, headers=h)
        body = _minimal_module()
        body["blocks"] = [
            {"type": "check", "payload": {
                "prompt_de": "2+2?", "prompt_en": "2+2?",
                "options_de": ["3", "4"], "options_en": ["3", "4"], "answer": 1}},
            {"type": "reveal", "value_de": "Versteckt DE", "value_en": "Hidden EN",
             "payload": {"teaser_de": "Was passiert?", "teaser_en": "What happens?"}},
        ]
        assert c.put("/api/trainer/content/modules/checkmod", json=body, headers=h).status_code == 200

        got = c.get("/api/trainer/content/modules/checkmod", headers=h).json()
        assert got["blocks"][0]["payload"]["answer"] == 1
        assert got["blocks"][1]["payload"]["teaser_de"] == "Was passiert?"

        # Teilnehmer-Auslieferung: sprachaufgelöst, check inkl. answer (Selbst-Check)
        code = c.post("/api/courses", json={"name": "CheckKurs"}, headers=h).json()["join_code"]
        p = {"Authorization": "Bearer " + c.post(
            "/api/join", json={"code": code, "name": "Chk"}).json()["access_token"]}
        pub = c.get("/api/modules/checkmod", headers=p).json()
        assert pub["blocks"][0] == {"type": "check", "kind": "choice", "prompt": "2+2?", "options": ["3", "4"], "answer": 1}
        assert pub["blocks"][1] == {"type": "reveal", "teaser": "Was passiert?", "value": "Versteckt DE"}


def test_check_block_validation():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "checkval", "title_de": "X"}, headers=h)
        body = _minimal_module()
        body["blocks"] = [{"type": "check", "payload": {
            "prompt_de": "F?", "prompt_en": "Q?",
            "options_de": ["a", "b"], "options_en": ["a", "b"], "answer": 5}}]
        assert c.put("/api/trainer/content/modules/checkval", json=body, headers=h).status_code == 422
        body["blocks"] = [{"type": "check", "payload": {"prompt_de": "F?", "prompt_en": "Q?"}}]
        assert c.put("/api/trainer/content/modules/checkval", json=body, headers=h).status_code == 422
        body["blocks"] = [{"type": "reveal", "value_de": "x", "value_en": "y", "payload": {}}]
        assert c.put("/api/trainer/content/modules/checkval", json=body, headers=h).status_code == 422


def test_get_module_reports_has_snapshot():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "snapmod", "title_de": "X"}, headers=h)

        fresh = c.get("/api/trainer/content/modules/snapmod", headers=h).json()
        assert fresh["has_snapshot"] is False

        c.put("/api/trainer/content/modules/snapmod", json=_minimal_module(order=1), headers=h)
        after_first_put = c.get("/api/trainer/content/modules/snapmod", headers=h).json()
        assert after_first_put["has_snapshot"] is True


def test_restore_requires_trainer():
    with TestClient(app) as c:
        assert c.post("/api/trainer/content/modules/vlan/restore").status_code in (401, 403)


def test_restore_unknown_module_404():
    with TestClient(app) as c:
        h = _trainer(c)
        assert c.post("/api/trainer/content/modules/does-not-exist/restore", headers=h).status_code == 404


def test_restore_without_snapshot_404():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "nosnap", "title_de": "X"}, headers=h)
        assert c.post("/api/trainer/content/modules/nosnap/restore", headers=h).status_code == 404


def test_restore_swaps_and_supports_redo():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "swapmod", "title_de": "X"}, headers=h)

        version_a = _minimal_module(order=1)
        version_a["title_de"] = "Version A"
        c.put("/api/trainer/content/modules/swapmod", json=version_a, headers=h)

        version_b = _minimal_module(order=1)
        version_b["title_de"] = "Version B"
        c.put("/api/trainer/content/modules/swapmod", json=version_b, headers=h)

        current = c.get("/api/trainer/content/modules/swapmod", headers=h).json()
        assert current["title_de"] == "Version B"

        r1 = c.post("/api/trainer/content/modules/swapmod/restore", headers=h)
        assert r1.status_code == 200
        after_restore_1 = c.get("/api/trainer/content/modules/swapmod", headers=h).json()
        assert after_restore_1["title_de"] == "Version A"
        assert after_restore_1["has_snapshot"] is True

        r2 = c.post("/api/trainer/content/modules/swapmod/restore", headers=h)
        assert r2.status_code == 200
        after_restore_2 = c.get("/api/trainer/content/modules/swapmod", headers=h).json()
        assert after_restore_2["title_de"] == "Version B"


def test_new_block_types_validation():
    """order/debug/reflect + Rechen-Check: kaputte Payloads -> 422, gültige -> 200."""
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "blockmod", "title_de": "X"}, headers=h)
        url = "/api/trainer/content/modules/blockmod"

        def put_with(block):
            body = _minimal_module()
            body["blocks"] = [block]
            return c.put(url, json=body, headers=h)

        # Rechen-Check: answer muss Zahl sein
        assert put_with({"type": "check", "payload": {
            "kind": "number", "prompt_de": "F?", "prompt_en": "Q?", "answer": "abc"}}).status_code == 422
        assert put_with({"type": "check", "payload": {
            "kind": "number", "prompt_de": "F?", "prompt_en": "Q?", "answer": 62}}).status_code == 200

        # order: ungleich lange Listen / zu wenige Schritte -> 422
        assert put_with({"type": "order", "payload": {
            "prompt_de": "F?", "prompt_en": "Q?",
            "items_de": ["a", "b"], "items_en": ["a"]}}).status_code == 422
        assert put_with({"type": "order", "payload": {
            "prompt_de": "F?", "prompt_en": "Q?",
            "items_de": ["a"], "items_en": ["a"]}}).status_code == 422
        assert put_with({"type": "order", "payload": {
            "prompt_de": "F?", "prompt_en": "Q?",
            "items_de": ["a", "b"], "items_en": ["a", "b"]}}).status_code == 200

        # debug: wrong-Index ausserhalb / keine Markierung / fehlende Erklaerung -> 422
        base_debug = {"prompt_de": "F?", "prompt_en": "Q?",
                      "lines_de": ["x", "y"], "lines_en": ["x", "y"],
                      "explanation_de": "E", "explanation_en": "E"}
        assert put_with({"type": "debug", "payload": {**base_debug, "wrong": [5]}}).status_code == 422
        assert put_with({"type": "debug", "payload": {**base_debug, "wrong": []}}).status_code == 422
        assert put_with({"type": "debug", "payload": {
            **{k: v for k, v in base_debug.items() if not k.startswith("explanation")},
            "wrong": [1]}}).status_code == 422
        assert put_with({"type": "debug", "payload": {**base_debug, "wrong": [1]}}).status_code == 200

        # reflect: prompt Pflicht
        assert put_with({"type": "reflect", "payload": {"prompt_de": "F?"}}).status_code == 422
        assert put_with({"type": "reflect", "payload": {
            "prompt_de": "F?", "prompt_en": "Q?"}}).status_code == 200


def test_new_block_types_delivery():
    """order/debug/reflect werden sprachaufgeloest an Teilnehmer ausgeliefert."""
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "delivmod", "title_de": "X"}, headers=h)
        body = _minimal_module()
        body["blocks"] = [
            {"type": "order", "payload": {
                "prompt_de": "Sortiere DE", "prompt_en": "Sort EN",
                "items_de": ["eins", "zwei"], "items_en": ["one", "two"]}},
            {"type": "debug", "payload": {
                "prompt_de": "Finde DE", "prompt_en": "Find EN",
                "lines_de": ["ok", "kaputt"], "lines_en": ["ok", "broken"],
                "wrong": [1], "explanation_de": "Erkl DE", "explanation_en": "Expl EN"}},
            {"type": "reflect", "payload": {"prompt_de": "Denk nach", "prompt_en": "Think"}},
            {"type": "check", "payload": {
                "kind": "number", "prompt_de": "Wieviel?", "prompt_en": "How many?", "answer": 62}},
        ]
        assert c.put("/api/trainer/content/modules/delivmod", json=body, headers=h).status_code == 200

        code = c.post("/api/courses", json={"name": "DelivKurs"}, headers=h).json()["join_code"]
        p = {"Authorization": "Bearer " + c.post(
            "/api/join", json={"code": code, "name": "Del"}).json()["access_token"]}
        pub = c.get("/api/modules/delivmod", headers=p).json()
        assert pub["blocks"][0] == {"type": "order", "prompt": "Sortiere DE", "items": ["eins", "zwei"]}
        assert pub["blocks"][1] == {"type": "debug", "prompt": "Finde DE",
                                    "lines": ["ok", "kaputt"], "wrong": [1], "explanation": "Erkl DE"}
        assert pub["blocks"][2] == {"type": "reflect", "prompt": "Denk nach"}
        assert pub["blocks"][3] == {"type": "check", "kind": "number", "prompt": "Wieviel?",
                                    "options": [], "answer": 62}


def test_reseed_restores_delivery_state_and_snapshots_previous():
    with TestClient(app) as c:
        h = _trainer(c)
        # Modul verbiegen: nur noch 1 Block, Titel geändert
        orig = c.get("/api/trainer/content/modules/dns", headers=h).json()
        mangled = {**{k: v for k, v in orig.items() if k not in ("key", "has_snapshot", "has_seed")},
                   "title_de": "Kaputt-DNS",
                   "blocks": [{"type": "text", "value_de": "nur noch das", "value_en": "only this"}],
                   "quiz": []}
        assert c.put("/api/trainer/content/modules/dns", json=mangled, headers=h).status_code == 200

        r = c.post("/api/trainer/content/modules/dns/reseed", headers=h)
        assert r.status_code == 200

        after = c.get("/api/trainer/content/modules/dns", headers=h).json()
        assert after["title_de"] != "Kaputt-DNS"
        assert len(after["blocks"]) > 1
        assert len(after["quiz"]) == 5  # inkl. PTR-Frage d5
        # PTR-Inhalt aus dem aktuellen Seed ist da
        assert any(b["value_de"] and "PTR" in b["value_de"] for b in after["blocks"] if b["type"] == "text")

        # Undo: Restore bringt den verbogenen Stand zurück
        assert c.post("/api/trainer/content/modules/dns/restore", headers=h).status_code == 200
        undone = c.get("/api/trainer/content/modules/dns", headers=h).json()
        assert undone["title_de"] == "Kaputt-DNS"
        # und nochmal Reseed für saubere Test-DB
        assert c.post("/api/trainer/content/modules/dns/reseed", headers=h).status_code == 200


def test_reseed_only_for_seed_modules():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "eigenbau", "title_de": "Eigenes"}, headers=h)
        r = c.post("/api/trainer/content/modules/eigenbau/reseed", headers=h)
        assert r.status_code == 404
        assert c.post("/api/trainer/content/modules/nope/reseed", headers=h).status_code == 404
        assert c.post("/api/trainer/content/modules/dns/reseed").status_code in (401, 403)


def test_get_module_reports_has_seed():
    with TestClient(app) as c:
        h = _trainer(c)
        assert c.get("/api/trainer/content/modules/dns", headers=h).json()["has_seed"] is True
        c.post("/api/trainer/content/modules", json={"key": "ohneseed", "title_de": "X"}, headers=h)
        assert c.get("/api/trainer/content/modules/ohneseed", headers=h).json()["has_seed"] is False
