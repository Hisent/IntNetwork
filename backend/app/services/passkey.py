"""WebAuthn-Passkey-Anmeldung für Trainer -- Zusatz zum Passwort, kein Ersatz.

Bewusst mit der Bibliothek `webauthn` (py_webauthn) statt eigenem CBOR-/COSE-/
Signatur-Code: ES256/RS256-Prüfung von Hand nachzubauen wäre hier der falsche
Sparansatz.

Registrierung verlangt eine Discoverable Credential (residentKey=required)
und die Anmeldung schickt ein leeres `allowCredentials` -- am Beamer soll
niemand eine Kennung eintippen, der Authenticator kennt seinen Trainer selbst.
Unterstützt ein Gerät das nicht, scheitert nur die Registrierung; das
Passwort bleibt ein vollwertiger zweiter Weg (siehe routers/auth.py).

RP-ID und Origin kommen beim Prüfen ausschließlich aus der Konfiguration
(settings.webauthn_rp_id / webauthn_origin), niemals aus Request-Headern --
ein gefälschter Host-/Origin-Header dürfte die Prüfung nie bestehen lassen.
"""
import time

import webauthn
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialRequestOptions,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

from app.config import settings

CHALLENGE_TTL_SECONDS = 300  # 5 Minuten

# Offene WebAuthn-Challenges im Prozessspeicher: dict challenge (base64url) ->
# Ablaufzeit (time.monotonic()-Sekunden). Einmalig verwendbar -- consume_challenge
# entnimmt den Eintrag, statt ihn nur zu lesen. Registrierung und Anmeldung
# teilen sich denselben Speicher: Challenges sind kryptographisch zufällige
# 32+ Byte (Kollision ausgeschlossen) und werden ohnehin beim ersten Prüfen
# sofort verbraucht.
# Das Backend läuft als EIN uvicorn-Prozess (backend/Dockerfile:13, kein
# --workers) -- kämen mehrere Worker-Prozesse dazu, müsste dieser Speicher in
# die Datenbank wandern (jeder Worker hätte sonst sein eigenes Dict).
_challenges: dict[str, float] = {}


def enabled() -> bool:
    """Passkey-Funktion ist an, wenn RP-ID UND Origin konfiguriert sind."""
    return bool(settings.webauthn_rp_id and settings.webauthn_origin)


def _drop_expired_challenges(now: float) -> None:
    """Raeumt abgelaufene, nie eingeloeste Challenges aus _challenges.
    Ohne das waechst das Dict mit jedem Registrierungs-/Anmeldeversuch, der
    abgebrochen wird (Nutzer schliesst den Browser-Dialog, Timeout, ...),
    unbegrenzt weiter -- bis Prozessende ueber Monate ein echtes Leck.
    Amortisiert bei jedem Aufruf statt per Hintergrund-Thread: billig (Dict
    bleibt durch die 5-Minuten-TTL ohnehin klein)."""
    expired = [key for key, expiry in _challenges.items() if expiry <= now]
    for key in expired:
        del _challenges[key]


def _store_challenge(challenge: bytes) -> None:
    now = time.monotonic()
    _drop_expired_challenges(now)
    key = webauthn.helpers.bytes_to_base64url(challenge)
    _challenges[key] = now + CHALLENGE_TTL_SECONDS


def consume_challenge(challenge: bytes) -> bool:
    """Prüft eine Challenge und entfernt sie dabei sofort (einmalig verwendbar).

    Gibt False zurück, wenn die Challenge unbekannt (schon verbraucht oder nie
    ausgestellt) oder abgelaufen ist."""
    key = webauthn.helpers.bytes_to_base64url(challenge)
    expiry = _challenges.pop(key, None)
    if expiry is None:
        return False
    return time.monotonic() < expiry


def build_registration_options(
    trainer_id: int, trainer_email: str, existing_credential_ids: list[str],
) -> PublicKeyCredentialCreationOptions:
    """Optionen für navigator.credentials.create(). Schließt bereits
    registrierte Passkeys dieses Trainers aus (exclude_credentials), damit
    dasselbe Gerät nicht doppelt registriert wird."""
    options = webauthn.generate_registration_options(
        rp_id=settings.webauthn_rp_id,
        rp_name=settings.webauthn_rp_name,
        user_id=str(trainer_id).encode(),
        user_name=trainer_email,
        user_display_name=trainer_email,
        authenticator_selection=AuthenticatorSelectionCriteria(
            resident_key=ResidentKeyRequirement.REQUIRED,
            user_verification=UserVerificationRequirement.PREFERRED,
        ),
        exclude_credentials=[
            PublicKeyCredentialDescriptor(id=webauthn.helpers.base64url_to_bytes(cid))
            for cid in existing_credential_ids
        ],
    )
    _store_challenge(options.challenge)
    return options


def build_authentication_options() -> PublicKeyCredentialRequestOptions:
    """Optionen für navigator.credentials.get(). allow_credentials bleibt
    leer -- Anmeldung ohne Benutzernamen, der Authenticator liefert selbst,
    welcher Passkey passt (Discoverable Credential)."""
    options = webauthn.generate_authentication_options(
        rp_id=settings.webauthn_rp_id,
        user_verification=UserVerificationRequirement.PREFERRED,
        allow_credentials=[],
    )
    _store_challenge(options.challenge)
    return options
