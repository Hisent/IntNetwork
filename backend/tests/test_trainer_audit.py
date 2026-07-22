from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_audit_log_requires_trainer():
    with TestClient(app) as c:
        assert c.get("/api/trainer/audit").status_code in (401, 403)


def test_mutating_actions_are_logged_newest_first():
    with TestClient(app) as c:
        h = _trainer(c)
        course = c.post("/api/courses", json={"name": "AuditKurs"}, headers=h).json()
        cid = course["id"]
        c.post("/api/join", json={"code": course["join_code"], "name": "Aud"})
        # Teilnehmer-Id ermitteln und wieder löschen -> zweiter Audit-Eintrag
        dash = c.get(f"/api/courses/{cid}/dashboard", headers=h).json()
        part_id = next(p["id"] for p in dash["participants"] if p["name"] == "Aud")
        c.delete(f"/api/courses/{cid}/participants/{part_id}", headers=h)

        entries = c.get("/api/trainer/audit", headers=h).json()
        actions = [e["action"] for e in entries]
        # neuestes zuerst -> delete kam nach create
        assert actions.index("participant.delete") < actions.index("course.create")
        create_entry = next(e for e in entries if e["action"] == "course.create" and e["target"] == f"course:{cid}")
        assert create_entry["trainer_email"] == "trainer@test.de"
        assert create_entry["detail"] == "AuditKurs"


def test_audit_action_filter():
    with TestClient(app) as c:
        h = _trainer(c)
        c.put("/api/trainer/features", json={"comments": False}, headers=h)
        c.put("/api/trainer/features", json={"comments": True}, headers=h)
        entries = c.get("/api/trainer/audit?action=feature.toggle", headers=h).json()
        assert entries and all(e["action"] == "feature.toggle" for e in entries)
