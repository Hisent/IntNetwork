import json
import re
from collections import defaultdict, deque

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.content.registry import MODULES
from app.database import get_db
from app.models.comment import Comment
from app.models.content import ContentBlock, ContentModule, ContentModuleSnapshot, ContentQuizQuestion
from app.models.workshop import Workshop
from app.services.audit import log_action
from app.services.deps import get_trainer

router = APIRouter(prefix="/trainer/content/modules", tags=["trainer-content"])

# Muss synchron zu frontend/src/widgets/registry.tsx (WIDGETS-Objekt) gepflegt werden.
VALID_WIDGET_IDS = {
    "ansible-lab",
    "mcp-inspector", "agent-orchestrator",
    "tokenizer-demo", "cli-simulator", "permission-simulator", "hook-lifecycle",
    "vlan-switch", "frame-builder", "osi-model", "mac-learning", "subnet-calc",
    "arp-demo", "routing-demo", "nat-demo", "dns-demo", "dhcp-demo", "ports-demo",
    "icmp-demo", "firewall-demo", "ipv6-demo", "wlan-demo", "vpn-demo",
    "troubleshoot-demo", "capstone-demo", "wireshark-demo",
    "learning-route", "learning-policy", "learning-dhcp", "learning-dns",
    "learning-packet", "learning-subnet", "learning-filter", "learning-attack",
    "learning-ipv6", "learning-evidence",
    "visual-topology", "visual-encapsulation", "visual-subnet-map",
    "visual-firewall-flow", "visual-dns-tree",
    "visual-vlan-tag-path", "visual-arp-resolution", "visual-route-match",
    "visual-nat-translation", "visual-dhcp-lease", "visual-tcp-session",
    "visual-ipv6-autoconfig",
    "visual-bitmask", "visual-broadcast-storm", "visual-dhcp-relay",
    "visual-ephemeral-ports", "visual-stateful-firewall",
    "crypto-hash", "crypto-aead", "crypto-keyexchange",
    "cert-inspector", "cert-chain", "tls-handshake-demo", "cert-errors",
    "ospf-demo", "redundancy-demo",
    "openssl-lab", "git-lab",
    "dot1x-flow", "nac-policy", "nac-posture", "nac-deployment",
}

KEY_RE = re.compile(r"^[a-z0-9-]+$")


class BlockIn(BaseModel):
    type: str
    value_de: str | None = None
    value_en: str | None = None
    widget_id: str | None = None
    note: str | None = None
    payload: dict | None = None


class QuestionIn(BaseModel):
    qtype: str
    prompt_de: str
    prompt_en: str
    options_de: list[str] | None = None
    options_en: list[str] | None = None
    answer: int | list[int]


class ModuleIn(BaseModel):
    title_de: str
    title_en: str
    order: int
    prerequisites: list[str] = []
    goals: list[str] = []
    scenario_de: str
    scenario_en: str
    blocks: list[BlockIn]
    quiz: list[QuestionIn]


class ModuleCreateIn(BaseModel):
    key: str
    title_de: str
    workshop_key: str = "network"


def _meta(m: ContentModule) -> dict:
    return {"key": m.key, "title_de": m.title_de, "title_en": m.title_en,
            "order": m.order, "workshop_key": m.workshop_key}


def _load_blocks_and_quiz(db: Session, key: str) -> tuple[list[ContentBlock], list[ContentQuizQuestion]]:
    blocks = db.query(ContentBlock).filter(ContentBlock.module_key == key).order_by(ContentBlock.position).all()
    questions = db.query(ContentQuizQuestion).filter(
        ContentQuizQuestion.module_key == key).order_by(ContentQuizQuestion.position).all()
    return blocks, questions


def _serialize_module(m: ContentModule, blocks: list[ContentBlock], questions: list[ContentQuizQuestion]) -> dict:
    """Form entspricht exakt ModuleIn-Feldern — so lässt sich das Ergebnis direkt
    wieder als ModuleIn(**data) einlesen (genutzt fürs Snapshot-Restore)."""
    return {
        "title_de": m.title_de, "title_en": m.title_en,
        "order": m.order,
        "prerequisites": m.prerequisites, "goals": m.goals,
        "scenario_de": m.scenario_de, "scenario_en": m.scenario_en,
        "blocks": [{"type": b.type, "value_de": b.value_de, "value_en": b.value_en,
                    "widget_id": b.widget_id, "note": b.note, "payload": b.payload} for b in blocks],
        "quiz": [{"qtype": q.qtype, "prompt_de": q.prompt_de, "prompt_en": q.prompt_en,
                  "options_de": q.options_de, "options_en": q.options_en, "answer": q.answer}
                 for q in questions],
    }


