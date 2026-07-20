import secrets
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# Ohne 0/O/1/I/L — auf Papier/mündlich verwechslungsarm.
_CODE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def generate_resume_code(length: int = 8) -> str:
    """Persönlicher Wiederaufnahme-Code: erlaubt späteres Fortsetzen unter
    demselben Namen, ohne dass ein Fremder den Lernstand übernehmen kann."""
    return "".join(secrets.choice(_CODE_ALPHABET) for _ in range(length))


def generate_certificate_id() -> str:
    """Öffentlich prüfbare, nicht erratbare Zertifikats-ID."""
    return secrets.token_hex(8)
