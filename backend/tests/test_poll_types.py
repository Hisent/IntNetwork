"""Abstimmungsarten über die API: eigene Fragen (Mehrfachauswahl, Skala, Freitext,
Wortwolke) und Multiple-Choice-Quizfragen — Prüfung, Auswertung, Ausblenden, Anonymität."""
from fastapi.testclient import TestClient
from sqlalchemy import event

from app.database import SessionLocal, engine
from app.main import app
from app.models.live_poll import LivePollVote
from tests.test_polls import MOD, _course, _join, _trainer, _vote


def _adhoc(c, h, cid, **body):
    return c.post(f"/api/trainer/courses/{cid}/poll", headers=h,
                  json={"module_key": MOD, "source": "adhoc", **body})


def _setup(c, name, n=2):
    h = _trainer(c)
    code, cid = _course(c, h, name)
    return h, cid, [_join(c, code, f"{name}-Person{i}") for i in range(n)]


def _mine(c, p):
    return c.get(f"/api/modules/{MOD}/poll", headers=p).json()


def _reveal(c, h, cid):
    return c.post(f"/api/trainer/courses/{cid}/poll/reveal", headers=h).json()


def test_start_prueft_eigene_fragen():
    with TestClient(app) as c:
        h, cid, _ = _setup(c, "TypPruef", 0)
        ok = {"kind": "multi", "prompt": "Was?", "options": ["a", "b"]}
        assert _adhoc(c, h, cid, **ok).status_code == 200
        for body in ({**ok, "kind": None}, {**ok, "kind": "umfrage"}, {**ok, "prompt": "  "},
                     {**ok, "options": ["a"]}, {**ok, "options": ["a", " "]}, {**ok, "options": ["x"] * 11},
                     {**ok, "options": ["a", "b"], "max_selections": 3}, {**ok, "prompt": "x" * 301},
                     {**ok, "options": ["x" * 121, "b"]},
                     {"kind": "scale", "prompt": "Wie?", "max": 11}, {"kind": "scale", "prompt": "Wie?", "min": 2},
                     {"kind": "scale", "prompt": "Wie?", "label_min": "x" * 41}):
            assert _adhoc(c, h, cid, **body).status_code == 422, body


def test_mehrfachauswahl():
    with TestClient(app) as c:
        h, cid, (a, b) = _setup(c, "TypMulti")
        poll = _adhoc(c, h, cid, kind="multi", prompt="Welche Protokolle?", options=["TCP", "UDP", "ICMP"],
                      max_selections=2).json()
        assert poll["kind"] == "multi" and poll["max_selections"] == 2 and poll["counts"] == [0, 0, 0]
        assert "answer" not in poll  # eigene Fragen haben keine Lösung
        seen = _mine(c, a)
        assert seen["options"] == ["TCP", "UDP", "ICMP"] and seen["my_choice"] is None and "counts" not in seen
        assert _vote(c, a, poll["id"], [0, 1, 2]).status_code == 422  # mehr als erlaubt
        assert _vote(c, a, poll["id"], 1).status_code == 422          # Einzelwert passt nicht zur Art
        assert _vote(c, a, poll["id"], [0, 1]).json()["my_choice"] == [0, 1]
        assert _vote(c, a, poll["id"], [1, 1]).json()["my_choice"] == [1]  # umentscheiden
        assert _vote(c, b, poll["id"], [2, 1]).status_code == 200
        out = _reveal(c, h, cid)
        assert out["counts"] == [0, 2, 1] and out["votes"] == 2
        mine = _mine(c, a)
        assert mine["counts"] == [0, 2, 1] and mine["my_choice"] == [1]


def test_skala_verteilung_und_mittelwert():
    with TestClient(app) as c:
        h, cid, (a, b) = _setup(c, "TypSkala")
        poll = _adhoc(c, h, cid, kind="scale", prompt="Wie sicher?", min=0, max=10,
                      label_min=" gar nicht ", label_max="sehr").json()
        assert (poll["min"], poll["max"], poll["label_min"], poll["label_max"]) == (0, 10, "gar nicht", "sehr")
        assert "options" not in poll
        for bad in (11, -1, [3], "3"):
            assert _vote(c, a, poll["id"], bad).status_code == 422
        _vote(c, a, poll["id"], 7)
        _vote(c, b, poll["id"], 10)
        assert set(_mine(c, a)) == {"id", "kind", "status", "prompt", "min", "max", "label_min", "label_max",
                                    "my_choice"}
        out = _reveal(c, h, cid)
        assert out["votes"] == 2 and out["mean"] == 8.5 and len(out["counts"]) == 11 and out["counts"][7] == 1
        assert _mine(c, b)["mean"] == 8.5


