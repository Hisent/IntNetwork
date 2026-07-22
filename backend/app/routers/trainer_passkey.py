"""API für Trainer-Passkeys (WebAuthn), Zusatz zum Passwort-Login (auth.py).

Ist die Funktion nicht konfiguriert (siehe app/services/passkey.py), antworten
alle Endpunkte außer /status mit 503 (Muster: routers/lab.py).
"""
import json

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import webauthn
from webauthn.helpers import base64url_to_bytes, bytes_to_base64url, parse_client_data_json
from webauthn.helpers.exceptions import InvalidAuthenticationResponse, InvalidRegistrationResponse

from app.config import settings
from app.database import get_db
from app.models.trainer import Trainer
from app.models.trainer_credential import TrainerCredential
from app.services import passkey
from app.services.audit import log_action
from app.services.deps import get_trainer
from app.services.ratelimit import rate_limit
from app.services.security import create_token
from app.utils import utc_now

router = APIRouter(prefix="/trainer/passkey", tags=["trainer-passkey"])

_LOGIN_FEHLER = "Passkey-Anmeldung fehlgeschlagen"


def _require_enabled() -> None:
    if not passkey.enabled():
        raise HTTPException(
            status_code=503,
            detail="Passkey-Anmeldung ist auf diesem Server nicht konfiguriert.",
        )


class RegisterVerifyBody(BaseModel):
    credential: dict
    label: str


class LoginVerifyBody(BaseModel):
    credential: dict


def _serialize(c: TrainerCredential) -> dict:
    return {
        "id": c.id,
        "label": c.label,
        "created_at": c.created_at.isoformat(),
        "last_used_at": c.last_used_at.isoformat() if c.last_used_at else None,
    }


def _client_data_challenge(credential: dict) -> bytes:
    """Liest die Challenge aus clientDataJSON, ohne die Signatur zu prüfen --
    nötig, um vor dem eigentlichen Verify gegen den einmalig verwendbaren
    Challenge-Speicher zu prüfen. Wirft HTTPException(401/400) bei kaputtem Input."""
    try:
        raw = credential["response"]["clientDataJSON"]
        client_data = parse_client_data_json(base64url_to_bytes(raw))
        return client_data.challenge
    except (KeyError, TypeError, ValueError) as err:
        raise HTTPException(status_code=400, detail="Ungültige Passkey-Antwort") from err


@router.get("/status")
def passkey_status() -> dict:
    return {"enabled": passkey.enabled()}


@router.post("/register/options", dependencies=[Depends(_require_enabled)])
def register_options(trainer: dict = Depends(get_trainer), db: Session = Depends(get_db)) -> dict:
    existing = db.query(TrainerCredential).filter(
        TrainerCredential.trainer_id == trainer["trainer_id"]
    ).all()
    options = passkey.build_registration_options(
        trainer_id=trainer["trainer_id"],
        trainer_email=trainer["sub"],
        existing_credential_ids=[c.credential_id for c in existing],
    )
    return {"publicKey": json.loads(webauthn.options_to_json(options))}


@router.post("/register/verify", dependencies=[Depends(_require_enabled)])
def register_verify(
    data: RegisterVerifyBody, trainer: dict = Depends(get_trainer), db: Session = Depends(get_db)
) -> dict:
    challenge = _client_data_challenge(data.credential)
    if not passkey.consume_challenge(challenge):
        raise HTTPException(status_code=400, detail="Challenge abgelaufen oder bereits verwendet")

    try:
        verification = webauthn.verify_registration_response(
            credential=data.credential,
            expected_challenge=challenge,
            expected_rp_id=settings.webauthn_rp_id,
            expected_origin=settings.webauthn_origin,
        )
    except InvalidRegistrationResponse as err:
        raise HTTPException(status_code=400, detail="Passkey-Registrierung fehlgeschlagen") from err

    transports = data.credential.get("response", {}).get("transports")
    label = data.label.strip() or "Passkey"
    cred = TrainerCredential(
        trainer_id=trainer["trainer_id"],
        credential_id=bytes_to_base64url(verification.credential_id),
        public_key=bytes_to_base64url(verification.credential_public_key),
        sign_count=verification.sign_count,
        transports=",".join(transports) if transports else None,
        label=label,
    )
    db.add(cred)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # from None: erwarteter Fall (Passkey schon bekannt), der Traceback
        # der IntegrityError sagt nichts aus, was die Meldung nicht schon sagt.
        raise HTTPException(status_code=422, detail="Dieser Passkey ist bereits registriert") from None
    db.refresh(cred)
    log_action(db, trainer, "passkey.register", target=f"trainer_credential:{cred.id}", detail=label)
    return {"id": cred.id, "label": cred.label, "created_at": cred.created_at.isoformat()}


