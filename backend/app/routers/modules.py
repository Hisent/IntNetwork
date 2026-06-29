from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.services.deps import get_participant
from app.services import grading
from app.content.registry import MODULES, module_meta, public_module
from app.utils import utc_now

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("")
def list_modules(_: Participant = Depends(get_participant)):
    return module_meta()


@router.get("/{key}")
def get_module(key: str, _: Participant = Depends(get_participant)):
    pub = public_module(key)
    if not pub:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    return pub


class QuizSubmit(BaseModel):
    answers: dict


@router.post("/{key}/quiz")
def submit_quiz(key: str, data: QuizSubmit, db: Session = Depends(get_db),
                p: Participant = Depends(get_participant)):
    module = MODULES.get(key)
    if not module:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    score, total = grading.grade(module["quiz"], data.answers)
    is_passed = grading.passed(score, total, module["pass_threshold"])

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
    db.commit()

    results = db.query(QuizResult).filter(
        QuizResult.participant_id == p.id, QuizResult.module_key == key).all()
    best_pct = max((r.score / r.total for r in results if r.total), default=0)
    return {"score": score, "total": total, "passed": is_passed, "best": round(best_pct * 100)}