def test_freitext_ausblenden_und_anonym():
    with TestClient(app) as c:
        h, cid, (a, b) = _setup(c, "TypText")
        poll = _adhoc(c, h, cid, kind="text", prompt="Was nehmt ihr mit?").json()
        assert _vote(c, a, poll["id"], "x" * 281).status_code == 422
        assert _vote(c, a, poll["id"], "   ").status_code == 422
        assert _vote(c, a, poll["id"], "Etwas  Unpassendes").json()["my_choice"] == "Etwas Unpassendes"
        _vote(c, b, poll["id"], "Trunks verstehen")
        # Vor dem Auflösen: Beamer (Trainer-Ansicht) und Teilnehmer sehen keine Texte,
        # der Trainer nur die Zahl und die Prüfliste.
        live = c.get(f"/api/trainer/courses/{cid}/poll", headers=h).json()
        assert "answers" not in live and live["votes"] == 2
        assert [x["text"] for x in live["moderation"]] == ["Etwas Unpassendes", "Trunks verstehen"]
        assert "answers" not in _mine(c, b) and "moderation" not in _mine(c, b)
        bad_id = live["moderation"][0]["id"]
        # vor dem Auflösen ausblenden
        hidden = c.patch(f"/api/trainer/courses/{cid}/poll/answers/{bad_id}", headers=h, json={"hidden": True}).json()
        assert hidden["moderation"][0]["hidden"] is True and hidden["votes"] == 2 and "answers" not in hidden
        # Ändern hebt das Ausblenden nicht auf
        _vote(c, a, poll["id"], "Noch was")
        out = _reveal(c, h, cid)
        assert {x["text"]: x["hidden"] for x in out["moderation"]} == {"Noch was": True, "Trunks verstehen": False}
        assert [x["text"] for x in out["answers"]] == ["Trunks verstehen"]  # Beamer: nur Sichtbares
        seen_b = c.get(f"/api/modules/{MOD}/poll", headers=b)
        assert seen_b.json()["answers"] == [{"text": "Trunks verstehen"}]
        assert _mine(c, a)["my_choice"] == "Noch was"  # die eigene Antwort sieht man selbst
        # nach dem Auflösen wieder einblenden
        r = c.patch(f"/api/trainer/courses/{cid}/poll/answers/{bad_id}", headers=h, json={"hidden": False})
        assert r.status_code == 200
        assert [x["text"] for x in _mine(c, b)["answers"]] == ["Noch was", "Trunks verstehen"]
        # Anonym: weder Namen noch ids/participant in irgendeiner Antwort
        for resp in (seen_b, r, c.get(f"/api/trainer/courses/{cid}/poll", headers=h)):
            assert "TypText-Person" not in resp.text and "participant" not in resp.text
        assert "id" not in _mine(c, b)["answers"][0] and "moderation" not in _mine(c, b)
        # Rollen und fremde/unpassende Ziele
        assert c.patch(f"/api/trainer/courses/{cid}/poll/answers/{bad_id}", headers=a,
                       json={"hidden": True}).status_code == 403
        assert c.patch(f"/api/trainer/courses/{cid}/poll/answers/999999", headers=h,
                       json={"hidden": True}).status_code == 404
        h2, cid2, _ = _setup(c, "TypTextFremd", 0)
        _adhoc(c, h2, cid2, kind="text", prompt="Andere")
        assert c.patch(f"/api/trainer/courses/{cid2}/poll/answers/{bad_id}", headers=h,
                       json={"hidden": True}).status_code == 404


def test_ausblenden_nur_bei_freitext():
    with TestClient(app) as c:
        h, cid, (a,) = _setup(c, "TypNurText", 1)
        poll = _adhoc(c, h, cid, kind="words", prompt="Ein Wort?").json()
        _vote(c, a, poll["id"], ["x"])
        with SessionLocal() as db:
            aid = db.query(LivePollVote.id).filter(LivePollVote.poll_id == poll["id"]).scalar()
        assert c.patch(f"/api/trainer/courses/{cid}/poll/answers/{aid}", headers=h,
                       json={"hidden": True}).status_code == 404


def test_wortwolke_normalisiert_und_zaehlt():
    with TestClient(app) as c:
        h, cid, (a, b) = _setup(c, "TypWolke")
        poll = _adhoc(c, h, cid, kind="words", prompt="Ein Wort zu VLANs?").json()
        assert _vote(c, a, poll["id"], ["a", "b", "c", "d"]).status_code == 422
        assert _vote(c, a, poll["id"], ["x" * 31]).status_code == 422
        assert _vote(c, a, poll["id"], ["", " "]).status_code == 422
        assert _vote(c, a, poll["id"], [" Trunk", "TAG", "trunk "]).json()["my_choice"] == ["trunk", "tag"]
        _vote(c, b, poll["id"], ["trunk", "Native  VLAN"])
        assert "words" not in _mine(c, a)
        live = c.get(f"/api/trainer/courses/{cid}/poll", headers=h).json()
        assert "words" not in live and live["votes"] == 2  # Beamer: vor dem Auflösen nur die Zahl
        assert live["moderation"][0] == {"word": "trunk", "count": 2, "hidden": False}
        out = _reveal(c, h, cid)
        assert out["votes"] == 2 and out["words"] == [
            {"word": "trunk", "count": 2}, {"word": "native vlan", "count": 1}, {"word": "tag", "count": 1}]
        assert _mine(c, b)["words"] == out["words"]


