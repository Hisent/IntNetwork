from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trainer import Trainer
from app.services.audit import log_action
from app.services.deps import get_trainer
from app.services.ratelimit import rate_limit
from app.services.security import DUMMY_PASSWORD_HASH, create_token, hash_password, verify_password

router = APIRouter(tags=["auth"])


class TrainerLogin(BaseModel):
    email: str = Field(max_length=254)
    password: str = Field(max_length=200)


@router.post("/trainer/login", dependencies=[Depends(rate_limit(10, 60))])
def trainer_login(data: TrainerLogin, db: Session = Depends(get_db)):
    t = db.query(Trainer).filter(Trainer.email == data.email.strip().lower()).first()
    if not t:
        # Trotzdem eine Bcrypt-Prüfung ausführen (gegen einen festen Dummy-Hash), damit
        # dieser Pfad genauso lange dauert wie "E-Mail bekannt, Passwort falsch" unten —
        # sonst ließe sich per Zeitmessung erraten, welche Trainer-E-Mails existieren.
        verify_password(data.password, DUMMY_PASSWORD_HASH)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login fehlgeschlagen")
    if not verify_password(data.password, t.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login fehlgeschlagen")
    return {"access_token": create_token(
        sub=t.email, role="trainer", extra={"trainer_id": t.id, "token_version": t.token_version})}


class TrainerPasswordChange(BaseModel):
    old_password: str = Field(max_length=200)
    new_password: str = Field(max_length=200)


@router.post("/trainer/password", dependencies=[Depends(rate_limit(10, 60))])
def change_trainer_password(data: TrainerPasswordChange, db: Session = Depends(get_db),
                            trainer: dict = Depends(get_trainer)):
    """Eingeloggter Trainer ändert sein eigenes Passwort. Bumpt token_version,
    damit alle anderen laufenden Sitzungen dieses Trainers (andere Geräte/Tabs)
    sofort ungültig werden -- analog zu Participant.reset_code
    (courses.py::reset_resume_code). Der zurückgegebene frische Token hält die
    aufrufende Sitzung selbst am Leben."""
    t = db.query(Trainer).filter(Trainer.id == trainer.get("trainer_id")).first()
    if not t:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Trainer nicht gefunden")
    if not verify_password(data.old_password, t.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Altes Passwort falsch")
    if len(data.new_password) < 8:
        raise HTTPException(status_code=422, detail="Passwort muss mindestens 8 Zeichen haben")
    t.password_hash = hash_password(data.new_password)
    t.token_version += 1
    db.commit()
    log_action(db, trainer, "trainer.password_change", target=f"trainer:{t.id}")
    return {"access_token": create_token(
        sub=t.email, role="trainer", extra={"trainer_id": t.id, "token_version": t.token_version})}
