from sqlalchemy.orm import Session

from app.models.content import ContentModule
from app.models.workshop import Workshop
from app.services.content_access import is_code_workshop, require_edit
from app.services.content_editor import KEY_RE, EditorError

THEMES = ("network", "claude", "infoblox", "ansible", "pki", "nac")
_FIELDS = ("title_de", "title_en", "summary_de", "summary_en", "theme", "context")


def _check(fields: dict) -> None:
    for f in ("title_de", "title_en"):
        if f in fields and not (fields[f] or "").strip():
            raise EditorError(422, "Titel darf nicht leer sein.")
    if "theme" in fields and fields["theme"] not in THEMES:
        raise EditorError(422, f"Unbekanntes Theme. Erlaubt: {', '.join(THEMES)}")


def create_workshop(db: Session, trainer: dict, key, title_de, title_en, summary_de, summary_en,
                    theme, context: dict | None) -> Workshop:
    if not KEY_RE.match(key or ""):
        raise EditorError(422, "Key darf nur a-z, 0-9 und - enthalten")
    if db.get(Workshop, key) or is_code_workshop(key):
        raise EditorError(422, "Key bereits vergeben")
    _check({"title_de": title_de, "title_en": title_en, "theme": theme})
    ws = Workshop(key=key, title_de=title_de, title_en=title_en, summary_de=summary_de,
                  summary_en=summary_en, theme=theme, sections=[], context=context,
                  status="draft", owner_trainer_id=trainer["trainer_id"])
    db.add(ws)
    db.commit()
    return ws


def _apply_sections(db: Session, ws: Workshop, sections: list[dict]) -> list[dict]:
    mods = {m.key: m for m in db.query(ContentModule).filter(ContentModule.workshop_key == ws.key)}
    named = [k for s in sections for k in s["modules"]]
    missing = sorted(set(mods) - set(named))
    dupes = sorted({k for k in named if named.count(k) > 1})
    foreign = sorted(set(named) - set(mods))
    if missing or dupes or foreign:
        raise EditorError(422, "Abschnitte müssen jedes Modul des Lehrgangs genau einmal enthalten. "
                               f"Fehlend: {missing}, doppelt: {dupes}, fremd: {foreign}")
    out, order = [], 0
    for i, s in enumerate(sections):
        start = order + 1
        for k in s["modules"]:
            order += 1
            mods[k].order = order
        out.append({"key": f"s{i + 1}", "from": start, "to": order,
                    "title_de": s["title_de"], "title_en": s["title_en"]})
    return out


def update_workshop(db: Session, trainer: dict, key: str, fields: dict,
                    sections: list[dict] | None) -> Workshop:
    ws = require_edit(db, trainer, key)
    if is_code_workshop(key):
        raise EditorError(422, "Mitgelieferte Lehrgänge werden im Code gepflegt.")
    _check(fields)
    new_sections = _apply_sections(db, ws, sections) if sections is not None else None
    for f in _FIELDS:
        if f in fields:
            setattr(ws, f, fields[f])
    if new_sections is not None:
        ws.sections = new_sections
    db.commit()
    return ws


def sections_view(db: Session, ws: Workshop) -> list[dict]:
    mods = db.query(ContentModule).filter(ContentModule.workshop_key == ws.key).order_by(
        ContentModule.order).all()
    return [{"title_de": s["title_de"], "title_en": s["title_en"],
             "modules": [m.key for m in mods if s["from"] <= m.order <= s["to"]]}
            for s in ws.sections]


def publish_workshop(db: Session, key: str) -> Workshop:
    ws = db.get(Workshop, key)
    if ws is None:
        raise EditorError(404, f"Workshop/Modul ‚{key}‘ existiert nicht.")
    if ws.status != "published":
        ws.status = "published"
        db.commit()
    return ws