def test_multiple_choice_quizfrage_mit_loesung():
    with TestClient(app) as c:
        h = _trainer(c)
        key, q = next(
            (m["key"], q)
            for m in c.get("/api/trainer/modules", headers=h).json() if m["workshop_key"] == "network"
            for q in c.get(f"/api/trainer/modules/{m['key']}", headers=h).json()["quiz"]["questions"]
            if q["type"] == "multi")
        code, cid = _course(c, h, "TypQuizMulti")
        p = _join(c, code, "P")
        poll = c.post(f"/api/trainer/courses/{cid}/poll", headers=h,
                      json={"module_key": key, "source": "quiz", "ref": q["id"]}).json()
        assert poll["kind"] == "multi" and poll["answer"] == q["answer"] and "max_selections" not in poll
        assert "answer" not in c.get(f"/api/modules/{key}/poll", headers=p).json()
        assert _vote(c, p, poll["id"], q["answer"], key=key).status_code == 200
        out = c.get(f"/api/modules/{key}/poll", headers=p).json()
        assert out["my_choice"] == sorted(q["answer"]) and out["status"] == "open"
        _reveal(c, h, cid)
        out = c.get(f"/api/modules/{key}/poll", headers=p).json()
        assert out["answer"] == q["answer"] and sum(out["counts"]) == len(q["answer"])


def test_wortwolke_wort_ausblenden():
    with TestClient(app) as c:
        h, cid, (a, b) = _setup(c, "TypWortWeg")
        poll = _adhoc(c, h, cid, kind="words", prompt="Ein Wort?").json()
        _vote(c, a, poll["id"], ["Mist", "vlan"])
        url = f"/api/trainer/courses/{cid}/poll/words"
        out = c.patch(url, headers=h, json={"word": "  MIST ", "hidden": True}).json()  # normalisiert
        assert "words" not in out and {"word": "mist", "count": 1, "hidden": True} in out["moderation"]
        _vote(c, b, poll["id"], ["mist", "trunk"])  # später genannt: bleibt ausgeblendet
        out = _reveal(c, h, cid)
        assert [w["word"] for w in out["words"]] == ["trunk", "vlan"] and out["votes"] == 2
        assert out["moderation"][0] == {"word": "mist", "count": 2, "hidden": True}
        seen = c.get(f"/api/modules/{MOD}/poll", headers=b)
        assert seen.json()["words"] == out["words"] and "moderation" not in seen.json()
        for text in (seen.text, str(out)):  # anonym: weder Namen noch Teilnehmer-Bezug
            assert "TypWortWeg-Person" not in text and "participant" not in text
        # wieder einblenden
        out = c.patch(url, headers=h, json={"word": "mist", "hidden": False}).json()
        assert out["words"][0] == {"word": "mist", "count": 2}
        # Rollen und unpassende Ziele
        assert c.patch(url, headers=a, json={"word": "vlan", "hidden": True}).status_code == 403
        assert c.patch(url, headers=h, json={"word": " ", "hidden": True}).status_code == 404
        h2, cid2, _ = _setup(c, "TypWortText", 0)
        _adhoc(c, h2, cid2, kind="text", prompt="Freitext")
        assert c.patch(f"/api/trainer/courses/{cid2}/poll/words", headers=h2,
                       json={"word": "x", "hidden": True}).status_code == 404


def test_wort_ausblenden_sperrt_die_zeile():
    """Read-modify-write auf config["hidden_words"] unter Zeilensperre. Prüfbar nur
    unter Postgres (CI-Job backend-postgres-migration): SQLite lässt FOR UPDATE weg."""
    statements = []
    with TestClient(app) as c:
        h, cid, (a,) = _setup(c, "TypWortSperre", 1)
        poll = _adhoc(c, h, cid, kind="words", prompt="Ein Wort?").json()
        _vote(c, a, poll["id"], ["mist"])
        listener = lambda *args: statements.append(args[2])  # noqa: E731 (conn, cursor, statement, ...)
        event.listen(engine, "before_cursor_execute", listener)
        try:
            out = c.patch(f"/api/trainer/courses/{cid}/poll/words", headers=h, json={"word": "mist", "hidden": True})
        finally:
            event.remove(engine, "before_cursor_execute", listener)
        assert out.status_code == 200 and out.json()["moderation"][0]["hidden"] is True
    if engine.dialect.name == "postgresql":
        assert any("FROM live_poll" in s and "FOR UPDATE" in s for s in statements)
