"""Live-Abstimmung im Präsenz-Workshop.

Der Trainer stellt im Präsentationsmodus eine Single-/Multiple-Choice-Quizfrage,
einen check-Block (Auswahl) oder eine eigene Frage (source "adhoc":
Mehrfachauswahl, Skala, Freitext, Wortwolke) zur Abstimmung; Teilnehmer mit
offenem Modul stimmen ab — eine Antwort je Teilnehmer, änderbar bis zur
Auflösung. Prüfung und Auswertung der Antworten: services/poll_tally.py.
Der gesamte Zustand liegt in der DB (live_poll, live_poll_vote) —
kein Prozessspeicher, damit mehrere Worker dasselbe sehen.

Die Abstimmung ist ungewertet: sie schreibt weder quiz_result noch progress.
Lösung, Erklärung und Ergebnis gehen an Teilnehmer erst bei status=revealed.
"""
from typing import Annotated, Literal

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
from app.services.poll_tally import TEXT_MAX, WORD_MAX, WORDS_MAX, parse_answer, tally, text_answers
from app.services.ratelimit import rate_limit

router = APIRouter(tags=["polls"])


def _question(db: Session, module_key: str, source: str, ref: str) -> dict | None:
    """Frage/Block zur Referenz, beide Sprachen samt Lösung. None, wenn es die
    Referenz im Modul nicht (mehr) gibt oder sie keine Single-/Multiple-Choice-
    Frage bzw. kein Auswahl-Check ist. `ref` trifft die stabile uid, ersatzweise
    die Zeilen-id (Trainer-Ansicht liefert bei Quizfragen nur die id)."""
    if source == "quiz":
        row = next((q for q in db.query(ContentQuizQuestion).filter(
            ContentQuizQuestion.module_key == module_key, ContentQuizQuestion.qtype.in_(("single", "multi")))
            if ref in (q.uid, str(q.id))), None)
        if not row:
            return None
        found = {"kind": row.qtype, "ref": row.uid or str(row.id), "prompt": (row.prompt_de, row.prompt_en),
                 "options": (row.options_de, row.options_en), "answer": row.answer,
                 "explanation": (row.explanation_de, row.explanation_en)}
    else:
        row = next((b for b in db.query(ContentBlock).filter(
            ContentBlock.module_key == module_key, ContentBlock.type == "check")
            if ref in (b.uid, str(b.id))), None)
        payload = (row.payload or {}) if row else {}
        if not row or payload.get("kind", "choice") != "choice":
            return None
        found = {"kind": "single", "ref": row.uid or str(row.id),
                 "prompt": (payload.get("prompt_de"), payload.get("prompt_en")),
                 "options": (payload.get("options_de"), payload.get("options_en")),
                 "answer": payload.get("answer"),
                 "explanation": (payload.get("explanation_de"), payload.get("explanation_en"))}
    options = found["options"][0]
    if not isinstance(options, list) or len(options) < 2:
        return None
    try:  # die Lösung muss selbst eine gültige Antwort sein
        parse_answer(found["kind"], found["answer"], len(options))
    except ValueError:
        return None
    return found


def _definition(db: Session, poll: LivePoll) -> dict | None:
    """Frage und Einstellungen einer laufenden Abstimmung: aus dem Inhalt (None,
    wenn gelöscht oder inzwischen von anderer Art) oder bei "adhoc" aus config."""
    if poll.source != "adhoc":
        found = _question(db, poll.module_key, poll.source, poll.ref)
        return found if found and found["kind"] == poll.kind else None
    c = poll.config or {}
    return {**c, "kind": poll.kind, "prompt": (c.get("prompt"), None), "options": (c.get("options"), None)}


def _current(db: Session, course_id: int) -> LivePoll | None:
    # ponytail: "höchstens eine offene je Kurs" setzt start_poll durch (schließt
    # die alten); starten zwei Trainer exakt gleichzeitig, gewinnt hier die
    # jüngste. Partieller Unique-Index, falls das je hart garantiert sein muss.
    return (db.query(LivePoll).filter(LivePoll.course_id == course_id, LivePoll.status != "closed")
            .order_by(LivePoll.id.desc()).first())


def _scale(question: dict) -> tuple[int, int]:
    return question.get("min", 1), question.get("max", 5)


