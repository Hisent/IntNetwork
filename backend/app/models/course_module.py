from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CourseModule(Base):
    """Die absichtlich aktivierte Modulmenge einer Kursdurchführung."""

    __tablename__ = "course_module"
    __table_args__ = (UniqueConstraint("course_id", "module_key", name="uq_course_module"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # ondelete="CASCADE": diese Zeilen sind reine Konfiguration einer
    # Kursdurchfuehrung, ohne Kurs bedeutungslos.
    course_id: Mapped[int] = mapped_column(
        ForeignKey("course.id", ondelete="CASCADE"), index=True, nullable=False)
    module_key: Mapped[str] = mapped_column(String, nullable=False)
