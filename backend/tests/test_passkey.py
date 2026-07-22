"""Tests für die Trainer-Passkey-Anmeldung (WebAuthn), Zusatz zum Passwort.

WICHTIG -- was hier NICHT abgedeckt ist: Die eigentliche kryptographische
Signaturprüfung (COSE-Schlüssel, CBOR-Attestation-Parsing, ES256/RS256-
Verifikation) lässt sich ohne einen echten Hardware-/Plattform-Authenticator
nicht ehrlich mit Fake-Daten testen. Alle Tests hier mocken deshalb
`webauthn.verify_registration_response` und `webauthn.verify_authentication_
response` direkt -- sie prüfen NICHT, dass py_webauthn eine echte, gültige
Signatur tatsächlich verlangt oder eine gefälschte tatsächlich ablehnt. Das
ist bewusstes Vertrauen in die Bibliothek (deshalb wurde sie genutzt statt
CBOR/COSE/Signaturprüfung selbst zu bauen), nicht etwas, das dieses Projekt
selbst absichert. Was diese Tests wirklich prüfen: die eigene Logik drumherum
-- Challenge-Verwaltung, Credential-Zuordnung, sign_count-Vergleich,
Berechtigungen, Protokollierung und die 401/503-Pfade.
"""
import base64
import json
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from webauthn.helpers import bytes_to_base64url

from app.config import settings
from app.database import SessionLocal
from app.main import app
from app.models.trainer_credential import TrainerCredential
from app.routers import trainer_passkey as passkey_router
from app.services import passkey as passkey_service


def _trainer_headers(c, email="trainer@test.de", password="trainerpass1"):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": email, "password": password}
    ).json()["access_token"]}


def _create_trainer(c, h, email, password="pass1234"):
    return c.post(
        "/api/trainer/accounts", json={"email": email, "name": email, "password": password}, headers=h
    ).json()


@pytest.fixture
def enable_passkeys(monkeypatch):
    monkeypatch.setattr(settings, "webauthn_rp_id", "localhost")
    monkeypatch.setattr(settings, "webauthn_origin", "http://localhost:5173")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _fake_credential(challenge_b64url: str, cred_id_b64url: str = "fake-cred-id",
                     ctype: str = "webauthn.get") -> dict:
    """Baut eine minimale, plausible PublicKeyCredential-JSON-Form nach. Die
    Felder attestationObject/authenticatorData/signature sind Platzhalter --
    sie werden nie wirklich geprüft, weil verify_* gemockt ist."""
    client_data = json.dumps({"type": ctype, "challenge": challenge_b64url, "origin": settings.webauthn_origin})
    return {
        "id": cred_id_b64url,
        "rawId": cred_id_b64url,
        "type": "public-key",
        "response": {
            "clientDataJSON": _b64url(client_data.encode()),
            "attestationObject": _b64url(b"unused"),
            "authenticatorData": _b64url(b"unused"),
            "signature": _b64url(b"unused"),
        },
    }


def _register_credential(c, h, monkeypatch, credential_id: bytes, sign_count: int = 0, label: str = "Notebook"):
    options = c.post("/api/trainer/passkey/register/options", headers=h).json()["publicKey"]
    challenge = options["challenge"]
    monkeypatch.setattr(
        passkey_router.webauthn, "verify_registration_response",
        lambda **kw: SimpleNamespace(credential_id=credential_id, credential_public_key=b"pubkey",
                                     sign_count=sign_count),
    )
    cred = _fake_credential(challenge, ctype="webauthn.create")
    r = c.post("/api/trainer/passkey/register/verify", json={"credential": cred, "label": label}, headers=h)
    assert r.status_code == 200
    return r.json()


def test_status_off_by_default():
    with TestClient(app) as c:
        assert c.get("/api/trainer/passkey/status").json() == {"enabled": False}


def test_status_on_when_configured(enable_passkeys):
    with TestClient(app) as c:
        assert c.get("/api/trainer/passkey/status").json() == {"enabled": True}


