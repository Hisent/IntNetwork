from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.content.registry import MODULES
from app.database import get_db
from app.models.content import ContentModule, ContentModuleSnapshot
from app.services import content_editor as ed
from app.services.audit import log_action
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


@router.get("")
def list_modules(db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    mods = db.query(ContentModule).order_by(ContentModule.order).all()
    return [_meta(m) for m in mods]


@router.get("/{key}")
def get_module(key: str, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    try:
        m, state, version = ed.module_state(db, key)
    except EditorError as e:
        raise _http(e) from None
    has_snapshot = db.query(ContentModuleSnapshot).filter(ContentModuleSnapshot.module_key == key).first() is not None
    return {"key": m.key, "workshop_key": m.workshop_key,
            "has_snapshot": has_snapshot, "has_seed": key in MODULES,
            "version": version, **state}


@router.post("")
def create_module(data: ModuleCreateIn, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
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
        version = ed.save_module(db, key, data, base_version)
    except EditorError as e:
        raise _http(e) from None
    log_action(db, trainer, "content.save", target=f"module:{key}")
    m = db.query(ContentModule).filter(ContentModule.key == key).first()
    return {**_meta(m), "version": version}


@router.post("/{key}/reseed")
def reseed_module(key: str, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    try:
        m = ed.reseed_module(db, key)
    except EditorError as e:
        raise _http(e) from None
    log_action(db, trainer, "content.reseed", target=f"module:{key}")
    return _meta(m)


@router.post("/{key}/restore")
def restore_module(key: str, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    try:
        m = ed.restore_module(db, key)
    except EditorError as e:
        raise _http(e) from None
    log_action(db, trainer, "content.restore", target=f"module:{key}")
    return _meta(m)
