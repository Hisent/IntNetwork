"""Werkzeuge des MCP-Endpunkts (routers/mcp.py): Lehrgänge per KI erstellen.

Jedes Tool ist (Beschreibung, JSON-Schema der Argumente, Handler). Handler
bekommen (db, trainer, args) mit bereits geprüften Top-Level-Argumenten und
rufen dieselben Services wie der REST-Editor. Fachliche Fehler: EditorError.
Veröffentlichen und Rechte ändern gibt es hier bewusst nicht."""
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.content import ContentModule
from app.models.trainer import Trainer
from app.models.workshop import Workshop
from app.services import content_editor as ed
from app.services import workshop_editor as we
from app.services.audit import log_action
from app.services.block_validation import DECLARATIVE_TYPES
from app.services.content_access import can_edit_workshop, can_see_workshop, require_edit
from app.services.content_editor import EditorError, ModuleIn

GUIDE = Path(__file__).resolve().parents[1] / "content" / "authoring.md"
CONFLICT = ("Modul wurde inzwischen geändert. Erst get_module aufrufen, dann "
            "Änderungen auf der neuen version erneut anwenden.")
NEEDS_BASE = "Modul existiert bereits. Erst get_module aufrufen und dessen version als base_version mitgeben."
BLOCK_TYPES = ["text", "widget", "check", "order", "debug", "reflect", "reveal", *sorted(DECLARATIVE_TYPES)]

EXAMPLE_MODULE = {
    "title_de": "VLANs im Überblick", "title_en": "VLANs at a glance",
    "prerequisites": [], "goals": ["Zweck von VLANs erklären"], "goals_en": ["Explain what VLANs are for"],
    "scenario_de": "Die Buchhaltung soll vom Gäste-WLAN getrennt werden.",
    "scenario_en": "Accounting must be separated from the guest Wi-Fi.",
    "blocks": [
        {"uid": "einstieg", "type": "text",
         "value_de": "Ein VLAN teilt einen Switch in getrennte Broadcast-Domänen.",
         "value_en": "A VLAN splits one switch into separate broadcast domains."},
        {"uid": "check-trennung", "type": "check", "payload": {
            "prompt_de": "Was trennt ein VLAN?", "prompt_en": "What does a VLAN separate?",
            "options_de": ["Broadcast-Domänen", "Stromkreise"],
            "options_en": ["Broadcast domains", "Power circuits"], "answer": 0}},
    ],
    "quiz": [
        {"uid": "q-tag", "qtype": "single",
         "prompt_de": "Welcher Standard beschreibt VLAN-Tags?", "prompt_en": "Which standard defines VLAN tags?",
         "options_de": ["IEEE 802.1Q", "IEEE 802.3af"], "options_en": ["IEEE 802.1Q", "IEEE 802.3af"],
         "answer": 0,
         "explanation_de": "802.1Q fügt das 4-Byte-Tag in den Ethernet-Frame ein.",
         "explanation_en": "802.1Q inserts the 4-byte tag into the Ethernet frame."},
    ],
}


class SectionIn(BaseModel):
    title_de: str
    title_en: str
    modules: list[str]


class Tool(NamedTuple):
    description: str
    input_schema: dict
    handler: Callable[[Session, dict, dict], object]


def _missing(key: str) -> EditorError:
    return EditorError(404, f"Workshop/Modul ‚{key}‘ existiert nicht.")


def _audit(db: Session, trainer: dict, action: str, target: str) -> None:
    log_action(db, trainer, action, target=target, detail=f"via=mcp, token={trainer['token_name']}")


def _visible_ws(db: Session, trainer: dict, key: str) -> Workshop:
    ws = db.get(Workshop, key)
    if ws is None or not can_see_workshop(trainer, ws):
        raise _missing(key)
    return ws


def _module(db: Session, trainer: dict, key: str, write: bool) -> ContentModule:
    """Modul samt Rechteprüfung über seinen Workshop; Unsichtbares gilt als nicht vorhanden."""
    m = db.get(ContentModule, key)
    if m is None:
        raise _missing(key)
    try:
        _visible_ws(db, trainer, m.workshop_key or "")
    except EditorError:
        raise _missing(key) from None
    if write:
        require_edit(db, trainer, m.workshop_key)
    return m


