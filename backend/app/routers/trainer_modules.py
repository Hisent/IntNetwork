from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.deps import get_trainer
from app.content.registry import module_meta, trainer_module

router = APIRouter(prefix="/trainer/modules", tags=["trainer-modules"])


@router.get("")
def list_trainer_modules(db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    return module_meta(db)


@router.get("/{key}")
def get_trainer_module(key: str, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    m = trainer_module(db, key)
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    return m
