"""Üben (/practice) und Suche (/search): serverseitig bewertet bzw. gefiltert,
kursisoliert, ohne Lösungen/Trainer-Notizen/gesperrte Inhalte — und ohne Spuren
in Quiz-Ergebnissen oder Fortschritt."""
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.content import ContentQuizQuestion
from app.models.quiz_result import QuizResult


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _join(c, h, name="Uli", workshop="network"):
    course = c.post("/api/courses", json={"name": f"Lern-{name}", "workshop_key": workshop}, headers=h).json()
    tok = c.post("/api/join", json={"code": course["join_code"], "name": name}).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}, course["id"]


def _answers(key):
    """Frage-id -> Lösung, direkt aus der DB (der Client bekommt sie nie)."""
    db = SessionLocal()
    try:
        return {str(q.id): q.answer for q in db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key == key)}
    finally:
        db.close()


def _wrong(answer):
    return [] if isinstance(answer, list) else answer + 1


def test_practice_serves_last_wrong_first_without_solutions_and_leaves_no_trace():
    with TestClient(app) as c:
        p, _cid = _join(c, _trainer(c))
        # ohne Abgabe gibt es nichts zu üben — und keine Frage lässt sich prüfen
        assert c.get("/api/practice", headers=p).json() == {"questions": [], "wrong_total": 0}
        solution = _answers("vlan")
        first = next(iter(solution))
        assert c.post("/api/practice/check", json={"question_id": first, "answer": solution[first]},
                      headers=p).status_code == 404

        # eine Frage falsch, Rest richtig
        submitted = {**solution, first: _wrong(solution[first])}
        c.post("/api/modules/vlan/quiz", json={"answers": submitted}, headers=p)
        me_before = c.get("/api/me", headers=p).json()

        wrong = c.get("/api/practice?mode=wrong", headers=p).json()
        assert [q["id"] for q in wrong["questions"]] == [first] and wrong["wrong_total"] == 1
        mixed = c.get("/api/practice?mode=mixed", headers=p).json()["questions"]
        assert mixed[0]["id"] == first and {q["id"] for q in mixed} == set(solution)
        for q in mixed:
            assert "answer" not in q and "explanation" not in q and q["module_key"] == "vlan"

        r = c.post("/api/practice/check", json={"question_id": first, "answer": submitted[first]}, headers=p).json()
        assert r["correct"] is False and "answer" not in r
        assert c.post("/api/practice/check", json={"question_id": first, "answer": solution[first]},
                      headers=p).json()["correct"] is True

        # Üben schreibt nichts: Ergebnisse, Bestwert, Fortschritt unverändert
        db = SessionLocal()
        try:
            assert db.query(QuizResult).filter(QuizResult.module_key == "vlan",
                                               QuizResult.participant_id == me_before["participant_id"]).count() == 1
        finally:
            db.close()
        assert c.get("/api/me", headers=p).json() == me_before
        # "zuletzt falsch" heißt letzte Abgabe: nach einer fehlerfreien ist nichts mehr offen
        c.post("/api/modules/vlan/quiz", json={"answers": solution}, headers=p)
        assert c.get("/api/practice?mode=wrong", headers=p).json()["questions"] == []


def test_practice_is_limited_to_own_course_and_attempted_modules():
    with TestClient(app) as c:
        h = _trainer(c)
        p, cid = _join(c, h, "Iso")
        solution = _answers("vlan")
        c.post("/api/modules/vlan/quiz", json={"answers": solution}, headers=p)
        # Frage eines anderen Lehrgangs (im Kurs nicht freigeschaltet)
        foreign = next(iter(_answers("llm-grundlagen")))
        assert c.post("/api/practice/check", json={"question_id": foreign, "answer": 0}, headers=p).status_code == 404
        # freigeschaltet, aber nie abgegeben
        untouched = next(iter(_answers("arp")))
        assert c.post("/api/practice/check", json={"question_id": untouched, "answer": 0}, headers=p).status_code == 404
        # Modul nachträglich gesperrt -> auch seine Fragen sind weg
        assert c.put(f"/api/courses/{cid}/modules", json={"module_key": "vlan", "active": False}, headers=h).status_code == 200
        assert c.get("/api/practice", headers=p).json()["questions"] == []
        assert c.post("/api/practice/check", json={"question_id": next(iter(solution)), "answer": 0},
                      headers=p).status_code == 404
        for bad in ({"question_id": "abc", "answer": 0}, {"question_id": "1", "answer": "x" * 3000}):
            assert c.post("/api/practice/check", json=bad, headers=p).status_code in (404, 422)
        assert c.get("/api/practice").status_code in (401, 403)
        assert c.get("/api/practice", headers=h).status_code == 403  # Trainer-Token ist kein Teilnehmer