def _validate(db: Session, key: str, data: ModuleIn) -> None:
    for p in data.prerequisites:
        if p == key:
            raise HTTPException(status_code=422, detail=f"Modul kann nicht eigene Voraussetzung sein: {p}")
        if not db.query(ContentModule).filter(ContentModule.key == p).first():
            raise HTTPException(status_code=422, detail=f"Unbekannte Voraussetzung: {p}")
    for b in data.blocks:
        if b.type == "widget":
            if b.widget_id not in VALID_WIDGET_IDS:
                raise HTTPException(status_code=422, detail=f"Unbekannte Widget-ID: {b.widget_id}")
        elif b.type == "text":
            if not b.value_de or not b.value_en:
                raise HTTPException(status_code=422, detail="Text-Block braucht value_de und value_en")
        elif b.type == "check":
            pl = b.payload or {}
            if not pl.get("prompt_de") or not pl.get("prompt_en"):
                raise HTTPException(status_code=422, detail="Check-Block braucht prompt_de und prompt_en")
            if pl.get("kind") == "number":
                ans = pl.get("answer")
                if isinstance(ans, bool) or not isinstance(ans, (int, float)):
                    raise HTTPException(status_code=422, detail="Rechen-Check: answer muss eine Zahl sein")
            else:
                opts_de, opts_en = pl.get("options_de"), pl.get("options_en")
                if not opts_de or not opts_en:
                    raise HTTPException(status_code=422, detail="Check-Block braucht options_de und options_en")
                if len(opts_de) != len(opts_en):
                    raise HTTPException(status_code=422, detail="Check-Block: options_de und options_en müssen gleich lang sein")
                ans = pl.get("answer")
                if not isinstance(ans, int) or not (0 <= ans < len(opts_de)):
                    raise HTTPException(status_code=422, detail="Check-Block: answer muss gültiger Options-Index sein")
        elif b.type == "order":
            pl = b.payload or {}
            items_de, items_en = pl.get("items_de"), pl.get("items_en")
            if not pl.get("prompt_de") or not pl.get("prompt_en") or not items_de or not items_en:
                raise HTTPException(status_code=422, detail="Order-Block braucht prompt_de/en und items_de/en")
            if len(items_de) != len(items_en):
                raise HTTPException(status_code=422, detail="Order-Block: items_de und items_en müssen gleich lang sein")
            if len(items_de) < 2:
                raise HTTPException(status_code=422, detail="Order-Block braucht mindestens 2 Schritte")
        elif b.type == "debug":
            pl = b.payload or {}
            lines_de, lines_en = pl.get("lines_de"), pl.get("lines_en")
            if not pl.get("prompt_de") or not pl.get("prompt_en") or not lines_de or not lines_en:
                raise HTTPException(status_code=422, detail="Debug-Block braucht prompt_de/en und lines_de/en")
            if len(lines_de) != len(lines_en):
                raise HTTPException(status_code=422, detail="Debug-Block: lines_de und lines_en müssen gleich lang sein")
            wrong = pl.get("wrong")
            if not isinstance(wrong, list) or not wrong:
                raise HTTPException(status_code=422, detail="Debug-Block: mindestens eine Zeile als fehlerhaft markieren")
            for idx in wrong:
                if not isinstance(idx, int) or not (0 <= idx < len(lines_de)):
                    raise HTTPException(status_code=422, detail=f"Debug-Block: ungültiger Zeilen-Index: {idx}")
            if not pl.get("explanation_de") or not pl.get("explanation_en"):
                raise HTTPException(status_code=422, detail="Debug-Block braucht explanation_de und explanation_en")
        elif b.type == "reflect":
            pl = b.payload or {}
            if not pl.get("prompt_de") or not pl.get("prompt_en"):
                raise HTTPException(status_code=422, detail="Reflexions-Block braucht prompt_de und prompt_en")
        elif b.type == "reveal":
            pl = b.payload or {}
            if not pl.get("teaser_de") or not pl.get("teaser_en"):
                raise HTTPException(status_code=422, detail="Reveal-Block braucht teaser_de und teaser_en")
            if not b.value_de or not b.value_en:
                raise HTTPException(status_code=422, detail="Reveal-Block braucht value_de und value_en (versteckter Inhalt)")
        else:
            raise HTTPException(status_code=422, detail=f"Unbekannter Block-Typ: {b.type}")
    for q in data.quiz:
        if q.qtype in ("single", "multi"):
            if not q.options_de or not q.options_en:
                raise HTTPException(status_code=422, detail="Frage braucht options_de und options_en")
            if len(q.options_de) != len(q.options_en):
                raise HTTPException(status_code=422, detail="Frage: options_de und options_en müssen gleich lang sein")
            n = len(q.options_de)
            if q.qtype == "single":
                if isinstance(q.answer, bool) or not isinstance(q.answer, int):
                    raise HTTPException(status_code=422, detail="Single-Choice braucht genau einen Antwort-Index")
                indices = [q.answer]
            else:
                if not isinstance(q.answer, list) or not q.answer:
                    raise HTTPException(status_code=422, detail="Multiple-Choice braucht mindestens einen Antwort-Index")
                if len(set(q.answer)) != len(q.answer):
                    raise HTTPException(status_code=422, detail="Multiple-Choice enthält doppelte Antwort-Indizes")
                indices = q.answer
            for idx in indices:
                if isinstance(idx, bool) or not isinstance(idx, int) or not (0 <= idx < n):
                    raise HTTPException(status_code=422, detail=f"Antwort-Index außerhalb Optionsliste: {idx}")
        elif q.qtype == "number":
            if isinstance(q.answer, bool) or not isinstance(q.answer, int):
                raise HTTPException(status_code=422, detail="Zahlenfrage braucht eine ganze Zahl als Antwort")
        else:
            raise HTTPException(status_code=422, detail=f"Unbekannter Fragetyp: {q.qtype}")


