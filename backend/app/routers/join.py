from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.course import Course
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.services.deps import get_participant
from app.services.security import create_token
from app.content.registry import module_meta, _resolve
from app.content.company import COMPANY

router = APIRouter(tags=["join"])


class JoinReq(BaseModel):
    code: str
    name: str


@router.post("/join")
def join(data: JoinReq, db: Session = Depends(get_db)):
    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Name fehlt")
    course = db.query(Course).filter(Course.join_code == data.code.strip().upper()).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs-Code ungültig")
    p = db.query(Participant).filter(
        Participant.course_id == course.id, Participant.name == name).first()
    if not p:
        p = Participant(course_id=course.id, name=name)
        db.add(p)
        try:
            db.commit()
        except IntegrityError:
            # Zwei gleichzeitige Joins mit demselben Namen (z.B. Doppelklick) ->
            # der andere Request hat die Zeile zwischen SELECT und COMMIT angelegt.
            db.rollback()
            p = db.query(Participant).filter(
                Participant.course_id == course.id, Participant.name == name).first()
        else:
            db.refresh(p)
    token = create_token(sub=name, role="participant",
                         extra={"participant_id": p.id, "course_id": course.id})
    return {"access_token": token, "course_name": course.name, "name": name}


@router.get("/me")
def me(db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    progress = []
    for m in module_meta(db):
        prog = db.query(Progress).filter(
            Progress.participant_id == p.id, Progress.module_key == m["key"]).first()
        best = db.query(QuizResult).filter(
            QuizResult.participant_id == p.id, QuizResult.module_key == m["key"]).all()
        best_pct = max((r.score / r.total for r in best if r.total), default=None)
        progress.append({"module_key": m["key"], "done": bool(prog and prog.done),
                         "best": round(best_pct * 100) if best_pct is not None else None})
    return {"name": p.name, "course_id": p.course_id, "language": p.language, "progress": progress}


class LanguageReq(BaseModel):
    language: str


@router.patch("/me/language")
def set_language(data: LanguageReq, db: Session = Depends(get_db),
                 p: Participant = Depends(get_participant)):
    if data.language not in ("de", "en"):
        raise HTTPException(status_code=422, detail="Sprache muss 'de' oder 'en' sein")
    p.language = data.language
    db.commit()
    return {"language": p.language}


@router.get("/company")
def company(p: Participant = Depends(get_participant)):
    return {
        "name": COMPANY["name"],
        "blurb": _resolve(COMPANY["blurb"], p.language),
        "sites": COMPANY["sites"],
        "devices": _resolve(COMPANY["devices"], p.language),
    }
