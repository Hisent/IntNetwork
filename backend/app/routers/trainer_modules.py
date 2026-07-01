from fastapi import APIRouter, Depends, HTTPException

from app.services.deps import get_trainer
from app.content.registry import module_meta, trainer_module

router = APIRouter(prefix="/trainer/modules", tags=["trainer-modules"])


@router.get("")
def list_trainer_modules(_t: dict = Depends(get_trainer)):
    return module_meta()


@router.get("/{key}")
def get_trainer_module(key: str, _t: dict = Depends(get_trainer)):
    m = trainer_module(key)
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    return m
