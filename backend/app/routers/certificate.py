from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.certificate import Certificate
from app.models.course import Course
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.workshop import Workshop
from app.services.course_membership import active_module_keys
from app.services.deps import get_participant
from app.utils import generate_certificate_id

router = APIRouter(tags=["certificate"])


def _out(cert: Certificate) -> dict:
    return {
        "id": cert.id,
        "participant_name": cert.participant_name,
        "course_name": cert.course_name,
        "workshop_title": cert.workshop_title,
        "module_count": cert.module_count,
        "issued_at": cert.issued_at.isoformat(),
    }


@router.post("/certificate")
def issue_certificate(db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    """Stellt die Teilnahmebestätigung aus — nur wenn alle aktiven Module bestanden
    sind. Idempotent: je Teilnehmer genau eine, weitere Aufrufe liefern dieselbe."""
    existing = db.query(Certificate).filter(Certificate.participant_id == p.id).first()
    if existing:
        return _out(existing)

    active = active_module_keys(db, p.course_id)
    done = {r.module_key for r in db.query(Progress).filter(
        Progress.participant_id == p.id, Progress.done).all()}
    if not active or not active.issubset(done):
        raise HTTPException(status_code=403, detail="Es sind noch nicht alle Module abgeschlossen.")

    course = db.get(Course, p.course_id)
    if course and course.require_approval and not p.approved:
        # Eigener Statuscode 409, damit das Frontend „wartet auf Freigabe" von
        # „noch nicht alle Module" (403) unterscheiden kann.
        raise HTTPException(status_code=409, detail="Die Teilnahmebestätigung wartet auf die Trainerfreigabe.")
    workshop = db.get(Workshop, course.workshop_key) if course and course.workshop_key else None
    cert = Certificate(
        id=generate_certificate_id(), participant_id=p.id, course_id=p.course_id,
        participant_name=p.name, course_name=course.name if course else "",
        workshop_title=workshop.title_de if workshop else (course.name if course else ""),
        module_count=len(active))
    db.add(cert)
    try:
        db.commit()
    except IntegrityError:
        # Doppelter Klick auf „Bestätigung anzeigen" -> der andere Request hat die
        # (unique participant_id) Zeile schon angelegt.
        db.rollback()
        cert = db.query(Certificate).filter(Certificate.participant_id == p.id).first()
    else:
        db.refresh(cert)
    return _out(cert)


@router.get("/verify/{cert_id}")
def verify_certificate(cert_id: str, db: Session = Depends(get_db)):
    """Öffentliche Prüfung — kein Login. Liefert den gespeicherten Snapshot."""
    cert = db.get(Certificate, cert_id.strip())
    if not cert:
        raise HTTPException(status_code=404, detail="Kein Zertifikat mit dieser ID gefunden.")
    return _out(cert)
