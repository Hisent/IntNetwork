from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.course import Course
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.services.codes import new_code
from app.services.deps import get_trainer
from app.content.registry import module_meta

router = APIRouter(prefix="/courses", tags=["courses"])


class CourseCreate(BaseModel):
    name: str


@router.post("")
def create_course(data: CourseCreate, db: Session = Depends(get_db), _=Depends(get_trainer)):
    if not data.name.strip():
        raise HTTPException(status_code=422, detail="Name fehlt")
    c = Course(name=data.name.strip(), join_code=new_code(db))
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "name": c.name, "join_code": c.join_code}


@router.get("")
def list_courses(db: Session = Depends(get_db), _=Depends(get_trainer)):
    return [{"id": c.id, "name": c.name, "join_code": c.join_code}
            for c in db.query(Course).order_by(Course.created_at.desc()).all()]


@router.get("/{course_id}/dashboard")
def dashboard(course_id: int, db: Session = Depends(get_db), _=Depends(get_trainer)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")
    metas = module_meta()
    participants = db.query(Participant).filter(Participant.course_id == course_id).all()
    rows = []
    for p in participants:
        cells = {}
        for m in metas:
            prog = db.query(Progress).filter(
                Progress.participant_id == p.id, Progress.module_key == m["key"]).first()
            best = db.query(QuizResult).filter(
                QuizResult.participant_id == p.id, QuizResult.module_key == m["key"]).all()
            best_pct = max((r.score / r.total for r in best if r.total), default=None)
            cells[m["key"]] = {"done": bool(prog and prog.done),
                               "best": round(best_pct * 100) if best_pct is not None else None}
        rows.append({"name": p.name, "cells": cells})
    return {"course": {"id": course.id, "name": course.name, "join_code": course.join_code},
            "modules": metas, "participants": rows}