def _block_signature(b) -> tuple:
    """Inhaltsabdruck eines Blocks, positionsunabhaengig. `b` ist entweder ein
    ContentBlock (alter Stand) oder ein BlockIn (neuer Stand aus dem Editor) --
    beide tragen dieselben Felder type/value_de/value_en/widget_id/note/payload,
    das reicht als Fingerabdruck um denselben inhaltlichen Block vor und nach
    dem Speichern wiederzuerkennen (gleiche Idee wie in content/seed.py
    _block_matches_source, nur mit Editor-Eingabe statt Seed-Dict verglichen)."""
    payload = b.payload
    return (b.type, b.value_de, b.value_en, b.widget_id, b.note,
            json.dumps(payload, sort_keys=True) if payload is not None else None)


def _remap_or_orphan_comments(db: Session, key: str, old_blocks: list[ContentBlock],
                              new_blocks: list[BlockIn]) -> None:
    """Rechnet Comment.block_index auf das Speichern eines Moduls um.

    Kommentare haengen an (module_key, block_index) -- also an der POSITION
    eines Blocks, nicht an einer Block-id (die es fuer Kommentare gar nicht
    gibt). _apply loescht beim Speichern aber ALLE ContentBlock-Zeilen und legt
    sie mit neuen ids und position 0..n-1 komplett neu an -- es gibt also keine
    stabile Block-Identitaet ueber das Speichern hinweg. Ohne diese Funktion
    wuerde jede Umsortierung/Einfuegung im Editor bestehende Kommentare stumm an
    einen fremden, inhaltlich anderen Block haengen.

    Zweistufige Zuordnung:

    Stufe 1 -- Inhaltssignatur (_block_signature): pro Signatur eine FIFO-
    Warteschlange der alten Positionen, beim Durchlauf der neuen Bloecke in
    Reihenfolge konsumiert. Das bildet reines Umsortieren und Einfuegen korrekt
    ab (Test: Block an Index 2 kommentiert, neuer Block bei 0 eingefuegt ->
    Kommentar zeigt danach auf Index 3, denselben inhaltlichen Block).

    Stufe 2 -- Positions-Fallback fuer alles, was Stufe 1 nicht zuordnen konnte:
    steht an der ALTEN Position von comment.block_index im neuen Blocklayout
    noch ein Block MIT GLEICHEM TYP, bleibt der Kommentar dort haengen. Das ist
    der normale Trainer-Workflow "Tippfehler in Block 2 korrigieren" -- der
    Block bleibt an seinem Platz und behaelt seinen Typ, nur value_de/value_en/
    payload aendern sich, wodurch sich zwangslaeufig auch die Signatur aendert.
    Ohne Fallback wuerde jede reine Textaenderung eines kommentierten Blocks den
    Kommentar loeschen (Datenverlust bei ganz normaler Nutzung).

    Geloescht wird ein Kommentar nur noch, wenn an seiner alten Position gar
    kein Block mehr existiert (Block entfernt) ODER sich dort der Block-TYP
    geaendert hat (z.B. text -> widget) -- dann ist der inhaltliche Bezug
    tatsaechlich weg und ein Clamp auf einen artfremden Block waere falsch.
    Eine "verwaist"-Markierung waere transparenter, verlangt aber ein neues Feld
    auf Comment (block_index ist NOT NULL, kein Status-Feld) -- Modelltyp-
    Aenderungen sind fuer diesen Fix bewusst tabu."""
    old_queue: dict[tuple, deque[int]] = defaultdict(deque)
    for pos, b in enumerate(old_blocks):
        old_queue[_block_signature(b)].append(pos)
    position_map: dict[int, int] = {}
    matched_new_positions: set[int] = set()
    for new_pos, b in enumerate(new_blocks):
        queue = old_queue.get(_block_signature(b))
        if queue:
            position_map[queue.popleft()] = new_pos
            matched_new_positions.add(new_pos)
    for comment in db.query(Comment).filter(Comment.module_key == key):
        new_pos = position_map.get(comment.block_index)
        if new_pos is not None:
            comment.block_index = new_pos
            continue
        # Stufe 2: gleiche Position, gleicher Typ, und diese Position wurde
        # nicht schon per Signatur von einem ANDEREN alten Block belegt (sonst
        # sitzt dort durch Umsortieren fremder Inhalt). Kein "Verbrauchen" der
        # Position hier noetig: mehrere Kommentare auf demselben alten Block
        # sollen alle gemeinsam an dessen (unveraenderter) Position bleiben.
        old_pos = comment.block_index
        if (0 <= old_pos < len(new_blocks) and old_pos not in matched_new_positions
                and old_pos < len(old_blocks)
                and old_blocks[old_pos].type == new_blocks[old_pos].type):
            continue
        db.delete(comment)


