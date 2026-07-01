from sqlalchemy.orm import Session

from app.config import settings
from app.models.trainer import Trainer
from app.services.security import hash_password


def seed_trainer_if_empty(db: Session) -> None:
    if db.query(Trainer).count() > 0:
        return
    if not settings.admin_password:
        return
    db.add(Trainer(email=settings.admin_email.strip().lower(), name="Trainer",
                   password_hash=hash_password(settings.admin_password)))
    db.commit()
