from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils import utc_now


class TrainerCredential(Base):
    """Ein registrierter WebAuthn-Passkey eines Trainers (Zusatz zum Passwort).

    ON DELETE CASCADE auf trainer_id: wird ein Trainer gelöscht, dürfen seine
    Passkeys nicht als verwaiste Zeilen liegen bleiben und erst recht nicht
    weiter zur Anmeldung taugen. Als zweite Absicherung lädt login/verify
    (trainer_passkey.py) den Trainer nach dem Fund des Credentials zusätzlich
    erneut und lehnt bei Nichtvorhandensein ab -- genau dieser Fehler (Prüfung
    nur der Rolle im Token, nicht der Existenz) ist in diesem Projekt schon
    einmal aufgetreten (siehe services/deps.py get_trainer).

    credential_id und public_key liegen base64url-kodiert als String vor
    (Ausgabeform der webauthn-Bibliothek) statt als Rohbytes -- einfacher zu
    loggen/inspizieren, ohne eigene Kodierungsentscheidung zu treffen.
    """
    __tablename__ = "trainer_credential"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trainer_id: Mapped[int] = mapped_column(
        ForeignKey("trainer.id", ondelete="CASCADE"), nullable=False, index=True)
    credential_id: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    public_key: Mapped[str] = mapped_column(String, nullable=False)
    sign_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    transports: Mapped[str | None] = mapped_column(String, nullable=True)
    label: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
