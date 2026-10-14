"""Üben und Suchen für Teilnehmer — beides nur über die im Kurs freigeschalteten
Module und ohne je etwas zu schreiben (kein QuizResult, kein Progress)."""
import json
import random
import re
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion
from app.models.participant import Participant
from app.models.quiz_result import QuizResult
from app.services import grading
from app.services.course_membership import active_module_keys
from app.services.deps import get_participant
from app.services.ratelimit import rate_limit

router = APIRouter(tags=["learning"])

PRACTICE_SIZE = 10
_QUESTION_ID = re.compile(r"[0-9]{1,9}")


def _last_answers(db: Session, p: Participant) -> dict[str, dict]:
    """Je freigeschaltetem, bereits bearbeitetem Modul die Antworten der LETZTEN
    Abgabe. Nur diese Module stehen zum Üben offen: wer ein Modul nie abgegeben
    hat, soll dessen Fragen nicht hier vorab durchprobieren."""
    active = active_module_keys(db, p.course_id)
    last: dict[str, dict] = {}
    for r in db.query(QuizResult).filter(QuizResult.participant_id == p.id).order_by(QuizResult.id):
        if r.module_key in active:
            last[r.module_key] = r.answers or {}
    return last


def as_graded(q: ContentQuizQuestion) -> dict:
    return {"type": q.qtype, "answer": q.answer}


@router.get("/practice", dependencies=[Depends(rate_limit(60, 60))])
def practice_questions(mode: str = Query("mixed", pattern="^(wrong|mixed)$"),
                       db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    """Bis zu PRACTICE_SIZE Fragen OHNE Lösung/Erklärung: zuerst die in der letzten
    Abgabe falsch beantworteten, bei mode=mixed zufällig aufgefüllt."""
    last = _last_answers(db, p)
    if not last:
        return {"questions": [], "wrong_total": 0}
    questions = db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key.in_(last)).all()
    wrong = [q for q in questions if str(q.id) in last[q.module_key]
             and not grading._correct(as_graded(q), last[q.module_key][str(q.id)])]
    random.shuffle(wrong)
    picked = wrong[:PRACTICE_SIZE]
    if mode == "mixed":
        rest = [q for q in questions if q not in wrong]
        picked += random.sample(rest, min(len(rest), PRACTICE_SIZE - len(picked)))
    return {"questions": public_questions(db, picked, p.language), "wrong_total": len(wrong)}


def public_questions(db: Session, picked: list[ContentQuizQuestion], lang: str) -> list[dict]:
    """Fragen für den Client: Text und Optionen in der Teilnehmersprache, ohne
    Lösung und Erklärung (auch von routers/review.py genutzt)."""
    titles = {m.key: (m.title_de, m.title_en) for m in
              db.query(ContentModule).filter(ContentModule.key.in_({q.module_key for q in picked}))}
    en = lang == "en"
    out = []
    for q in picked:
        qd = {"id": str(q.id), "type": q.qtype, "module_key": q.module_key,
              "module_title": titles[q.module_key][1 if en else 0],
              "prompt": q.prompt_en if en else q.prompt_de}
        if q.qtype != "number":
            qd["options"] = q.options_en if en else q.options_de
        out.append(qd)
    return out


def explanation(q: ContentQuizQuestion, lang: str) -> str | None:
    return (q.explanation_en if lang == "en" else None) or q.explanation_de


def question_by_id(db: Session, raw: str) -> ContentQuizQuestion | None:
    # Nur ASCII-Ziffern, höchstens 9: str.isdigit() lässt auch "²" durch (int() wirft),
    # und 10+ Ziffern sprengen den Integer der Datenbank.
    return db.get(ContentQuizQuestion, int(raw)) if _QUESTION_ID.fullmatch(raw) else None


class PracticeCheck(BaseModel):
    question_id: str = Field(max_length=20)
    answer: Any = None

    @field_validator("answer")
    @classmethod
    def _begrenzt(cls, v):
        if len(json.dumps(v)) > 2_000:
            raise ValueError("Antwort zu gross")
        return v


