from datetime import timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models.participant import Participant
from app.utils import utc_now


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _course_and_id(c, h, name):
    course = c.post("/api/courses", json={"name": name}, headers=h).json()
    cid = next(x["id"] for x in c.get("/api/courses", headers=h).json()
               if x["join_code"] == course["join_code"])
    return course["join_code"], cid


def _join(c, code, name):
    return {"Authorization": "Bearer " + c.post(
        "/api/join", json={"code": code, "name": name}).json()["access_token"]}


def test_heartbeat_sets_current_module_and_last_seen():
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course_and_id(c, h, "KursHB")
        p = _join(c, code, "P1")

        r = c.post("/api/modules/switching/heartbeat", headers=p)
        assert r.status_code == 200 and r.json() == {"ok": True}


def test_presence_shows_recent_and_hides_stale_and_is_course_scoped():
    with TestClient(app) as c:
        h = _trainer(c)
        code_a, cid_a = _course_and_id(c, h, "KursPresA")
        code_b, cid_b = _course_and_id(c, h, "KursPresB")
        a1 = _join(c, code_a, "Anna")
        a2 = _join(c, code_a, "Bert")
        b1 = _join(c, code_b, "Cara")

        assert c.post("/api/modules/switching/heartbeat", headers=a1).status_code == 200
        assert c.post("/api/modules/vlan/heartbeat", headers=b1).status_code == 200

        # Bert hat noch nie einen Heartbeat gesendet -> nicht aktiv
        active_a = c.get(f"/api/trainer/courses/{cid_a}/presence", headers=h).json()
        assert len(active_a) == 1
        assert active_a[0]["name"] == "Anna"
        assert active_a[0]["module_key"] == "switching"
        assert active_a[0]["module_title"]

        active_b = c.get(f"/api/trainer/courses/{cid_b}/presence", headers=h).json()
        assert len(active_b) == 1 and active_b[0]["name"] == "Cara"

        # Anna's letzten Heartbeat künstlich veralten lassen
        db = SessionLocal()
        try:
            part = db.query(Participant).filter(Participant.name == "Anna", Participant.course_id == cid_a).first()
            part.last_seen = utc_now() - timedelta(seconds=45)
            db.commit()
        finally:
            db.close()

        stale = c.get(f"/api/trainer/courses/{cid_a}/presence", headers=h).json()
        assert stale == []


def test_presence_requires_trainer():
    with TestClient(app) as c:
        assert c.get("/api/trainer/courses/1/presence").status_code in (401, 403)
