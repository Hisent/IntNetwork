from datetime import datetime
from sqlalchemy import DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils import utc_now


class Participant(Base):
    __tablename__ = "participant"
    __table_args__ = (UniqueConstraint("course_id", "name", name="uq_participant"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    language: Mapped[str] = mapped_column(String, default="de", nullable=False)
    current_module_key: Mapped[str | None] = mapped_column(String, nullable=True)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # Persönlicher Wiederaufnahme-Code. Nullable für Bestands-Teilnehmer, die vor
    # Einführung des Codes beigetreten sind — die dürfen weiter nur per Name fort.
    resume_code: Mapped[str | None] = mapped_column(String, nullable=True)