# Wie beim Quiz (60/min je IP), nur dass hier JEDE Frage einzeln geprüft wird:
# ein NAT-Klassenraum mit 20 Teilnehmern × ~12 Antworten/min = 240.
@router.post("/practice/check", dependencies=[Depends(rate_limit(240, 60))])
def practice_check(data: PracticeCheck, db: Session = Depends(get_db),
                   p: Participant = Depends(get_participant)):
    """Bewertet EINE Frage serverseitig und liefert richtig/falsch + Erklärung —
    wie das Quiz nie die Lösung selbst. Schreibt nichts: gespeicherte Ergebnisse,
    Fortschritt und Zertifikat bleiben unberührt."""
    q = question_by_id(db, data.question_id)
    if q is None or q.module_key not in _last_answers(db, p):
        raise HTTPException(status_code=404, detail="Frage nicht gefunden")
    return {"correct": grading._correct(as_graded(q), data.answer), "explanation": explanation(q, p.language)}


SEARCH_MAX_HITS = 30
# Markdown-Zeichen; der Unterstrich nur als Hervorhebung am Wortrand — in
# gather_facts oder os_family gehört er zum Wort.
_MARKUP = re.compile(r"[*`#>]+|(?<!\w)_+|_+(?!\w)")


def _plain(text: str | None) -> str:
    """Text ohne Markdown-Zeichen und mit einfachen Leerzeichen — für den
    durchsuchten Text UND den Suchbegriff, sonst träfe `--check` oder
    *wort* nie."""
    return " ".join(_MARKUP.sub("", text or "").split())


def _snippet(text: str | None, needle: str) -> str | None:
    """Ausschnitt um den ersten Treffer (ohne Markdown-Zeichen), sonst None."""
    plain = _plain(text)
    at = plain.casefold().find(needle)
    if at < 0:
        return None
    start, end = max(0, at - 60), min(len(plain), at + len(needle) + 90)
    return ("…" if start else "") + plain[start:end] + ("…" if end < len(plain) else "")


# ponytail: lädt je Anfrage die Text-Blöcke der freigeschalteten Module und sucht
# in Python (casefold, damit Umlaute auch unter SQLite stimmen). Trägt bis zu
# einigen hundert Blöcken je Kurs (heute max. ~20 Module × ~15 Text-Blöcke);
# darüber: Postgres-Volltext (tsvector + GIN) oder pg_trgm auf value_de/value_en.
@router.get("/search", dependencies=[Depends(rate_limit(60, 60))])
def search(q: str = Query(min_length=2, max_length=80), db: Session = Depends(get_db),
           p: Participant = Depends(get_participant)):
    """Sucht in Titel, Lernzielen und Text-Blöcken der FREIGESCHALTETEN Module, in
    der Teilnehmersprache. Bewusst nicht durchsucht: Quiz (Fragen, Lösungen,
    Erklärungen), Trainer-Notizen, Übungs-Payloads und nicht freigeschaltete Module."""
    needle = _plain(q).casefold()
    if len(needle) < 2:
        raise HTTPException(status_code=422, detail="Suchbegriff zu kurz")
    active = active_module_keys(db, p.course_id)
    en = p.language == "en"
    modules = db.query(ContentModule).filter(ContentModule.key.in_(active)).order_by(ContentModule.order).all()
    blocks: dict[str, list[ContentBlock]] = {}
    for b in (db.query(ContentBlock).filter(ContentBlock.module_key.in_(active), ContentBlock.type == "text")
              .order_by(ContentBlock.position)):
        blocks.setdefault(b.module_key, []).append(b)
    hits = []
    for m in modules:
        title = m.title_en if en else m.title_de
        goals = m.goals_en if en and m.goals_en and len(m.goals_en) == len(m.goals) else m.goals
        found = [("title", None, _snippet(title, needle))]
        found += [("goal", None, _snippet(g, needle)) for g in goals or []]
        found += [("text", b.uid, _snippet((b.value_en if en else None) or b.value_de, needle))
                  for b in blocks.get(m.key, [])]
        hits += [{"module_key": m.key, "module_title": title, "kind": kind, "uid": uid, "snippet": snippet}
                 for kind, uid, snippet in found if snippet]
    return {"hits": hits[:SEARCH_MAX_HITS], "more": len(hits) > SEARCH_MAX_HITS}
