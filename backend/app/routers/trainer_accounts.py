import threading
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trainer import Trainer
from app.services.audit import log_action
from app.services.deps import get_admin, get_trainer
from app.services.security import hash_password

router = APIRouter(prefix="/trainer/accounts", tags=["trainer-accounts"])

# Serialisiert die Check-dann-Schreib-Schritte in delete_trainer() und
# set_role() gegeneinander, sonst koennten zwei gleichzeitige Requests beide
# die "noch ein anderer Admin"-Pruefung bestehen und gemeinsam den letzten
# Admin entfernen (Lockout). Der Python-Lock deckt den einen Prozess ab (uvicorn
# ohne --workers, siehe Dockerfile); with_for_update() in _admin_count() sperrt
# auf Postgres zusaetzlich die Admin-Zeilen, damit es auch mit mehreren Workern
# haelt (SQLite ignoriert FOR UPDATE -- dort ist es ohnehin ein Prozess).
_accounts_lock = threading.Lock()


def _serialize(t: Trainer, me: int | None) -> dict:
    # is_self: das Frontend leitet daraus die eigene Rolle ab (Admin-Bedienelemente
    # ein-/ausblenden) -- spart einen eigenen /me-Endpunkt.
    return {"id": t.id, "email": t.email, "name": t.name, "role": t.role, "is_self": t.id == me}


def _admin_count(db: Session) -> int:
    return len(db.query(Trainer.id).filter(Trainer.role == "admin").with_for_update().all())


class TrainerCreate(BaseModel):
    email: str
    name: str
    password: str


class RoleChange(BaseModel):
    role: Literal["admin", "trainer"]


@router.get("")
def list_trainers(db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    return [_serialize(t, trainer.get("trainer_id"))
            for t in db.query(Trainer).order_by(Trainer.email).all()]


@router.post("")
def create_trainer(data: TrainerCreate, db: Session = Depends(get_db), trainer: dict = Depends(get_admin)):
    email = data.email.strip().lower()
    if not email or "@" not in email:
        raise HTTPException(status_code=422, detail="Ungültige E-Mail")
    if len(data.password) < 8:
        raise HTTPException(status_code=422, detail="Passwort muss mindestens 8 Zeichen haben")
    if db.query(Trainer).filter(Trainer.email == email).first():
        raise HTTPException(status_code=422, detail="E-Mail bereits vergeben")
    # Neue Zugänge sind immer "trainer"; Admin wird man nur per Rollenwechsel.
    t = Trainer(email=email, name=data.name.strip() or email, password_hash=hash_password(data.password))
    db.add(t)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # from None: erwarteter Fall, der Traceback der IntegrityError sagt nichts
        # aus, was die Meldung nicht schon sagt.
        raise HTTPException(status_code=422, detail="E-Mail bereits vergeben") from None
    db.refresh(t)
    log_action(db, trainer, "trainer.create", target=f"trainer:{t.id}", detail=t.email)
    return _serialize(t, trainer.get("trainer_id"))


@router.delete("/{tid}")
def delete_trainer(tid: int, db: Session = Depends(get_db), trainer: dict = Depends(get_admin)):
    with _accounts_lock:
        t = db.query(Trainer).filter(Trainer.id == tid).first()
        if not t:
            raise HTTPException(status_code=404, detail="Trainer nicht gefunden")
        # Eigener Zugang: das eigene Token wäre sofort ungültig (Selbst-Aussperren).
        if t.id == trainer.get("trainer_id"):
            raise HTTPException(status_code=422, detail="Der eigene Zugang kann nicht gelöscht werden")
        if t.role == "admin" and _admin_count(db) <= 1:
            raise HTTPException(status_code=422, detail="Letzter Admin-Zugang kann nicht gelöscht werden")
        email = t.email
        db.delete(t)
        db.commit()
    log_action(db, trainer, "trainer.delete", target=f"trainer:{tid}", detail=email)
    return {"ok": True}


@router.patch("/{tid}/role")
def set_role(tid: int, data: RoleChange, db: Session = Depends(get_db), trainer: dict = Depends(get_admin)):
    with _accounts_lock:
        t = db.query(Trainer).filter(Trainer.id == tid).first()
        if not t:
            raise HTTPException(status_code=404, detail="Trainer nicht gefunden")
        old = t.role
        if old == data.role:
            return _serialize(t, trainer.get("trainer_id"))
        # Gilt auch für sich selbst: der letzte Admin kann sich nicht herabstufen.
        if old == "admin" and _admin_count(db) <= 1:
            raise HTTPException(status_code=422, detail="Letzter Admin kann nicht herabgestuft werden")
        t.role = data.role
        db.commit()
        db.refresh(t)
    log_action(db, trainer, "trainer.role_change", target=f"trainer:{tid}",
               detail=f"{t.email}: {old} -> {data.role}")
    return _serialize(t, trainer.get("trainer_id"))