# --- Handler -----------------------------------------------------------------

def get_authoring_guide(db: Session, trainer: dict, args: dict) -> dict:
    return {"guide": GUIDE.read_text(encoding="utf-8"), "widget_ids": sorted(ed.VALID_WIDGET_IDS),
            "block_types": BLOCK_TYPES, "themes": list(we.THEMES), "example_module": EXAMPLE_MODULE}


def list_workshops(db: Session, trainer: dict, args: dict) -> list[dict]:
    names = dict(db.query(Trainer.id, Trainer.name).all())
    return [{"key": ws.key, "title_de": ws.title_de, "title_en": ws.title_en, "status": ws.status,
             "owner": names.get(ws.owner_trainer_id), "editable": can_edit_workshop(trainer, ws)}
            for ws in db.query(Workshop).order_by(Workshop.key) if can_see_workshop(trainer, ws)]


def get_workshop(db: Session, trainer: dict, args: dict) -> dict:
    ws = _visible_ws(db, trainer, args["key"])
    mods = db.query(ContentModule).filter(ContentModule.workshop_key == ws.key).order_by(ContentModule.order)
    return {"key": ws.key, "status": ws.status, "editable": can_edit_workshop(trainer, ws),
            **{f: getattr(ws, f) for f in we._FIELDS},
            "sections": we.sections_view(db, ws),
            "modules": [{"key": m.key, "title_de": m.title_de, "title_en": m.title_en, "order": m.order}
                        for m in mods]}


def create_workshop(db: Session, trainer: dict, args: dict) -> dict:
    ws = we.create_workshop(db, trainer, args["key"], args["title_de"], args["title_en"],
                            args["summary_de"], args["summary_en"], args["theme"], args.get("context"))
    _audit(db, trainer, "workshop.create", f"workshop:{ws.key}")
    return {"key": ws.key, "status": ws.status}


def update_workshop(db: Session, trainer: dict, args: dict) -> dict:
    sections = args.get("sections")
    if sections is not None:
        sections = [SectionIn.model_validate(s).model_dump() for s in sections]
    fields = {f: args[f] for f in we._FIELDS if f in args}
    we.update_workshop(db, trainer, args["key"], fields, sections)
    _audit(db, trainer, "workshop.update", f"workshop:{args['key']}")
    return get_workshop(db, trainer, args)


def get_module(db: Session, trainer: dict, args: dict) -> dict:
    m = _module(db, trainer, args["key"], write=False)
    _, state, version = ed.module_state(db, m.key)
    return {"key": m.key, "workshop_key": m.workshop_key, "version": version, **state}


def save_module(db: Session, trainer: dict, args: dict) -> dict:
    key, workshop_key, base = args["key"], args["workshop_key"], args.get("base_version")
    m = db.get(ContentModule, key)
    if m is not None:
        _module(db, trainer, key, write=True)
        if m.workshop_key != workshop_key:
            raise EditorError(422, f"Modul ‚{key}‘ gehört zum Workshop ‚{m.workshop_key}‘.")
        if base is None:
            raise EditorError(409, NEEDS_BASE)
    else:
        require_edit(db, trainer, workshop_key)
    # order ist optional: bestehendes Modul behält seine, neues hängt sich hinten an (unten gesetzt).
    data = ModuleIn.model_validate({"order": m.order if m else 0, **args["module"]})
    ed.validate_module(db, key, data)  # vor dem Anlegen: kein leeres Modul bei Validierungsfehler
    if m is None:
        m = ed.create_module(db, key, workshop_key, data.title_de)
        _audit(db, trainer, "content.create", f"module:{key}")
        if "order" not in args["module"]:
            data.order = m.order
        base = ed.module_state(db, key)[2]
    try:
        version = ed.save_module(db, key, data, base)
    except EditorError as e:
        if e.status == 409:
            raise EditorError(409, CONFLICT) from None
        raise
    _audit(db, trainer, "content.save", f"module:{key}")
    return {"key": key, "workshop_key": workshop_key, "order": data.order, "version": version}


