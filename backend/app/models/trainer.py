from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils import utc_now


class Trainer(Base):
    __tablename__ = "trainer"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    # Erlaubt serverseitige Invalidierung des 8-Stunden-JWTs: wird bei jedem
    # eigenen Passwortwechsel erhoeht, ins Token geschrieben und beim Pruefen
    # mit der DB verglichen (siehe app/services/deps.py::get_trainer) --
    # analog zu Participant.token_version.
    token_version: Mapped[int] = mapped_column(Integer, default=0, nullable=False, server_default="0")
