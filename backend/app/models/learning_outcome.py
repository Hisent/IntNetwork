"""Lernerfolg je Kurs: Wissenstest vorher/nachher und anonyme Kursbewertung
(routers/learning_outcomes.py). Zustand des Tests (Fragen, offene Phase) und der
Bewertung (offen ja/nein) steht als Spalten an Course; Teilnehmer.evaluation_submitted
merkt sich nur, DASS jemand bewertet hat."""
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils import utc_now


class AssessmentAnswer(Base):
    """Abgabe EINES Teilnehmers für EINE Phase (pre/post) — personenbezogen,
    hängt per CASCADE am Teilnehmer und geht mit der Aufbewahrungslöschung."""
    __tablename__ = "assessment_answer"
    __table_args__ = (UniqueConstraint("participant_id", "phase", name="uq_assessment_answer"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    participant_id: Mapped[int] = mapped_column(
        ForeignKey("participant.id", ondelete="CASCADE"), index=True, nullable=False)
    phase: Mapped[str] = mapped_column(String, nullable=False)  # "pre" | "post"
    answers: Mapped[dict] = mapped_column(JSON, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class CourseEvaluation(Base):
    """Eine anonyme Kursbewertung. BEWUSST ohne participant_id, ohne Zeitstempel
    und mit zufälliger statt fortlaufender id: nichts in der Zeile verweist auf
    eine Person oder die Reihenfolge der Abgaben. Bleibt beim Kurs (CASCADE nur
    am Kurs), auch wenn Teilnehmerdaten gelöscht werden."""
    __tablename__ = "course_evaluation"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("course.id", ondelete="CASCADE"), index=True, nullable=False)
    overall: Mapped[int] = mapped_column(Integer, nullable=False)  # 1..5
    clarity: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Inhalt verständlich 1..5
    practice: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Praxisanteil 1..5
    pace: Mapped[str | None] = mapped_column(String, nullable=True)  # slow | ok | fast
    trainer: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Trainer 1..5
    good: Mapped[str | None] = mapped_column(Text, nullable=True)
    improve: Mapped[str | None] = mapped_column(Text, nullable=True)
