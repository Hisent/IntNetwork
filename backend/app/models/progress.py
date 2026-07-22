from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Progress(Base):
    __tablename__ = "progress"
    __table_args__ = (UniqueConstraint("participant_id", "module_key", name="uq_progress"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # ondelete="CASCADE": Fortschritt eines geloeschten Teilnehmers ist toter
    # Ballast, kein eigenstaendiger Datensatz (anders als Certificate, siehe dort).
    participant_id: Mapped[int] = mapped_column(
        ForeignKey("participant.id", ondelete="CASCADE"), index=True, nullable=False)
    module_key: Mapped[str] = mapped_column(String, nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
