from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trainer import Trainer
from app.models.workshop import Workshop
from app.routers.workshops import _card
from app.services.audit import log_action
from app.services.content_access import can_edit_workshop, can_see_workshop
from app.services.content_editor import EditorError
from app.services.deps import get_admin, get_trainer
from app.services.workshop_editor import publish_workshop

router = APIRouter(prefix="/trainer/workshops", tags=["trainer-workshops"])


def _trainer_card(ws: Workshop, trainer: dict, names: dict[int, str]) -> dict:
    return {**_card(ws), "status": ws.status,
            "owner_name": names.get(ws.owner_trainer_id) if ws.owner_trainer_id else None,
            "editable": can_edit_workshop(trainer, ws)}


@router.get("")
def list_workshops(db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    names = dict(db.query(Trainer.id, Trainer.name).all())
    return [_trainer_card(ws, trainer, names) for ws in db.query(Workshop).order_by(Workshop.key)
            if can_see_workshop(trainer, ws)]


@router.post("/{key}/publish")
def publish(key: str, db: Session = Depends(get_db), admin: dict = Depends(get_admin)):
    try:
        ws = publish_workshop(db, key)
    except EditorError as e:
        raise HTTPException(status_code=e.status, detail=e.message) from None
    log_action(db, admin, "workshop.publish", target=f"workshop:{key}")
    return _trainer_card(ws, admin, dict(db.query(Trainer.id, Trainer.name).all()))
