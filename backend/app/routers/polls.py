"""Live-Abstimmung im Präsenz-Workshop.

Der Trainer stellt im Präsentationsmodus eine Single-Choice-Quizfrage oder
einen check-Block (Auswahl) zur Abstimmung; Teilnehmer mit offenem Modul
stimmen ab. Der gesamte Zustand liegt in der DB (live_poll, live_poll_vote) —
kein Prozessspeicher, damit mehrere Worker dasselbe sehen.

Die Abstimmung ist ungewertet: sie schreibt weder quiz_result noch progress.
Lösung, Erklärung und Verteilung gehen an Teilnehmer erst bei status=revealed.
"""
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.content import ContentBlock, ContentQuizQuestion
from app.models.course import Course
from app.models.live_poll import LivePoll, LivePollVote
from app.models.participant import Participant
from app.services.audit import log_action
from app.services.course_membership import active_module_keys
from app.services.deps import get_participant, get_trainer
from app.services.ratelimit import rate_limit

router = APIRouter(tags=["polls"])


def _question(db: Session, module_key: str, source: str, ref: str) -> dict | None:
    """Frage/Block zur Referenz, beide Sprachen samt Lösung. None, wenn es die
    Referenz im Modul nicht (mehr) gibt oder sie keine Single-Choice-Frage ist.
    `ref` trifft die stabile uid, ersatzweise die Zeilen-id (Trainer-Ansicht
    liefert bei Quizfragen nur die id)."""
    if source == "quiz":
        row = next((q for q in db.query(ContentQuizQuestion).filter(
            ContentQuizQuestion.module_key == module_key, ContentQuizQuestion.qtype == "single")
            if ref in (q.uid, str(q.id))), None)
        if not row:
            return None
        found = {"ref": row.uid or str(row.id), "prompt": (row.prompt_de, row.prompt_en),
                 "options": (row.options_de, row.options_en), "answer": row.answer,
                 "explanation": (row.explanation_de, row.explanation_en)}
    else:
        row = next((b for b in db.query(ContentBlock).filter(
            ContentBlock.module_key == module_key, ContentBlock.type == "check")
            if ref in (b.uid, str(b.id))), None)
        payload = (row.payload or {}) if row else {}
        if not row or payload.get("kind", "choice") != "choice":
            return None
        found = {"ref": row.uid or str(row.id),
                 "prompt": (payload.get("prompt_de"), payload.get("prompt_en")),
                 "options": (payload.get("options_de"), payload.get("options_en")),
                 "answer": payload.get("answer"),
                 "explanation": (payload.get("explanation_de"), payload.get("explanation_en"))}
    options, answer = found["options"][0], found["answer"]
    if (not isinstance(options, list) or len(options) < 2 or isinstance(answer, bool)
            or not isinstance(answer, int) or not 0 <= answer < len(options)):
        return None
    return found


def _current(db: Session, course_id: int) -> LivePoll | None:
    # ponytail: "höchstens eine offene je Kurs" setzt start_poll durch (schließt
    # die alten); starten zwei Trainer exakt gleichzeitig, gewinnt hier die
    # jüngste. Partieller Unique-Index, falls das je hart garantiert sein muss.
    return (db.query(LivePoll).filter(LivePoll.course_id == course_id, LivePoll.status != "closed")
            .order_by(LivePoll.id.desc()).first())


def _view(db: Session, poll: LivePoll, question: dict, lang: str, solution: bool) -> dict:
    """Feste Optionsreihenfolge (wie gespeichert) — Beamer und Teilnehmer sehen
    dieselben Buchstaben. Lösung, Erklärung und Verteilung nur mit solution=True."""
    de, en = question["options"]
    options = en if lang == "en" and isinstance(en, list) and len(en) == len(de) else de
    prompt = (question["prompt"][1] if lang == "en" else None) or question["prompt"][0] or ""
    out = {"id": poll.id, "status": poll.status, "prompt": prompt, "options": options}
    if solution:
        # Anonym: nur Summen je Option, nie participant_id.
        tally = dict(db.query(LivePollVote.choice, func.count()).filter(
            LivePollVote.poll_id == poll.id).group_by(LivePollVote.choice).all())
        out["counts"] = [tally.get(i, 0) for i in range(len(options))]
        out["votes"] = sum(out["counts"])
        out["answer"] = question["answer"]
        out["explanation"] = (question["explanation"][1] if lang == "en" else None) or question["explanation"][0]
    return out


def _close_open(db: Session, course_id: int) -> None:
    db.query(LivePoll).filter(LivePoll.course_id == course_id, LivePoll.status != "closed").update(
        {"status": "closed"}, synchronize_session=False)


