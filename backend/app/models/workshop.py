from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Workshop(Base):
    __tablename__ = "workshop"

    key: Mapped[str] = mapped_column(String, primary_key=True)
    title_de: Mapped[str] = mapped_column(String, nullable=False)
    title_en: Mapped[str] = mapped_column(String, nullable=False)
    summary_de: Mapped[str] = mapped_column(Text, nullable=False)
    summary_en: Mapped[str] = mapped_column(Text, nullable=False)
    theme: Mapped[str] = mapped_column(String, nullable=False)
    sections: Mapped[list] = mapped_column(JSON, default=list)
    context: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # "draft" (nur für Trainer sichtbar) | "published". Bestehende Workshops: published.
    status: Mapped[str] = mapped_column(String, nullable=False, default="published", server_default="published")
    # Ersteller (per MCP angelegte Workshops); NULL = eingebaut/unbekannt.
    owner_trainer_id: Mapped[int | None] = mapped_column(
        ForeignKey("trainer.id", ondelete="SET NULL"), nullable=True)
