from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trainer import Trainer
from app.services.ratelimit import rate_limit
from app.services.security import create_token, verify_password

router = APIRouter(tags=["auth"])


class TrainerLogin(BaseModel):
    email: str = Field(max_length=254)
    password: str = Field(max_length=200)


@router.post("/trainer/login", dependencies=[Depends(rate_limit(10, 60))])
def trainer_login(data: TrainerLogin, db: Session = Depends(get_db)):
    t = db.query(Trainer).filter(Trainer.email == data.email.strip().lower()).first()
    if not t or not verify_password(data.password, t.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login fehlgeschlagen")
    return {"access_token": create_token(sub=t.email, role="trainer", extra={"trainer_id": t.id})}
