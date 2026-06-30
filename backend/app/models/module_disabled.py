from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ModuleDisabled(Base):
    """Ein 'aus'-Eintrag für ein Modul in einem Kurs. Fehlt = aktiv."""
    __tablename__ = "module_disabled"
    __table_args__ = (UniqueConstraint("course_id", "module_key", name="uq_module_disabled"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    module_key: Mapped[str] = mapped_column(String, nullable=False)
