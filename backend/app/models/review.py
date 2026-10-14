from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils import utc_now


class ReviewItem(Base):
    """Wiederholungs-Verlauf je Teilnehmer und Quizfrage (Leitner-Kasten, siehe
    services/review.py). question_id ist die Zeilen-id der Frage — dieselbe, an
    der die Quiz-Abgaben hängen (Content-Sync behält sie je Kennung). Bewusst
    ohne FK: eine aus dem Inhalt entfernte Frage lässt die Zeile verwaisen, die
    Auswahl übergeht sie einfach."""
    __tablename__ = "review_item"
    __table_args__ = (UniqueConstraint("participant_id", "question_id", name="uq_review_item"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    participant_id: Mapped[int] = mapped_column(
        ForeignKey("participant.id", ondelete="CASCADE"), index=True, nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, nullable=False)
    last_reviewed: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    streak: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # richtige Wiederholungen in Folge


class Warmup(Base):
    """Aufwärmrunde: der Trainer schickt alle Teilnehmer eines Kurses in ihre
    persönliche Wiederholung. Aktiv = ended_at leer und jünger als
    services/review.WARMUP_MAX_AGE."""
    __tablename__ = "warmup"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("course.id", ondelete="CASCADE"), index=True, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class WarmupResult(Base):
    """Je Teilnehmer und Aufwärmrunde nur Summen (beantwortet/richtig) — der
    Trainer sieht Teilnahme und Durchschnitt, keine Einzelliste."""
    __tablename__ = "warmup_result"
    __table_args__ = (UniqueConstraint("warmup_id", "participant_id", name="uq_warmup_result"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    warmup_id: Mapped[int] = mapped_column(
        ForeignKey("warmup.id", ondelete="CASCADE"), index=True, nullable=False)
    participant_id: Mapped[int] = mapped_column(
        ForeignKey("participant.id", ondelete="CASCADE"), index=True, nullable=False)
    answered: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    correct: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
