"""Wiederholung (spaced review) und Aufwärmrunde: Auswahlregeln (rein) und API
(Fälligkeit, Leitner-Verlauf, Kursisolation, keine Spuren in Fortschritt/Quiz)."""
import random
from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.content import ContentQuizQuestion
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.models.review import ReviewItem
from app.services import review
from app.services.review import Candidate, due_in_order, is_due, next_streak
from app.utils import utc_now

NOW = datetime(2026, 10, 14, 9, 0)


def _c(qid, *, reviewed=None, streak=0, wrong=False, completed=NOW - timedelta(days=1)):
    return Candidate(qid=qid, completed_at=completed, last_reviewed=reviewed, streak=streak, wrong=wrong)


def test_leitner_spacing():
    assert is_due(None, 0, NOW)
    # falsch -> nach INTERVALS[0] wieder dran, richtig -> der Abstand wächst je Kasten
    assert not is_due(NOW - timedelta(minutes=5), 0, NOW) and is_due(NOW - timedelta(minutes=10), 0, NOW)
    assert not is_due(NOW - timedelta(hours=19), 1, NOW) and is_due(NOW - timedelta(hours=20), 1, NOW)
    assert not is_due(NOW - timedelta(days=2), 2, NOW) and is_due(NOW - timedelta(days=3), 2, NOW)
    assert not is_due(NOW - timedelta(days=20), 99, NOW) and is_due(NOW - timedelta(days=21), 99, NOW)  # letzter Kasten
    assert next_streak(2, True) == 3 and next_streak(3, False) == 0


def test_order_wrong_first_then_least_recently_seen_and_skips_not_due():
    cands = [
        _c(1),                                                    # nie wiederholt, kein Fehler
        _c(2, wrong=True),                                        # Fehler in einer Abgabe
        _c(3, reviewed=NOW - timedelta(hours=2), streak=1),       # richtig wiederholt, noch nicht fällig
        _c(4, reviewed=NOW - timedelta(days=4), streak=2),        # fällig, lange nicht gesehen
        _c(5, reviewed=NOW - timedelta(hours=1), streak=0, wrong=True),  # zuletzt falsch, fällig
        _c(6, completed=NOW - timedelta(days=5)),                 # nie wiederholt, älteres Modul
    ]
    order = due_in_order(cands, NOW, random.Random(1))
    assert 3 not in order
    assert set(order[:2]) == {2, 5}          # Fehler zuerst …
    assert order[:2] == [2, 5]               # … davon das am längsten nicht gesehene vorn (Abschluss gestern < vor 1 h)
    assert order[2:] == [6, 4, 1]            # Rest: ältester "gesehen"-Zeitpunkt zuerst


def test_ties_are_shuffled():
    cands = [_c(i) for i in range(20)]
    assert due_in_order(cands, NOW, random.Random(1)) != due_in_order(cands, NOW, random.Random(2))


# --- API ---------------------------------------------------------------------

def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}).json()["access_token"]}


def _join(c, h, name):
    course = c.post("/api/courses", json={"name": f"Rev-{name}", "workshop_key": "network"}, headers=h).json()
    tok = c.post("/api/join", json={"code": course["join_code"], "name": name}).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}, course["id"]


def _solution(key):
    with SessionLocal() as db:
        return {str(q.id): q.answer for q in db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key == key)}


def _wrong(answer):
    return [] if isinstance(answer, list) else answer + 1


def _age_completion(p_headers, c, hours):
    pid = c.get("/api/me", headers=p_headers).json()["participant_id"]
    with SessionLocal() as db:
        db.query(Progress).filter(Progress.participant_id == pid).update(
            {"completed_at": utc_now().replace(tzinfo=None) - timedelta(hours=hours)})
        db.commit()
    return pid


