"""Live-Steuerung im Präsenz-Workshop.

„Gerade aktiv / Wer hängt fest?“: wer ist in welchem Modul, wie lange schon,
wie viele Quiz-Fehlversuche dort — mit einem einfachen Hilfe-Hinweis
(stuck_reasons). Namen sieht nur der Trainer.

„Folgt mir“: der Trainer teilt, bei welchem Modul (und Block) er gerade ist;
Teilnehmer desselben Kurses fragen das per GET /follow ab und sehen einen
Hinweis — nie eine erzwungene Navigation.
"""
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.course import Course
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.services import grading
from app.services.course_membership import active_module_keys
from app.services.deps import get_participant, get_trainer
from app.content.registry import module_meta
from app.utils import iso_utc, utc_now

router = APIRouter(tags=["presence"])

STALE_AFTER_SECONDS = 30

# „Braucht evtl. Hilfe“, solange das aktuelle Modul nicht bestanden ist, wenn
#   (a) >= STUCK_FAILED_ATTEMPTS Quiz-Abgaben unter der Bestehensgrenze in diesem
#       Modul UND >= STUCK_FAILED_MINUTES im Modul, oder
#   (b) >= STUCK_LONG_MINUTES im Modul (ohne Abschluss).
# ponytail: feste Faustwerte für alle Module; an die geschätzte Bearbeitungszeit
# je Modul koppeln (modules.estimated_minutes), falls Trainer zu viele/zu wenige
# Treffer sehen. „Leerlauf bei offener Übung“ bräuchte neues Tracking — fehlt bewusst.
STUCK_FAILED_ATTEMPTS = 2
STUCK_FAILED_MINUTES = 10
STUCK_LONG_MINUTES = 40
# Länger kein Heartbeat (Pause, anderer Tag) -> die Rückkehr zählt als neuer Einstieg.
ENTER_RESET_MINUTES = 10
# ponytail: „Folgt mir“ ohne Trainer-Heartbeat — ein Stand, den seit FOLLOW_TTL
# kein Folienwechsel erneuert hat, gilt als vergessen. Heartbeat aus der
# Präsentation, falls Trainer länger auf einer Folie stehen.
FOLLOW_TTL = timedelta(hours=3)


def _naive(dt: datetime) -> datetime:
    """DB-Spalten sind zeitzonenlos (UTC); utc_now() ist zeitzonenbehaftet."""
    return dt.astimezone(timezone.utc).replace(tzinfo=None) if dt.tzinfo else dt


def stuck_reasons(minutes: float, failed: int, done: bool) -> list[str]:
    """Gründe für „braucht evtl. Hilfe“ (leer = keiner). Regeln oben."""
    if done:
        return []
    reasons = []
    if failed >= STUCK_FAILED_ATTEMPTS and minutes >= STUCK_FAILED_MINUTES:
        reasons.append("failed_attempts")
    if minutes >= STUCK_LONG_MINUTES:
        reasons.append("long_in_module")
    return reasons


def touch_presence(p: Participant, key: str) -> None:
    """Heartbeat: aktuelles Modul, zuletzt gesehen, Einstieg ins Modul."""
    now = utc_now()
    if (p.current_module_key != key or p.module_entered_at is None or p.last_seen is None
            or _naive(p.last_seen) < _naive(now) - timedelta(minutes=ENTER_RESET_MINUTES)):
        p.module_entered_at = now
    p.current_module_key = key
    p.last_seen = now


@router.get("/trainer/courses/{cid}/presence")
def course_presence(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    now = _naive(utc_now())
    cutoff = now - timedelta(seconds=STALE_AFTER_SECONDS)
    titles = {m["key"]: m["title"] for m in module_meta(db)}
    rows = db.query(Participant).filter(
        Participant.course_id == cid,
        Participant.last_seen.isnot(None),
        Participant.last_seen >= cutoff,
        Participant.current_module_key.isnot(None),
    ).all()
    pids = [p.id for p in rows]
    current = {p.id: p.current_module_key for p in rows}
    # 2 Queries für alle statt 2 je Teilnehmer; gefiltert wird in Python aufs jeweils aktuelle Modul.
    failed: dict[int, int] = {}
    for pid, key, score, total in db.query(
            QuizResult.participant_id, QuizResult.module_key, QuizResult.score, QuizResult.total
    ).filter(QuizResult.participant_id.in_(pids), QuizResult.module_key.in_(list(set(current.values())))):
        if current[pid] == key and not grading.passed(score, total):
            failed[pid] = failed.get(pid, 0) + 1
    done = {(pid, key) for pid, key in db.query(Progress.participant_id, Progress.module_key).filter(
        Progress.participant_id.in_(pids), Progress.done)}
    out = []
    for p in rows:
        minutes = int((now - _naive(p.module_entered_at)).total_seconds() // 60) if p.module_entered_at else 0
        is_done = (p.id, p.current_module_key) in done
        reasons = stuck_reasons(minutes, failed.get(p.id, 0), is_done)
        out.append({"participant_id": p.id, "name": p.name, "module_key": p.current_module_key,
                    "module_title": titles.get(p.current_module_key, p.current_module_key),
                    "minutes_in_module": minutes, "failed_attempts": failed.get(p.id, 0), "done": is_done,
                    "needs_help": bool(reasons), "reasons": reasons})
    out.sort(key=lambda e: (not e["needs_help"], e["name"]))  # wer Hilfe braucht, zuerst
    return out


def current_follow(course: Course, active: set[str]) -> dict | None:
    """Geteilte Trainer-Position oder None (nicht gesetzt, veraltet, Modul nicht mehr im Kurs)."""
    if (not course.follow_module_key or course.follow_module_key not in active
            or not course.follow_updated_at
            or _naive(course.follow_updated_at) < _naive(utc_now()) - FOLLOW_TTL):
        return None
    return {"module_key": course.follow_module_key, "block_uid": course.follow_block_uid,
            "updated_at": iso_utc(course.follow_updated_at)}


def _course(db: Session, cid: int) -> Course:
    course = db.get(Course, cid)
    if not course:
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")
    return course


class FollowSet(BaseModel):
    module_key: str = Field(max_length=200)
    block_uid: str | None = Field(None, max_length=200)


@router.put("/trainer/courses/{cid}/follow")
def set_follow(cid: int, data: FollowSet, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    # Kein Audit-Eintrag: feuert bei jedem Folienwechsel und ändert keine Daten der Teilnehmer.
    course = _course(db, cid)
    active = active_module_keys(db, cid)
    if data.module_key not in active:
        raise HTTPException(status_code=404, detail="Modul ist in diesem Kurs nicht aktiv")
    course.follow_module_key = data.module_key
    course.follow_block_uid = data.block_uid or None
    course.follow_updated_at = utc_now()
    db.commit()
    return current_follow(course, active)


@router.delete("/trainer/courses/{cid}/follow")
def clear_follow(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    course = _course(db, cid)
    course.follow_module_key = course.follow_block_uid = course.follow_updated_at = None
    db.commit()
    return {"ok": True}


# BEWUSST ohne Rate-Limit (wie heartbeat/poll): feuert je Teilnehmer alle 10 s, rein lesend.
@router.get("/follow")
def participant_follow(db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    course = db.get(Course, p.course_id)  # nur der eigene Kurs
    return current_follow(course, active_module_keys(db, p.course_id)) if course else None
