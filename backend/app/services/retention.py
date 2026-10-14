"""DSGVO-Aufbewahrung: löscht Teilnehmerdaten von Kursen, in denen seit
COURSE_RETENTION_DAYS Tagen kein Teilnehmer mehr aktiv war.

Aktivität = jüngster Zeitstempel aus Beitritt, Heartbeat (last_seen),
Fortschritt, Quiz-Abgabe, Wissenstest-Abgabe, Teilnehmer-Kommentar,
gespeichertem Übungs-/Lesestand und Wiederholung. Gelöscht werden die
Teilnehmer; Fortschritt, Quiz-Ergebnisse, Wissenstest-Antworten
(vorher/nachher), Kommentare, Abstimmungs-Stimmen, Übungs-/Lesestand
(module_state), Wiederholungs-Verlauf (review_item) und Aufwärm-Ergebnisse
hängen per ON DELETE CASCADE daran. Kurs, Kurs-Code, Modulauswahl,
Trainer-Kommentare, Teilnahmebestätigungen (bewusst ohne FK, siehe
models/certificate.py) und die anonymen Kursbewertungen (kein Personenbezug,
siehe models/learning_outcome.py) bleiben.

Mehrere Worker/Neustarts: jeder Lauf ist ein einziges DELETE ... WHERE in einer
Transaktion; läuft er doppelt, findet der zweite nichts mehr. Die Zahlen kommen
aus dem rowcount der eigenen DELETEs, zählen also nie doppelt. Kein In-Prozess-Lock.
"""
import logging
import threading
import time
from datetime import timedelta

from sqlalchemy import func, select, union_all
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models.comment import Comment
from app.models.learning_outcome import AssessmentAnswer
from app.models.module_state import ModuleState
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.models.review import ReviewItem, WarmupResult
from app.services.audit import log_action
from app.utils import utc_now

# warning statt info: Root-Logger steht auf WARN (alembic.ini), wie beim Content-Sync.
logger = logging.getLogger(__name__)

_SYSTEM = {"sub": "system:retention", "trainer_id": None}
_INTERVAL_SECONDS = 24 * 3600


def stale_course_ids(db: Session, days: int, now=None) -> list[int]:
    cutoff = (now or utc_now()) - timedelta(days=days)
    activity = union_all(
        select(Participant.course_id.label("cid"), Participant.created_at.label("ts")),
        select(Participant.course_id, Participant.last_seen),
        select(Participant.course_id, Progress.completed_at).join(Progress, Progress.participant_id == Participant.id),
        select(Participant.course_id, QuizResult.created_at).join(QuizResult, QuizResult.participant_id == Participant.id),
        select(Participant.course_id, AssessmentAnswer.created_at).join(
            AssessmentAnswer, AssessmentAnswer.participant_id == Participant.id),
        select(Comment.course_id, Comment.created_at).where(Comment.participant_id.isnot(None)),
        select(Participant.course_id, ModuleState.updated_at).join(ModuleState, ModuleState.participant_id == Participant.id),
        select(Participant.course_id, ReviewItem.last_reviewed).join(ReviewItem, ReviewItem.participant_id == Participant.id),
    ).subquery()
    # max() ignoriert NULL (nie gesehen / nicht abgeschlossen); created_at ist immer gesetzt.
    return list(db.scalars(
        select(activity.c.cid).group_by(activity.c.cid).having(func.max(activity.c.ts) < cutoff)))


def purge(db: Session, days: int, now=None) -> dict:
    """Ein Lauf. Gibt nur Zahlen zurück (keine Namen) und protokolliert sie."""
    stale = stale_course_ids(db, days, now)
    counts = {"courses": len(stale), "participants": 0, "progress": 0, "quiz_results": 0, "assessment_answers": 0,
              "comments": 0, "module_state": 0, "review": 0}
    if not stale:
        return counts
    pids = select(Participant.id).where(Participant.course_id.in_(stale)).scalar_subquery()
    # Kindtabellen explizit (statt nur per Kaskade), damit rowcount die Mengen liefert.
    counts["progress"] = db.query(Progress).filter(Progress.participant_id.in_(pids)).delete(synchronize_session=False)
    counts["quiz_results"] = db.query(QuizResult).filter(QuizResult.participant_id.in_(pids)).delete(synchronize_session=False)
    counts["assessment_answers"] = db.query(AssessmentAnswer).filter(
        AssessmentAnswer.participant_id.in_(pids)).delete(synchronize_session=False)
    counts["comments"] = db.query(Comment).filter(Comment.participant_id.in_(pids)).delete(synchronize_session=False)
    counts["module_state"] = db.query(ModuleState).filter(ModuleState.participant_id.in_(pids)).delete(synchronize_session=False)
    counts["review"] = db.query(ReviewItem).filter(ReviewItem.participant_id.in_(pids)).delete(synchronize_session=False)
    db.query(WarmupResult).filter(WarmupResult.participant_id.in_(pids)).delete(synchronize_session=False)
    counts["participants"] = db.query(Participant).filter(Participant.course_id.in_(stale)).delete(synchronize_session=False)
    db.commit()
    if counts["participants"]:
        detail = " ".join(f"{k}={v}" for k, v in counts.items())
        logger.warning("Aufbewahrung (%s Tage): gelöscht %s", days, detail)
        log_action(db, _SYSTEM, "retention.purge", target=f"days:{days}", detail=detail)
    return counts


def _loop(days: int) -> None:
    while True:
        db = SessionLocal()
        try:
            purge(db, days)
        except Exception:
            # Nie den Thread sterben lassen: ein Fehler heute (DB kurz weg) darf
            # die Löschung morgen nicht verhindern.
            logger.exception("Aufbewahrungs-Lauf fehlgeschlagen")
            db.rollback()
        finally:
            db.close()
        time.sleep(_INTERVAL_SECONDS)


def start() -> None:
    """Startet den täglichen Lauf (erster Lauf sofort) in einem Daemon-Thread.
    ponytail: einfacher Schlaf-Thread je Prozess statt Scheduler -- bei mehreren
    Workern läuft er mehrfach, was die Idempotenz oben abfängt; ein Neustart
    setzt den 24-h-Takt zurück (Start zählt als Lauf)."""
    days = settings.course_retention_days
    if days <= 0:
        return
    logger.warning("Aufbewahrung aktiv: Teilnehmerdaten nach %s Tagen ohne Aktivität löschen", days)
    threading.Thread(target=_loop, args=(days,), name="retention", daemon=True).start()
