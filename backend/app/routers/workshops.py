from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.content import ContentModule
from app.models.workshop import Workshop


router = APIRouter(prefix="/workshops", tags=["workshops"])


def _card(workshop: Workshop) -> dict:
    return {
        "key": workshop.key,
        "title": {"de": workshop.title_de, "en": workshop.title_en},
        "summary": {"de": workshop.summary_de, "en": workshop.summary_en},
        "theme": workshop.theme,
        "sections": workshop.sections,
        "context": workshop.context,
    }


@router.get("")
def list_workshops(db: Session = Depends(get_db)):
    return [_card(workshop) for workshop in db.query(Workshop).order_by(Workshop.key).all()]


@router.get("/{key}")
def get_workshop(key: str, db: Session = Depends(get_db)):
    workshop = db.get(Workshop, key)
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop nicht gefunden")
    card = _card(workshop)
    card["modules"] = [
        {"key": module.key, "title": {"de": module.title_de, "en": module.title_en}, "order": module.order}
        for module in db.query(ContentModule).filter(ContentModule.workshop_key == key)
        .order_by(ContentModule.order).all()
    ]
    return card