def _view(db: Session, poll: LivePoll, question: dict, lang: str, solution: bool, moderator: bool = False) -> dict:
    """Feste Optionsreihenfolge (wie gespeichert) — Beamer und Teilnehmer sehen
    dieselben Buchstaben. Lösung, Erklärung und Ergebnis nur mit solution=True;
    ausgeblendete Freitexte und deren ids nur mit moderator=True (Trainer)."""
    kind = question["kind"]
    prompt = (question["prompt"][1] if lang == "en" else None) or question["prompt"][0] or ""
    out = {"id": poll.id, "kind": kind, "status": poll.status, "prompt": prompt}
    de, en = question["options"]
    options = (en if lang == "en" and isinstance(en, list) and len(en) == len(de or []) else de) or []
    if kind in ("single", "multi"):
        out["options"] = options
    if question.get("max_selections"):
        out["max_selections"] = question["max_selections"]
    if kind == "scale":
        out.update({k: question.get(k) for k in ("min", "max", "label_min", "label_max")})
    if not solution:
        return out
    # Anonym: nur Summen bzw. Texte, nie participant_id.
    if kind == "single":
        counts = dict(db.query(LivePollVote.choice, func.count()).filter(
            LivePollVote.poll_id == poll.id).group_by(LivePollVote.choice).all())
        out["counts"] = [counts.get(i, 0) for i in range(len(options))]
        out["votes"] = sum(out["counts"])
    elif kind == "text":
        out.update(text_answers(db.query(LivePollVote.id, LivePollVote.value, LivePollVote.hidden).filter(
            LivePollVote.poll_id == poll.id).all(), moderator))
    else:
        values = [v for (v,) in db.query(LivePollVote.value).filter(LivePollVote.poll_id == poll.id)]
        out.update(tally(kind, values, len(options), *_scale(question)))
    if "answer" in question:  # nur Inhaltsfragen haben eine Lösung
        out["answer"] = question["answer"]
        out["explanation"] = (question["explanation"][1] if lang == "en" else None) or question["explanation"][0]
    return out


def _close_open(db: Session, course_id: int) -> None:
    db.query(LivePoll).filter(LivePoll.course_id == course_id, LivePoll.status != "closed").update(
        {"status": "closed"}, synchronize_session=False)


def _trainer_view(db: Session, poll: LivePoll | None) -> dict | None:
    question = poll and _definition(db, poll)
    if not question:  # keine Abstimmung, oder die Frage wurde inzwischen gelöscht
        return None
    return {**_view(db, poll, question, "de", solution=True, moderator=True),
            "module_key": poll.module_key, "source": poll.source, "ref": poll.ref}


def _course(db: Session, cid: int) -> None:
    if not db.get(Course, cid):
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")


Label = Annotated[str, Field(max_length=40)]


class PollStart(BaseModel):
    module_key: str = Field(max_length=200)
    source: Literal["quiz", "check", "adhoc"]
    ref: str = Field("", max_length=200)
    # Nur source "adhoc": eigene Frage des Trainers.
    kind: Literal["multi", "scale", "text", "words"] | None = None
    prompt: str = Field("", max_length=300)
    options: list[Annotated[str, Field(max_length=120)]] = Field(default_factory=list, max_length=10)
    max_selections: int | None = Field(None, ge=1, le=10)
    min: int = Field(1, ge=0, le=1)
    max: int = Field(5, ge=2, le=10)
    label_min: Label = ""
    label_max: Label = ""


def _adhoc(data: PollStart) -> dict:
    """Definition einer eigenen Frage — nur die zur Art gehörenden Felder."""
    prompt = data.prompt.strip()
    if not data.kind or not prompt:
        raise HTTPException(status_code=422, detail="Art und Frage sind Pflicht")
    config: dict = {"prompt": prompt}
    if data.kind == "multi":
        options = [o.strip() for o in data.options]
        if len(options) < 2 or not all(options):
            raise HTTPException(status_code=422, detail="Mindestens zwei nicht leere Antworten")
        if data.max_selections and data.max_selections > len(options):
            raise HTTPException(status_code=422, detail="Höchstzahl größer als die Zahl der Antworten")
        config.update(options=options, max_selections=data.max_selections)
    elif data.kind == "scale":
        config.update({"min": data.min, "max": data.max,
                       "label_min": data.label_min.strip(), "label_max": data.label_max.strip()})
    return config


