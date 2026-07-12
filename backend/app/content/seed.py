import json

from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.content.registry import MODULES
from app.models.comment import Comment
from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion
from app.models.setting import Setting


LEARNING_LABS_MIGRATION = "content-migration:learning-labs-v1"
LEARNING_LAB_ANCHORS = {
    "paket": ("learning-packet", "frame-builder"),
    "subnetting": ("learning-subnet", "subnet-calc"),
    "routing": ("learning-route", "routing-demo"),
    "dns": ("learning-dns", "dns-demo"),
    "dhcp": ("learning-dhcp", "dhcp-demo"),
    "firewall": ("learning-policy", "firewall-demo"),
    "ipv6": ("learning-ipv6", "ipv6-demo"),
    "wlan": ("learning-attack", "wlan-demo"),
    "troubleshooting": ("learning-evidence", "troubleshoot-demo"),
    "wireshark": ("learning-filter", "wireshark-demo"),
}


def _migrate_learning_labs(db: Session) -> None:
    """Fügt Release-Labore genau einmal ein und setzt sie hinter ihr
    fachliches Haupt-Widget. Spätere Trainer-Änderungen bleiben unangetastet."""
    if db.get(Setting, LEARNING_LABS_MIGRATION):
        return
    for module_key, (lab_id, anchor_id) in LEARNING_LAB_ANCHORS.items():
        blocks = db.query(ContentBlock).filter(
            ContentBlock.module_key == module_key
        ).order_by(ContentBlock.position).all()
        if not blocks:
            continue
        lab = next((block for block in blocks if block.widget_id == lab_id), None)
        if lab is None:
            source = next(block for block in MODULES[module_key]["blocks"]
                          if block.get("id") == lab_id)
            lab = ContentBlock(module_key=module_key, position=len(blocks),
                               type="widget", widget_id=lab_id,
                               note=source.get("note"))
            db.add(lab)
        old_positions = {block.id: block.position for block in blocks if block.id is not None}
        ordered = [block for block in blocks if block is not lab]
        anchor_index = next(
            (i for i, block in enumerate(ordered) if block.widget_id == anchor_id),
            len(ordered) - 1,
        )
        ordered.insert(anchor_index + 1, lab)
        for position, block in enumerate(ordered):
            block.position = position
        new_positions = {block.id: block.position for block in ordered if block.id is not None}
        for comment in db.query(Comment).filter(Comment.module_key == module_key):
            matching_id = next((block_id for block_id, old_position in old_positions.items()
                                if old_position == comment.block_index), None)
            if matching_id in new_positions:
                comment.block_index = new_positions[matching_id]
    db.add(Setting(key=LEARNING_LABS_MIGRATION, value="applied"))
    db.flush()


def seed_missing_content(db: Session) -> None:
    """Seedet alle Module, deren Key noch nicht in der DB steht — beim ersten
    Start also alles, bei Updates nur neu hinzugekommene Module. Versionierte
    Release-Migrationen laufen separat und jeweils nur einmal."""
    existing = {key for (key,) in db.query(ContentModule.key)}
    legacy_pass_threshold = "pass_threshold" in {
        col["name"] for col in inspect(db.bind).get_columns("content_module")
    }
    for m in MODULES.values():
        if m["key"] in existing:
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
    _migrate_learning_labs(db)
    db.commit()
