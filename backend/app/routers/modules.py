import json
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion
from app.models.module_state import ModuleState
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.services.deps import get_participant
from app.services import grading
from app.services.course_membership import active_module_keys
from app.services.ratelimit import rate_limit
from app.routers.presence import touch_presence
from app.content.registry import module_meta, public_module, trainer_module
from app.utils import iso_utc, utc_now

router = APIRouter(prefix="/modules", tags=["modules"])


def estimated_minutes(db: Session, keys: set[str]) -> dict[str, int]:
    """Geschätzte Bearbeitungszeit je Modul, aus dem Umfang berechnet (kein
    Pflegefeld): Lesetext ~1000 Zeichen/min, je interaktivem Block 2 min, je
    Quizfrage 1 min; auf 5 min gerundet.
    ponytail: Faustformel über den deutschen Text; wenn Autoren abweichende
    Zeiten brauchen, ein optionales Feld je Modul ergänzen, das hier gewinnt."""
    raw: dict[str, float] = dict.fromkeys(keys, 0.0)
    for key, type_, n, chars in (db.query(ContentBlock.module_key, ContentBlock.type, func.count(),
                                          func.sum(func.length(ContentBlock.value_de)))
                                 .filter(ContentBlock.module_key.in_(keys))
                                 .group_by(ContentBlock.module_key, ContentBlock.type)):
        raw[key] += (chars or 0) / 1000 if type_ == "text" else 2 * n
    for key, n in (db.query(ContentQuizQuestion.module_key, func.count())
                   .filter(ContentQuizQuestion.module_key.in_(keys)).group_by(ContentQuizQuestion.module_key)):
        raw[key] += n
    return {key: max(5, round(minutes / 5) * 5) for key, minutes in raw.items()}


def _unavailable(db: Session, p: Participant, key: str) -> JSONResponse | None:
    """404, wenn das Modul dem Teilnehmer nicht offensteht — mit maschinenlesbarem
    Grund im Feld `code` NEBEN `detail` (das bleibt Text, wie überall):
    module_not_enabled = gibt es, ist in seinem Kurs aber abgewählt;
    module_unknown = gibt es nicht. Das Frontend zeigt je Code eine passende Meldung."""
    if key in active_module_keys(db, p.course_id):
        return None
    if db.get(ContentModule, key):
        content = {"detail": "Modul ist in diesem Kurs nicht freigeschaltet", "code": "module_not_enabled"}
    else:
        content = {"detail": "Modul nicht gefunden", "code": "module_unknown"}
    return JSONResponse(status_code=404, content=content)