def _apply(db: Session, key: str, m: ContentModule, data: ModuleIn,
          old_blocks: list[ContentBlock]) -> None:
    m.title_de = data.title_de
    m.title_en = data.title_en
    m.order = data.order
    m.prerequisites = data.prerequisites
    m.goals = data.goals
    m.scenario_de = data.scenario_de
    m.scenario_en = data.scenario_en
    _remap_or_orphan_comments(db, key, old_blocks, data.blocks)
    db.query(ContentBlock).filter(ContentBlock.module_key == key).delete()
    db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key == key).delete()
    for i, b in enumerate(data.blocks):
        db.add(ContentBlock(module_key=key, position=i, type=b.type,
                            value_de=b.value_de, value_en=b.value_en,
                            widget_id=b.widget_id, note=b.note, payload=b.payload))
    for i, q in enumerate(data.quiz):
        db.add(ContentQuizQuestion(module_key=key, position=i, qtype=q.qtype,
                                   prompt_de=q.prompt_de, prompt_en=q.prompt_en,
                                   options_de=q.options_de, options_en=q.options_en, answer=q.answer))


def _upsert_snapshot(db: Session, key: str, data: dict) -> None:
    snap = db.query(ContentModuleSnapshot).filter(ContentModuleSnapshot.module_key == key).first()
    if snap:
        snap.data = data
    else:
        db.add(ContentModuleSnapshot(module_key=key, data=data))