def restore_module(db: Session, trainer: dict, args: dict) -> dict:
    _module(db, trainer, args["key"], write=True)
    ed.restore_module(db, args["key"])
    _audit(db, trainer, "content.restore", f"module:{args['key']}")
    return {"key": args["key"], "version": ed.module_state(db, args["key"])[2]}


def delete_module(db: Session, trainer: dict, args: dict) -> dict:
    _module(db, trainer, args["key"], write=True)
    ed.delete_module(db, args["key"])
    _audit(db, trainer, "content.delete", f"module:{args['key']}")
    return {"deleted": args["key"]}


# --- Tool-Liste ----------------------------------------------------------------

_STR = {"type": "string"}
_KEY = {"type": "string", "description": "Kennung: nur a-z, 0-9 und -"}
_META = {"title_de": _STR, "title_en": _STR, "summary_de": _STR, "summary_en": _STR,
         "theme": {"type": "string", "enum": list(we.THEMES)},
         "context": {"type": "object", "description": "optionaler Lehrgangskontext (frei strukturiert)"}}


def _schema(required: tuple = (), **props) -> dict:
    return {"type": "object", "properties": props, "required": list(required), "additionalProperties": False}


TOOLS: dict[str, Tool] = {
    "get_authoring_guide": Tool(
        "Autorenreferenz (Markdown), gültige Widget-IDs, Blocktypen, Themes und ein vollständiges "
        "Beispielmodul. Vor dem ersten Schreiben IMMER zuerst aufrufen.",
        _schema(), get_authoring_guide),
    "list_workshops": Tool(
        "Alle für dich sichtbaren Lehrgänge mit status (draft/published), owner und editable.",
        _schema(), list_workshops),
    "get_workshop": Tool(
        "Metadaten eines Lehrgangs, Abschnitte [{title_de, title_en, modules:[keys]}] und Modulliste.",
        _schema(("key",), key=_KEY), get_workshop),
    "create_workshop": Tool(
        "Legt einen neuen Lehrgang als Entwurf (draft) an; du wirst Besitzer. Veröffentlichen kann nur "
        "ein Admin in der Plattform. key darf noch nicht existieren.",
        _schema(("key", "title_de", "title_en", "summary_de", "summary_en", "theme"), key=_KEY, **_META),
        create_workshop),
    "update_workshop": Tool(
        "Ändert Metadaten eines eigenen Lehrgangs. sections legt Abschnitte und Modulreihenfolge fest: "
        "jedes Modul des Lehrgangs muss in genau einem Abschnitt stehen; der Server vergibt order. Eine Änderung an sections ändert die Reihenfolge und damit die version "
        "aller Module des Lehrgangs: vor dem nächsten save_module get_module erneut aufrufen.",
        _schema(("key",), key=_KEY, **_META, sections={"type": "array", "items": _schema(
            ("title_de", "title_en", "modules"), title_de=_STR, title_en=_STR,
            modules={"type": "array", "items": _STR})}),
        update_workshop),
    "get_module": Tool(
        "Vollständiges Modul in der Form von save_module.module plus version. Vor jeder Änderung an "
        "einem bestehenden Modul aufrufen und version als base_version an save_module geben.",
        _schema(("key",), key=_KEY), get_module),
    "save_module": Tool(
        "Speichert ein Modul vollständig (ersetzt Blöcke und Quiz). Neues Modul: ohne base_version, "
        "wird am Ende des Lehrgangs angelegt. Bestehendes Modul: base_version = version aus get_module "
        "ist Pflicht. module hat die Felder des Beispielmoduls aus get_authoring_guide; order optional. "
        "Liefert die neue version.",
        _schema(("key", "workshop_key", "module"), key=_KEY, workshop_key=_KEY,
                module={"type": "object", "description": "Modulinhalt (title_de/en, goals, scenario_de/en, "
                        "blocks, quiz, …) wie example_module"},
                base_version=_STR),
        save_module),
    "restore_module": Tool(
        "Stellt den Stand vor dem letzten Speichern wieder her (tauscht aktuellen Stand und Snapshot).",
        _schema(("key",), key=_KEY), restore_module),
    "delete_module": Tool(
        "Löscht ein Modul samt Blöcken und Quiz. Nur in Lehrgängen im Status draft.",
        _schema(("key",), key=_KEY), delete_module),
}
