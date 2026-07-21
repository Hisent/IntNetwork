from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils import utc_now


class AuditLog(Base):
    """Protokoll mutierender Trainer-Aktionen.

    Bewusst ohne Fremdschlüssel und mit denormalisierter trainer_email: ein
    Eintrag muss lesbar bleiben, auch wenn der zugehörige Trainer- oder
    Teilnehmer-Datensatz später gelöscht wird.
    """
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    trainer_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    trainer_email: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False, index=True)
    target: Mapped[str | None] = mapped_column(String, nullable=True)
    detail: Mapped[str | None] = mapped_column(String, nullable=True)
