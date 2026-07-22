from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.services.deps import get_participant
from app.services import grading
from app.services.course_membership import active_module_keys
from app.services.ratelimit import rate_limit
from app.content.registry import module_meta, public_module, trainer_module
from app.utils import utc_now

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("")
def list_modules(db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    active = active_module_keys(db, p.course_id)
    return [m for m in module_meta(db) if m["key"] in active]


@router.get("/{key}")
def get_module(key: str, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    if key not in active_module_keys(db, p.course_id):
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    pub = public_module(db, key, p.language)
    if not pub:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    return pub


class QuizSubmit(BaseModel):
    answers: dict


# Ein NAT-Klassenraum (bis ~20 Teilnehmer) teilt sich eine WAN-IP. Beim gemeinsamen
# Quiz-Ende klicken viele fast gleichzeitig ab, manche mehrfach (Doppelklick) ->
# 20 * 3 = 60 gibt der ganzen Gruppe genug Puffer und bremst nur Skript-Spam.
@router.post("/{key}/quiz", dependencies=[Depends(rate_limit(60, 60))])
def submit_quiz(key: str, data: QuizSubmit, db: Session = Depends(get_db),
                p: Participant = Depends(get_participant)):
    if key not in active_module_keys(db, p.course_id):
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    module = trainer_module(db, key)
    if not module:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    score, total = grading.grade(module["quiz"], data.answers)
    is_passed = grading.passed(score, total)

    db.add(QuizResult(participant_id=p.id, module_key=key, score=score,
                      total=total, answers=data.answers))

    prog = db.query(Progress).filter(
        Progress.participant_id == p.id, Progress.module_key == key).first()
    if not prog:
        prog = Progress(participant_id=p.id, module_key=key, done=False)
        db.add(prog)
    if is_passed and not prog.done:
        prog.done = True
        prog.completed_at = utc_now()
    try:
        db.commit()
    except IntegrityError:
        # Doppelsubmit (z.B. Doppelklick) -> die andere Anfrage hat die
        # Progress-Zeile zwischen SELECT und COMMIT angelegt. Rollback nimmt
        # auch den QuizResult-Insert zurück, also beides neu anlegen.
        db.rollback()
        db.add(QuizResult(participant_id=p.id, module_key=key, score=score,
                          total=total, answers=data.answers))
        prog = db.query(Progress).filter(
            Progress.participant_id == p.id, Progress.module_key == key).first()
        if is_passed and not prog.done:
            prog.done = True
            prog.completed_at = utc_now()
        db.commit()

    results = db.query(QuizResult).filter(
        QuizResult.participant_id == p.id, QuizResult.module_key == key).all()
    best_pct = max((r.score / r.total for r in results if r.total), default=0)
    return {"score": score, "total": total, "passed": is_passed, "best": round(best_pct * 100),
            "details": grading.question_results(module["quiz"], data.answers)}


@router.post("/{key}/heartbeat")
def heartbeat(key: str, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    # sonst landet jeder beliebige URL-String als current_module_key in der DB
    # und die Presence-Ansicht zeigt Rohtext an
    #
    # BEWUSST ohne Rate-Limit: heartbeat feuert alle 20s je Teilnehmer und ist ein
    # reines UPDATE auf einer bestehenden Zeile, kein Schreib-Missbrauchsrisiko wie
    # bei Kommentaren/Quiz. Hinter NAT wäre ein Limit hier zuerst die eigene
    # Klassenraum-Gruppe treffen, nicht Angreifer.
    if key not in active_module_keys(db, p.course_id):
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    p.current_module_key = key
    p.last_seen = utc_now()
    db.commit()
    return {"ok": True}
