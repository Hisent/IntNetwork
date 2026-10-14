"""Lernerfolg messen: Wissenstest vorher/nachher, anonyme Kursbewertung, CSV-Export.

Wissenstest: je Kurs EIN Fragensatz aus den Quizfragen der aktiven Module (je
Modul 1–2, höchstens MAX_QUESTIONS), deterministisch aus Kurs-id + Seed gezogen
und beim ersten Öffnen festgeschrieben — Eingangs- und Abschlusstest sind damit
dieselben Fragen. Je Teilnehmer und Phase genau eine Abgabe (Unique-Constraint).
Nach dem Eingangstest nur die Punktzahl (nicht auf den Test hin lehren), nach dem
Abschlusstest auch richtig/falsch und Erklärungen. Schreibt weder quiz_result
noch progress: Fortschritt und Teilnahmebestätigung bleiben unberührt.

Kursbewertung: anonym. Die Antwortzeile (course_evaluation) trägt weder
participant_id noch Zeitstempel und hat eine zufällige id; am Teilnehmer steht
nur das Flag evaluation_submitted. Flag und Zeile entstehen in EINER Transaktion,
das bedingte UPDATE auf das Flag verhindert Doppelabgaben. Trainer-Ansicht und CSV
zeigen Inhalte erst ab MIN_EVALUATIONS Abgaben. Grenze der Anonymität
(bewusst, siehe docs/confluence/04-trainer-handbuch.md): bei sehr kleinen Gruppen
oder wenn der Trainer live zusieht, wer gerade abgibt, lässt sich eine Antwort
über die Zahl der Abgaben einer Person zuordnen; mit DB-Zugriff zusätzlich über
die physische Reihenfolge der Zeilen.
"""
import random
import secrets
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.content.registry import module_meta
from app.database import get_db
from app.models.content import ContentModule, ContentQuizQuestion
from app.models.course import Course
from app.models.learning_outcome import AssessmentAnswer, CourseEvaluation
from app.models.participant import Participant
from app.models.quiz_result import QuizResult
from app.routers.modules import QuizSubmit
from app.services import grading
from app.services.audit import log_action
from app.services.course_membership import active_module_keys
from app.services.csv_export import csv_response
from app.services.deps import get_participant, get_trainer
from app.services.ratelimit import rate_limit
from app.utils import iso_utc

router = APIRouter(tags=["learning-outcomes"])

MAX_QUESTIONS = 15
SCALES = ("overall", "clarity", "practice", "trainer")
PACES = ("slow", "ok", "fast")
# Kursbewertung: Mittelwerte, Verteilung und Freitexte erst ab so vielen Abgaben
# (Trainer-Ansicht und CSV) -- darunter ließe sich eine Antwort zu leicht einer
# Person zuordnen. Bis dahin nur die Zahl der Abgaben.
MIN_EVALUATIONS = 3


# --- Fragensatz -------------------------------------------------------------

def draw_questions(by_module: list[list[str]], seed: str) -> list[str]:
    """Gleiche Eingabe + gleicher Seed -> gleiche Fragen (random.Random mit
    str-Seed ist prozessübergreifend stabil). Je Modul 2 Fragen, solange das
    unter MAX_QUESTIONS bleibt, sonst 1; Reihenfolge = Kurs-/Fragenreihenfolge."""
    by_module = [ids for ids in by_module if ids]
    rng = random.Random(seed)
    per = 2 if 2 * len(by_module) <= MAX_QUESTIONS else 1
    picked = [ids[i] for ids in by_module for i in sorted(rng.sample(range(len(ids)), min(per, len(ids))))]
    if len(picked) > MAX_QUESTIONS:
        picked = [picked[i] for i in sorted(rng.sample(range(len(picked)), MAX_QUESTIONS))]
    return picked


def _draw(db: Session, course: Course) -> list[str]:
    active = active_module_keys(db, course.id)
    order = {m.key: m.order for m in db.query(ContentModule).filter(ContentModule.key.in_(active))}
    by_module: dict[str, list[str]] = {}
    for q in (db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key.in_(active))
              .order_by(ContentQuizQuestion.position, ContentQuizQuestion.id)):
        by_module.setdefault(q.module_key, []).append(str(q.id))
    keys = sorted(by_module, key=lambda k: (order.get(k, 0), k))
    return draw_questions([by_module[k] for k in keys], f"{course.id}:{course.assessment_seed}")


def _question_ids(db: Session, course: Course) -> list[str]:
    """Festgeschriebener Satz, vor dem ersten Öffnen die Vorschau (dieselbe Ziehung)."""
    return course.assessment_questions if course.assessment_questions is not None else _draw(db, course)


