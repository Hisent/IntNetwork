from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.course import Course
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.models.course_module import CourseModule
from app.models.workshop import Workshop
from app.models.certificate import Certificate
from app.models.comment import Comment
from app.services.codes import new_code
from app.services.deps import get_trainer
from app.services.course_membership import active_module_keys
from app.content.registry import module_meta
from app.models.content import ContentModule
from app.utils import generate_resume_code

router = APIRouter(prefix="/courses", tags=["courses"])


class CourseCreate(BaseModel):
    name: str
    workshop_key: str = "network"


@router.post("")
def create_course(data: CourseCreate, db: Session = Depends(get_db), _=Depends(get_trainer)):
    if not data.name.strip():
        raise HTTPException(status_code=422, detail="Name fehlt")
    workshop = db.get(Workshop, data.workshop_key)
    if not workshop:
        raise HTTPException(status_code=422, detail="Unbekannter Workshop")
    c = Course(name=data.name.strip(), join_code=new_code(db), workshop_key=workshop.key)
    db.add(c)
    db.flush()
    for module in db.query(ContentModule).filter(ContentModule.workshop_key == workshop.key):
        db.add(CourseModule(course_id=c.id, module_key=module.key))
    db.commit()
    db.refresh(c)
    return {"id": c.id, "name": c.name, "join_code": c.join_code, "workshop_key": c.workshop_key}


@router.get("")
def list_courses(db: Session = Depends(get_db), _=Depends(get_trainer)):
    counts = dict(db.query(Participant.course_id, func.count(Participant.id))
                  .group_by(Participant.course_id).all())
    return [{"id": c.id, "name": c.name, "join_code": c.join_code, "workshop_key": c.workshop_key,
             "participant_count": counts.get(c.id, 0), "require_approval": c.require_approval}
            for c in db.query(Course).order_by(Course.created_at.desc()).all()]


class ApprovalToggle(BaseModel):
    require_approval: bool


@router.patch("/{course_id}/approval")
def set_course_approval(course_id: int, data: ApprovalToggle,
                        db: Session = Depends(get_db), _=Depends(get_trainer)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")
    course.require_approval = data.require_approval
    db.commit()
    return {"require_approval": course.require_approval}


class ParticipantApproval(BaseModel):
    approved: bool


@router.post("/{course_id}/participants/{participant_id}/approve")
def approve_participant(course_id: int, participant_id: int, data: ParticipantApproval,
                        db: Session = Depends(get_db), _=Depends(get_trainer)):
    p = db.query(Participant).filter(
        Participant.id == participant_id, Participant.course_id == course_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Teilnehmer nicht gefunden")
    p.approved = data.approved
    db.commit()
    return {"id": p.id, "approved": p.approved}


@router.post("/{course_id}/participants/{participant_id}/reset-code")
def reset_resume_code(course_id: int, participant_id: int,
                      db: Session = Depends(get_db), _=Depends(get_trainer)):
    """Vergibt einen neuen Wiederaufnahme-Code — für Teilnehmer, die ihren verloren
    haben. Der alte wird ungültig; der Trainer gibt den neuen persönlich weiter."""
    p = db.query(Participant).filter(
        Participant.id == participant_id, Participant.course_id == course_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Teilnehmer nicht gefunden")
    p.resume_code = generate_resume_code()
    db.commit()
    return {"id": p.id, "resume_code": p.resume_code}


@router.delete("/{course_id}/participants/{participant_id}")
def delete_participant(course_id: int, participant_id: int,
                       db: Session = Depends(get_db), _=Depends(get_trainer)):
    """Entfernt einen Teilnehmer samt aller personenbezogenen Daten (Fortschritt,
    Quiz-Ergebnisse, Kommentare, Bestätigung) — für Abmeldungen/DSGVO-Löschungen."""
    p = db.query(Participant).filter(
        Participant.id == participant_id, Participant.course_id == course_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Teilnehmer nicht gefunden")
    db.query(Progress).filter(Progress.participant_id == participant_id).delete()
    db.query(QuizResult).filter(QuizResult.participant_id == participant_id).delete()
    db.query(Comment).filter(Comment.participant_id == participant_id).delete()
    db.query(Certificate).filter(Certificate.participant_id == participant_id).delete()
    db.delete(p)
    db.commit()
    return {"ok": True}


@router.get("/{course_id}/dashboard")
def dashboard(course_id: int, db: Session = Depends(get_db), _=Depends(get_trainer)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")
    active_keys = active_module_keys(db, course_id)
    metas = [m for m in module_meta(db) if m["key"] in active_keys]
    participants = db.query(Participant).filter(Participant.course_id == course_id).all()
    # 3 Queries gesamt statt 2 pro Teilnehmer x Modul (vorher ~900 bei 30 x 15)
    pids = [p.id for p in participants]
    done_pairs = {(r.participant_id, r.module_key) for r in db.query(Progress).filter(
        Progress.participant_id.in_(pids), Progress.done).all()}
    best_map = {(pid, key): pct for pid, key, pct in db.query(
        QuizResult.participant_id, QuizResult.module_key,
        func.max(QuizResult.score * 1.0 / QuizResult.total)
    ).filter(QuizResult.participant_id.in_(pids), QuizResult.total > 0)
     .group_by(QuizResult.participant_id, QuizResult.module_key).all()}
    rows = []
    for p in participants:
        cells = {}
        for m in metas:
            pct = best_map.get((p.id, m["key"]))
            cells[m["key"]] = {"done": (p.id, m["key"]) in done_pairs,
                               "best": round(pct * 100) if pct is not None else None}
        rows.append({"id": p.id, "name": p.name, "approved": p.approved, "cells": cells})
    return {"course": {"id": course.id, "name": course.name, "join_code": course.join_code,
                       "workshop_key": course.workshop_key, "require_approval": course.require_approval},
            "modules": metas, "participants": rows}


@router.get("/{course_id}/modules")
def course_modules(course_id: int, db: Session = Depends(get_db), _=Depends(get_trainer)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")
    active_keys = active_module_keys(db, course_id)
    allowed_workshop = course.workshop_key
    return [{"key": m["key"], "title": m["title"], "order": m["order"],
             "workshop_key": m["workshop_key"], "active": m["key"] in active_keys}
            for m in module_meta(db)
            if allowed_workshop is None or m["workshop_key"] == allowed_workshop]


class ModuleToggle(BaseModel):
    module_key: str
    active: bool


@router.put("/{course_id}/modules")
def set_course_module(course_id: int, data: ModuleToggle,
                      db: Session = Depends(get_db), _=Depends(get_trainer)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")
    module = db.query(ContentModule).filter(ContentModule.key == data.module_key).first()
    if not module:
        raise HTTPException(status_code=422, detail="Unbekanntes Modul")
    if course.workshop_key and module.workshop_key != course.workshop_key:
        raise HTTPException(status_code=422, detail="Modul gehört zu einem anderen Workshop")
    row = db.query(CourseModule).filter(
        CourseModule.course_id == course_id,
        CourseModule.module_key == data.module_key).first()
    if data.active:
        if not row:
            db.add(CourseModule(course_id=course_id, module_key=data.module_key))
    else:
        if row:
            db.delete(row)
    db.commit()
    return {"ok": True}
