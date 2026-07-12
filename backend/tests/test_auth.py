from fastapi.testclient import TestClient
from app.main import app
from app.services.security import create_token, decode_token
from app.utils import utc_now


def test_trainer_login_ok_and_bad():
    with TestClient(app) as c:
        r = c.post("/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"})
        assert r.status_code == 200
        assert r.json()["access_token"]

        bad = c.post("/api/trainer/login", json={"email": "trainer@test.de", "password": "wrong"})
        assert bad.status_code == 401


def test_trainer_tokens_expire_earlier_than_participant_tokens():
    now = utc_now().timestamp()
    trainer = decode_token(create_token("trainer", "trainer"))
    participant = decode_token(create_token("participant", "participant"))
    assert trainer is not None and participant is not None
    assert 7 * 3600 < trainer["exp"] - now <= 8 * 3600
    assert participant["exp"] - trainer["exp"] > 20 * 24 * 3600
