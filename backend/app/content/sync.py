"""Zieht geänderte Auslieferungsinhalte beim Start in Bestands-Datenbanken nach.

Ablauf (aufgerufen aus seed_missing_content, siehe dort):

1. pristine_modules() — VOR den Release-Migrationen: welche Module tragen
   noch einen Auslieferungsstand, also keine Trainer-Änderung?
2. Die bisherigen Migrationen laufen wie gehabt.
3. sync_content() — gleicht genau diese Module in-place an die Quelle an.

"Unverändert" ist ein Modul, wenn eines davon gilt:
- sein DB-Stand hat noch den Hash, den der letzte Sync gespeichert hat
  (Setting "content-sync:<key>"),
- es gibt noch keinen gespeicherten Hash (Bestands-DB vor Einführung des
  Syncs) und das Modul wurde nie über den Editor gespeichert (kein
  ContentModuleSnapshot — Speichern und "Auslieferungszustand laden" legen
  immer einen an) oder sein Stand ist ein bekannter Auslieferungsstand aus
  sync_baseline.json,
- sein Stand entspricht bereits der aktuellen Quelle.

Alles andere gilt als Trainer-Stand und wird nie angefasst, nur gemeldet.
"""
import hashlib
import json
import logging
from collections import defaultdict
from pathlib import Path

from sqlalchemy.orm import Session

from app.content.registry import MODULES
from app.models.audit_log import AuditLog
from app.models.comment import Comment
from app.models.content import ContentBlock, ContentModule, ContentModuleSnapshot, ContentQuizQuestion
from app.models.quiz_result import QuizResult
from app.models.setting import Setting
from app.routers.trainer_content import _serialize_module

log = logging.getLogger(__name__)

HASH_KEY = "content-sync:"          # + Modul-Key -> Hash der zuletzt eingespielten Quelle
SKIPPED_KEY = "content-sync-skipped:"  # + Modul-Key -> Quell-Hash, für den das Auslassen schon gemeldet wurde
# {Modul-Key: [Hashes aller Stände, die eine nie editierte DB bis v1.41.1 haben
# kann]} — erzeugt von backend/build_content_baseline.py, nur für den Bootstrap.
BASELINE: dict[str, list[str]] = json.loads(
    Path(__file__).with_name("sync_baseline.json").read_text(encoding="utf-8"))

PAYLOAD_BLOCK_TYPES = ("check", "reveal", "order", "debug", "reflect")
_MODULE_FIELDS = ("title_de", "title_en", "order", "prerequisites", "goals", "scenario_de", "scenario_en")


def source_state(seed: dict) -> dict:
    """Seed-Dict aus app/content/*.py in der Form von _serialize_module — die
    eine kanonische Form für Seed, Vergleich und In-place-Update. Der
    JSON-Roundtrip gleicht Tupel/Listen an, damit Quelle und DB-Stand direkt
    vergleichbar sind."""
    blocks = []
    for b in seed["blocks"]:
        value = b.get("value") or {}
        if b["type"] == "text" or b["type"] in PAYLOAD_BLOCK_TYPES:
            blocks.append({"type": b["type"], "value_de": value.get("de"), "value_en": value.get("en"),
                           "widget_id": None, "note": b.get("note"),
                           "payload": b["payload"] if b["type"] in PAYLOAD_BLOCK_TYPES else None})
        else:
            blocks.append({"type": "widget", "value_de": None, "value_en": None,
                           "widget_id": b["id"], "note": b.get("note"), "payload": None})
    quiz = []
    for q in seed["quiz"]["questions"]:
        options = q.get("options") or {}
        quiz.append({"qtype": q["type"], "prompt_de": q["prompt"]["de"], "prompt_en": q["prompt"]["en"],
                     "options_de": options.get("de"), "options_en": options.get("en"), "answer": q["answer"]})
    return json.loads(json.dumps({
        "title_de": seed["title"], "title_en": seed.get("title_en", seed["title"]),
        "order": seed["order"], "prerequisites": seed.get("prerequisites", []),
        "goals": seed.get("goals", []),
        "scenario_de": seed["scenario"]["de"], "scenario_en": seed["scenario"]["en"],
        "blocks": blocks, "quiz": quiz,
    }))


