"""Lernerfolg: Wissenstest vorher/nachher, anonyme Kursbewertung, CSV-Export."""
from datetime import timedelta

from fastapi.testclient import TestClient
from sqlalchemy import inspect

from app.database import SessionLocal, engine
from app.main import app
from app.models.content import ContentQuizQuestion
from app.models.course import Course
from app.models.learning_outcome import AssessmentAnswer, CourseEvaluation
from app.models.participant import Participant
from app.models.quiz_result import QuizResult
from app.routers.learning_outcomes import MAX_QUESTIONS, MIN_EVALUATIONS, draw_questions
from app.services import retention
from app.services.csv_export import to_csv
from app.utils import utc_now


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _course(c, h, name):
    return c.post("/api/courses", json={"name": name, "workshop_key": "network"}, headers=h).json()


def _join(c, course, name):
    tok = c.post("/api/join", json={"code": course["join_code"], "name": name}).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}


def _solutions(ids):
    db = SessionLocal()
    try:
        return {str(q.id): q.answer for q in db.query(ContentQuizQuestion).filter(
            ContentQuizQuestion.id.in_([int(i) for i in ids]))}
    finally:
        db.close()


def test_draw_is_deterministic_and_capped():
    modules = [[f"{m}-{i}" for i in range(4)] for m in range(5)]
    assert draw_questions(modules, "7:0") == draw_questions(modules, "7:0")
    assert len(draw_questions(modules, "7:0")) == 10  # 5 Module x 2
    assert draw_questions(modules, "7:0") != draw_questions(modules, "7:1") or \
        draw_questions(modules, "7:0") != draw_questions(modules, "7:2")
    many = [[f"{m}-{i}" for i in range(3)] for m in range(20)]
    picked = draw_questions(many, "1:0")
    assert len(picked) == MAX_QUESTIONS and len({p.split("-")[0] for p in picked}) == MAX_QUESTIONS
    # Reihenfolge = Modulreihenfolge
    assert [int(p.split("-")[0]) for p in picked] == sorted(int(p.split("-")[0]) for p in picked)
    assert draw_questions([[], ["a"]], "x") == ["a"] and draw_questions([], "x") == []


def test_pre_post_flow_scoring_and_one_answer_per_phase():
    with TestClient(app) as c:
        h = _trainer(c)
        course = _course(c, h, "LO-Flow")
        cid = course["id"]
        p = _join(c, course, "Pia")
        me_before = c.get("/api/me", headers=p).json()
        assert me_before["tasks"] == {"assessment": None, "evaluation": False}
        assert c.get("/api/assessment", headers=p).json() is None

        preview = c.get(f"/api/trainer/courses/{cid}/assessment", headers=h).json()
        ids = [q["id"] for q in preview["questions"]]
        assert 0 < len(ids) <= MAX_QUESTIONS and not preview["fixed"] and preview["phase"] is None
        # Regenerieren vor der ersten Antwort ist erlaubt und zieht neu
        regen = c.post(f"/api/trainer/courses/{cid}/assessment/regenerate", headers=h).json()
        ids = [q["id"] for q in regen["questions"]]
        opened = c.put(f"/api/trainer/courses/{cid}/assessment", json={"phase": "pre"}, headers=h).json()
        assert [q["id"] for q in opened["questions"]] == ids and opened["fixed"]

        assert c.get("/api/me", headers=p).json()["tasks"]["assessment"] == "pre"
        open_test = c.get("/api/assessment", headers=p).json()
        assert open_test["phase"] == "pre" and open_test["result"] is None
        assert [q["id"] for q in open_test["questions"]] == ids
        assert all("answer" not in q and "explanation" not in q for q in open_test["questions"])

        solution = _solutions(ids)
        # falsche Phase -> 409, nichts gespeichert
        assert c.post("/api/assessment", json={"phase": "post", "answers": solution}, headers=p).status_code == 409
        first = ids[0]
        wrong = {**solution, first: [] if isinstance(solution[first], list) else solution[first] + 1}
        pre = c.post("/api/assessment", json={"phase": "pre", "answers": wrong}, headers=p)
        assert pre.status_code == 200
        assert pre.json() == {"score": len(ids) - 1, "total": len(ids)}  # vorher: keine Erklärungen, kein richtig/falsch
        assert c.post("/api/assessment", json={"phase": "pre", "answers": solution}, headers=p).status_code == 409
        again = c.get("/api/assessment", headers=p).json()
        assert again["questions"] == [] and again["result"]["score"] == len(ids) - 1
        assert c.get("/api/me", headers=p).json()["tasks"]["assessment"] is None
        # Mit Antworten bleibt der Satz fest
        assert c.post(f"/api/trainer/courses/{cid}/assessment/regenerate", headers=h).status_code == 409

        c.put(f"/api/trainer/courses/{cid}/assessment", json={"phase": "post"}, headers=h)
        post = c.post("/api/assessment", json={"phase": "post", "answers": solution}, headers=p).json()
        assert post["score"] == post["total"] == len(ids)
        assert all(post["details"].values()) and set(post["details"]) == set(ids)
        assert "explanations" in post

        view = c.get(f"/api/trainer/courses/{cid}/assessment", headers=h).json()
        row = next(r for r in view["participants"] if r["name"] == "Pia")
        assert row["post"] == 100 and row["pre"] == round((len(ids) - 1) * 100 / len(ids))
        assert view["summary"]["avg_gain"] == round(100 - row["pre"], 1) and view["summary"]["gain_count"] == 1
        q0 = next(q for q in view["questions"] if q["id"] == first)
        assert (q0["pre_correct"], q0["pre_attempts"], q0["post_correct"], q0["post_attempts"]) == (0, 1, 1, 1)

        # Fortschritt, Bestwerte, Quiz-Ergebnisse unberührt
        me_after = c.get("/api/me", headers=p).json()
        assert me_after["progress"] == me_before["progress"]
        db = SessionLocal()
        try:
            assert db.query(QuizResult).filter(QuizResult.participant_id == me_before["participant_id"]).count() == 0
        finally:
            db.close()

        # Schließen: nichts mehr offen
        c.put(f"/api/trainer/courses/{cid}/assessment", json={"phase": None}, headers=h)
        assert c.get("/api/assessment", headers=p).json() is None
        assert c.post("/api/assessment", json={"phase": "post", "answers": {}}, headers=p).status_code == 409


