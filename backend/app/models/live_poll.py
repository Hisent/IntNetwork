from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils import utc_now


class LivePoll(Base):
    """Live-Abstimmung im Präsenz-Workshop: der Trainer stellt eine Quizfrage
    (single) oder einen check-Block eines Moduls zur Abstimmung. Je Kurs gilt
    höchstens eine nicht geschlossene Abstimmung (routers/polls.py)."""
    __tablename__ = "live_poll"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("course.id", ondelete="CASCADE"), index=True, nullable=False)
    module_key: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)  # "quiz" | "check"
    # Stabile Kennung (uid) der Frage bzw. des Blocks; ohne uid die Zeilen-id.
    ref: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="open")  # open | revealed | closed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class LivePollVote(Base):
    __tablename__ = "live_poll_vote"
    __table_args__ = (UniqueConstraint("poll_id", "participant_id", name="uq_live_poll_vote"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    poll_id: Mapped[int] = mapped_column(
        ForeignKey("live_poll.id", ondelete="CASCADE"), index=True, nullable=False)
    participant_id: Mapped[int] = mapped_column(
        ForeignKey("participant.id", ondelete="CASCADE"), index=True, nullable=False)
    choice: Mapped[int] = mapped_column(Integer, nullable=False)
