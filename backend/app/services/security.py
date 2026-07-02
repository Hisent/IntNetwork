from datetime import timedelta

import bcrypt
import jwt

from app.config import settings
from app.utils import utc_now

ALGORITHM = "HS256"


# bcrypt >= 4 wirft ValueError bei Passwörtern über 72 Bytes (statt wie früher
# still zu kürzen) -> ohne Kürzung wäre /trainer/login mit langem Passwort ein
# unauthentifizierter 500er. Beide Seiten kürzen identisch, bleibt konsistent.
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode()[:72], bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode()[:72], password_hash.encode())


def create_token(sub: str, role: str, extra: dict | None = None) -> str:
    payload = {"sub": sub, "role": role, "exp": utc_now() + timedelta(days=30)}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
