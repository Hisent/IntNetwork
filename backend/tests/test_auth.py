from fastapi.testclient import TestClient
from app.main import app
from app.routers import auth as auth_module
from app.services.security import create_token, decode_token
from app.utils import utc_now


def test_trainer_login_ok_and_bad():
    with TestClient(app) as c:
        r = c.post("/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"})
        assert r.status_code == 200
        assert r.json()["access_token"]

        bad = c.post("/api/trainer/login", json={"email": "trainer@test.de", "password": "wrong"})
        assert bad.status_code == 401


def test_trainer_login_unknown_email_still_verifies_password(monkeypatch):
    """Timing-Seitenkanal-Fix: unbekannte E-Mail und falsches Passwort müssen
    beide verify_password aufrufen (gleiche Bcrypt-Arbeit) und identisch
    antworten -- sonst ließe sich per Zeitmessung erraten, welche
    Trainer-E-Mails existieren."""
    calls = []
    original = auth_module.verify_password

    def counting(password, password_hash):
        calls.append(password_hash)
        return original(password, password_hash)

    monkeypatch.setattr(auth_module, "verify_password", counting)
    with TestClient(app) as c:
        unknown = c.post("/api/trainer/login",
                         json={"email": "nichtvorhanden@test.de", "password": "irgendwas"})
        known_bad = c.post("/api/trainer/login",
                           json={"email": "trainer@test.de", "password": "wrong"})

    assert unknown.status_code == 401
    assert known_bad.status_code == 401
    assert unknown.json()["detail"] == known_bad.json()["detail"] == "Login fehlgeschlagen"
    assert len(calls) == 2  # beide Pfade haben verify_password aufgerufen


def test_trainer_tokens_expire_earlier_than_participant_tokens():
    now = utc_now().timestamp()
    trainer = decode_token(create_token("trainer", "trainer"))
    participant = decode_token(create_token("participant", "participant"))
    assert trainer is not None and participant is not None
    assert 7 * 3600 < trainer["exp"] - now <= 8 * 3600
    assert participant["exp"] - trainer["exp"] > 20 * 24 * 3600