def test_evaluation_is_anonymous_and_once_per_participant():
    with TestClient(app) as c:
        h = _trainer(c)
        course = _course(c, h, "LO-Eval")
        cid = course["id"]
        anna, ben = _join(c, course, "Anna Anonym"), _join(c, course, "Ben Anonym")
        body = {"overall": 4, "clarity": 5, "pace": "fast", "good": "Viele Übungen", "improve": "Mehr Pausen"}
        assert c.post("/api/evaluation", json=body, headers=anna).status_code == 409  # noch nicht geöffnet

        c.put(f"/api/trainer/courses/{cid}/evaluation", json={"open": True}, headers=h)
        assert c.get("/api/me", headers=anna).json()["tasks"]["evaluation"] is True
        assert c.post("/api/evaluation", json={**body, "overall": 6}, headers=anna).status_code == 422
        assert c.post("/api/evaluation", json={"clarity": 3}, headers=anna).status_code == 422  # overall Pflicht
        assert c.post("/api/evaluation", json=body, headers=anna).status_code == 200
        assert c.post("/api/evaluation", json=body, headers=anna).status_code == 409
        assert c.get("/api/me", headers=anna).json()["tasks"]["evaluation"] is False
        assert c.post("/api/evaluation", json={"overall": 2}, headers=ben).status_code == 200

        # Unter MIN_EVALUATIONS nur die Zahl -- weder API noch CSV verraten Inhalte.
        res = c.get(f"/api/trainer/courses/{cid}/evaluation", headers=h)
        assert res.json() == {"open": True, "count": 2, "min_count": MIN_EVALUATIONS, "hidden": True}
        ev = c.get(f"/api/trainer/courses/{cid}/export/evaluation", headers=h).content.decode("utf-8-sig")
        assert "Viele Übungen" not in ev and "Mehr Pausen" not in ev and "Gesamteindruck" not in ev
        assert ev.splitlines()[:3] == ["Abgaben;2", "", "Ergebnisse erst ab 3 Abgaben (Anonymität)."]

        assert c.post("/api/evaluation", json={"overall": 3}, headers=_join(c, course, "Cleo Anonym")).status_code == 200
        res = c.get(f"/api/trainer/courses/{cid}/evaluation", headers=h)
        data = res.json()
        assert data["count"] == 3 and data["hidden"] is False
        assert data["overall"] == {"n": 3, "mean": 3.0, "counts": [0, 1, 1, 1, 0]}
        assert data["clarity"]["n"] == 1 and data["pace"] == {"slow": 0, "ok": 0, "fast": 1}
        assert data["good"] == ["Viele Übungen"] and data["improve"] == ["Mehr Pausen"]
        assert "Anonym" not in res.text and "participant" not in res.text

        # Die Zeile selbst kennt keine Person und keinen Zeitpunkt.
        cols = {col["name"] for col in inspect(engine).get_columns("course_evaluation")}
        assert cols == {"id", "course_id", "overall", "clarity", "practice", "pace", "trainer", "good", "improve"}
        db = SessionLocal()
        try:
            rows = db.query(CourseEvaluation).filter(CourseEvaluation.course_id == cid).all()
            pids = {p.id for p in db.query(Participant).filter(Participant.course_id == cid)}
            assert len(rows) == 3 and all(len(r.id) == 24 for r in rows)  # zufällig, nicht fortlaufend
            # Teilnehmer löschen lässt die anonyme Bewertung stehen
            c.delete(f"/api/courses/{cid}/participants/{min(pids)}", headers=h)
            assert db.query(CourseEvaluation).filter(CourseEvaluation.course_id == cid).count() == 3
        finally:
            db.close()

        c.put(f"/api/trainer/courses/{cid}/evaluation", json={"open": False}, headers=h)
        assert c.get("/api/me", headers=ben).json()["tasks"]["evaluation"] is False


