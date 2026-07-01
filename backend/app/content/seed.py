from sqlalchemy.orm import Session

from app.content.registry import MODULES
from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion


def seed_content_if_empty(db: Session) -> None:
    if db.query(ContentModule).count() > 0:
        return
    for m in MODULES.values():
        db.add(ContentModule(
            key=m["key"], order=m["order"], pass_threshold=m.get("pass_threshold", 0.7),
            prerequisites=m.get("prerequisites", []), title_de=m["title"],
            title_en=m.get("title_en", m["title"]), goals=m.get("goals", []),
            scenario_de=m["scenario"]["de"], scenario_en=m["scenario"]["en"],
        ))
        for i, b in enumerate(m["blocks"]):
            if b["type"] == "text":
                db.add(ContentBlock(module_key=m["key"], position=i, type="text",
                                    value_de=b["value"]["de"], value_en=b["value"]["en"],
                                    note=b.get("note")))
            else:
                db.add(ContentBlock(module_key=m["key"], position=i, type="widget",
                                    widget_id=b["id"], note=b.get("note")))
        for i, q in enumerate(m["quiz"]["questions"]):
            has_options = "options" in q
            db.add(ContentQuizQuestion(
                module_key=m["key"], position=i, qtype=q["type"],
                prompt_de=q["prompt"]["de"], prompt_en=q["prompt"]["en"],
                options_de=q["options"]["de"] if has_options else None,
                options_en=q["options"]["en"] if has_options else None,
                answer=q["answer"],
            ))
    db.commit()
