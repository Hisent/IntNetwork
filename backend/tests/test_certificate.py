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


def test_certificate_gated_by_trainer_approval():
    with TestClient(app) as c:
        h = _trainer(c)
        course = c.post("/api/courses", json={"name": "ApprKurs", "workshop_key": "network"}, headers=h).json()
        assert c.patch(f"/api/courses/{course['id']}/approval",
                       json={"require_approval": True}, headers=h).status_code == 200

        joined = c.post("/api/join", json={"code": course["join_code"], "name": "Max"}).json()
        auth = {"Authorization": f"Bearer {joined['access_token']}"}
        db = SessionLocal()
        part = db.query(Participant).filter(Participant.name == "Max").first()
        pid, cid = part.id, part.course_id
        db.close()
        _mark_all_done(cid, pid)

        # Alle Module done, aber ohne Freigabe -> 409 (nicht 403 „Module offen")
        assert c.post("/api/certificate", headers=auth).status_code == 409

        approved = c.post(f"/api/courses/{course['id']}/participants/{pid}/approve",
                          json={"approved": True}, headers=h)
        assert approved.status_code == 200 and approved.json()["approved"] is True

        # Nach Freigabe wird ausgestellt
        assert c.post("/api/certificate", headers=auth).status_code == 200

        # Dashboard zeigt Freigabe-Status
        dash = c.get(f"/api/courses/{course['id']}/dashboard", headers=h).json()
        assert dash["course"]["require_approval"] is True
        assert any(p["id"] == pid and p["approved"] for p in dash["participants"])


def test_trainer_resets_code_and_deletes_participant():
    with TestClient(app) as c:
        h = _trainer(c)
        course = c.post("/api/courses", json={"name": "MgmtKurs"}, headers=h).json()
        code, cid = course["join_code"], course["id"]
        old = c.post("/api/join", json={"code": code, "name": "Nils"}).json()["resume_code"]
        db = SessionLocal()
        pid = db.query(Participant).filter(Participant.name == "Nils").first().id
        db.close()

        reset = c.post(f"/api/courses/{cid}/participants/{pid}/reset-code", headers=h)
        assert reset.status_code == 200
        new = reset.json()["resume_code"]
        assert new and new != old
        # Alter Code ungültig, neuer gültig
        assert c.post("/api/join", json={"code": code, "name": "Nils", "resume_code": old}).status_code == 403
        assert c.post("/api/join", json={"code": code, "name": "Nils", "resume_code": new}).status_code == 200

        # Löschen entfernt den Teilnehmer -> Name danach wieder frei (neuer Datensatz)
        assert c.delete(f"/api/courses/{cid}/participants/{pid}", headers=h).status_code == 200
        again = c.post("/api/join", json={"code": code, "name": "Nils"})
        assert again.status_code == 200 and again.json()["resume_code"]


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
