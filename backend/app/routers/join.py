from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.course import Course
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.models.workshop import Workshop
from app.services.deps import get_participant
from app.services.security import create_token
from app.content.registry import module_meta, _resolve
from app.content.company import COMPANY
from app.services.course_membership import active_module_keys

router = APIRouter(tags=["join"])


class JoinReq(BaseModel):
    code: str
    name: str
    workshop_key: str | None = None


@router.post("/join")
def join(data: JoinReq, db: Session = Depends(get_db)):
    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Name fehlt")
    course = db.query(Course).filter(Course.join_code == data.code.strip().upper()).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs-Code ungültig")
    if data.workshop_key and course.workshop_key != data.workshop_key:
        raise HTTPException(status_code=404, detail="Kurs-Code passt nicht zu diesem Workshop")
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
    # 2 Aggregat-Queries statt 2 Queries pro Modul (vorher N+1 bei 15 Modulen)
    done_keys = {r.module_key for r in db.query(Progress).filter(
        Progress.participant_id == p.id, Progress.done).all()}
    best_map = dict(db.query(
        QuizResult.module_key, func.max(QuizResult.score * 1.0 / QuizResult.total)
    ).filter(QuizResult.participant_id == p.id, QuizResult.total > 0)
     .group_by(QuizResult.module_key).all())
    active = active_module_keys(db, p.course_id)
    progress = [{"module_key": m["key"], "done": m["key"] in done_keys,
                 "best": round(best_map[m["key"]] * 100) if m["key"] in best_map else None}
                for m in module_meta(db) if m["key"] in active]
    course = db.get(Course, p.course_id)
    workshop = db.get(Workshop, course.workshop_key) if course and course.workshop_key else None
    workshop_data = None if not workshop else {
        "key": workshop.key,
        "title": {"de": workshop.title_de, "en": workshop.title_en},
        "summary": {"de": workshop.summary_de, "en": workshop.summary_en},
        "theme": workshop.theme,
        "sections": workshop.sections,
        "context": workshop.context,
    }
    return {"name": p.name, "course_id": p.course_id, "language": p.language,
            "course": {"id": course.id, "name": course.name}, "workshop": workshop_data,
            "progress": progress}


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
def company(db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    course = db.get(Course, p.course_id)
    if not course or course.workshop_key != "network":
        raise HTTPException(status_code=404, detail="Kein Unternehmenskontext für diesen Workshop")
    return {
        "name": COMPANY["name"],
        "blurb": _resolve(COMPANY["blurb"], p.language),
        "sites": COMPANY["sites"],
        "devices": _resolve(COMPANY["devices"], p.language),
    }