def test_csv_quoting_bom_and_formula_guard():
    out = to_csv([["Name", "Wert"], ["=SUM(A1)", 5], ["+1", -3], ["-x", 2.5], ["@a", None],
                  ["\tTab", "a;b"], ["\rCR", 'sagt "hi"\nzweite Zeile'], ["normal", "ok"]])
    assert out.startswith("﻿Name;Wert\r\n")
    lines = out[1:].split("\r\n")
    assert lines[1] == "'=SUM(A1);5"
    assert lines[2] == "'+1;-3"  # Zahl bleibt Zahl
    assert lines[3] == "'-x;2,5"  # Dezimalkomma
    assert lines[4] == "'@a;"
    assert lines[5] == "'\tTab;\"a;b\""
    assert out.count('"sagt ""hi""\nzweite Zeile"') == 1
    assert "'\rCR" in out


def test_csv_exports_authz_and_content():
    with TestClient(app) as c:
        h = _trainer(c)
        course = _course(c, h, "LO-CSV")
        cid = course["id"]
        evil = _join(c, course, "=HYPERLINK(\"http://x\")")
        c.put(f"/api/trainer/courses/{cid}/evaluation", json={"open": True}, headers=h)
        c.post("/api/evaluation", json={"overall": 5, "good": "@cmd; \"quoted\""}, headers=evil)
        for name in ("Zwei", "Drei"):  # ab MIN_EVALUATIONS zeigt der Export Inhalte
            c.post("/api/evaluation", json={"overall": 5}, headers=_join(c, course, name))
        c.put(f"/api/trainer/courses/{cid}/assessment", json={"phase": "pre"}, headers=h)

        for kind in ("dashboard", "quiz", "assessment", "evaluation"):
            r = c.get(f"/api/trainer/courses/{cid}/export/{kind}", headers=h)
            assert r.status_code == 200, kind
            assert r.headers["content-type"].startswith("text/csv")
            assert "attachment" in r.headers["content-disposition"]
            assert r.content.startswith(b"\xef\xbb\xbf")
        dash = c.get(f"/api/trainer/courses/{cid}/export/dashboard", headers=h).content.decode("utf-8-sig")
        assert dash.splitlines()[0].startswith("Teilnehmer;Module erledigt;")
        assert '"\'=HYPERLINK(""http://x"")"' in dash
        assert "\n=HYPERLINK" not in dash
        ev = c.get(f"/api/trainer/courses/{cid}/export/evaluation?lang=en", headers=h).content.decode("utf-8-sig")
        assert "Overall;3;5,0;0;0;0;0;3" in ev and '"\'@cmd; ""quoted"""' in ev

        # Nur Trainer; unbekannter Kurs/Typ
        assert c.get(f"/api/trainer/courses/{cid}/export/dashboard", headers=evil).status_code == 403
        assert c.get(f"/api/trainer/courses/{cid}/export/dashboard").status_code in (401, 403)
        assert c.get("/api/trainer/courses/999999/export/dashboard", headers=h).status_code == 404
        assert c.get(f"/api/trainer/courses/{cid}/export/secrets", headers=h).status_code == 422
        for url in (f"/api/trainer/courses/{cid}/assessment", f"/api/trainer/courses/{cid}/evaluation"):
            assert c.get(url, headers=evil).status_code == 403
        assert c.put(f"/api/trainer/courses/{cid}/evaluation", json={"open": False}, headers=evil).status_code == 403


def test_retention_purges_assessment_answers_but_keeps_evaluations():
    with TestClient(app):
        pass
    db = SessionLocal()
    try:
        old = utc_now() - timedelta(days=300)
        course = Course(name="LO-Ret", join_code="LORET1")
        db.add(course)
        db.flush()
        p = Participant(course_id=course.id, name="Alt", created_at=old, evaluation_submitted=True)
        db.add(p)
        db.flush()
        db.add(AssessmentAnswer(participant_id=p.id, phase="pre", answers={}, score=0, total=1, created_at=old))
        db.add(CourseEvaluation(id="ret-test-1", course_id=course.id, overall=3))
        db.commit()
        pid, cid = p.id, course.id
        counts = retention.purge(db, 90)
        assert counts["assessment_answers"] >= 1
        assert db.query(AssessmentAnswer).filter(AssessmentAnswer.participant_id == pid).count() == 0
        assert db.query(CourseEvaluation).filter(CourseEvaluation.course_id == cid).count() == 1
    finally:
        db.close()
