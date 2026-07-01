from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils import utc_now


class Comment(Base):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    module_key: Mapped[str] = mapped_column(String, index=True, nullable=False)
    block_index: Mapped[int] = mapped_column(Integer, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_kind: Mapped[str] = mapped_column(String, nullable=False)
    author_name: Mapped[str] = mapped_column(String, nullable=False)
    participant_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
