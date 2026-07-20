from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.content.links import LINKS_BY_WORKSHOP
from app.database import get_db
from app.models.course import Course
from app.models.participant import Participant
from app.services.deps import get_participant

router = APIRouter(tags=["links"])


@router.get("/links")
def links(db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    """Kuratierte Vertiefungslinks des jeweiligen Workshops — bilingual, Client wählt die Sprache."""
    course = db.get(Course, p.course_id)
    key = course.workshop_key if course else None
    return LINKS_BY_WORKSHOP.get(key, [])
