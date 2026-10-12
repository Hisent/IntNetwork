from sqlalchemy.orm import Session

from app.config import settings
from app.models.trainer import Trainer
from app.services.security import hash_password


def seed_trainer_if_empty(db: Session) -> None:
    if db.query(Trainer).count() > 0:
        return
    if not settings.admin_password:
        return
    # Greift nur bei leerer trainer-Tabelle (Erststart): der Platzhalter aus
    # .env.example darf nie zum echten ersten Trainer-Passwort werden.
    if not settings.debug and settings.admin_password.startswith("change-me"):
        raise RuntimeError("ADMIN_PASSWORD ist noch der change-me-Platzhalter aus .env.example.")
    db.add(Trainer(email=settings.admin_email.strip().lower(), name="Trainer",
                   password_hash=hash_password(settings.admin_password)))
    db.commit()
