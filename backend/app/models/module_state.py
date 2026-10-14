from datetime import datetime
from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ModuleState(Base):
    """Lese-Haken und Übungsstand eines Teilnehmers in einem Modul — das, was
    frontend/src/lib/readProgress.ts und exerciseState.ts im Browser halten, als
    ein JSON-Blob ({"read": [...], "exercises": {...}}), damit er nach der
    Wiederaufnahme auf einem anderen Gerät da ist. Konfliktregel: letzter
    Schreiber gewinnt (updated_at, siehe routers/modules.py::put_state)."""
    __tablename__ = "module_state"
    __table_args__ = (UniqueConstraint("participant_id", "module_key", name="uq_module_state"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    participant_id: Mapped[int] = mapped_column(
        ForeignKey("participant.id", ondelete="CASCADE"), index=True, nullable=False)
    module_key: Mapped[str] = mapped_column(String, nullable=False)
    data: Mapped[dict] = mapped_column(JSON, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