def test_endpoints_503_without_configuration():
    with TestClient(app) as c:
        h = _trainer_headers(c)
        assert c.post("/api/trainer/passkey/register/options", headers=h).status_code == 503
        assert c.post("/api/trainer/passkey/register/verify",
                      json={"credential": {}, "label": "x"}, headers=h).status_code == 503
        assert c.post("/api/trainer/passkey/login/options", json={}).status_code == 503
        assert c.post("/api/trainer/passkey/login/verify", json={"credential": {}}).status_code == 503
        assert c.get("/api/trainer/passkey", headers=h).status_code == 503
        assert c.delete("/api/trainer/passkey/1", headers=h).status_code == 503


def test_register_creates_credential_and_logs(enable_passkeys, monkeypatch):
    with TestClient(app) as c:
        h = _trainer_headers(c)
        body = _register_credential(c, h, monkeypatch, b"credA", label="Notebook")
        assert body["label"] == "Notebook"
        assert "id" in body and "created_at" in body

        db = SessionLocal()
        try:
            row = db.query(TrainerCredential).filter(TrainerCredential.id == body["id"]).first()
            assert row is not None
            assert row.label == "Notebook"
            assert row.sign_count == 0
        finally:
            db.close()

        entries = c.get("/api/trainer/audit?action=passkey.register", headers=h).json()
        assert any(e["target"] == f"trainer_credential:{body['id']}" for e in entries)


def test_login_returns_working_token(enable_passkeys, monkeypatch):
    with TestClient(app) as c:
        h = _trainer_headers(c)
        _register_credential(c, h, monkeypatch, b"credB", sign_count=0)

        options = c.post("/api/trainer/passkey/login/options", json={}).json()["publicKey"]
        assert options["allowCredentials"] == []
        challenge = options["challenge"]
        cred_id_b64url = bytes_to_base64url(b"credB")

        monkeypatch.setattr(passkey_router.webauthn, "verify_authentication_response",
                            lambda **kw: SimpleNamespace(new_sign_count=1))

        login_cred = _fake_credential(challenge, cred_id_b64url=cred_id_b64url, ctype="webauthn.get")
        r = c.post("/api/trainer/passkey/login/verify", json={"credential": login_cred})
        assert r.status_code == 200
        token = r.json()["access_token"]

        new_h = {"Authorization": f"Bearer {token}"}
        assert c.get("/api/trainer/modules", headers=new_h).status_code == 200


def test_passkey_login_token_survives_only_until_password_change(enable_passkeys, monkeypatch):
    """Regression: Der Passkey-Login muss token_version ins Token schreiben.
    Sonst gilt der Claim als 0, und ein Passwortwechsel (der token_version
    hochzaehlt) wuerde den frisch per Passkey ausgestellten Token NICHT
    entwerten — bzw. schlimmer, ein vor dem Wechsel ausgestellter Token bliebe
    gueltig. Beide Enden werden hier geprueft."""
    with TestClient(app) as c:
        # Eigener Trainer statt des geteilten Default-Kontos: der Test aendert
        # unten das Passwort, das darf andere Tests nicht verschmutzen.
        admin = _trainer_headers(c)
        _create_trainer(c, admin, "passkeypwchange@test.de", password="passkeypw1")
        h = _trainer_headers(c, "passkeypwchange@test.de", "passkeypw1")
        _register_credential(c, h, monkeypatch, b"credPW", sign_count=0)

        zaehler = {"n": 0}

        def _passkey_login() -> str:
            # sign_count muss je Lauf STEIGEN, sonst schlaegt die Klon-Erkennung
            # beim zweiten Login zu (verhindert Wiedereinspielen).
            zaehler["n"] += 1
            options = c.post("/api/trainer/passkey/login/options", json={}).json()["publicKey"]
            monkeypatch.setattr(passkey_router.webauthn, "verify_authentication_response",
                                lambda **kw: SimpleNamespace(new_sign_count=zaehler["n"]))
            cred = _fake_credential(options["challenge"],
                                    cred_id_b64url=bytes_to_base64url(b"credPW"),
                                    ctype="webauthn.get")
            r = c.post("/api/trainer/passkey/login/verify", json={"credential": cred})
            assert r.status_code == 200
            return r.json()["access_token"]

        alter_token = _passkey_login()
        alt_h = {"Authorization": f"Bearer {alter_token}"}
        assert c.get("/api/trainer/modules", headers=alt_h).status_code == 200

        # Passwort aendern -> token_version++ -> alter Passkey-Token ungueltig.
        assert c.post("/api/trainer/password", headers=alt_h,
                      json={"old_password": "passkeypw1", "new_password": "passkeypw2"}
                      ).status_code == 200
        assert c.get("/api/trainer/modules", headers=alt_h).status_code == 401

        # Ein danach per Passkey ausgestellter Token traegt die neue Version.
        neuer_token = _passkey_login()
        neu_h = {"Authorization": f"Bearer {neuer_token}"}
        assert c.get("/api/trainer/modules", headers=neu_h).status_code == 200


