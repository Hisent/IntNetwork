from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.participant import Participant
from app.models.trainer import Trainer
from app.services.security import decode_token

bearer = HTTPBearer()


def _payload(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    data = decode_token(creds.credentials)
    if not data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ungültiges Token")
    return data


def get_trainer(payload: dict = Depends(_payload), db: Session = Depends(get_db)) -> dict:
    if payload.get("role") != "trainer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nur Trainer")
    if not db.query(Trainer).filter(Trainer.id == payload.get("trainer_id")).first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Trainer nicht gefunden")
    return payload


def get_participant(payload: dict = Depends(_payload), db: Session = Depends(get_db)) -> Participant:
    if payload.get("role") != "participant":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nur Teilnehmer")
    p = db.query(Participant).filter(Participant.id == payload.get("participant_id")).first()
    if not p:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Teilnehmer nicht gefunden")
    # Fehlt token_version im Payload (Alt-Token von vor dieser Änderung), gilt es
    # als 0 -> Bestands-Tokens werden nicht schlagartig ungültig.
    if payload.get("token_version", 0) != p.token_version:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Sitzung abgelaufen, bitte neu beitreten")
    return p
