"""Persönliche API-Tokens (`lgt_…`) für den MCP-Endpunkt.

Gilt bewusst NUR dort: get_trainer dekodiert JWTs, ein `lgt_`-Token ist keiner
und wird an der normalen Trainer-REST-API mit 401 abgewiesen.
"""
import hashlib
import secrets

from sqlalchemy.orm import Session

from app.models.api_token import TrainerApiToken
from app.models.trainer import Trainer
from app.utils import utc_now


def _hash(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


def issue_token(db: Session, trainer_id: int, name: str) -> tuple[TrainerApiToken, str]:
    """Legt einen Token an; der Klartext existiert nur im Rückgabewert."""
    token = "lgt_" + secrets.token_urlsafe(32)
    row = TrainerApiToken(trainer_id=trainer_id, name=name, token_hash=_hash(token), prefix=token[:8])
    db.add(row)
    db.commit()
    db.refresh(row)
    return row, token


def resolve_token(db: Session, raw: str) -> dict | None:
    """Trainer-Dict wie get_trainer (plus token_name) oder None bei unbekanntem Token."""
    hit = (db.query(TrainerApiToken, Trainer)
           .join(Trainer, Trainer.id == TrainerApiToken.trainer_id)
           .filter(TrainerApiToken.token_hash == _hash(raw)).first())
    if not hit:
        return None
    row, t = hit
    row.last_used_at = utc_now()
    db.commit()
    return {"sub": t.email, "role": "trainer", "trainer_id": t.id,
            "is_admin": t.role == "admin", "token_name": row.name}
