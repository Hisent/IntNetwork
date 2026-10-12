from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.comment import Comment
from app.models.course import Course
from app.models.course_module import CourseModule
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_delete_course_cascades_participants_progress_quiz_comments():
    """Deckt B (CASCADE-Fremdschlüssel) über den neuen Endpunkt aus C ab: ein
    Kurs mit Teilnehmer, Fortschritt, Quiz-Ergebnis und Kommentar wird gelöscht
    -> alle zugehörigen Zeilen in den Kindtabellen müssen mitverschwinden."""
    with TestClient(app) as c:
        h = _trainer(c)
        created = c.post("/api/courses", json={"name": "LoeschKurs"}, headers=h).json()
        cid = created["id"]
        code = created["join_code"]

        joined = c.post("/api/join", json={"code": code, "name": "Kim"}).json()
        p_auth = {"Authorization": f"Bearer {joined['access_token']}"}

        mod = c.get("/api/modules/vlan", headers=p_auth).json()
        ids = [q["id"] for q in mod["quiz"]["questions"]]
        answers = {ids[0]: 1, ids[1]: 1, ids[2]: [0, 1, 3], ids[3]: 20}
        assert c.post("/api/modules/vlan/quiz", json={"answers": answers}, headers=p_auth).status_code == 200
        assert c.post("/api/modules/vlan/comments", json={"block_index": 0, "body": "Frage"},
                      headers=p_auth).status_code == 200

        db = SessionLocal()
        try:
            pid = db.query(Participant).filter(Participant.name == "Kim").first().id
            assert db.query(Progress).filter(Progress.participant_id == pid).count() > 0
            assert db.query(QuizResult).filter(QuizResult.participant_id == pid).count() > 0
            assert db.query(Comment).filter(Comment.course_id == cid).count() > 0
            assert db.query(CourseModule).filter(CourseModule.course_id == cid).count() > 0
        finally:
            db.close()

        r = c.delete(f"/api/courses/{cid}", headers=h)
        assert r.status_code == 200

        db = SessionLocal()
        try:
            assert db.query(Course).filter(Course.id == cid).first() is None
            assert db.query(Participant).filter(Participant.course_id == cid).count() == 0
            assert db.query(Progress).filter(Progress.participant_id == pid).count() == 0
            assert db.query(QuizResult).filter(QuizResult.participant_id == pid).count() == 0
            assert db.query(Comment).filter(Comment.course_id == cid).count() == 0
            assert db.query(CourseModule).filter(CourseModule.course_id == cid).count() == 0
        finally:
            db.close()

        # Kurs weg -> Dashboard/Module-Endpunkte melden jetzt 404 statt leerer Daten.
        assert c.get(f"/api/courses/{cid}/dashboard", headers=h).status_code == 404


def test_delete_course_requires_trainer():
    with TestClient(app) as c:
        h = _trainer(c)
        created = c.post("/api/courses", json={"name": "KursOhneAuth"}, headers=h).json()
        assert c.delete(f"/api/courses/{created['id']}").status_code in (401, 403)
        # aufraeumen
        c.delete(f"/api/courses/{created['id']}", headers=h)


def test_delete_unknown_course_404():
    with TestClient(app) as c:
        h = _trainer(c)
        assert c.delete("/api/courses/999999", headers=h).status_code == 404


def _kurs_mit_zertifikat(c, h, name, pid):
    from app.models.certificate import Certificate
    created = c.post("/api/courses", json={"name": name}, headers=h).json()
    db = SessionLocal()
    db.add(Certificate(id=f"cert-{name}", participant_id=pid, course_id=created["id"],
                       participant_name="Kim", course_name=name, workshop_title="W", module_count=1))
    db.commit()
    db.close()
    return created["id"], f"cert-{name}"


def test_delete_course_keeps_certificates_by_default_and_reports_count():
    with TestClient(app) as c:
        h = _trainer(c)
        cid, cert = _kurs_mit_zertifikat(c, h, "ZertBehalten", 900_001)
        assert c.get(f"/api/courses/{cid}/dashboard", headers=h).json()["course"]["certificate_count"] == 1

        r = c.delete(f"/api/courses/{cid}", headers=h)
        assert r.json() == {"ok": True, "certificates_deleted": 0, "certificates_kept": 1}
        assert c.get(f"/api/verify/{cert}").status_code == 200


def test_delete_course_can_delete_certificates_explicitly():
    with TestClient(app) as c:
        h = _trainer(c)
        cid, cert = _kurs_mit_zertifikat(c, h, "ZertWeg", 900_002)

        r = c.delete(f"/api/courses/{cid}?delete_certificates=true", headers=h)
        # >= 1: SQLite vergibt die Kurs-ID des Tests davor erneut (kein
        # AUTOINCREMENT), dessen behaltenes Zertifikat zaehlt hier dann mit.
        # Postgres-Sequenzen vergeben IDs nicht doppelt.
        assert r.json()["certificates_deleted"] >= 1 and r.json()["certificates_kept"] == 0
        assert c.get(f"/api/verify/{cert}").status_code == 404
