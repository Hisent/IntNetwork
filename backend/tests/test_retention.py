from datetime import timedelta

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.audit_log import AuditLog
from app.models.certificate import Certificate
from app.models.comment import Comment
from app.models.course import Course
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.services import retention
from app.utils import generate_certificate_id, utc_now


def _course(db, name, joined_days_ago, **activity_days_ago):
    """Kurs mit einem Teilnehmer, der vor joined_days_ago beigetreten ist; optional
    jüngere Aktivität (last_seen/progress/quiz/comment) vor n Tagen."""
    now = utc_now()
    c = Course(name=name, join_code=f"RET{name}"[:12].upper(), workshop_key=None)
    db.add(c)
    db.flush()
    p = Participant(course_id=c.id, name=f"Person {name}", created_at=now - timedelta(days=joined_days_ago))
    if "seen" in activity_days_ago:
        p.last_seen = now - timedelta(days=activity_days_ago["seen"])
    db.add(p)
    db.flush()
    db.add(Progress(participant_id=p.id, module_key="m1", done=True,
                    completed_at=now - timedelta(days=activity_days_ago.get("progress", joined_days_ago))))
    db.add(QuizResult(participant_id=p.id, module_key="m1", score=1, total=1, answers={},
                      created_at=now - timedelta(days=activity_days_ago.get("quiz", joined_days_ago))))
    db.add(Comment(course_id=c.id, module_key="m1", block_index=0, body="x", author_kind="participant",
                   author_name=p.name, participant_id=p.id,
                   created_at=now - timedelta(days=activity_days_ago.get("comment", joined_days_ago))))
    db.add(Comment(course_id=c.id, module_key="m1", block_index=0, body="t", author_kind="trainer",
                   author_name="Trainer", participant_id=None, created_at=now - timedelta(days=400)))
    db.add(Certificate(id=generate_certificate_id(), participant_id=p.id, course_id=c.id,
                       participant_name=p.name, course_name=c.name, workshop_title="W", module_count=1))
    db.commit()
    return c.id, p.id


def test_purge_removes_only_participant_data_of_inactive_courses():
    with TestClient(app):
        pass
    db = SessionLocal()
    try:
        old, old_p = _course(db, "old", 200)
        recent_seen, _ = _course(db, "seen", 200, seen=5)
        recent_quiz, _ = _course(db, "quiz", 200, quiz=5)
        recent_comment, _ = _course(db, "cmt", 200, comment=5)

        stale = retention.stale_course_ids(db, 90)
        assert old in stale
        assert not {recent_seen, recent_quiz, recent_comment} & set(stale)

        counts = retention.purge(db, 90)
        assert counts["participants"] >= 1 and counts["progress"] >= 1
        assert counts["quiz_results"] >= 1 and counts["comments"] >= 1

        assert db.get(Course, old) is not None  # Kurs bleibt
        assert db.query(Participant).filter(Participant.course_id == old).count() == 0
        assert db.query(Progress).filter(Progress.participant_id == old_p).count() == 0
        assert db.query(QuizResult).filter(QuizResult.participant_id == old_p).count() == 0
        # Teilnehmer-Kommentar weg, Trainer-Kommentar bleibt; Bestätigung bleibt (bewusst).
        assert [c.author_kind for c in db.query(Comment).filter(Comment.course_id == old)] == ["trainer"]
        assert db.query(Certificate).filter(Certificate.participant_id == old_p).count() == 1
        for cid in (recent_seen, recent_quiz, recent_comment):
            assert db.query(Participant).filter(Participant.course_id == cid).count() == 1

        audit = db.query(AuditLog).filter(AuditLog.action == "retention.purge").order_by(AuditLog.id.desc()).first()
        assert audit.trainer_email == "system:retention"
        assert "participants=" in audit.detail and "Person" not in audit.detail

        # Idempotent: zweiter Lauf findet nichts mehr und schreibt keinen Audit-Eintrag.
        before = db.query(AuditLog).filter(AuditLog.action == "retention.purge").count()
        assert retention.purge(db, 90)["participants"] == 0
        assert db.query(AuditLog).filter(AuditLog.action == "retention.purge").count() == before
    finally:
        db.close()


def test_retention_off_by_default_starts_no_thread(monkeypatch):
    started = []
    monkeypatch.setattr(retention.threading, "Thread", lambda **kw: started.append(kw))
    monkeypatch.setattr(retention.settings, "course_retention_days", 0)
    retention.start()
    assert started == []


def test_purge_removes_module_state_review_history_and_warmup_results():
    from app.models.module_state import ModuleState
    from app.models.review import ReviewItem, Warmup, WarmupResult

    with TestClient(app):
        pass
    db = SessionLocal()
    try:
        long_ago = utc_now() - timedelta(days=200)
        old, old_p = _course(db, "st-old", 200)
        recent, recent_p = _course(db, "st-new", 200)
        warmup = Warmup(course_id=old, started_at=long_ago)
        db.add(warmup)
        db.flush()
        db.add_all([ModuleState(participant_id=old_p, module_key="m1", data={"read": [1]}, updated_at=long_ago),
                    ReviewItem(participant_id=old_p, question_id=1, last_reviewed=long_ago, streak=1),
                    WarmupResult(warmup_id=warmup.id, participant_id=old_p, answered=1, correct=1),
                    # gestern noch Übungsstand gespeichert -> Kurs gilt als aktiv
                    ModuleState(participant_id=recent_p, module_key="m1", data={},
                                updated_at=utc_now() - timedelta(days=1))])
        db.commit()

        assert old in retention.stale_course_ids(db, 90) and recent not in retention.stale_course_ids(db, 90)
        counts = retention.purge(db, 90)
        assert counts["module_state"] >= 1 and counts["review"] >= 1
        assert db.query(ModuleState).filter(ModuleState.participant_id == old_p).count() == 0
        assert db.query(ReviewItem).filter(ReviewItem.participant_id == old_p).count() == 0
        assert db.query(WarmupResult).filter(WarmupResult.participant_id == old_p).count() == 0
        assert db.query(ModuleState).filter(ModuleState.participant_id == recent_p).count() == 1
    finally:
        db.close()