@router.post("/trainer/courses/{cid}/poll")
def start_poll(cid: int, data: PollStart, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    _course(db, cid)
    if data.module_key not in active_module_keys(db, cid):
        raise HTTPException(status_code=404, detail="Modul ist in diesem Kurs nicht aktiv")
    if data.source == "adhoc":
        config, kind, ref = _adhoc(data), data.kind, ""
    else:
        question = _question(db, data.module_key, data.source, data.ref)
        if not question:
            raise HTTPException(status_code=422, detail="Frage nicht gefunden oder keine Auswahlfrage")
        config, kind, ref = None, question["kind"], question["ref"]
    _close_open(db, cid)  # neue Abstimmung schließt die alte
    poll = LivePoll(course_id=cid, module_key=data.module_key, source=data.source, ref=ref, kind=kind, config=config)
    db.add(poll)
    db.commit()
    log_action(db, trainer, "poll.start", target=f"course:{cid}",
               detail=f"{data.module_key} {data.source}:{ref or kind}")
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


class AnswerHidden(BaseModel):
    hidden: bool


@router.patch("/trainer/courses/{cid}/poll/answers/{aid}")
def hide_answer(cid: int, aid: int, data: AnswerHidden, db: Session = Depends(get_db),
                _t: dict = Depends(get_trainer)):
    """Freitext aus- bzw. wieder einblenden, vor und nach dem Auflösen. Ändert
    der Teilnehmer ihn danach noch, bleibt er ausgeblendet."""
    _course(db, cid)
    poll = _current(db, cid)
    row = db.get(LivePollVote, aid) if poll and poll.kind == "text" else None
    if not row or row.poll_id != poll.id:
        raise HTTPException(status_code=404, detail="Antwort nicht gefunden")
    row.hidden = data.hidden
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
    question = poll and poll.module_key == key and _definition(db, poll)
    if not question:
        return None
    mine = db.query(LivePollVote.choice if poll.kind == "single" else LivePollVote.value).filter(
        LivePollVote.poll_id == poll.id, LivePollVote.participant_id == p.id).scalar()
    return {**_view(db, poll, question, p.language, solution=poll.status == "revealed"), "my_choice": mine}


# Grobe Obergrenzen schon beim Parsen; die genaue Prüfung je Art macht parse_answer.
Answer = (int | Annotated[list[int], Field(max_length=10)] | Annotated[str, Field(max_length=TEXT_MAX * 2)]
          | Annotated[list[Annotated[str, Field(max_length=WORD_MAX * 2)]], Field(max_length=WORDS_MAX)])


class PollVote(BaseModel):
    poll_id: int
    choice: Answer


# NAT-Klassenraum teilt sich eine IP; Umentscheiden ist erlaubt -> großzügig, bremst nur Skript-Spam.
# Freitext/Wortwolke laufen ebenfalls hier durch: je Teilnehmer bleibt es bei
# EINER Zeile (Upsert), die gespeicherte Textmenge ist also begrenzt.
@router.post("/modules/{key}/poll/vote", dependencies=[Depends(rate_limit(240, 60))])
def vote(key: str, data: PollVote, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    _require_active(db, p, key)
    poll = db.get(LivePoll, data.poll_id)
    if not poll or poll.course_id != p.course_id or poll.module_key != key:
        raise HTTPException(status_code=404, detail="Abstimmung nicht gefunden")
    if poll.status != "open":
        raise HTTPException(status_code=409, detail="Abstimmung ist beendet")
    question = _definition(db, poll)
    if not question:
        raise HTTPException(status_code=422, detail="Ungültige Auswahl")
    try:
        value = parse_answer(poll.kind, data.choice, len(question["options"][0] or []),
                             question.get("max_selections"), *_scale(question))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from None
    fields = {"choice": value} if poll.kind == "single" else {"value": value}
    # ponytail: Status-Prüfung und Schreiben sind nicht atomar — eine Stimme kann
    # Millisekunden nach "Auflösen" noch landen. Für eine ungewertete Abstimmung egal.
    mine = db.query(LivePollVote).filter(
        LivePollVote.poll_id == poll.id, LivePollVote.participant_id == p.id)
    if not mine.update(fields, synchronize_session=False):
        db.add(LivePollVote(poll_id=poll.id, participant_id=p.id, **fields))
    try:
        db.commit()
    except IntegrityError:  # Doppelklick: die Parallel-Anfrage hat die Zeile gerade angelegt
        db.rollback()
        mine.update(fields, synchronize_session=False)
        db.commit()
    return {"ok": True, "my_choice": value}
