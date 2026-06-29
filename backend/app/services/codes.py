import secrets

from app.models.course import Course

_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # ohne verwechselbare Zeichen


def new_code(db) -> str:
    while True:
        code = "".join(secrets.choice(_ALPHABET) for _ in range(6))
        if not db.query(Course).filter(Course.join_code == code).first():
            return code
