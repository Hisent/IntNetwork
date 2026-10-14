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


def test_heartbeat_rejects_unknown_module_key():
    with TestClient(app) as c:
        h = _trainer(c)
        code, _cid = _course_and_id(c, h, "KursHBBad")
        p = _join(c, code, "P2")
        assert c.post("/api/modules/garbage-nicht-da/heartbeat", headers=p).status_code == 404


def test_presence_shows_recent_and_hides_stale_and_is_course_scoped():
    with TestClient(app) as c:
        h = _trainer(c)
        code_a, cid_a = _course_and_id(c, h, "KursPresA")
        code_b, cid_b = _course_and_id(c, h, "KursPresB")
        a1 = _join(c, code_a, "Anna")
        _join(c, code_a, "Bert")  # nur anlegen, Token wird hier nicht gebraucht
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


# --- „Wer hängt fest?“ -------------------------------------------------------

def test_stuck_reasons_rules():
    from app.routers.presence import STUCK_FAILED_MINUTES as F, STUCK_LONG_MINUTES as L, stuck_reasons
    assert stuck_reasons(F, 2, done=False) == ["failed_attempts"]
    assert stuck_reasons(F - 1, 5, done=False) == []        # Fehlversuche, aber noch frisch im Modul
    assert stuck_reasons(L, 1, done=False) == ["long_in_module"]
    assert stuck_reasons(L, 2, done=False) == ["failed_attempts", "long_in_module"]
    assert stuck_reasons(L * 3, 9, done=True) == []          # bestanden -> hängt nicht fest
    assert stuck_reasons(0, 0, done=False) == []


def _age(cid, name, **minutes):
    """Setzt Zeitstempel eines Teilnehmers um so viele Minuten in die Vergangenheit."""
    db = SessionLocal()
    try:
        part = db.query(Participant).filter(Participant.name == name, Participant.course_id == cid).first()
        for field, m in minutes.items():
            setattr(part, field, utc_now() - timedelta(minutes=m))
        db.commit()
    finally:
        db.close()


def test_presence_flags_stuck_participant_first():
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course_and_id(c, h, "KursStuck")
        stuck = _join(c, code, "Zoe")
        fine = _join(c, code, "Adam")
        for p in (stuck, fine):
            assert c.post("/api/modules/switching/heartbeat", headers=p).status_code == 200
        for _ in range(2):  # zwei Abgaben unter der Bestehensgrenze
            assert c.post("/api/modules/switching/quiz", json={"answers": {}}, headers=stuck).status_code == 200
        _age(cid, "Zoe", module_entered_at=15)

        rows = c.get(f"/api/trainer/courses/{cid}/presence", headers=h).json()
        assert [r["name"] for r in rows] == ["Zoe", "Adam"]  # trotz Alphabet: Hilfe zuerst
        zoe, adam = rows
        assert zoe["needs_help"] and zoe["reasons"] == ["failed_attempts"]
        assert zoe["failed_attempts"] == 2 and zoe["minutes_in_module"] >= 15 and zoe["done"] is False
        assert adam["needs_help"] is False and adam["failed_attempts"] == 0 and adam["minutes_in_module"] == 0

        # Heartbeat im selben Modul behält den Einstieg; Modulwechsel setzt ihn neu.
        assert c.post("/api/modules/switching/heartbeat", headers=stuck).status_code == 200
        assert c.get(f"/api/trainer/courses/{cid}/presence", headers=h).json()[0]["minutes_in_module"] >= 15
        assert c.post("/api/modules/vlan/heartbeat", headers=stuck).status_code == 200
        zoe = next(r for r in c.get(f"/api/trainer/courses/{cid}/presence", headers=h).json() if r["name"] == "Zoe")
        assert zoe["module_key"] == "vlan" and zoe["minutes_in_module"] == 0 and zoe["failed_attempts"] == 0


def test_heartbeat_after_long_pause_counts_as_new_entry():
    from app.routers.presence import ENTER_RESET_MINUTES
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course_and_id(c, h, "KursPause")
        p = _join(c, code, "Pia")
        assert c.post("/api/modules/switching/heartbeat", headers=p).status_code == 200
        _age(cid, "Pia", module_entered_at=120, last_seen=ENTER_RESET_MINUTES + 1)
        assert c.post("/api/modules/switching/heartbeat", headers=p).status_code == 200
        assert c.get(f"/api/trainer/courses/{cid}/presence", headers=h).json()[0]["minutes_in_module"] == 0


