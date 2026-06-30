from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.course import Course
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.models.module_disabled import ModuleDisabled
from app.services.codes import new_code
from app.services.deps import get_trainer
from app.services.activation import disabled_keys
from app.content.registry import MODULES, module_meta

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


@router.get("/{course_id}/modules")
def course_modules(course_id: int, db: Session = Depends(get_db), _=Depends(get_trainer)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")
    off = disabled_keys(db, course_id)
    return [{"key": m["key"], "title": m["title"], "order": m["order"],
             "active": m["key"] not in off} for m in module_meta()]


class ModuleToggle(BaseModel):
    module_key: str
    active: bool


@router.put("/{course_id}/modules")
def set_course_module(course_id: int, data: ModuleToggle,
                      db: Session = Depends(get_db), _=Depends(get_trainer)):
    if not db.query(Course).filter(Course.id == course_id).first():
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")
    if data.module_key not in MODULES:
        raise HTTPException(status_code=422, detail="Unbekanntes Modul")
    row = db.query(ModuleDisabled).filter(
        ModuleDisabled.course_id == course_id,
        ModuleDisabled.module_key == data.module_key).first()
    if data.active:
        if row:
            db.delete(row)
    else:
        if not row:
            db.add(ModuleDisabled(course_id=course_id, module_key=data.module_key))
    db.commit()
    return {"ok": True}