def test_login_unknown_credential_401(enable_passkeys):
    with TestClient(app) as c:
        options = c.post("/api/trainer/passkey/login/options", json={}).json()["publicKey"]
        challenge = options["challenge"]
        cred = _fake_credential(challenge, cred_id_b64url="not-registered")
        r = c.post("/api/trainer/passkey/login/verify", json={"credential": cred})
        assert r.status_code == 401


def test_deleted_trainer_passkey_401(enable_passkeys, monkeypatch):
    with TestClient(app) as c:
        h = _trainer_headers(c)
        created = _create_trainer(c, h, "passkeyowner@test.de")
        owner_h = _trainer_headers(c, "passkeyowner@test.de", "pass1234")
        _register_credential(c, owner_h, monkeypatch, b"credOwner", sign_count=0)

        # Trainer löschen -> sein Passkey darf danach nicht mehr anmelden
        # (siehe login/verify: erneutes Laden des Trainers nach Credential-Fund).
        assert c.delete(f"/api/trainer/accounts/{created['id']}", headers=h).status_code == 200

        options = c.post("/api/trainer/passkey/login/options", json={}).json()["publicKey"]
        challenge = options["challenge"]
        cred_id_b64url = bytes_to_base64url(b"credOwner")
        monkeypatch.setattr(passkey_router.webauthn, "verify_authentication_response",
                            lambda **kw: SimpleNamespace(new_sign_count=1))
        login_cred = _fake_credential(challenge, cred_id_b64url=cred_id_b64url)
        r = c.post("/api/trainer/passkey/login/verify", json={"credential": login_cred})
        assert r.status_code == 401


def test_deleted_trainer_credentials_are_removed_by_cascade(enable_passkeys, monkeypatch):
    """Zweite Haelfte des Schutzes: Die Zeile soll nicht nur wirkungslos sein,
    sondern verschwinden. Das haengt daran, dass SQLite Fremdschluessel
    ueberhaupt durchsetzt — ohne `PRAGMA foreign_keys=ON` (app/database.py)
    blieben die Credentials als Waisen stehen, waehrend Postgres in Produktion
    kaskadiert. Genau diese Abweichung zwischen den Umgebungen faengt der Test.
    """
    from app.database import SessionLocal
    from app.models.trainer_credential import TrainerCredential

    with TestClient(app) as c:
        h = _trainer_headers(c)
        created = _create_trainer(c, h, "cascade@test.de")
        owner_h = _trainer_headers(c, "cascade@test.de", "pass1234")
        _register_credential(c, owner_h, monkeypatch, b"credCascade", sign_count=0)

        db = SessionLocal()
        try:
            assert db.query(TrainerCredential).filter(
                TrainerCredential.trainer_id == created["id"]).count() == 1
        finally:
            db.close()

        assert c.delete(f"/api/trainer/accounts/{created['id']}", headers=h).status_code == 200

        db = SessionLocal()
        try:
            assert db.query(TrainerCredential).filter(
                TrainerCredential.trainer_id == created["id"]).count() == 0
        finally:
            db.close()


