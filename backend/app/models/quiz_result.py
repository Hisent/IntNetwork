from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils import utc_now


class QuizResult(Base):
    __tablename__ = "quiz_result"
    # Composite-Index fuer quiz_stats (trainer_modules.py): filtert dort immer
    # zuerst auf module_key, teils zusaetzlich per Join auf participant_id ->
    # deckt beide Zugriffsmuster ab, statt ueber die ganze Tabelle zu scannen.
    __table_args__ = (Index("ix_quiz_result_module_key_participant_id", "module_key", "participant_id"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # ondelete="CASCADE": Quiz-Ergebnisse eines geloeschten Teilnehmers sind
    # toter Ballast, kein eigenstaendiger Datensatz (anders als Certificate).
    participant_id: Mapped[int] = mapped_column(
        ForeignKey("participant.id", ondelete="CASCADE"), index=True, nullable=False)
    module_key: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    answers: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
