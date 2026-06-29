import hmac

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.config import settings
from app.services.security import create_token

router = APIRouter(tags=["auth"])


class TrainerLogin(BaseModel):
    email: str
    password: str


@router.post("/trainer/login")
def trainer_login(data: TrainerLogin):
    if not settings.admin_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Trainer-Login nicht konfiguriert")
    ok_mail = hmac.compare_digest(data.email.lower(), settings.admin_email.lower())
    ok_pw = hmac.compare_digest(data.password, settings.admin_password)
    if not (ok_mail and ok_pw):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login fehlgeschlagen")
    return {"access_token": create_token(sub=settings.admin_email, role="trainer")}
