from sqlalchemy.orm import Session

from app.content.registry import MODULES
from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion


def seed_missing_content(db: Session) -> None:
    """Seedet alle Module, deren Key noch nicht in der DB steht — beim ersten
    Start also alles, bei Updates nur neu hinzugekommene Module. Bestehende
    (ggf. vom Trainer editierte) Module werden nie angefasst."""
    existing = {key for (key,) in db.query(ContentModule.key)}
    for m in MODULES.values():
        if m["key"] in existing:
            continue
        db.add(ContentModule(
            key=m["key"], order=m["order"],
            prerequisites=m.get("prerequisites", []), title_de=m["title"],
            title_en=m.get("title_en", m["title"]), goals=m.get("goals", []),
            scenario_de=m["scenario"]["de"], scenario_en=m["scenario"]["en"],
        ))
        db.flush()  # ContentModule-Zeile muss existieren, bevor Blocks/Quiz per FK darauf verweisen (kein relationship() -> UOW ordnet sonst nicht)
        for i, b in enumerate(m["blocks"]):
            if b["type"] == "text":
                db.add(ContentBlock(module_key=m["key"], position=i, type="text",
                                    value_de=b["value"]["de"], value_en=b["value"]["en"],
                                    note=b.get("note")))
            elif b["type"] in ("check", "reveal", "order", "debug", "reflect"):
                value = b.get("value") or {}
                db.add(ContentBlock(module_key=m["key"], position=i, type=b["type"],
                                    value_de=value.get("de"), value_en=value.get("en"),
                                    note=b.get("note"), payload=b["payload"]))
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
