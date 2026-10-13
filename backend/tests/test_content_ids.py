"""Kennungen (uid) und Quiz-Erklärungen über die API: Speichern und
"Auslieferungszustand laden" im Editor behalten die Fragen-Zeilen (an deren id
hängen Abgaben und Statistik), Erklärungen erreichen Teilnehmer erst mit dem
bewerteten Ergebnis."""
from fastapi.testclient import TestClient

from app.main import app

KEY = "icmp"


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _participant(c, h, name, language="de"):
    code = c.post("/api/courses", json={"name": f"Kurs {name}"}, headers=h).json()["join_code"]
    token = c.post("/api/join", json={"code": code, "name": name}).json()["access_token"]
    ph = {"Authorization": f"Bearer {token}"}
    assert c.patch("/api/me/language", json={"language": language}, headers=ph).status_code == 200
    return ph


def _question_ids(c, h):
    """{Kennung: ausgelieferte Frage-id} — Editor und Trainer-Ansicht liefern in derselben Reihenfolge."""
    editor = c.get(f"/api/trainer/content/modules/{KEY}", headers=h).json()
    delivered = c.get(f"/api/trainer/modules/{KEY}", headers=h).json()
    return {q["uid"]: d["id"] for q, d in zip(editor["quiz"], delivered["quiz"]["questions"], strict=True)}


def test_save_and_reseed_keep_question_rows_submissions_and_stats():
    with TestClient(app) as c:
        h = _trainer(c)
        url = f"/api/trainer/content/modules/{KEY}"
        assert c.post(f"{url}/reseed", headers=h).status_code == 200
        ids = _question_ids(c, h)
        editor = c.get(url, headers=h).json()
        assert all(b["uid"] for b in editor["blocks"]) and all(q["uid"] for q in editor["quiz"])

        # Teilnehmer lädt das Quiz, gibt aber erst NACH den Änderungen ab (laufende Abgabe)
        ph = _participant(c, h, "Ida")
        loaded = c.get(f"/api/modules/{KEY}", headers=ph).json()["quiz"]["questions"]
        assert [q["id"] for q in loaded] == list(ids.values())
        answers = {d["id"]: q["answer"] for q, d in zip(editor["quiz"], loaded, strict=True)}

        # Speichern: Frage vorn eingefügt, erste alte Frage umformuliert, zwei Blöcke getauscht
        edited = {**editor, "quiz": [
            {"qtype": "number", "prompt_de": "Neu?", "prompt_en": "New?", "answer": 7},
            {**editor["quiz"][0], "prompt_de": "Umformuliert?", "explanation_de": "Darum.", "explanation_en": "Hence."},
            *editor["quiz"][1:]],
            "blocks": [editor["blocks"][1], editor["blocks"][0], *editor["blocks"][2:]]}
        assert c.put(url, json=edited, headers=h).status_code == 200
        after_save = _question_ids(c, h)
        assert {uid: after_save[uid] for uid in ids} == ids and len(after_save) == len(ids) + 1
        saved = c.get(url, headers=h).json()
        assert [b["uid"] for b in saved["blocks"]] == [b["uid"] for b in edited["blocks"]]

        # die vor dem Speichern geladene Abgabe trifft weiter ihre Fragen (nur die neue fehlt ihr)
        r = c.post(f"/api/modules/{KEY}/quiz", json={"answers": answers}, headers=ph).json()
        assert (r["score"], r["total"]) == (len(ids), len(ids) + 1)
        # Erklärungen aller Fragen der Abgabe; die umformulierte trägt die neue
        assert r["explanations"] == {after_save[q["uid"]]: q["explanation_de"] for q in saved["quiz"] if q["explanation_de"]}
        assert r["explanations"][ids[editor["quiz"][0]["uid"]]] == "Darum."

        # Auslieferungszustand laden: dieselben Zeilen, die Abgabe bleibt in der Statistik
        assert c.post(f"{url}/reseed", headers=h).status_code == 200
        assert _question_ids(c, h) == ids
        stats = c.get(f"/api/trainer/modules/{KEY}/quiz-stats", headers=h).json()
        assert [(s["id"], s["correct"], s["attempts"]) for s in stats["questions"]] == [(i, 1, 1) for i in ids.values()]
        # … und "Vorherige Version wiederherstellen" ebenso
        assert c.post(f"{url}/restore", headers=h).status_code == 200
        restored = _question_ids(c, h)  # die eigene Frage war gelöscht und ist als neue Zeile zurück
        assert restored.keys() == after_save.keys() and {uid: restored[uid] for uid in ids} == ids
        assert c.post(f"{url}/reseed", headers=h).status_code == 200


def test_explanation_only_after_grading_and_in_participant_language():
    with TestClient(app) as c:
        h = _trainer(c)
        url = f"/api/trainer/content/modules/{KEY}"
        editor = c.get(url, headers=h).json()
        first = editor["quiz"][0]

        half = {**editor, "quiz": [{**first, "explanation_de": "Nur deutsch", "explanation_en": None}, *editor["quiz"][1:]]}
        assert c.put(url, json=half, headers=h).status_code == 422

        full = {**editor, "quiz": [{**first, "explanation_de": "Weil A.", "explanation_en": "Because A."},
                                   {**editor["quiz"][1], "explanation_de": "  ", "explanation_en": ""},
                                   *editor["quiz"][2:]]}
        assert c.put(url, json=full, headers=h).status_code == 200
        stored = c.get(url, headers=h).json()["quiz"]
        assert (stored[0]["explanation_de"], stored[1]["explanation_de"], stored[1]["explanation_en"]) == ("Weil A.", None, None)
        trainer_view = c.get(f"/api/trainer/modules/{KEY}", headers=h).json()["quiz"]["questions"]
        assert trainer_view[0]["explanation"] == "Weil A." and "explanation" not in trainer_view[1]

        ph = _participant(c, h, "Eve", language="en")
        delivered = c.get(f"/api/modules/{KEY}", headers=ph).json()
        assert "Because A." not in str(delivered) and "Weil A." not in str(delivered)
        assert all("explanation" not in q and "answer" not in q for q in delivered["quiz"]["questions"])
        qid = delivered["quiz"]["questions"][0]["id"]
        r = c.post(f"/api/modules/{KEY}/quiz", json={"answers": {}}, headers=ph).json()
        expected = {d["id"]: q["explanation_en"] for q, d in zip(stored, delivered["quiz"]["questions"], strict=True)
                    if q["explanation_en"]}
        assert r["explanations"] == expected and r["details"][qid] is False
        assert expected[qid] == "Because A." and delivered["quiz"]["questions"][1]["id"] not in expected

        assert c.post(f"{url}/reseed", headers=h).status_code == 200
