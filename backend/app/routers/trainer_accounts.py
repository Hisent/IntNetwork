import threading

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trainer import Trainer
from app.services.audit import log_action
from app.services.deps import get_trainer
from app.services.security import hash_password

router = APIRouter(prefix="/trainer/accounts", tags=["trainer-accounts"])

# Serialisiert den Check-dann-Loesch-Schritt in delete_trainer() gegen sich
# selbst, sonst koennten zwei gleichzeitige Deletes beide die "count > 1"-
# Pruefung bestehen und gemeinsam den letzten Trainer-Zugang loeschen
# (Lockout). Ein Python-Lock reicht, weil uvicorn hier ohne --workers laeuft
# (ein Prozess, siehe Dockerfile) -> bei mehreren Worker-Prozessen bräuchte
# das einen DB- oder Redis-Lock statt eines In-Prozess-Locks.
_delete_lock = threading.Lock()


def _serialize(t: Trainer) -> dict:
    return {"id": t.id, "email": t.email, "name": t.name}


class TrainerCreate(BaseModel):
    email: str
    name: str
    password: str


@router.get("")
def list_trainers(db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    return [_serialize(t) for t in db.query(Trainer).order_by(Trainer.email).all()]


@router.post("")
def create_trainer(data: TrainerCreate, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    email = data.email.strip().lower()
    if not email or "@" not in email:
        raise HTTPException(status_code=422, detail="Ungültige E-Mail")
    if len(data.password) < 8:
        raise HTTPException(status_code=422, detail="Passwort muss mindestens 8 Zeichen haben")
    if db.query(Trainer).filter(Trainer.email == email).first():
        raise HTTPException(status_code=422, detail="E-Mail bereits vergeben")
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
    return _serialize(t)


@router.delete("/{tid}")
def delete_trainer(tid: int, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    with _delete_lock:
        t = db.query(Trainer).filter(Trainer.id == tid).first()
        if not t:
            raise HTTPException(status_code=404, detail="Trainer nicht gefunden")
        if db.query(Trainer).count() <= 1:
            raise HTTPException(status_code=422, detail="Letzter Trainer-Zugang kann nicht gelöscht werden")
        email = t.email
        db.delete(t)
        db.commit()
    log_action(db, trainer, "trainer.delete", target=f"trainer:{tid}", detail=email)
    return {"ok": True}