def test_review_flow_spacing_and_no_trace():
    with TestClient(app) as c:
        p, _cid = _join(c, _trainer(c), "Rita")
        assert c.get("/api/review/status", headers=p).json() == {"due": 0, "candidates": 0, "warmup": None}
        solution = _solution("vlan")
        first = next(iter(solution))
        submitted = {**solution, first: _wrong(solution[first])}  # eine falsch, Rest richtig -> bestanden
        assert c.post("/api/modules/vlan/quiz", json={"answers": submitted}, headers=p).json()["passed"]

        # gerade erst bestanden: noch nichts fällig, und prüfen lässt sich nichts
        assert c.get("/api/review", headers=p).json() == {"questions": [], "due": 0}
        assert c.post("/api/review/check", json={"question_id": first, "answer": 0}, headers=p).status_code == 404

        pid = _age_completion(p, c, hours=4)
        me_before = c.get("/api/me", headers=p).json()
        status = c.get("/api/review/status", headers=p).json()
        assert status["due"] == len(solution) == status["candidates"]
        got = c.get("/api/review", headers=p).json()
        assert got["due"] == len(solution)
        assert len(got["questions"]) == min(review.SET_SIZE, len(solution))
        assert got["questions"][0]["id"] == first  # in der Abgabe falsch -> zuerst
        assert all("answer" not in q and "explanation" not in q for q in got["questions"])

        # richtig -> Kasten 1, nicht mehr fällig; "Nochmal" zählt nicht doppelt
        r = c.post("/api/review/check", json={"question_id": first, "answer": solution[first]}, headers=p).json()
        assert r["correct"] is True and "explanation" in r
        c.post("/api/review/check", json={"question_id": first, "answer": solution[first]}, headers=p)
        second = [q for q in solution if q != first][0]
        assert c.post("/api/review/check", json={"question_id": second, "answer": _wrong(solution[second])},
                      headers=p).json()["correct"] is False
        with SessionLocal() as db:
            streaks = {r.question_id: r.streak for r in db.query(ReviewItem).filter(ReviewItem.participant_id == pid)}
        assert streaks == {int(first): 1, int(second): 0}
        assert c.get("/api/review/status", headers=p).json()["due"] == len(solution) - 2  # second: erst in 10 min

        # Wiederholung schreibt nichts in Fortschritt/Quiz
        assert c.get("/api/me", headers=p).json() == me_before
        with SessionLocal() as db:
            assert db.query(QuizResult).filter(QuizResult.participant_id == pid).count() == 1


def test_review_ignores_disabled_modules_other_courses_and_deleted_questions():
    with TestClient(app) as c:
        h = _trainer(c)
        p, cid = _join(c, h, "Otto")
        other, _ = _join(c, h, "Olga")
        solution = _solution("vlan")
        c.post("/api/modules/vlan/quiz", json={"answers": solution}, headers=p)
        _age_completion(p, c, hours=30)
        qid = next(iter(solution))
        # fremder Kurs: Frage unbekannt
        assert c.post("/api/review/check", json={"question_id": qid, "answer": 0}, headers=other).status_code == 404
        assert c.post("/api/review/check", json={"question_id": "²", "answer": 0}, headers=p).status_code == 404
        # Verlauf zu einer Frage, die es nicht (mehr) gibt, stört nicht
        pid = c.get("/api/me", headers=p).json()["participant_id"]
        with SessionLocal() as db:
            db.add(ReviewItem(participant_id=pid, question_id=999_999, last_reviewed=datetime(2020, 1, 1), streak=0))
            db.commit()
        assert c.get("/api/review/status", headers=p).json()["due"] == len(solution)
        # Modul abgewählt -> keine Wiederholung daraus
        c.put(f"/api/courses/{cid}/modules", json={"module_key": "vlan", "active": False}, headers=h)
        assert c.get("/api/review/status", headers=p).json()["due"] == 0
        assert c.get("/api/review/status", headers=h).status_code == 403  # Trainer-Token ist kein Teilnehmer


def test_warmup_counts_participation_and_average():
    with TestClient(app) as c:
        h = _trainer(c)
        p, cid = _join(c, h, "Wanda")
        solution = _solution("vlan")
        c.post("/api/modules/vlan/quiz", json={"answers": solution}, headers=p)
        _age_completion(p, c, hours=20)
        assert c.get(f"/api/trainer/courses/{cid}/warmup", headers=h).json() is None
        assert c.post(f"/api/trainer/courses/{cid}/warmup", headers=p).status_code == 403
        started = c.post(f"/api/trainer/courses/{cid}/warmup", headers=h).json()
        assert started["active"] and started["participants"] == 0 and started["average"] is None
        assert c.get("/api/review/status", headers=p).json()["warmup"] == {"id": started["id"], "answered": 0}

        a, b = list(solution)[:2]
        c.post("/api/review/check", json={"question_id": a, "answer": solution[a]}, headers=p)
        c.post("/api/review/check", json={"question_id": b, "answer": _wrong(solution[b])}, headers=p)
        view = c.get(f"/api/trainer/courses/{cid}/warmup", headers=h).json()
        assert view["participants"] == 1 and view["average"] == 50 and "Wanda" not in str(view)
        assert c.get("/api/review/status", headers=p).json()["warmup"]["answered"] == 2

        ended = c.delete(f"/api/trainer/courses/{cid}/warmup", headers=h).json()
        assert not ended["active"] and ended["participants"] == 1
        assert c.get("/api/review/status", headers=p).json()["warmup"] is None
        assert c.get("/api/trainer/courses/999999/warmup", headers=h).status_code == 404
