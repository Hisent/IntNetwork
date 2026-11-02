from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.content.registry import MODULES
from app.database import get_db
from app.models.content import ContentModule, ContentModuleSnapshot
from app.models.workshop import Workshop
from app.services import content_editor as ed
from app.services.audit import log_action
from app.services.content_access import can_edit_workshop, can_see_workshop, require_edit, visible_workshop_keys
from app.services.content_editor import EditorError, ModuleIn
from app.services.deps import get_trainer

router = APIRouter(prefix="/trainer/content/modules", tags=["trainer-content"])


class ModuleCreateIn(BaseModel):
    key: str
    title_de: str
    workshop_key: str = "network"


def _meta(m: ContentModule) -> dict:
    return {"key": m.key, "title_de": m.title_de, "title_en": m.title_en,
            "order": m.order, "workshop_key": m.workshop_key}


def _http(e: EditorError) -> HTTPException:
    return HTTPException(status_code=e.status, detail=e.message)


def _require_module_edit(db: Session, trainer: dict, key: str) -> None:
    """Erst 404 (unbekanntes Modul), dann 403 (fremder Workshop) — vor Validierung/Sperre."""
    m = db.query(ContentModule).filter(ContentModule.key == key).first()
    if not m:
        raise EditorError(404, "Modul nicht gefunden")
    ws = db.get(Workshop, m.workshop_key or "")
    if ws is not None and not can_see_workshop(trainer, ws):
        raise EditorError(404, "Modul nicht gefunden")
    require_edit(db, trainer, m.workshop_key or "")


@router.get("")
def list_modules(db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    visible = visible_workshop_keys(db, trainer)
    mods = db.query(ContentModule).order_by(ContentModule.order).all()
    return [_meta(m) for m in mods if m.workshop_key in visible]


@router.get("/{key}")
def get_module(key: str, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    try:
        m, state, version = ed.module_state(db, key)
    except EditorError as e:
        raise _http(e) from None
    if m.workshop_key not in visible_workshop_keys(db, trainer):
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    has_snapshot = db.query(ContentModuleSnapshot).filter(ContentModuleSnapshot.module_key == key).first() is not None
    return {"key": m.key, "workshop_key": m.workshop_key,
            "has_snapshot": has_snapshot, "has_seed": key in MODULES,
            "version": version, **state}


@router.post("")
def create_module(data: ModuleCreateIn, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    ws = db.get(Workshop, data.workshop_key)
    # Unbekannter Workshop bleibt wie bisher 422 aus create_module.
    if ws and not can_see_workshop(trainer, ws):
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    if ws and not can_edit_workshop(trainer, ws):
        raise HTTPException(status_code=403, detail=f"Lehrgang ‚{ws.key}‘ gehört einem anderen Trainer.")
    try:
        m = ed.create_module(db, data.key, data.workshop_key, data.title_de)
    except EditorError as e:
        raise _http(e) from None
    log_action(db, trainer, "content.create", target=f"module:{m.key}", detail=data.title_de)
    return _meta(m)


@router.put("/{key}")
def update_module(key: str, data: ModuleIn, base_version: str | None = None,
                  db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    try:
        _require_module_edit(db, trainer, key)
        version = ed.save_module(db, key, data, base_version)
    except EditorError as e:
        raise _http(e) from None
    log_action(db, trainer, "content.save", target=f"module:{key}")
    m = db.query(ContentModule).filter(ContentModule.key == key).first()
    return {**_meta(m), "version": version}


@router.post("/{key}/reseed")
def reseed_module(key: str, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    try:
        _require_module_edit(db, trainer, key)
        m = ed.reseed_module(db, key)
    except EditorError as e:
        raise _http(e) from None
    log_action(db, trainer, "content.reseed", target=f"module:{key}")
    return _meta(m)


@router.post("/{key}/restore")
def restore_module(key: str, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    try:
        _require_module_edit(db, trainer, key)
        m = ed.restore_module(db, key)
    except EditorError as e:
        raise _http(e) from None
    log_action(db, trainer, "content.restore", target=f"module:{key}")
    return _meta(m)