def db_state(m: ContentModule, blocks: list[ContentBlock], questions: list[ContentQuizQuestion]) -> dict:
    state = _serialize_module(m, blocks, questions)
    for b in state["blocks"]:
        # "Auslieferungszustand laden" im Editor schreibt die Quell-id auch an
        # Nicht-Widget-Blöcke, der Seed nicht — inhaltlich ist das derselbe Stand.
        if b["type"] != "widget":
            b["widget_id"] = None
    return state


def content_hash(state: dict) -> str:
    return hashlib.sha256(json.dumps(state, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def load_all(db: Session) -> dict[str, tuple[ContentModule, list[ContentBlock], list[ContentQuizQuestion]]]:
    db.flush()  # SessionLocal läuft mit autoflush=False
    blocks, questions = defaultdict(list), defaultdict(list)
    for b in db.query(ContentBlock).order_by(ContentBlock.position, ContentBlock.id):
        blocks[b.module_key].append(b)
    for q in db.query(ContentQuizQuestion).order_by(ContentQuizQuestion.position, ContentQuizQuestion.id):
        questions[q.module_key].append(q)
    return {m.key: (m, blocks[m.key], questions[m.key]) for m in db.query(ContentModule)}


def _settings(db: Session, prefix: str) -> dict[str, str]:
    return {s.key[len(prefix):]: s.value
            for s in db.query(Setting).filter(Setting.key.startswith(prefix, autoescape=True))}


def _set(db: Session, key: str, value: str) -> None:
    row = db.get(Setting, key)
    if row is None:
        db.add(Setting(key=key, value=value))
    else:
        row.value = value


def pristine_modules(db: Session) -> set[str]:
    """Keys der ausgelieferten Module ohne Trainer-Änderung (siehe Modul-Docstring).
    Fehlende Module zählen dazu — sie werden in diesem Lauf frisch geseedet."""
    loaded = load_all(db)
    stored = _settings(db, HASH_KEY)
    edited_once = {key for (key,) in db.query(ContentModuleSnapshot.module_key)}
    pristine = set()
    for key, seed in MODULES.items():
        if key not in loaded:
            pristine.add(key)
            continue
        state = db_state(*loaded[key])
        current = content_hash(state)
        if key in stored:
            unedited = current == stored[key]
        else:
            unedited = key not in edited_once or current in BASELINE.get(key, ())
        if unedited or state == source_state(seed):
            pristine.add(key)
    return pristine


def _write_rows(db: Session, model, key: str, existing: list, matched: list, values: list[dict]) -> None:
    """Schreibt values in die zugeordneten Zeilen (matched[i] gehört zu values[i],
    None = neu anlegen) und löscht nicht zugeordnete. Zugeordnete Zeilen behalten
    ihre id — an der Frage-id hängen die Quiz-Abgaben."""
    for position, (row, fields) in enumerate(zip(matched, values, strict=True)):
        if row is None:
            row = model(module_key=key)
            db.add(row)
        row.position = position
        for name, value in fields.items():
            setattr(row, name, value)
    kept = {id(row) for row in matched}
    for row in existing:
        if id(row) not in kept:
            db.delete(row)


def _match_blocks(blocks: list[ContentBlock], src_blocks: list[dict]) -> list[ContentBlock | None]:
    """Ordnet jedem Quellblock die vorhandene Zeile zu: Widgets über ihre
    widget_id, alle anderen als n-ter Block ihres Typs. Bei gleicher
    Typ-Reihenfolge ist das genau die Zuordnung per Position; zusätzlich deckt
    es reine Umsortierungen ab (die Widget-Migrationen stellen Widgets direkt
    hinter ihren Anker, die Quelle hat sie teils an anderer Stelle)."""
    pools: dict[tuple, list[ContentBlock]] = defaultdict(list)
    for block in reversed(blocks):
        pools[(block.type, block.widget_id if block.type == "widget" else None)].append(block)
    matched = []
    for src in src_blocks:
        pool = pools[(src["type"], src["widget_id"])]
        matched.append(pool.pop() if pool else None)
    return matched


def _update_in_place(db: Session, key: str, m: ContentModule, blocks: list[ContentBlock],
                     questions: list[ContentQuizQuestion], src: dict) -> str | None:
    """Schreibt den Quellstand in die vorhandenen Zeilen. Gibt statt zu raten
    einen Grund zurück (und ändert nichts), wenn die Struktur so abweicht, dass
    Teilnehmerdaten ihren Bezug verlören: Kommentare hängen an der Blockposition,
    Quiz-Abgaben an der Frage-id."""
    matched_blocks = _match_blocks(blocks, src["blocks"])
    comments = db.query(Comment).filter(Comment.module_key == key).all()
    if comments and (None in matched_blocks or len(matched_blocks) != len(blocks)):
        return "Blöcke sind hinzugekommen oder entfallen und es gibt Kommentare an den Blöcken"
    if ([q.qtype for q in questions] != [q["qtype"] for q in src["quiz"]]
            and db.query(QuizResult.id).filter(QuizResult.module_key == key).first()):
        return "Quizstruktur weicht von der Quelle ab und es gibt Quiz-Abgaben"

    new_index = {id(row): position for position, row in enumerate(matched_blocks)}
    for comment in comments:  # Kommentar wandert mit seinem Block mit
        if 0 <= comment.block_index < len(blocks):
            comment.block_index = new_index[id(blocks[comment.block_index])]
    for name in _MODULE_FIELDS:
        setattr(m, name, src[name])
    _write_rows(db, ContentBlock, key, blocks, matched_blocks, src["blocks"])
    by_position = [questions[i] if i < len(questions) else None for i in range(len(src["quiz"]))]
    _write_rows(db, ContentQuizQuestion, key, questions, by_position, src["quiz"])
    return None


def sync_content(db: Session, pristine: set[str], fresh: frozenset[str] = frozenset()) -> dict:
    """Bringt die unveränderten Module auf den Quellstand und merkt sich dessen
    Hash. Je Modul ein Savepoint: ein Fehler rollt nur dieses Modul zurück.
    Committet nicht — das macht der Aufrufer zusammen mit dem Rest des Seeds.

    fresh: in diesem Lauf erst geseedete Module. Die Widget-Migrationen sortieren
    auch dort einzelne Blöcke um; das wird angeglichen, ist aber kein Update,
    das man melden müsste."""
    loaded = load_all(db)
    stored = _settings(db, HASH_KEY)
    reported = _settings(db, SKIPPED_KEY)
    updated, skipped, failed = [], {}, []
    for key, seed in MODULES.items():
        if key not in loaded:
            continue
        m, blocks, questions = loaded[key]
        src = source_state(seed)
        src_hash = content_hash(src)
        if key not in pristine:
            if db_state(m, blocks, questions) != src:
                skipped[key] = "vom Trainer geändert"
            continue
        try:
            with db.begin_nested():
                if db_state(m, blocks, questions) != src:
                    reason = _update_in_place(db, key, m, blocks, questions, src)
                    if reason:
                        skipped[key] = reason
                        continue
                    if key not in fresh:
                        updated.append(key)
                if stored.get(key) != src_hash:
                    _set(db, HASH_KEY + key, src_hash)
        except Exception:
            log.exception("Content-Sync: Modul %s konnte nicht aktualisiert werden", key)
            failed.append(key)
            if key in updated:
                updated.remove(key)

    # Ausgelassene Module einmal je neuem Quellstand ins Audit-Log (Trainer-Oberfläche).
    # Bekannt ist ein Quellstand, wenn er schon gemeldet, zuletzt eingespielt oder
    # (Bootstrap) Teil der Baseline ist — dann gibt es nichts Neues zu verpassen.
    news = []
    for key, reason in skipped.items():
        src_hash = content_hash(source_state(MODULES[key]))
        if src_hash in {reported.get(key), stored.get(key), *BASELINE.get(key, ())}:
            continue
        news.append(key)
        _set(db, SKIPPED_KEY + key, src_hash)
        db.add(AuditLog(trainer_email="system", action="content.sync.skipped", target=f"module:{key}",
                        detail=f"Neuer Auslieferungsinhalt nicht eingespielt: {reason}"))
    # Bewusst WARNING: uvicorn zeigt für App-Logger ohne eigene Konfiguration nur
    # WARNING aufwärts, und beide Meldungen soll man nach einem Deploy sehen.
    if updated:
        db.add(AuditLog(trainer_email="system", action="content.sync",
                        detail=f"{len(updated)} Module auf Auslieferungsstand aktualisiert: " + ", ".join(updated)))
        log.warning("Content-Sync: %s Module auf Auslieferungsstand aktualisiert: %s",
                    len(updated), ", ".join(updated))
    if skipped:
        log.warning("Content-Sync: %s Module weichen vom Auslieferungsstand ab und bleiben unangetastet: %s",
                    len(skipped), "; ".join(f"{key} ({reason})" for key, reason in skipped.items()))
    db.flush()
    return {"updated": updated, "skipped": skipped, "failed": failed}
