from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils import utc_now


class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    join_code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    workshop_key: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