@router.get("")
def list_modules(db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    active = active_module_keys(db, p.course_id)
    minutes = estimated_minutes(db, active)
    return [{**m, "minutes": minutes[m["key"]]} for m in module_meta(db) if m["key"] in active]


@router.get("/{key}")
def get_module(key: str, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    if denied := _unavailable(db, p, key):
        return denied
    pub = public_module(db, key, p.language)
    if not pub:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    return pub


class QuizSubmit(BaseModel):
    answers: dict

    @field_validator("answers")
    @classmethod
    def _begrenzt(cls, v: dict) -> dict:
        # answers landet 1:1 als JSON in quiz_result -- ohne Grenze liesse sich
        # die DB mit beliebig grossen Abgaben fuellen (60/min je IP und Modul).
        if len(json.dumps(v)) > 20_000:
            raise ValueError("Abgabe zu gross")
        return v


# Ein NAT-Klassenraum (bis ~20 Teilnehmer) teilt sich eine WAN-IP. Beim gemeinsamen
# Quiz-Ende klicken viele fast gleichzeitig ab, manche mehrfach (Doppelklick) ->
# 20 * 3 = 60 gibt der ganzen Gruppe genug Puffer und bremst nur Skript-Spam.
@router.post("/{key}/quiz", dependencies=[Depends(rate_limit(60, 60))])
def submit_quiz(key: str, data: QuizSubmit, db: Session = Depends(get_db),
                p: Participant = Depends(get_participant)):
    if denied := _unavailable(db, p, key):
        return denied
    module = trainer_module(db, key, p.language)
    if not module:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    score, total = grading.grade(module["quiz"], data.answers)
    is_passed = grading.passed(score, total)

    db.add(QuizResult(participant_id=p.id, module_key=key, score=score,
                      total=total, answers=data.answers))

    prog = db.query(Progress).filter(
        Progress.participant_id == p.id, Progress.module_key == key).first()
    if not prog:
        prog = Progress(participant_id=p.id, module_key=key, done=False)
        db.add(prog)
    if is_passed and not prog.done:
        prog.done = True
        prog.completed_at = utc_now()
    try:
        db.commit()
    except IntegrityError:
        # Doppelsubmit (z.B. Doppelklick) -> die andere Anfrage hat die
        # Progress-Zeile zwischen SELECT und COMMIT angelegt. Rollback nimmt
        # auch den QuizResult-Insert zurück, also beides neu anlegen.
        db.rollback()
        db.add(QuizResult(participant_id=p.id, module_key=key, score=score,
                          total=total, answers=data.answers))
        prog = db.query(Progress).filter(
            Progress.participant_id == p.id, Progress.module_key == key).first()
        if is_passed and not prog.done:
            prog.done = True
            prog.completed_at = utc_now()
        db.commit()

    results = db.query(QuizResult).filter(
        QuizResult.participant_id == p.id, QuizResult.module_key == key).all()
    best_pct = max((r.score / r.total for r in results if r.total), default=0)
    return {"score": score, "total": total, "passed": is_passed, "best": round(best_pct * 100),
            "details": grading.question_results(module["quiz"], data.answers),
            # Erst hier, nach der Bewertung: public_module liefert sie nicht aus.
            "explanations": {q["id"]: q["explanation"] for q in module["quiz"]["questions"]
                             if q.get("explanation")}}


@router.post("/{key}/heartbeat")
def heartbeat(key: str, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    # sonst landet jeder beliebige URL-String als current_module_key in der DB
    # und die Presence-Ansicht zeigt Rohtext an
    #
    # BEWUSST ohne Rate-Limit: heartbeat feuert alle 20s je Teilnehmer und ist ein
    # reines UPDATE auf einer bestehenden Zeile, kein Schreib-Missbrauchsrisiko wie
    # bei Kommentaren/Quiz. Hinter NAT wäre ein Limit hier zuerst die eigene
    # Klassenraum-Gruppe treffen, nicht Angreifer.
    if denied := _unavailable(db, p, key):
        return denied
    touch_presence(p, key)
    db.commit()
    return {"ok": True}


# Lese-Haken + Übungsstand je Modul (frontend/src/lib/moduleStateSync.ts). Obergrenze
# für den ganzen Blob: ein Modul hat ~15 Übungen mit je wenigen hundert Bytes Stand.
STATE_MAX_BYTES = 64_000


class ModuleStateIn(BaseModel):
    read: list[Annotated[int, Field(ge=0, le=10_000)]] = Field(default_factory=list, max_length=1_000)
    exercises: dict[Annotated[str, Field(max_length=200)], Any] = Field(default_factory=dict, max_length=500)

    @model_validator(mode="after")
    def _begrenzt(self):
        if len(json.dumps(self.model_dump())) > STATE_MAX_BYTES:
            raise ValueError("Stand zu gross")
        return self


@router.get("/{key}/state")
def get_state(key: str, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    if denied := _unavailable(db, p, key):
        return denied
    row = db.query(ModuleState).filter(ModuleState.participant_id == p.id, ModuleState.module_key == key).first()
    if not row:
        return {"read": [], "exercises": {}, "updated_at": None}
    return {**row.data, "updated_at": iso_utc(row.updated_at)}


# Gespeichert wird entprellt (~1,5 s nach der letzten Änderung); ein NAT-Klassenraum
# teilt sich die IP -> großzügig, bremst nur Skript-Spam.
@router.put("/{key}/state", dependencies=[Depends(rate_limit(600, 60))])
def put_state(key: str, data: ModuleStateIn, db: Session = Depends(get_db),
              p: Participant = Depends(get_participant)):
    """Ersetzt den ganzen Stand. Konfliktregel: letzter Schreiber gewinnt — der
    Server stempelt updated_at; der Client vergleicht beim Öffnen seinen noch
    nicht gesendeten lokalen Stand mit diesem Zeitpunkt (moduleStateSync.ts)."""
    if denied := _unavailable(db, p, key):
        return denied
    now = utc_now().replace(tzinfo=None)
    values = {"data": data.model_dump(), "updated_at": now}
    mine = db.query(ModuleState).filter(ModuleState.participant_id == p.id, ModuleState.module_key == key)
    if not mine.update(values, synchronize_session=False):
        db.add(ModuleState(participant_id=p.id, module_key=key, **values))
    try:
        db.commit()
    except IntegrityError:  # zwei Tabs speichern gleichzeitig zum ersten Mal
        db.rollback()
        mine.update(values, synchronize_session=False)
        db.commit()
    return {"updated_at": iso_utc(now)}
