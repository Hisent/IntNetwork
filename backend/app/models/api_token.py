from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils import utc_now


class TrainerApiToken(Base):
    """Persönlicher API-Token eines Trainers (für den MCP-Endpunkt).

    Gespeichert wird nur sha256(token).hexdigest(); der Klartext (`lgt_…`) wird
    einmalig beim Anlegen angezeigt. `prefix` (erste 8 Zeichen) dient nur der
    Wiedererkennung in der Liste. ON DELETE CASCADE: mit dem Trainer
    verschwinden auch seine Tokens.
    """
    __tablename__ = "trainer_api_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trainer_id: Mapped[int] = mapped_column(
        ForeignKey("trainer.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    token_hash: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    prefix: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
