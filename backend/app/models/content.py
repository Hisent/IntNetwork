from sqlalchemy import ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ContentModule(Base):
    __tablename__ = "content_module"
    key: Mapped[str] = mapped_column(String, primary_key=True)
    workshop_key: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    order: Mapped[int] = mapped_column(Integer)
    prerequisites: Mapped[list] = mapped_column(JSON, default=list)
    title_de: Mapped[str] = mapped_column(String)
    title_en: Mapped[str] = mapped_column(String)
    goals: Mapped[list] = mapped_column(JSON, default=list)
    scenario_de: Mapped[str] = mapped_column(Text)
    scenario_en: Mapped[str] = mapped_column(Text)


class ContentBlock(Base):
    __tablename__ = "content_block"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    module_key: Mapped[str] = mapped_column(ForeignKey("content_module.key"))
    position: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String)  # "text" | "widget" | "check" | "reveal"
    value_de: Mapped[str | None] = mapped_column(Text, nullable=True)
    value_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    widget_id: Mapped[str | None] = mapped_column(String, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    # typ-spezifische Zusatzdaten: check -> prompt/options/answer, reveal -> teaser
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class ContentQuizQuestion(Base):
    __tablename__ = "content_quiz_question"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    module_key: Mapped[str] = mapped_column(ForeignKey("content_module.key"))
    position: Mapped[int] = mapped_column(Integer)
    qtype: Mapped[str] = mapped_column(String)  # "single" | "multi" | "number"
    prompt_de: Mapped[str] = mapped_column(Text)
    prompt_en: Mapped[str] = mapped_column(Text)
    options_de: Mapped[list | None] = mapped_column(JSON, nullable=True)
    options_en: Mapped[list | None] = mapped_column(JSON, nullable=True)
    answer: Mapped[object] = mapped_column(JSON)  # int (single/number) oder list[int] (multi)


class ContentModuleSnapshot(Base):
    __tablename__ = "content_module_snapshot"
    module_key: Mapped[str] = mapped_column(ForeignKey("content_module.key"), primary_key=True)
    data: Mapped[dict] = mapped_column(JSON)