def _questions(db: Session, ids: list[str]) -> list[ContentQuizQuestion]:
    """In Satz-Reihenfolge; inzwischen gelöschte Fragen fallen heraus."""
    rows = {str(q.id): q for q in db.query(ContentQuizQuestion).filter(
        ContentQuizQuestion.id.in_([int(i) for i in ids]))} if ids else {}
    return [rows[i] for i in ids if i in rows]


def _quiz(qs: list[ContentQuizQuestion]) -> dict:
    return {"questions": [{"id": str(q.id), "type": q.qtype, "answer": q.answer} for q in qs]}


def _public(q: ContentQuizQuestion, lang: str) -> dict:
    en = lang == "en"
    out = {"id": str(q.id), "type": q.qtype, "module_key": q.module_key,
           "prompt": (q.prompt_en if en else None) or q.prompt_de}
    if q.qtype != "number":
        out["options"] = (q.options_en if en and q.options_en else None) or q.options_de
    return out


def _explanation(q: ContentQuizQuestion, lang: str) -> str | None:
    return (q.explanation_en if lang == "en" else None) or q.explanation_de


def _pct(a: AssessmentAnswer | None) -> int | None:
    return round(a.score * 100 / a.total) if a and a.total else None


def _mean(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 1) if values else None


def _course(db: Session, cid: int) -> Course:
    course = db.get(Course, cid)
    if not course:
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")
    return course


def _assessment_view(db: Session, course: Course) -> dict:
    qs = _questions(db, _question_ids(db, course))
    participants = db.query(Participant).filter(Participant.course_id == course.id).order_by(Participant.name).all()
    answers = {(a.participant_id, a.phase): a for a in db.query(AssessmentAnswer).filter(
        AssessmentAnswer.participant_id.in_([p.id for p in participants]))}
    rows, gains = [], []
    for p in participants:
        pre, post = answers.get((p.id, "pre")), answers.get((p.id, "post"))
        if pre and post and pre.total and post.total:
            gains.append(_pct(post) - _pct(pre))
        rows.append({"id": p.id, "name": p.name, "pre": _pct(pre), "post": _pct(post)})
    quiz = _quiz(qs)
    stats = {phase: grading.question_stats(quiz, [a.answers for (_pid, ph), a in answers.items() if ph == phase])
             for phase in ("pre", "post")}
    titles = {m["key"]: m["title"] for m in module_meta(db)}
    return {
        "phase": course.assessment_phase, "fixed": course.assessment_questions is not None,
        "answered": bool(answers),
        "questions": [{**_public(q, "de"), "module_title": titles.get(q.module_key, q.module_key),
                       "answer": q.answer, "explanation": q.explanation_de,
                       "pre_correct": pre["correct"], "pre_attempts": pre["attempts"],
                       "post_correct": post["correct"], "post_attempts": post["attempts"]}
                      for q, pre, post in zip(qs, stats["pre"], stats["post"], strict=True)],
        "participants": rows,
        "summary": {"pre_count": sum(1 for r in rows if r["pre"] is not None),
                    "post_count": sum(1 for r in rows if r["post"] is not None),
                    "avg_pre": _mean([r["pre"] for r in rows if r["pre"] is not None]),
                    "avg_post": _mean([r["post"] for r in rows if r["post"] is not None]),
                    # nur Teilnehmer mit beiden Tests -- sonst verzerren Nachzügler den Zuwachs
                    "avg_gain": _mean(gains), "gain_count": len(gains)},
    }


# --- Wissenstest: Trainer ---------------------------------------------------

