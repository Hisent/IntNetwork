import hashlib
import json
import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.content.registry import MODULES
from app.content.sync import apply_state, serialize_module as _serialize_module, source_state
from app.database import get_db
from app.models.content import ContentBlock, ContentModule, ContentModuleSnapshot, ContentQuizQuestion
from app.models.workshop import Workshop
from app.services.audit import log_action
from app.services.block_validation import DECLARATIVE_TYPES, validate_block
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
    "wapi-console",
    "nac-radius-lab",
}

KEY_RE = re.compile(r"^[a-z0-9-]+$")


class BlockIn(BaseModel):
    # Stabile Kennung (app/content/sync.py). Der Editor schickt sie unverändert
    # zurück; ohne uid gilt der Block als neu bzw. wird über Inhalt/Position wiedererkannt.
    uid: str | None = Field(None, max_length=64)
    type: str
    value_de: str | None = None
    value_en: str | None = None
    widget_id: str | None = None
    note: str | None = None
    payload: dict | None = None

    @field_validator("value_de", "value_en", "widget_id", "note")
    @classmethod
    def _leer_ist_keine(cls, v: str | None) -> str | None:
        # Der Editor schickt für ein geleertes Feld "": ohne das wiche der Hash
        # vom Auslieferungsstand (None) ab und das Modul gälte als editiert.
        return v if v and v.strip() else None


class QuestionIn(BaseModel):
    uid: str | None = Field(None, max_length=64)  # wie BlockIn.uid
    qtype: str
    prompt_de: str
    prompt_en: str
    options_de: list[str] | None = None
    options_en: list[str] | None = None
    answer: int | list[int]
    # Erklärung zur Lösung, optional — Teilnehmer sehen sie erst nach der Abgabe.
    explanation_de: str | None = None
    explanation_en: str | None = None

    @field_validator("explanation_de", "explanation_en")
    @classmethod
    def _leer_ist_keine(cls, v: str | None) -> str | None:
        return v.strip() or None if v else None


class ModuleIn(BaseModel):
    title_de: str
    title_en: str
    order: int
    prerequisites: list[str] = []
    goals: list[str] = []
    # Englische Lernziele, optional; wenn gesetzt: je Ziel genau eine Übersetzung.
    goals_en: list[str] | None = None
    scenario_de: str
    scenario_en: str
    blocks: list[BlockIn]
    quiz: list[QuestionIn]

    @field_validator("goals_en")
    @classmethod
    def _leer_ist_keine(cls, v: list[str] | None) -> list[str] | None:
        return v or None  # [] wie "fehlt": sonst wiche der Hash vom Auslieferungsstand ab


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


def _validate(db: Session, key: str, data: ModuleIn) -> None:
    for p in data.prerequisites:
        if p == key:
            raise HTTPException(status_code=422, detail=f"Modul kann nicht eigene Voraussetzung sein: {p}")
        if not db.query(ContentModule).filter(ContentModule.key == p).first():
            raise HTTPException(status_code=422, detail=f"Unbekannte Voraussetzung: {p}")
    if data.goals_en and (len(data.goals_en) != len(data.goals) or not all(g.strip() for g in data.goals_en)):
        raise HTTPException(status_code=422, detail="Lernziele (EN): je deutschem Lernziel genau eine "
                                                    "nichtleere Übersetzung — oder das Feld ganz leer lassen")
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
        elif b.type in DECLARATIVE_TYPES:
            # Deklarativer Baukasten (docs/content-authoring.md): Meldung nennt Block-id und Feldpfad.
            try:
                validate_block(b.type, b.payload)
            except ValueError as err:
                label = b.uid or b.widget_id or f"#{data.blocks.index(b) + 1}"
                raise HTTPException(status_code=422, detail=f"{b.type}-Block '{label}': {err}") from None
        else:
            raise HTTPException(status_code=422, detail=f"Unbekannter Block-Typ: {b.type}")
    for q in data.quiz:
        if bool(q.explanation_de) != bool(q.explanation_en):
            raise HTTPException(status_code=422, detail="Frage: Erklärung braucht explanation_de und explanation_en")
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


def _apply(db: Session, key: str, m: ContentModule, data: ModuleIn,
           blocks: list[ContentBlock], questions: list[ContentQuizQuestion]) -> None:
    """Schreibt data in-place über die Kennungen (apply_state): unveränderte
    Blöcke und Fragen behalten ihre Zeile — Quiz-Abgaben und -Statistik hängen an
    der Frage-id, Kommentare wandern mit ihrem Block; der Kommentar an einem
    entfernten Block wird gelöscht."""
    apply_state(db, key, m, blocks, questions, data.model_dump())


def _locked_module(db: Session, key: str) -> ContentModule | None:
    """Die Modulzeile, unter Postgres mit Zeilensperre bis zum Commit (FOR NO KEY
    UPDATE; SQLite ignoriert das): Speichern, Auslieferungszustand laden,
    Wiederherstellen und der Content-Sync laufen je Modul nacheinander. Ein
    zweites gleichzeitiges PUT wartet hier, liest danach den Stand des ersten
    und scheitert an base_version (409) statt Kennungen zu doppeln."""
    return (db.query(ContentModule).filter(ContentModule.key == key)
            .with_for_update(key_share=True).populate_existing().first())


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


