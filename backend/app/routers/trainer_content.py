import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.content import ContentBlock, ContentModule, ContentModuleSnapshot, ContentQuizQuestion
from app.services.deps import get_trainer
from app.utils import utc_now

router = APIRouter(prefix="/trainer/content/modules", tags=["trainer-content"])

# Muss synchron zu frontend/src/widgets/registry.tsx (WIDGETS-Objekt) gepflegt werden.
VALID_WIDGET_IDS = {
    "vlan-switch", "frame-builder", "osi-model", "mac-learning", "subnet-calc",
    "arp-demo", "routing-demo", "nat-demo", "dns-demo", "dhcp-demo", "ports-demo",
    "icmp-demo", "firewall-demo", "ipv6-demo", "wlan-demo", "vpn-demo",
}

KEY_RE = re.compile(r"^[a-z0-9-]+$")


class BlockIn(BaseModel):
    type: str
    value_de: str | None = None
    value_en: str | None = None
    widget_id: str | None = None
    note: str | None = None


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
    pass_threshold: float = 0.7
    prerequisites: list[str] = []
    goals: list[str] = []
    scenario_de: str
    scenario_en: str
    blocks: list[BlockIn]
    quiz: list[QuestionIn]


class ModuleCreateIn(BaseModel):
    key: str
    title_de: str


def _meta(m: ContentModule) -> dict:
    return {"key": m.key, "title_de": m.title_de, "title_en": m.title_en, "order": m.order}


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
        "order": m.order, "pass_threshold": m.pass_threshold,
        "prerequisites": m.prerequisites, "goals": m.goals,
        "scenario_de": m.scenario_de, "scenario_en": m.scenario_en,
        "blocks": [{"type": b.type, "value_de": b.value_de, "value_en": b.value_en,
                    "widget_id": b.widget_id, "note": b.note} for b in blocks],
        "quiz": [{"qtype": q.qtype, "prompt_de": q.prompt_de, "prompt_en": q.prompt_en,
                  "options_de": q.options_de, "options_en": q.options_en, "answer": q.answer}
                 for q in questions],
    }


def _validate(db: Session, key: str, data: ModuleIn) -> None:
    if not (0.0 <= data.pass_threshold <= 1.0):
        raise HTTPException(status_code=422, detail="pass_threshold muss zwischen 0 und 1 liegen")
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
        else:
            raise HTTPException(status_code=422, detail=f"Unbekannter Block-Typ: {b.type}")
    for q in data.quiz:
        if q.qtype in ("single", "multi"):
            if not q.options_de or not q.options_en:
                raise HTTPException(status_code=422, detail="Frage braucht options_de und options_en")
            n = len(q.options_de)
            indices = q.answer if isinstance(q.answer, list) else [q.answer]
            for idx in indices:
                if not isinstance(idx, int) or not (0 <= idx < n):
                    raise HTTPException(status_code=422, detail=f"Antwort-Index außerhalb Optionsliste: {idx}")
        elif q.qtype != "number":
            raise HTTPException(status_code=422, detail=f"Unbekannter Fragetyp: {q.qtype}")


def _apply(db: Session, key: str, m: ContentModule, data: ModuleIn) -> None:
    m.title_de = data.title_de
    m.title_en = data.title_en
    m.order = data.order
    m.pass_threshold = data.pass_threshold
    m.prerequisites = data.prerequisites
    m.goals = data.goals
    m.scenario_de = data.scenario_de
    m.scenario_en = data.scenario_en
    db.query(ContentBlock).filter(ContentBlock.module_key == key).delete()
    db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key == key).delete()
    for i, b in enumerate(data.blocks):
        db.add(ContentBlock(module_key=key, position=i, type=b.type,
                            value_de=b.value_de, value_en=b.value_en,
                            widget_id=b.widget_id, note=b.note))
    for i, q in enumerate(data.quiz):
        db.add(ContentQuizQuestion(module_key=key, position=i, qtype=q.qtype,
                                   prompt_de=q.prompt_de, prompt_en=q.prompt_en,
                                   options_de=q.options_de, options_en=q.options_en, answer=q.answer))


def _upsert_snapshot(db: Session, key: str, data: dict) -> None:
    snap = db.query(ContentModuleSnapshot).filter(ContentModuleSnapshot.module_key == key).first()
    if snap:
        snap.data = data
        snap.saved_at = utc_now()
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
    return {"key": m.key, "has_snapshot": has_snapshot, **_serialize_module(m, blocks, questions)}


@router.post("")
def create_module(data: ModuleCreateIn, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    if not KEY_RE.match(data.key):
        raise HTTPException(status_code=422, detail="Key darf nur a-z, 0-9 und - enthalten")
    if db.query(ContentModule).filter(ContentModule.key == data.key).first():
        raise HTTPException(status_code=422, detail="Key bereits vergeben")
    max_order = db.query(ContentModule).count()
    m = ContentModule(key=data.key, order=max_order + 1, pass_threshold=0.7,
                      prerequisites=[], title_de=data.title_de, title_en=data.title_de,
                      goals=[], scenario_de="", scenario_en="")
    db.add(m)
    try:
        db.commit()
    except IntegrityError:
        # Zwei gleichzeitige Create-Requests mit demselben Key (z.B. Doppelklick).
        db.rollback()
        raise HTTPException(status_code=422, detail="Key bereits vergeben")
    return _meta(m)


@router.put("/{key}")
def update_module(key: str, data: ModuleIn, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    m = db.query(ContentModule).filter(ContentModule.key == key).first()
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    _validate(db, key, data)
    blocks, questions = _load_blocks_and_quiz(db, key)
    _upsert_snapshot(db, key, _serialize_module(m, blocks, questions))
    _apply(db, key, m, data)
    db.commit()
    return _meta(m)


@router.post("/{key}/restore")
def restore_module(key: str, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    m = db.query(ContentModule).filter(ContentModule.key == key).first()
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    snap = db.query(ContentModuleSnapshot).filter(ContentModuleSnapshot.module_key == key).first()
    if not snap:
        raise HTTPException(status_code=404, detail="Keine vorherige Version vorhanden")
    blocks, questions = _load_blocks_and_quiz(db, key)
    current_data = _serialize_module(m, blocks, questions)
    restored = ModuleIn(**snap.data)
    _apply(db, key, m, restored)
    snap.data = current_data
    snap.saved_at = utc_now()
    db.commit()
    return _meta(m)
