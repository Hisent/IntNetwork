from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _minimal_module(blocks, order=99):
    return {
        "title_de": "Test DE", "title_en": "Test EN", "order": order,
        "prerequisites": [], "goals": [],
        "scenario_de": "Szenario DE", "scenario_en": "Scenario EN",
        "blocks": blocks, "quiz": [],
    }


def _text_block(label):
    return {"type": "text", "value_de": f"Text {label} DE", "value_en": f"Text {label} EN"}


def test_insert_block_before_shifts_comment_to_same_content_block():
    """Kommentar an Block 2 -> neuer Block bei 0 eingefuegt -> Kommentar muss auf
    Position 3 zeigen (denselben inhaltlichen Block), nicht auf einen fremden."""
    with TestClient(app) as c:
        h = _trainer(c)
        key = "remap-insert"
        c.post("/api/trainer/content/modules", json={"key": key, "title_de": "X"}, headers=h)

        blocks = [_text_block("A"), _text_block("B"), _text_block("C"), _text_block("D")]
        assert c.put(f"/api/trainer/content/modules/{key}", json=_minimal_module(blocks), headers=h).status_code == 200

        course = c.post("/api/courses", json={"name": "RemapKurs"}, headers=h).json()
        cid = course["id"]
        comment_url = f"/api/trainer/courses/{cid}/modules/{key}/comments"
        r = c.post(comment_url, json={"block_index": 2, "body": "Kommentar auf C"}, headers=h)
        assert r.status_code == 200

        new_blocks = [_text_block("NEU")] + blocks
        assert c.put(f"/api/trainer/content/modules/{key}", json=_minimal_module(new_blocks), headers=h).status_code == 200

        comments = c.get(f"/api/trainer/courses/{cid}/comments", headers=h).json()
        assert len(comments) == 1
        assert comments[0]["block_index"] == 3
        assert comments[0]["body"] == "Kommentar auf C"


def test_deleted_block_orphans_its_comment_instead_of_pointing_elsewhere():
    """Wird der Block, an dem ein Kommentar haengt, ersatzlos entfernt, darf der
    Kommentar danach nicht stumm an einem fremden Block haengen -- er wird geloescht."""
    with TestClient(app) as c:
        h = _trainer(c)
        key = "remap-delete"
        c.post("/api/trainer/content/modules", json={"key": key, "title_de": "X"}, headers=h)

        blocks = [_text_block("A"), _text_block("B"), _text_block("C")]
        assert c.put(f"/api/trainer/content/modules/{key}", json=_minimal_module(blocks), headers=h).status_code == 200

        course = c.post("/api/courses", json={"name": "RemapKurs2"}, headers=h).json()
        cid = course["id"]
        comment_url = f"/api/trainer/courses/{cid}/modules/{key}/comments"
        assert c.post(comment_url, json={"block_index": 1, "body": "An B"}, headers=h).status_code == 200

        new_blocks = [_text_block("A"), _text_block("C")]  # B entfernt
        assert c.put(f"/api/trainer/content/modules/{key}", json=_minimal_module(new_blocks), headers=h).status_code == 200

        comments = c.get(f"/api/trainer/courses/{cid}/comments", headers=h).json()
        assert comments == []


def test_text_edit_of_commented_block_keeps_comment_at_same_position():
    """Reiner Tippfehler-Fix am kommentierten Block darf den Kommentar nicht
    loeschen: die Inhaltssignatur aendert sich zwar, aber Position und Typ
    bleiben gleich -> der Positions-Fallback muss greifen (Regression zum
    P2-Datenverlust-Bug: Editor loeschte Kommentare bei reiner Textaenderung)."""
    with TestClient(app) as c:
        h = _trainer(c)
        key = "remap-textedit"
        c.post("/api/trainer/content/modules", json={"key": key, "title_de": "X"}, headers=h)

        blocks = [_text_block("A"), _text_block("B"), _text_block("C")]
        assert c.put(f"/api/trainer/content/modules/{key}", json=_minimal_module(blocks), headers=h).status_code == 200

        course = c.post("/api/courses", json={"name": "RemapKurs4"}, headers=h).json()
        cid = course["id"]
        comment_url = f"/api/trainer/courses/{cid}/modules/{key}/comments"
        assert c.post(comment_url, json={"block_index": 1, "body": "An B"}, headers=h).status_code == 200

        edited = [_text_block("A"),
                  {"type": "text", "value_de": "Text B DE korrigiert", "value_en": "Text B EN fixed"},
                  _text_block("C")]
        assert c.put(f"/api/trainer/content/modules/{key}", json=_minimal_module(edited), headers=h).status_code == 200

        comments = c.get(f"/api/trainer/courses/{cid}/comments", headers=h).json()
        assert len(comments) == 1
        assert comments[0]["block_index"] == 1
        assert comments[0]["body"] == "An B"


def test_pure_reorder_keeps_comment_on_same_content_block():
    with TestClient(app) as c:
        h = _trainer(c)
        key = "remap-reorder"
        c.post("/api/trainer/content/modules", json={"key": key, "title_de": "X"}, headers=h)

        blocks = [_text_block("A"), _text_block("B"), _text_block("C")]
        assert c.put(f"/api/trainer/content/modules/{key}", json=_minimal_module(blocks), headers=h).status_code == 200

        course = c.post("/api/courses", json={"name": "RemapKurs3"}, headers=h).json()
        cid = course["id"]
        comment_url = f"/api/trainer/courses/{cid}/modules/{key}/comments"
        assert c.post(comment_url, json={"block_index": 0, "body": "An A"}, headers=h).status_code == 200

        reordered = [_text_block("B"), _text_block("A"), _text_block("C")]
        assert c.put(f"/api/trainer/content/modules/{key}", json=_minimal_module(reordered), headers=h).status_code == 200

        comments = c.get(f"/api/trainer/courses/{cid}/comments", headers=h).json()
        assert len(comments) == 1
        assert comments[0]["block_index"] == 1  # A ist jetzt an Position 1
        assert comments[0]["body"] == "An A"
