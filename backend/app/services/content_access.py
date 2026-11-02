"""Wer darf welchen Workshop sehen/bearbeiten. Gilt für REST-Editor und MCP gleichermaßen.

Mitgelieferte Workshops (owner_trainer_id NULL) gehören den Admins; Entwürfe sieht
nur, wer sie bearbeiten darf (Besitzer oder Admin)."""
from sqlalchemy.orm import Session

from app.content.workshops import WORKSHOPS
from app.models.workshop import Workshop
from app.services.content_editor import EditorError


def can_edit_workshop(trainer: dict, ws: Workshop) -> bool:
    if trainer.get("is_admin"):
        return True
    return ws.owner_trainer_id is not None and ws.owner_trainer_id == trainer.get("trainer_id")


def can_see_workshop(trainer: dict | None, ws: Workshop) -> bool:
    if ws.status == "published":
        return True
    return trainer is not None and can_edit_workshop(trainer, ws)


def visible_workshop_keys(db: Session, trainer: dict | None) -> set[str]:
    return {ws.key for ws in db.query(Workshop) if can_see_workshop(trainer, ws)}


def require_edit(db: Session, trainer: dict, workshop_key: str) -> Workshop:
    ws = db.get(Workshop, workshop_key)
    if ws is None:
        raise EditorError(404, f"Workshop/Modul ‚{workshop_key}‘ existiert nicht.")
    if not can_edit_workshop(trainer, ws):
        raise EditorError(403, f"Lehrgang ‚{workshop_key}‘ gehört einem anderen Trainer.")
    return ws


def is_code_workshop(key: str) -> bool:
    return key in WORKSHOPS