@router.post(
    "/login/options",
    dependencies=[Depends(_require_enabled), Depends(rate_limit(10, 60))],
)
def login_options() -> dict:
    options = passkey.build_authentication_options()
    return {"publicKey": json.loads(webauthn.options_to_json(options))}


@router.post(
    "/login/verify",
    dependencies=[Depends(_require_enabled), Depends(rate_limit(10, 60))],
)
def login_verify(data: LoginVerifyBody, db: Session = Depends(get_db)) -> dict:
    challenge = _client_data_challenge(data.credential)

    raw_id = data.credential.get("id") or data.credential.get("rawId")
    cred = db.query(TrainerCredential).filter(TrainerCredential.credential_id == raw_id).first()
    if not cred:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_LOGIN_FEHLER)

    # Zweite Absicherung neben ON DELETE CASCADE: den Trainer nach dem Fund
    # des Credentials erneut laden. Ist er inzwischen gelöscht, darf sein
    # Passkey nicht mehr anmelden -- get_trainer prüfte diese Existenz früher
    # nicht, genau das ist in diesem Projekt schon einmal ein Bug gewesen.
    t = db.query(Trainer).filter(Trainer.id == cred.trainer_id).first()
    if not t:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_LOGIN_FEHLER)

    if not passkey.consume_challenge(challenge):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_LOGIN_FEHLER)

    try:
        verification = webauthn.verify_authentication_response(
            credential=data.credential,
            expected_challenge=challenge,
            expected_rp_id=settings.webauthn_rp_id,
            expected_origin=settings.webauthn_origin,
            credential_public_key=base64url_to_bytes(cred.public_key),
            credential_current_sign_count=cred.sign_count,
        )
    except InvalidAuthenticationResponse as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_LOGIN_FEHLER) from err

    payload = {"sub": t.email, "trainer_id": t.id}

    # Rückläufiger (oder gleichbleibender) sign_count bei zwei Zählern > 0 ist
    # der klassische Hinweis auf einen geklonten Authenticator (Secure Element
    # dupliziert, beide melden denselben/ähnlichen Zählerstand) -- ablehnen und
    # protokollieren, statt die Anmeldung durchzulassen.
    if cred.sign_count > 0 and verification.new_sign_count > 0 and verification.new_sign_count <= cred.sign_count:
        log_action(
            db, payload, "passkey.login",
            target=f"trainer_credential:{cred.id}",
            detail="abgelehnt: sign_count nicht gestiegen (moeglicher geklonter Passkey)",
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_LOGIN_FEHLER)

    cred.sign_count = verification.new_sign_count
    cred.last_used_at = utc_now()
    db.commit()
    log_action(db, payload, "passkey.login", target=f"trainer_credential:{cred.id}")
    # token_version MUSS mit — sonst gilt der Claim als 0, und nach einem
    # Passwortwechsel (der token_version hochzaehlt) wuerde get_trainer diesen
    # Passkey-Login-Token ablehnen. Gleiche Token-Form wie der Passwort-Login.
    return {"access_token": create_token(
        sub=t.email, role="trainer", extra={"trainer_id": t.id, "token_version": t.token_version})}


@router.get("", dependencies=[Depends(_require_enabled)])
def list_passkeys(trainer: dict = Depends(get_trainer), db: Session = Depends(get_db)) -> list[dict]:
    creds = (
        db.query(TrainerCredential)
        .filter(TrainerCredential.trainer_id == trainer["trainer_id"])
        .order_by(TrainerCredential.created_at)
        .all()
    )
    return [_serialize(c) for c in creds]


@router.delete("/{cid}", status_code=204, dependencies=[Depends(_require_enabled)])
def delete_passkey(cid: int, trainer: dict = Depends(get_trainer), db: Session = Depends(get_db)) -> None:
    cred = (
        db.query(TrainerCredential)
        .filter(TrainerCredential.id == cid, TrainerCredential.trainer_id == trainer["trainer_id"])
        .first()
    )
    if not cred:
        raise HTTPException(status_code=404, detail="Passkey nicht gefunden")
    label = cred.label
    db.delete(cred)
    db.commit()
    log_action(db, trainer, "passkey.delete", target=f"trainer_credential:{cid}", detail=label)