# --- „Folgt mir“ ---------------------------------------------------------------

def test_follow_set_seen_by_own_course_only_and_cleared():
    with TestClient(app) as c:
        h = _trainer(c)
        code_a, cid_a = _course_and_id(c, h, "KursFollowA")
        code_b, _cid_b = _course_and_id(c, h, "KursFollowB")
        pa, pb = _join(c, code_a, "Fa"), _join(c, code_b, "Fb")
        assert c.get("/api/follow", headers=pa).json() is None

        r = c.put(f"/api/trainer/courses/{cid_a}/follow", json={"module_key": "vlan", "block_uid": "b-1"}, headers=h)
        assert r.status_code == 200 and r.json()["module_key"] == "vlan"
        seen = c.get("/api/follow", headers=pa).json()
        assert (seen["module_key"], seen["block_uid"]) == ("vlan", "b-1") and seen["updated_at"].endswith("+00:00")
        assert c.get("/api/follow", headers=pb).json() is None  # anderer Kurs sieht nichts
        assert c.get(f"/api/courses/{cid_a}/dashboard", headers=h).json()["course"]["follow"]["module_key"] == "vlan"

        # ohne Block: Feld wird geleert
        c.put(f"/api/trainer/courses/{cid_a}/follow", json={"module_key": "switching"}, headers=h)
        assert c.get("/api/follow", headers=pa).json()["block_uid"] is None

        assert c.delete(f"/api/trainer/courses/{cid_a}/follow", headers=h).json() == {"ok": True}
        assert c.get("/api/follow", headers=pa).json() is None
        assert c.get(f"/api/courses/{cid_a}/dashboard", headers=h).json()["course"]["follow"] is None


def test_follow_hidden_when_stale_or_module_disabled():
    from app.models.course import Course
    from app.routers.presence import FOLLOW_TTL
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course_and_id(c, h, "KursFollowStale")
        p = _join(c, code, "Fs")
        c.put(f"/api/trainer/courses/{cid}/follow", json={"module_key": "vlan"}, headers=h)
        c.put(f"/api/courses/{cid}/modules", json={"module_key": "vlan", "active": False}, headers=h)
        assert c.get("/api/follow", headers=p).json() is None
        c.put(f"/api/courses/{cid}/modules", json={"module_key": "vlan", "active": True}, headers=h)
        assert c.get("/api/follow", headers=p).json()["module_key"] == "vlan"
        db = SessionLocal()
        try:
            db.get(Course, cid).follow_updated_at = utc_now() - FOLLOW_TTL - timedelta(minutes=1)
            db.commit()
        finally:
            db.close()
        assert c.get("/api/follow", headers=p).json() is None


def test_follow_authorization_and_validation():
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course_and_id(c, h, "KursFollowAuth")
        p = _join(c, code, "Fz")
        body = {"module_key": "vlan"}
        # Teilnehmer dürfen die Position weder setzen noch löschen, noch Präsenz sehen.
        assert c.put(f"/api/trainer/courses/{cid}/follow", json=body, headers=p).status_code == 403
        assert c.delete(f"/api/trainer/courses/{cid}/follow", headers=p).status_code == 403
        assert c.get(f"/api/trainer/courses/{cid}/presence", headers=p).status_code == 403
        assert c.put(f"/api/trainer/courses/{cid}/follow", json=body).status_code in (401, 403)
        # /follow ist nur für Teilnehmer (eigener Kurs aus dem Token), ohne Token gar nichts.
        assert c.get("/api/follow", headers=h).status_code == 403
        assert c.get("/api/follow").status_code in (401, 403)
        assert c.put("/api/trainer/courses/999999/follow", json=body, headers=h).status_code == 404
        assert c.put(f"/api/trainer/courses/{cid}/follow", json={"module_key": "gibt-es-nicht"},
                     headers=h).status_code == 404
        assert c.put(f"/api/trainer/courses/{cid}/follow", json={"module_key": "vlan", "block_uid": "x" * 201},
                     headers=h).status_code == 422