def test_challenge_single_use(enable_passkeys, monkeypatch):
    with TestClient(app) as c:
        h = _trainer_headers(c)
        _register_credential(c, h, monkeypatch, b"credC", sign_count=0)

        options = c.post("/api/trainer/passkey/login/options", json={}).json()["publicKey"]
        challenge = options["challenge"]
        cred_id_b64url = bytes_to_base64url(b"credC")
        monkeypatch.setattr(passkey_router.webauthn, "verify_authentication_response",
                            lambda **kw: SimpleNamespace(new_sign_count=1))
        login_cred = _fake_credential(challenge, cred_id_b64url=cred_id_b64url)

        first = c.post("/api/trainer/passkey/login/verify", json={"credential": login_cred})
        assert first.status_code == 200

        second = c.post("/api/trainer/passkey/login/verify", json={"credential": login_cred})
        assert second.status_code == 401


def test_expired_challenge_rejected(enable_passkeys, monkeypatch):
    with TestClient(app) as c:
        monkeypatch.setattr(passkey_service, "CHALLENGE_TTL_SECONDS", -1)
        options = c.post("/api/trainer/passkey/login/options", json={}).json()["publicKey"]
        challenge = options["challenge"]
        cred = _fake_credential(challenge, cred_id_b64url="whatever")
        r = c.post("/api/trainer/passkey/login/verify", json={"credential": cred})
        assert r.status_code == 401


def test_regressing_sign_count_rejected_and_logged(enable_passkeys, monkeypatch):
    with TestClient(app) as c:
        h = _trainer_headers(c)
        _register_credential(c, h, monkeypatch, b"credD", sign_count=5)

        options = c.post("/api/trainer/passkey/login/options", json={}).json()["publicKey"]
        challenge = options["challenge"]
        cred_id_b64url = bytes_to_base64url(b"credD")
        monkeypatch.setattr(passkey_router.webauthn, "verify_authentication_response",
                            lambda **kw: SimpleNamespace(new_sign_count=3))
        login_cred = _fake_credential(challenge, cred_id_b64url=cred_id_b64url)
        r = c.post("/api/trainer/passkey/login/verify", json={"credential": login_cred})
        assert r.status_code == 401

        db = SessionLocal()
        try:
            row = db.query(TrainerCredential).filter(TrainerCredential.credential_id == cred_id_b64url).first()
            assert row.sign_count == 5  # unveraendert -- Ablehnung kam vor dem Update
        finally:
            db.close()

        entries = c.get("/api/trainer/audit?action=passkey.login", headers=h).json()
        assert any("geklont" in (e["detail"] or "") for e in entries)


def test_list_and_delete_only_own(enable_passkeys, monkeypatch):
    with TestClient(app) as c:
        h = _trainer_headers(c)
        _create_trainer(c, h, "otherpasskey@test.de")
        other_h = _trainer_headers(c, "otherpasskey@test.de", "pass1234")

        mine = _register_credential(c, h, monkeypatch, b"credMine", label="Mein Notebook")
        theirs = _register_credential(c, other_h, monkeypatch, b"credTheirs", label="Deren Notebook")

        my_list = c.get("/api/trainer/passkey", headers=h).json()
        assert any(p["id"] == mine["id"] for p in my_list)
        assert not any(p["id"] == theirs["id"] for p in my_list)

        # Fremden Passkey löschen -> 404 (nicht 403 -- verrät nicht, ob die ID existiert)
        assert c.delete(f"/api/trainer/passkey/{theirs['id']}", headers=h).status_code == 404

        assert c.delete(f"/api/trainer/passkey/{mine['id']}", headers=h).status_code == 204
        my_list_after = c.get("/api/trainer/passkey", headers=h).json()
        assert not any(p["id"] == mine["id"] for p in my_list_after)

        entries = c.get("/api/trainer/audit?action=passkey.delete", headers=h).json()
        assert any(e["target"] == f"trainer_credential:{mine['id']}" for e in entries)