def _version(state: dict) -> str:
    """Fingerabdruck des gespeicherten Modulstands für die optimistische Sperre
    des Editors (GET liefert ihn als `version`, PUT prüft `base_version`).
    Bewusst ein Hash über den Inhalt statt einer updated_at-Spalte: braucht
    keine Migration und erkennt auch Reseed, Restore und Content-Sync.
    Atomar wird Prüfen + Speichern durch die Zeilensperre in _locked_module."""
    return hashlib.sha256(json.dumps(state, sort_keys=True, default=str).encode()).hexdigest()[:16]


@router.get("/{key}")
def get_module(key: str, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    m = db.query(ContentModule).filter(ContentModule.key == key).first()
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    blocks, questions = _load_blocks_and_quiz(db, key)
    has_snapshot = db.query(ContentModuleSnapshot).filter(ContentModuleSnapshot.module_key == key).first() is not None
    state = _serialize_module(m, blocks, questions)
    return {"key": m.key, "workshop_key": m.workshop_key,
            "has_snapshot": has_snapshot, "has_seed": key in MODULES,
            "version": _version(state), **state}


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
def update_module(key: str, data: ModuleIn, base_version: str | None = None,
                  db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    m = _locked_module(db, key)
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    # base_version ist Pflicht: ein Editor-Tab von vor dem Update kennt neuere
    # Felder (Erklärungen, goals_en) nicht und würde sie mit seinem PUT still
    # löschen. Bewusst 409 mit Klartext statt des 422 eines Pflicht-Parameters.
    if base_version is None:
        raise HTTPException(
            status_code=409,
            detail="Dieser Editor-Tab stammt von vor einem Update der Plattform. Nichts wurde "
                   "gespeichert. Bitte eigene Änderungen sichern, die Seite neu laden und erneut einpflegen.")
    _validate(db, key, data)
    blocks, questions = _load_blocks_and_quiz(db, key)
    current = _serialize_module(m, blocks, questions)
    # Optimistische Sperre: Der Editor schickt die Version mit, auf der seine
    # Änderungen beruhen. Hat inzwischen jemand anderes gespeichert, würde
    # dieses PUT dessen Stand komplett überschreiben.
    if base_version != _version(current):
        raise HTTPException(
            status_code=409,
            detail="Dieses Modul wurde inzwischen an anderer Stelle geändert (anderer Trainer, "
                   "zweiter Tab oder Content-Update). Nichts wurde gespeichert. Bitte eigene "
                   "Änderungen sichern, die Seite neu laden und erneut einpflegen.")
    _upsert_snapshot(db, key, current)
    _apply(db, key, m, data, blocks, questions)
    db.commit()
    log_action(db, trainer, "content.save", target=f"module:{key}")
    return {**_meta(m), "version": _version(_serialize_module(m, *_load_blocks_and_quiz(db, key)))}


def _seed_to_module_in(seed: dict) -> ModuleIn:
    """Seed-Dict aus app/content/*.py in der ModuleIn-Form — dieselbe kanonische
    Form (samt Kennungen), die der Content-Sync einspielt."""
    return ModuleIn(**source_state(seed))


@router.post("/{key}/reseed")
def reseed_module(key: str, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    """Setzt ein Seed-Modul auf den Auslieferungszustand aus app/content/*.py
    zurück — z.B. um Content-Updates auf eine Bestandsinstallation zu holen.
    Der bisherige Stand landet im Snapshot, Restore macht es rückgängig."""
    seed = MODULES.get(key)
    m = _locked_module(db, key)
    if not seed or not m:
        raise HTTPException(status_code=404,
                            detail="Kein Auslieferungszustand vorhanden (nur für mitgelieferte Module)")
    data = _seed_to_module_in(seed)
    _validate(db, key, data)  # fängt Fehler in der Seed-Datei früh ab
    blocks, questions = _load_blocks_and_quiz(db, key)
    _upsert_snapshot(db, key, _serialize_module(m, blocks, questions))
    _apply(db, key, m, data, blocks, questions)
    db.commit()
    log_action(db, trainer, "content.reseed", target=f"module:{key}")
    return _meta(m)


@router.post("/{key}/restore")
def restore_module(key: str, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    m = _locked_module(db, key)
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    snap = db.query(ContentModuleSnapshot).filter(ContentModuleSnapshot.module_key == key).first()
    if not snap:
        raise HTTPException(status_code=404, detail="Keine vorherige Version vorhanden")
    blocks, questions = _load_blocks_and_quiz(db, key)
    current_data = _serialize_module(m, blocks, questions)
    restored = ModuleIn(**snap.data)
    _apply(db, key, m, restored, blocks, questions)
    snap.data = current_data
    db.commit()
    log_action(db, trainer, "content.restore", target=f"module:{key}")
    return _meta(m)