def _search_module(c, h, key, workshop, word):
    """Eigenes Modul über den Editor: Text mit Suchwort, dazu Trainer-Notiz und Quiz mit Geheimwörtern."""
    assert c.post("/api/trainer/content/modules", json={"key": key, "title_de": f"Suchmodul {key}",
                                                         "workshop_key": workshop}, headers=h).status_code == 200
    body = {"title_de": f"Suchmodul {key}", "title_en": f"Search module {key}", "order": 90, "prerequisites": [],
            "goals": ["Zielwort Kranich verstehen"], "goals_en": ["Understand the goal word heron"],
            "scenario_de": "Szenario", "scenario_en": "Scenario",
            "blocks": [{"uid": "text-such", "type": "text", "note": "Trainergeheimnis Kolibri",
                        "value_de": f"## Kapitel\n\nDas **Zauberwort** heißt {word}.",
                        "value_en": f"## Chapter\n\nThe **magic word** is {word}-en."},
                       {"uid": "check-such", "type": "check", "payload": {
                           "prompt_de": "Uebungsgeheimnis?", "prompt_en": "Exercise secret?",
                           "options_de": ["a", "b"], "options_en": ["a", "b"], "answer": 1}}],
            "quiz": [{"qtype": "single", "prompt_de": "Quizgeheimnis?", "prompt_en": "Quiz secret?",
                      "options_de": ["Optionsgeheimnis", "B"], "options_en": ["A", "B"], "answer": 0,
                      "explanation_de": "Erklaergeheimnis", "explanation_en": "Explanation secret"}]}
    assert c.put(f"/api/trainer/content/modules/{key}", json=body, headers=h).status_code == 200


def test_search_finds_text_in_active_modules_only_and_never_leaks_quiz_or_notes():
    with TestClient(app) as c:
        h = _trainer(c)
        _search_module(c, h, "suchmod", "network", "Übertragungsgürtel")
        _search_module(c, h, "fremdmod", "claude-code", "Fremdkurswort")
        p, cid = _join(c, h, "Such")  # Kurs NACH dem Anlegen: enthält suchmod, nicht fremdmod

        def find(q):
            return c.get("/api/search", params={"q": q}, headers=p).json()["hits"]

        hits = find("ÜBERTRAGUNGSGÜRTEL")  # Groß/Klein samt Umlauten
        assert [(x["module_key"], x["kind"], x["uid"]) for x in hits] == [("suchmod", "text", "text-such")]
        assert "Zauberwort heißt" in hits[0]["snippet"]  # Markdown-Zeichen entfernt
        assert [(x["module_key"], x["kind"]) for x in find("Suchmodul suchmod")] == [("suchmod", "title")]
        assert [(x["module_key"], x["kind"]) for x in find("kranich")] == [("suchmod", "goal")]
        # nie durchsucht: Trainer-Notiz, Quiz (Frage/Option/Erklärung), Übungs-Payload, fremder Lehrgang
        for secret in ("Kolibri", "Quizgeheimnis", "Optionsgeheimnis", "Erklaergeheimnis", "Uebungsgeheimnis",
                       "Fremdkurswort"):
            assert find(secret) == [], secret

        # Teilnehmersprache: englischer Text und englische Lernziele, der deutsche Wortlaut trifft nicht mehr
        assert c.patch("/api/me/language", json={"language": "en"}, headers=p).status_code == 200
        assert [x["kind"] for x in find("heron")] == ["goal"] and find("kranich") == []
        assert "magic word is" in find("gürtel-en")[0]["snippet"]

        assert c.put(f"/api/courses/{cid}/modules", json={"module_key": "suchmod", "active": False},
                     headers=h).status_code == 200
        assert find("Übertragungsgürtel") == [] and find("heron") == []

        assert c.get("/api/search", params={"q": "a"}, headers=p).status_code == 422
        assert c.get("/api/search", params={"q": "  a  "}, headers=p).status_code == 422
        assert c.get("/api/search", params={"q": "x" * 81}, headers=p).status_code == 422
        assert c.get("/api/search", params={"q": "vlan"}).status_code in (401, 403)
        assert c.get("/api/search", params={"q": "vlan"}, headers=h).status_code == 403


def test_module_list_carries_estimated_minutes():
    with TestClient(app) as c:
        p, _cid = _join(c, _trainer(c), "Zeit")
        mods = c.get("/api/modules", headers=p).json()
        assert mods and all(isinstance(m["minutes"], int) and m["minutes"] >= 5 and m["minutes"] % 5 == 0 for m in mods)
