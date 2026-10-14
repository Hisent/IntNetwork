"""Wiederholung (spaced review) und Aufwärmrunde.

Teilnehmer: GET /review/status (fällige Zahl + laufende Aufwärmrunde; wird
gepollt wie die Live-Abstimmung), GET /review (der Satz), POST /review/check
(bewertet serverseitig wie /practice/check, schreibt aber den Leitner-Verlauf
review_item). Auswahlregeln: services/review.py. Nichts davon berührt
Progress, QuizResult oder die Teilnahmebestätigung.

Trainer: /trainer/courses/{cid}/warmup starten, ansehen (Teilnahme +
Durchschnitt, keine Einzelliste), beenden.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.content import ContentQuizQuestion
from app.models.course import Course
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.models.review import ReviewItem, Warmup, WarmupResult
from app.routers.learning import PracticeCheck, as_graded, explanation, public_questions, question_by_id
from app.services import grading, review
from app.services.audit import log_action
from app.services.course_membership import active_module_keys
from app.services.deps import get_participant, get_trainer
from app.services.ratelimit import rate_limit
from app.utils import iso_utc, utc_now

router = APIRouter(tags=["review"])


def _now():
    # Spalten sind zeitzonenlos und enthalten UTC (siehe database.py).
    return utc_now().replace(tzinfo=None)


def _candidates(db: Session, p: Participant, now) -> dict[int, tuple[review.Candidate, ContentQuizQuestion]]:
    """Kandidaten nach Regel 1 samt Verlauf und Fehlern aus allen Abgaben. Fragen,
    die es im Inhalt nicht mehr gibt, tauchen hier gar nicht erst auf."""
    active = active_module_keys(db, p.course_id)
    completed = {key: at for key, at in db.query(Progress.module_key, Progress.completed_at).filter(
        Progress.participant_id == p.id, Progress.done.is_(True))
        if key in active and at is not None and now - at >= review.MIN_AGE}
    if not completed:
        return {}
    questions = {q.id: q for q in db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key.in_(completed))}
    wrong: set[int] = set()
    for answers, in db.query(QuizResult.answers).filter(
            QuizResult.participant_id == p.id, QuizResult.module_key.in_(completed)):
        for qid, answer in (answers or {}).items():
            q = questions.get(int(qid)) if str(qid).isdigit() else None
            if q and not grading._correct(as_graded(q), answer):
                wrong.add(q.id)
    history = {r.question_id: r for r in db.query(ReviewItem).filter(
        ReviewItem.participant_id == p.id, ReviewItem.question_id.in_(questions))}
    out = {}
    for qid, q in questions.items():
        h = history.get(qid)
        out[qid] = (review.Candidate(qid=qid, completed_at=completed[q.module_key],
                                     last_reviewed=h.last_reviewed if h else None, streak=h.streak if h else 0,
                                     wrong=qid in wrong or (h is not None and h.streak == 0)), q)
    return out


def _active_warmup(db: Session, course_id: int, now) -> Warmup | None:
    w = db.query(Warmup).filter(Warmup.course_id == course_id).order_by(Warmup.id.desc()).first()
    return w if w and w.ended_at is None and now - w.started_at < review.WARMUP_MAX_AGE else None


# BEWUSST ohne Rate-Limit (wie die Live-Abstimmung): rein lesend, je Teilnehmer
# alle 15 s von Lernseite/Modul. ponytail: rechnet die Fälligkeit jedes Mal neu
# (eine Handvoll Abfragen über ~20 Module); Zähler cachen, falls das je bremst.
@router.get("/review/status")
def review_status(db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    now = _now()
    cands = [c for c, _q in _candidates(db, p, now).values()]
    w = _active_warmup(db, p.course_id, now)
    mine = w and db.query(WarmupResult.answered).filter(
        WarmupResult.warmup_id == w.id, WarmupResult.participant_id == p.id).scalar()
    return {"due": sum(review.is_due(c.last_reviewed, c.streak, now) for c in cands),
            "candidates": len(cands),
            "warmup": {"id": w.id, "answered": mine or 0} if w else None}


@router.get("/review", dependencies=[Depends(rate_limit(60, 60))])
def review_set(db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    """Bis zu SET_SIZE fällige Fragen OHNE Lösung/Erklärung (Regeln: services/review.py)."""
    now = _now()
    cands = _candidates(db, p, now)
    order = review.due_in_order([c for c, _q in cands.values()], now)
    return {"questions": public_questions(db, [cands[qid][1] for qid in order[:review.SET_SIZE]], p.language),
            "due": len(order)}


@router.post("/review/check", dependencies=[Depends(rate_limit(240, 60))])
def review_check(data: PracticeCheck, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    """Bewertet EINE Frage. War sie fällig, rückt der Leitner-Kasten vor (bzw.
    zurück auf 0) und — während einer Aufwärmrunde — zählt sie dort mit."""
    now = _now()
    q = question_by_id(db, data.question_id)
    cand = _candidates(db, p, now).get(q.id) if q else None
    if cand is None:
        raise HTTPException(status_code=404, detail="Frage nicht gefunden")
    c = cand[0]
    correct = grading._correct(as_graded(q), data.answer)
    if review.is_due(c.last_reviewed, c.streak, now):
        values = {"last_reviewed": now, "streak": review.next_streak(c.streak, correct)}
        row = db.query(ReviewItem).filter(ReviewItem.participant_id == p.id, ReviewItem.question_id == q.id)
        if not row.update(values, synchronize_session=False):
            db.add(ReviewItem(participant_id=p.id, question_id=q.id, **values))
        if w := _active_warmup(db, p.course_id, now):
            res = db.query(WarmupResult).filter(WarmupResult.warmup_id == w.id, WarmupResult.participant_id == p.id)
            if not res.update({"answered": WarmupResult.answered + 1, "correct": WarmupResult.correct + int(correct)},
                              synchronize_session=False):
                db.add(WarmupResult(warmup_id=w.id, participant_id=p.id, answered=1, correct=int(correct)))
        try:
            db.commit()
        except IntegrityError:  # Doppelklick: die Parallel-Anfrage hat gerade angelegt -> deren Wertung gilt
            db.rollback()
    return {"correct": correct, "explanation": explanation(q, p.language)}


def _course(db: Session, cid: int) -> None:
    if not db.get(Course, cid):
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")


def _warmup_view(db: Session, cid: int) -> dict | None:
    """Letzte Aufwärmrunde des Kurses: Teilnahme und Durchschnitt (Mittel der
    Quoten je Teilnehmer, in Prozent) — keine Namen."""
    w = db.query(Warmup).filter(Warmup.course_id == cid).order_by(Warmup.id.desc()).first()
    if not w:
        return None
    n, avg = db.query(func.count(), func.avg(1.0 * WarmupResult.correct / WarmupResult.answered)).filter(
        WarmupResult.warmup_id == w.id, WarmupResult.answered > 0).one()
    return {"id": w.id, "started_at": iso_utc(w.started_at), "active": _active_warmup(db, cid, _now()) is not None,
            "participants": n, "average": round(avg * 100) if avg is not None else None}


@router.get("/trainer/courses/{cid}/warmup")
def get_warmup(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    _course(db, cid)
    return _warmup_view(db, cid)


@router.post("/trainer/courses/{cid}/warmup")
def start_warmup(cid: int, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    """Startet eine neue Runde (eine laufende endet damit)."""
    _course(db, cid)
    now = _now()
    db.query(Warmup).filter(Warmup.course_id == cid, Warmup.ended_at.is_(None)).update(
        {"ended_at": now}, synchronize_session=False)
    db.add(Warmup(course_id=cid, started_at=now))
    db.commit()
    log_action(db, trainer, "warmup.start", target=f"course:{cid}")
    return _warmup_view(db, cid)


@router.delete("/trainer/courses/{cid}/warmup")
def end_warmup(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    _course(db, cid)
    db.query(Warmup).filter(Warmup.course_id == cid, Warmup.ended_at.is_(None)).update(
        {"ended_at": _now()}, synchronize_session=False)
    db.commit()
    return _warmup_view(db, cid)
