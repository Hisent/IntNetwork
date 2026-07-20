from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils import utc_now


class Certificate(Base):
    """Unveränderlicher Abschluss-Nachweis. Wird einmal je Teilnehmer ausgestellt
    (unique participant_id) und über die öffentliche ID verifizierbar. Name/Kurs/
    Modulzahl werden als Snapshot gespeichert, damit die Prüfseite ohne Zugriff
    auf Teilnehmer-/Kursdaten auskommt und spätere Änderungen sie nicht verfälschen."""
    __tablename__ = "certificate"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    participant_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    course_id: Mapped[int] = mapped_column(Integer, nullable=False)
    participant_name: Mapped[str] = mapped_column(String, nullable=False)
    course_name: Mapped[str] = mapped_column(String, nullable=False)
    workshop_title: Mapped[str] = mapped_column(String, nullable=False)
    module_count: Mapped[int] = mapped_column(Integer, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