@router.get("/trainer/courses/{cid}/assessment")
def trainer_assessment(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    return _assessment_view(db, _course(db, cid))


class PhaseIn(BaseModel):
    phase: Literal["pre", "post"] | None


@router.put("/trainer/courses/{cid}/assessment")
def set_assessment_phase(cid: int, data: PhaseIn, db: Session = Depends(get_db),
                         trainer: dict = Depends(get_trainer)):
    """Eingangs- oder Abschlusstest öffnen (None = schließen). Das erste Öffnen
    schreibt den Fragensatz fest."""
    course = _course(db, cid)
    if data.phase and course.assessment_questions is None:
        ids = _draw(db, course)
        if not ids:
            raise HTTPException(status_code=422, detail="Die aktiven Module haben keine Quizfragen.")
        course.assessment_questions = ids
    course.assessment_phase = data.phase
    db.commit()
    log_action(db, trainer, "assessment.phase", target=f"course:{cid}", detail=f"phase={data.phase}")
    return _assessment_view(db, course)


@router.post("/trainer/courses/{cid}/assessment/regenerate")
def regenerate_assessment(cid: int, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    """Neue Ziehung — nur solange niemand geantwortet hat, sonst wären vorher und
    nachher nicht mehr dieselben Fragen."""
    course = _course(db, cid)
    if db.query(AssessmentAnswer.id).join(Participant).filter(Participant.course_id == cid).first():
        raise HTTPException(status_code=409, detail="Es gibt schon Antworten — der Fragensatz bleibt.")
    course.assessment_seed += 1
    if course.assessment_questions is not None:
        course.assessment_questions = _draw(db, course) or course.assessment_questions
    db.commit()
    log_action(db, trainer, "assessment.regenerate", target=f"course:{cid}")
    return _assessment_view(db, course)


# --- Wissenstest: Teilnehmer ------------------------------------------------

def _result(a: AssessmentAnswer, qs: list[ContentQuizQuestion], lang: str) -> dict:
    out = {"score": a.score, "total": a.total}
    if a.phase == "post":  # erst nach dem Abschlusstest: richtig/falsch + Erklärungen
        out["details"] = grading.question_results(_quiz(qs), a.answers)
        out["explanations"] = {str(q.id): e for q in qs if (e := _explanation(q, lang))}
    return out


@router.get("/assessment")
def participant_assessment(db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    """Offener Test des eigenen Kurses (None = keiner). Fragen ohne Lösung; nach
    der Abgabe das Ergebnis (beim Eingangstest nur die Punktzahl)."""
    course = db.get(Course, p.course_id)
    phase = course.assessment_phase if course and course.assessment_questions else None
    if not phase:
        return None
    qs = _questions(db, course.assessment_questions)
    mine = db.query(AssessmentAnswer).filter(
        AssessmentAnswer.participant_id == p.id, AssessmentAnswer.phase == phase).first()
    return {"phase": phase,
            "questions": [_public(q, p.language) for q in qs] if not mine or phase == "post" else [],
            "result": _result(mine, qs, p.language) if mine else None}


class AssessmentSubmit(QuizSubmit):
    phase: Literal["pre", "post"]


@router.post("/assessment", dependencies=[Depends(rate_limit(60, 60))])
def submit_assessment(data: AssessmentSubmit, db: Session = Depends(get_db),
                      p: Participant = Depends(get_participant)):
    course = db.get(Course, p.course_id)
    # phase im Body: hat der Trainer inzwischen umgeschaltet, landet die Abgabe nicht in der falschen Phase.
    if not course or course.assessment_phase != data.phase or not course.assessment_questions:
        raise HTTPException(status_code=409, detail="Dieser Test ist nicht (mehr) geöffnet.")
    qs = _questions(db, course.assessment_questions)
    known = {str(q.id) for q in qs}
    answers = {k: v for k, v in data.answers.items() if k in known}
    score, total = grading.grade(_quiz(qs), answers)
    row = AssessmentAnswer(participant_id=p.id, phase=data.phase, answers=answers, score=score, total=total)
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Du hast diesen Test schon abgegeben.") from None
    return _result(row, qs, p.language)


def open_tasks(db: Session, p: Participant, course: Course | None) -> dict:
    """Für GET /me: was der Teilnehmer gerade tun kann (Hinweiskarte auf der Kursseite)."""
    if not course:
        return {"assessment": None, "evaluation": False}
    phase = course.assessment_phase if course.assessment_questions else None
    if phase and db.query(AssessmentAnswer.id).filter(
            AssessmentAnswer.participant_id == p.id, AssessmentAnswer.phase == phase).first():
        phase = None
    return {"assessment": phase, "evaluation": course.evaluation_open and not p.evaluation_submitted}


# --- Kursbewertung ----------------------------------------------------------

def _evaluation_summary(rows: list[CourseEvaluation]) -> dict:
    out: dict = {"count": len(rows), "min_count": MIN_EVALUATIONS, "hidden": len(rows) < MIN_EVALUATIONS}
    if out["hidden"]:
        return out
    out["pace"] = {k: sum(1 for r in rows if r.pace == k) for k in PACES}
    for field in SCALES:
        values = [v for r in rows if (v := getattr(r, field)) is not None]
        out[field] = {"n": len(values), "mean": _mean(values), "counts": [values.count(i) for i in range(1, 6)]}
    for field in ("good", "improve"):
        texts = [t for r in rows if (t := getattr(r, field))]
        random.shuffle(texts)  # Reihenfolge der Abgabe soll nichts verraten
        out[field] = texts
    return out


@router.get("/trainer/courses/{cid}/evaluation")
def trainer_evaluation(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    course = _course(db, cid)
    rows = db.query(CourseEvaluation).filter(CourseEvaluation.course_id == cid).all()
    return {"open": course.evaluation_open, **_evaluation_summary(rows)}


class EvaluationToggle(BaseModel):
    open: bool


@router.put("/trainer/courses/{cid}/evaluation")
def set_evaluation_open(cid: int, data: EvaluationToggle, db: Session = Depends(get_db),
                        trainer: dict = Depends(get_trainer)):
    course = _course(db, cid)
    course.evaluation_open = data.open
    db.commit()
    log_action(db, trainer, "evaluation.toggle", target=f"course:{cid}", detail=f"open={data.open}")
    return trainer_evaluation(cid, db, trainer)


Rating = Annotated[int | None, Field(ge=1, le=5)]


class EvaluationIn(BaseModel):
    overall: int = Field(ge=1, le=5)
    clarity: Rating = None
    practice: Rating = None
    pace: Literal["slow", "ok", "fast"] | None = None
    trainer: Rating = None
    good: str = Field("", max_length=2000)
    improve: str = Field("", max_length=2000)


@router.post("/evaluation", dependencies=[Depends(rate_limit(60, 60))])
def submit_evaluation(data: EvaluationIn, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    course = db.get(Course, p.course_id)
    if not course or not course.evaluation_open:
        raise HTTPException(status_code=409, detail="Die Kursbewertung ist nicht geöffnet.")
    # Bedingtes UPDATE = Sperre gegen Doppelabgaben (auch bei zwei parallelen
    # Anfragen gewinnt genau eine). Flag und anonyme Zeile in derselben Transaktion.
    claimed = db.query(Participant).filter(
        Participant.id == p.id, Participant.evaluation_submitted.is_(False)
    ).update({"evaluation_submitted": True}, synchronize_session=False)
    if not claimed:
        raise HTTPException(status_code=409, detail="Du hast den Kurs schon bewertet.")
    db.add(CourseEvaluation(id=secrets.token_hex(12), course_id=p.course_id,
                            **data.model_dump(exclude={"good", "improve"}),
                            good=data.good.strip() or None, improve=data.improve.strip() or None))
    db.commit()
    return {"ok": True}


# --- CSV-Export -------------------------------------------------------------

_H = {
    "de": {"name": "Teilnehmer", "done": "Module erledigt", "best": "Bestwert % {t}", "last": "Letzte Aktivität (UTC)",
           "module": "Modul", "question": "Frage", "correct": "Richtig", "attempts": "Versuche", "rate": "Quote %",
           "pre": "Eingangstest %", "post": "Abschlusstest %", "gain": "Zuwachs (Prozentpunkte)",
           "pre_c": "Eingangstest richtig", "post_c": "Abschlusstest richtig", "avg": "Durchschnitt",
           "item": "Frage", "n": "Antworten", "mean": "Mittelwert", "count": "Abgaben",
           "overall": "Gesamteindruck", "clarity": "Inhalt verständlich", "practice": "Praxisanteil",
           "trainer": "Trainer", "pace": "Tempo", "slow": "zu langsam", "ok": "passend", "fast": "zu schnell",
           "good": "Was war gut?", "improve": "Was verbessern?", "kind": "Art", "text": "Text",
           "hidden": "Ergebnisse erst ab {n} Abgaben (Anonymität)."},
    "en": {"name": "Participant", "done": "Modules done", "best": "Best % {t}", "last": "Last activity (UTC)",
           "module": "Module", "question": "Question", "correct": "Correct", "attempts": "Attempts", "rate": "Rate %",
           "pre": "Pre-test %", "post": "Post-test %", "gain": "Gain (percentage points)",
           "pre_c": "Pre-test correct", "post_c": "Post-test correct", "avg": "Average",
           "item": "Item", "n": "Answers", "mean": "Mean", "count": "Submissions",
           "overall": "Overall", "clarity": "Content clear", "practice": "Hands-on share",
           "trainer": "Trainer", "pace": "Pace", "slow": "too slow", "ok": "right", "fast": "too fast",
           "good": "What was good?", "improve": "What to improve?", "kind": "Type", "text": "Text",
           "hidden": "Results only from {n} submissions on (anonymity)."},
}


def _dashboard_rows(db: Session, course: Course, h: dict, lang: str) -> list[list]:
    from app.routers.courses import dashboard  # ponytail: Routenfunktion direkt aufgerufen = dieselben Zahlen wie im UI
    dash = dashboard(course.id, db, None)
    titles = {m["key"]: (m["title_en"] if lang == "en" and m["title_en"] else m["title"]) for m in dash["modules"]}
    pids = [r["id"] for r in dash["participants"]]
    last_quiz = dict(db.query(QuizResult.participant_id, func.max(QuizResult.created_at))
                     .filter(QuizResult.participant_id.in_(pids)).group_by(QuizResult.participant_id).all())
    seen = {p.id: max(t for t in (p.created_at, p.last_seen, last_quiz.get(p.id)) if t)
            for p in db.query(Participant).filter(Participant.id.in_(pids))}
    rows = [[h["name"], h["done"], *[h["best"].format(t=titles[k]) for k in titles], h["last"]]]
    for r in dash["participants"]:
        cells = r["cells"]
        rows.append([r["name"], f"{sum(c['done'] for c in cells.values())}/{len(titles)}",
                     *[cells[k]["best"] for k in titles], iso_utc(seen[r["id"]])[:16].replace("T", " ")])
    return rows


def _quiz_rows(db: Session, course: Course, h: dict, lang: str) -> list[list]:
    active = active_module_keys(db, course.id)
    pids = [pid for (pid,) in db.query(Participant.id).filter(Participant.course_id == course.id)]
    rows = [[h["module"], h["question"], h["correct"], h["attempts"], h["rate"]]]
    for m in module_meta(db):
        if m["key"] not in active:
            continue
        qs = db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key == m["key"]).order_by(
            ContentQuizQuestion.position).all()
        submissions = [a for (a,) in db.query(QuizResult.answers).filter(
            QuizResult.module_key == m["key"], QuizResult.participant_id.in_(pids))]
        title = m["title_en"] if lang == "en" and m["title_en"] else m["title"]
        for q, s in zip(qs, grading.question_stats(_quiz(qs), submissions), strict=True):
            rows.append([title, _public(q, lang)["prompt"], s["correct"], s["attempts"],
                         round(s["correct"] * 100 / s["attempts"]) if s["attempts"] else None])
    return rows


def _assessment_rows(db: Session, course: Course, h: dict, _lang: str) -> list[list]:
    view = _assessment_view(db, course)
    s = view["summary"]
    rows = [[h["name"], h["pre"], h["post"], h["gain"]]]
    for r in view["participants"]:
        gain = r["post"] - r["pre"] if r["pre"] is not None and r["post"] is not None else None
        rows.append([r["name"], r["pre"], r["post"], gain])
    rows += [[h["avg"], s["avg_pre"], s["avg_post"], s["avg_gain"]], [],
             [h["module"], h["question"], h["pre_c"], h["attempts"], h["post_c"], h["attempts"]]]
    rows += [[q["module_title"], q["prompt"], q["pre_correct"], q["pre_attempts"], q["post_correct"],
              q["post_attempts"]] for q in view["questions"]]
    return rows


def _evaluation_rows(db: Session, course: Course, h: dict, _lang: str) -> list[list]:
    s = _evaluation_summary(db.query(CourseEvaluation).filter(CourseEvaluation.course_id == course.id).all())
    if s["hidden"]:
        return [[h["count"], s["count"]], [], [h["hidden"].format(n=MIN_EVALUATIONS)]]
    rows = [[h["count"], s["count"]], [], [h["item"], h["n"], h["mean"], "1", "2", "3", "4", "5"]]
    rows += [[h[f], s[f]["n"], s[f]["mean"], *s[f]["counts"]] for f in SCALES]
    rows += [[], [h["pace"], h["slow"], h["ok"], h["fast"]], ["", *[s["pace"][k] for k in PACES]],
             [], [h["kind"], h["text"]]]
    rows += [[h[f], t] for f in ("good", "improve") for t in s[f]]
    return rows


_EXPORTS = {"dashboard": _dashboard_rows, "quiz": _quiz_rows,
            "assessment": _assessment_rows, "evaluation": _evaluation_rows}


@router.get("/trainer/courses/{cid}/export/{kind}")
def export_csv(cid: int, kind: Literal["dashboard", "quiz", "assessment", "evaluation"],
               lang: Literal["de", "en"] = "de", db: Session = Depends(get_db),
               trainer: dict = Depends(get_trainer)):
    """CSV für Excel. Gleiche Berechtigung wie das Kurs-Dashboard (jeder Trainer)."""
    course = _course(db, cid)
    rows = _EXPORTS[kind](db, course, _H[lang], lang)
    # Export personenbezogener Daten -> nachvollziehbar im Audit-Log
    log_action(db, trainer, "course.export", target=f"course:{cid}", detail=kind)
    return csv_response(rows, f"intlab-kurs{cid}-{kind}.csv")
