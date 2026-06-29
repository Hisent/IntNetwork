from datetime import timedelta

from jose import JWTError, jwt

from app.config import settings
from app.utils import utc_now

ALGORITHM = "HS256"


def create_token(sub: str, role: str, extra: dict | None = None) -> str:
    payload = {"sub": sub, "role": role, "exp": utc_now() + timedelta(days=30)}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except JWTError:
        return None
