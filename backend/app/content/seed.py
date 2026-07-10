import json

from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.content.registry import MODULES
from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion


def seed_missing_content(db: Session) -> None:
    """Seedet alle Module, deren Key noch nicht in der DB steht — beim ersten
    Start also alles, bei Updates nur neu hinzugekommene Module. Bestehende
    (ggf. vom Trainer editierte) Module werden nie angefasst."""
    existing = {key for (key,) in db.query(ContentModule.key)}
    legacy_pass_threshold = "pass_threshold" in {
        col["name"] for col in inspect(db.bind).get_columns("content_module")
    }
    for m in MODULES.values():
        if m["key"] in existing:
            # Neue Widgets werden additiv nachgezogen, ohne bestehende
            # Trainertexte, Positionen oder Quizfragen zu überschreiben.
            existing_widgets = {
                b.widget_id for b in db.query(ContentBlock)
                .filter(ContentBlock.module_key == m["key"], ContentBlock.type == "widget")
            }
            current_max = db.query(ContentBlock.position).filter(
                ContentBlock.module_key == m["key"]
            ).order_by(ContentBlock.position.desc()).first()
            next_position = (current_max[0] + 1) if current_max else 0
            for block in m["blocks"]:
                widget_id = block.get("id")
                if block.get("type") != "widget" or widget_id in existing_widgets:
                    continue
                db.add(ContentBlock(module_key=m["key"], position=next_position,
                                    type="widget", widget_id=widget_id,
                                    note=block.get("note")))
                existing_widgets.add(widget_id)
                next_position += 1
            continue
        values = {
            "key": m["key"], "order": m["order"],
            "prerequisites": m.get("prerequisites", []), "title_de": m["title"],
            "title_en": m.get("title_en", m["title"]), "goals": m.get("goals", []),
            "scenario_de": m["scenario"]["de"], "scenario_en": m["scenario"]["en"],
        }
        if legacy_pass_threshold:
            # Alte Installationen hatten eine verpflichtende, inzwischen nicht
            # mehr verwendete Spalte. Sie bleibt erhalten, wird beim Einfügen
            # neuer Module aber mit dem historischen Standardwert versorgt.
            db.execute(text("""
                INSERT INTO content_module
                (key, "order", prerequisites, title_de, title_en, goals,
                 scenario_de, scenario_en, pass_threshold)
                VALUES (:key, :order, :prerequisites, :title_de, :title_en,
                        :goals, :scenario_de, :scenario_en, :pass_threshold)
            """), {**{k: json.dumps(v, ensure_ascii=False) if isinstance(v, list) else v
                       for k, v in values.items()}, "pass_threshold": 0.7})
        else:
            db.add(ContentModule(**values))
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