@router.get("")
def list_modules(db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    mods = db.query(ContentModule).order_by(ContentModule.order).all()
    return [_meta(m) for m in mods]


@router.get("/{key}")
def get_module(key: str, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    m = db.query(ContentModule).filter(ContentModule.key == key).first()
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    blocks, questions = _load_blocks_and_quiz(db, key)
    has_snapshot = db.query(ContentModuleSnapshot).filter(ContentModuleSnapshot.module_key == key).first() is not None
    return {"key": m.key, "workshop_key": m.workshop_key,
            "has_snapshot": has_snapshot, "has_seed": key in MODULES,
            **_serialize_module(m, blocks, questions)}


@router.post("")
def create_module(data: ModuleCreateIn, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    if not KEY_RE.match(data.key):
        raise HTTPException(status_code=422, detail="Key darf nur a-z, 0-9 und - enthalten")
    if db.query(ContentModule).filter(ContentModule.key == data.key).first():
        raise HTTPException(status_code=422, detail="Key bereits vergeben")
    if not db.get(Workshop, data.workshop_key):
        raise HTTPException(status_code=422, detail="Unbekannter Workshop")
    max_order = db.query(ContentModule.order).filter(
        ContentModule.workshop_key == data.workshop_key).order_by(ContentModule.order.desc()).first()
    order = (max_order[0] if max_order else (100 if data.workshop_key == "claude-code" else 0)) + 1
    m = ContentModule(key=data.key, workshop_key=data.workshop_key, order=order,
                      prerequisites=[], title_de=data.title_de, title_en=data.title_de,
                      goals=[], scenario_de="", scenario_en="")
    db.add(m)
    try:
        db.commit()
    except IntegrityError:
        # Zwei gleichzeitige Create-Requests mit demselben Key (z.B. Doppelklick).
        db.rollback()
        raise HTTPException(status_code=422, detail="Key bereits vergeben") from None
    log_action(db, trainer, "content.create", target=f"module:{m.key}", detail=data.title_de)
    return _meta(m)


@router.put("/{key}")
def update_module(key: str, data: ModuleIn, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    m = db.query(ContentModule).filter(ContentModule.key == key).first()
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    _validate(db, key, data)
    blocks, questions = _load_blocks_and_quiz(db, key)
    _upsert_snapshot(db, key, _serialize_module(m, blocks, questions))
    _apply(db, key, m, data, blocks)
    db.commit()
    log_action(db, trainer, "content.save", target=f"module:{key}")
    return _meta(m)


def _seed_to_module_in(seed: dict) -> ModuleIn:
    """Übersetzt ein Seed-Dict aus app/content/*.py in die ModuleIn-Form
    (Sprach-Dicts {"de","en"} -> flache _de/_en-Felder)."""
    blocks = []
    for b in seed["blocks"]:
        value = b.get("value") or {}
        blocks.append(BlockIn(type=b["type"], value_de=value.get("de"), value_en=value.get("en"),
                              widget_id=b.get("id"), note=b.get("note"), payload=b.get("payload")))
    quiz = []
    for q in seed["quiz"]["questions"]:
        opts = q.get("options")
        quiz.append(QuestionIn(qtype=q["type"], prompt_de=q["prompt"]["de"], prompt_en=q["prompt"]["en"],
                               options_de=opts["de"] if opts else None,
                               options_en=opts["en"] if opts else None, answer=q["answer"]))
    return ModuleIn(title_de=seed["title"], title_en=seed.get("title_en", seed["title"]),
                    order=seed["order"], prerequisites=seed.get("prerequisites", []),
                    goals=seed.get("goals", []),
                    scenario_de=seed["scenario"]["de"], scenario_en=seed["scenario"]["en"],
                    blocks=blocks, quiz=quiz)


@router.post("/{key}/reseed")
def reseed_module(key: str, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    """Setzt ein Seed-Modul auf den Auslieferungszustand aus app/content/*.py
    zurück — z.B. um Content-Updates auf eine Bestandsinstallation zu holen.
    Der bisherige Stand landet im Snapshot, Restore macht es rückgängig."""
    seed = MODULES.get(key)
    m = db.query(ContentModule).filter(ContentModule.key == key).first()
    if not seed or not m:
        raise HTTPException(status_code=404,
                            detail="Kein Auslieferungszustand vorhanden (nur für mitgelieferte Module)")
    data = _seed_to_module_in(seed)
    _validate(db, key, data)  # fängt Fehler in der Seed-Datei früh ab
    blocks, questions = _load_blocks_and_quiz(db, key)
    _upsert_snapshot(db, key, _serialize_module(m, blocks, questions))
    _apply(db, key, m, data, blocks)
    db.commit()
    log_action(db, trainer, "content.reseed", target=f"module:{key}")
    return _meta(m)


@router.post("/{key}/restore")
def restore_module(key: str, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    m = db.query(ContentModule).filter(ContentModule.key == key).first()
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    snap = db.query(ContentModuleSnapshot).filter(ContentModuleSnapshot.module_key == key).first()
    if not snap:
        raise HTTPException(status_code=404, detail="Keine vorherige Version vorhanden")
    blocks, questions = _load_blocks_and_quiz(db, key)
    current_data = _serialize_module(m, blocks, questions)
    restored = ModuleIn(**snap.data)
    _apply(db, key, m, restored, blocks)
    snap.data = current_data
    db.commit()
    log_action(db, trainer, "content.restore", target=f"module:{key}")
    return _meta(m)
