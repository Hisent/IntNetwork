from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.api_token import TrainerApiToken
from app.services.api_tokens import issue_token
from app.services.audit import log_action
from app.services.deps import get_trainer

router = APIRouter(prefix="/trainer/api-tokens", tags=["trainer-api-tokens"])


class TokenCreate(BaseModel):
    name: str = Field(min_length=1, max_length=60)


def _serialize(t: TrainerApiToken) -> dict:
    return {"id": t.id, "name": t.name, "prefix": t.prefix,
            "created_at": t.created_at, "last_used_at": t.last_used_at}


@router.get("")
def list_tokens(db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    return [_serialize(t) for t in db.query(TrainerApiToken)
            .filter(TrainerApiToken.trainer_id == trainer["trainer_id"])
            .order_by(TrainerApiToken.created_at.desc()).all()]


@router.post("")
def create_token(data: TokenCreate, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    row, token = issue_token(db, trainer["trainer_id"], data.name)
    out = {**_serialize(row), "token": token}  # Klartext nur in dieser Antwort
    log_action(db, trainer, "api_token.create", target=f"api_token:{row.id}", detail=row.name)
    return out


@router.delete("/{token_id}")
def delete_token(token_id: int, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    row = db.query(TrainerApiToken).filter(TrainerApiToken.id == token_id,
                                           TrainerApiToken.trainer_id == trainer["trainer_id"]).first()
    if not row:
        raise HTTPException(status_code=404, detail="Token nicht gefunden")
    name = row.name
    db.delete(row)
    db.commit()
    log_action(db, trainer, "api_token.delete", target=f"api_token:{token_id}", detail=name)
    return {"ok": True}
