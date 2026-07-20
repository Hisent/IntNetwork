from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.participant import Participant
from app.models.progress import Progress
from app.services.course_membership import active_module_keys


def _trainer(c):
    tok = c.post("/api/trainer/login", json={
        "email": "trainer@test.de", "password": "trainerpass1"}).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}


def _mark_all_done(course_id: int, participant_id: int) -> int:
    db = SessionLocal()
    try:
        active = active_module_keys(db, course_id)
        for key in active:
            db.add(Progress(participant_id=participant_id, module_key=key, done=True))
        db.commit()
        return len(active)
    finally:
        db.close()


def test_certificate_requires_all_done_then_issues_and_verifies():
    with TestClient(app) as c:
        h = _trainer(c)
        course = c.post("/api/courses", json={"name": "CertKurs", "workshop_key": "network"}, headers=h).json()
        joined = c.post("/api/join", json={"code": course["join_code"], "name": "Zoe"}).json()
        auth = {"Authorization": f"Bearer {joined['access_token']}"}

        # Noch nicht alle Module bestanden -> keine Bestätigung.
        assert c.post("/api/certificate", headers=auth).status_code == 403

        db = SessionLocal()
        part = db.query(Participant).filter(Participant.name == "Zoe").first()
        pid, cid = part.id, part.course_id
        db.close()
        count = _mark_all_done(cid, pid)

        issued = c.post("/api/certificate", headers=auth)
        assert issued.status_code == 200
        cert = issued.json()
        assert cert["participant_name"] == "Zoe"
        assert cert["module_count"] == count
        assert cert["id"]

        # Idempotent: gleiche ID bei erneutem Ausstellen.
        assert c.post("/api/certificate", headers=auth).json()["id"] == cert["id"]

        # Öffentliche Prüfung ohne Login.
        verified = c.get(f"/api/verify/{cert['id']}")
        assert verified.status_code == 200
        assert verified.json()["participant_name"] == "Zoe"
        assert verified.json()["module_count"] == count

        assert c.get("/api/verify/does-not-exist").status_code == 404


def test_legacy_participant_without_resume_code_can_rejoin_and_gets_one():
    """Teilnehmer von vor der Code-Einführung (resume_code IS NULL) dürfen weiter
    per Name fort — bekommen dabei nachträglich einen Code."""
    with TestClient(app) as c:
        h = _trainer(c)
        course = c.post("/api/courses", json={"name": "LegacyKurs"}, headers=h).json()
        cid = course["id"]
        db = SessionLocal()
        legacy = Participant(course_id=cid, name="Alt", resume_code=None)
        db.add(legacy)
        db.commit()
        db.close()

        again = c.post("/api/join", json={"code": course["join_code"], "name": "Alt"})
        assert again.status_code == 200
        assert again.json()["resume_code"]  # nachträglich vergeben und angezeigt