def _trainer_view(db: Session, poll: LivePoll | None) -> dict | None:
    question = poll and _question(db, poll.module_key, poll.source, poll.ref)
    if not question:  # keine Abstimmung, oder die Frage wurde inzwischen gelöscht
        return None
    return {**_view(db, poll, question, "de", solution=True),
            "module_key": poll.module_key, "source": poll.source, "ref": poll.ref}


def _course(db: Session, cid: int) -> None:
    if not db.get(Course, cid):
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")


class PollStart(BaseModel):
    module_key: str = Field(max_length=200)
    source: Literal["quiz", "check"]
    ref: str = Field(max_length=200)


@router.post("/trainer/courses/{cid}/poll")
def start_poll(cid: int, data: PollStart, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    _course(db, cid)
    if data.module_key not in active_module_keys(db, cid):
        raise HTTPException(status_code=404, detail="Modul ist in diesem Kurs nicht aktiv")
    question = _question(db, data.module_key, data.source, data.ref)
    if not question:
        raise HTTPException(status_code=422, detail="Frage nicht gefunden oder keine Single-Choice-Frage")
    _close_open(db, cid)  # neue Abstimmung schließt die alte
    poll = LivePoll(course_id=cid, module_key=data.module_key, source=data.source, ref=question["ref"])
    db.add(poll)
    db.commit()
    log_action(db, trainer, "poll.start", target=f"course:{cid}",
               detail=f"{data.module_key} {data.source}:{question['ref']}")
    return _trainer_view(db, poll)


@router.get("/trainer/courses/{cid}/poll")
def trainer_poll(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    _course(db, cid)
    return _trainer_view(db, _current(db, cid))


@router.post("/trainer/courses/{cid}/poll/reveal")
def reveal_poll(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    _course(db, cid)
    poll = _current(db, cid)
    if not poll:
        raise HTTPException(status_code=404, detail="Keine laufende Abstimmung")
    poll.status = "revealed"
    db.commit()
    return _trainer_view(db, poll)


@router.delete("/trainer/courses/{cid}/poll")
def close_poll(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    _course(db, cid)
    _close_open(db, cid)
    db.commit()
    return {"ok": True}


def _require_active(db: Session, p: Participant, key: str) -> None:
    if key not in active_module_keys(db, p.course_id):
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")


# BEWUSST ohne Rate-Limit (wie heartbeat): feuert je Teilnehmer alle 5 s, rein lesend.
@router.get("/modules/{key}/poll")
def participant_poll(key: str, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    _require_active(db, p, key)
    poll = _current(db, p.course_id)  # nur der eigene Kurs
    question = poll and poll.module_key == key and _question(db, key, poll.source, poll.ref)
    if not question:
        return None
    mine = db.query(LivePollVote.choice).filter(
        LivePollVote.poll_id == poll.id, LivePollVote.participant_id == p.id).scalar()
    return {**_view(db, poll, question, p.language, solution=poll.status == "revealed"), "my_choice": mine}


class PollVote(BaseModel):
    poll_id: int
    choice: int = Field(ge=0)


# NAT-Klassenraum teilt sich eine IP; Umentscheiden ist erlaubt -> großzügig, bremst nur Skript-Spam.
@router.post("/modules/{key}/poll/vote", dependencies=[Depends(rate_limit(240, 60))])
def vote(key: str, data: PollVote, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    _require_active(db, p, key)
    poll = db.get(LivePoll, data.poll_id)
    if not poll or poll.course_id != p.course_id or poll.module_key != key:
        raise HTTPException(status_code=404, detail="Abstimmung nicht gefunden")
    if poll.status != "open":
        raise HTTPException(status_code=409, detail="Abstimmung ist beendet")
    question = _question(db, key, poll.source, poll.ref)
    if not question or data.choice >= len(question["options"][0]):
        raise HTTPException(status_code=422, detail="Ungültige Auswahl")
    # ponytail: Status-Prüfung und Schreiben sind nicht atomar — eine Stimme kann
    # Millisekunden nach "Auflösen" noch landen. Für eine ungewertete Abstimmung egal.
    mine = db.query(LivePollVote).filter(
        LivePollVote.poll_id == poll.id, LivePollVote.participant_id == p.id)
    if not mine.update({"choice": data.choice}, synchronize_session=False):
        db.add(LivePollVote(poll_id=poll.id, participant_id=p.id, choice=data.choice))
    try:
        db.commit()
    except IntegrityError:  # Doppelklick: die Parallel-Anfrage hat die Zeile gerade angelegt
        db.rollback()
        mine.update({"choice": data.choice}, synchronize_session=False)
        db.commit()
    return {"ok": True, "my_choice": data.choice}
