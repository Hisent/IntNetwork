"""Zieht geänderte Auslieferungsinhalte beim Start in Bestands-Datenbanken nach.

Ablauf (aufgerufen aus seed_missing_content, siehe dort):

1. pristine_modules() — VOR den Release-Migrationen: welche Module tragen
   noch einen Auslieferungsstand, also keine Trainer-Änderung? (Sperrt die
   Modulzeilen und merkt sich je Modul den gesehenen Stand.)
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

Zuordnung: Jeder Block und jede Frage trägt eine je Modul eindeutige Kennung
(Spalte uid, in der Quelle "id"). apply_state() — genutzt vom Sync UND vom
Editor (Speichern, Auslieferungszustand laden, Wiederherstellen) — ordnet
darüber zu: bekannte Kennung = Zeile wird überschrieben und behält ihre DB-id
(an der Frage-id hängen die Quiz-Abgaben, an der Blockzeile die Kommentare),
neue Kennung = Zeile wird eingefügt, fehlende = gelöscht, Reihenfolge = Vorgabe.
Ausnahme Fragen: ändert sich der Lösungsschlüssel (Typ, Lösung oder
Reihenfolge der Optionen), entsteht trotz gleicher Kennung eine neue Zeile —
alte Abgaben zählen für diese Frage dann nicht mehr (siehe _same_key).
Der Inhalt eines Blocks ist dabei ein beliebiges Dict (blocktyp-agnostisch).
"""
import hashlib
import json
import logging
import secrets
from collections import Counter, defaultdict
from pathlib import Path

from sqlalchemy import event
from sqlalchemy.orm import Session

from app.content.registry import MODULES
from app.models.audit_log import AuditLog
from app.models.comment import Comment
from app.models.content import ContentBlock, ContentModule, ContentModuleSnapshot, ContentQuizQuestion
from app.models.setting import Setting

log = logging.getLogger(__name__)

HASH_KEY = "content-sync:"          # + Modul-Key -> Hash der zuletzt eingespielten Quelle
SKIPPED_KEY = "content-sync-skipped:"  # + Modul-Key -> Quell-Hash, für den das Auslassen schon gemeldet wurde
# Erzeugt von backend/build_content_baseline.py, nur für den Bootstrap von
# Datenbanken, die noch keinen gespeicherten Hash bzw. keine Kennungen haben:
# BASELINE  {Modul-Key: [Hashes aller Stände, die eine nie editierte DB bis v1.42.0 haben kann]}
# STRUCTURE {Modul-Key: {"blocks": [[Typ, Kennung], …], "quiz": [[Typ, Kennung], …]}} — Stand v1.42.0,
#           der letzte ohne Kennungen in der DB (siehe _assign_missing_uids).
_BASELINE_FILE = json.loads(Path(__file__).with_name("sync_baseline.json").read_text(encoding="utf-8"))
BASELINE: dict[str, list[str]] = _BASELINE_FILE["hashes"]
STRUCTURE: dict[str, dict[str, list[list[str]]]] = _BASELINE_FILE["structure"]

_MODULE_FIELDS = ("title_de", "title_en", "order", "prerequisites", "goals", "goals_en",
                  "scenario_de", "scenario_en")
# Inhaltsfelder je Zeile; das erste ist der Typ. Die Kennung (uid) kommt dazu.
BLOCK_FIELDS = ("type", "value_de", "value_en", "widget_id", "note", "payload")
QUESTION_FIELDS = ("qtype", "prompt_de", "prompt_en", "options_de", "options_en", "answer",
                   "explanation_de", "explanation_en")


def new_uid() -> str:
    """Kennung für Blöcke/Fragen, die nicht aus der Quelle stammen (im Editor angelegt)."""
    return "x" + secrets.token_hex(4)


def serialize_module(m: ContentModule, blocks: list[ContentBlock], questions: list[ContentQuizQuestion]) -> dict:
    """Die eine kanonische Form eines Moduls — für Seed, Vergleich, Editor (die
    Felder entsprechen ModuleIn) und Snapshot."""
    return {
        **{name: getattr(m, name) for name in _MODULE_FIELDS},
        "blocks": [{"uid": b.uid, **{f: getattr(b, f) for f in BLOCK_FIELDS}} for b in blocks],
        "quiz": [{"uid": q.uid, **{f: getattr(q, f) for f in QUESTION_FIELDS}} for q in questions],
    }


def source_state(seed: dict) -> dict:
    """Seed-Dict aus app/content/*.py in der Form von serialize_module. Der
    JSON-Roundtrip gleicht Tupel/Listen an, damit Quelle und DB-Stand direkt
    vergleichbar sind. Blocktyp-agnostisch: "payload" wird unbesehen übernommen.

    Die Kennung ist die "id" aus der Quelle (Pflicht, erzwingt
    tests/test_content_structure.py). Der Ersatz "<typ>-<n>" (n-ter Block seines
    Typs) ist nur für alte Quellstände ohne Block-ids da: genau so wurden die
    ids einmalig vergeben, und so leitet build_content_baseline.py sie für
    STRUCTURE ab."""
    blocks, nth = [], Counter()
    for b in seed["blocks"]:
        nth[b["type"]] += 1
        value = b.get("value") or {}
        blocks.append({"uid": b.get("id") or f"{b['type']}-{nth[b['type']]}",
                       "type": b["type"], "value_de": value.get("de"), "value_en": value.get("en"),
                       "widget_id": b["id"] if b["type"] == "widget" else None,
                       "note": b.get("note"), "payload": b.get("payload")})
    quiz = []
    for q in seed["quiz"]["questions"]:
        options, explanation = q.get("options") or {}, q.get("explanation") or {}
        quiz.append({"uid": q["id"], "qtype": q["type"],
                     "prompt_de": q["prompt"]["de"], "prompt_en": q["prompt"]["en"],
                     "options_de": options.get("de"), "options_en": options.get("en"), "answer": q["answer"],
                     "explanation_de": explanation.get("de"), "explanation_en": explanation.get("en")})
    return json.loads(json.dumps({
        "title_de": seed["title"], "title_en": seed.get("title_en", seed["title"]),
        "order": seed["order"], "prerequisites": seed.get("prerequisites", []),
        "goals": seed.get("goals", []), "goals_en": seed.get("goals_en") or None,
        "scenario_de": seed["scenario"]["de"], "scenario_en": seed["scenario"]["en"],
        "blocks": blocks, "quiz": quiz,
    }))


def db_state(m: ContentModule, blocks: list[ContentBlock], questions: list[ContentQuizQuestion]) -> dict:
    state = serialize_module(m, blocks, questions)
    for b in state["blocks"]:
        # "Auslieferungszustand laden" schrieb bis v1.42.0 die Quell-id auch an
        # Nicht-Widget-Blöcke, der Seed nicht — inhaltlich ist das derselbe Stand.
        if b["type"] != "widget":
            b["widget_id"] = None
    return state


def content_hash(state: dict) -> str:
    """Hash über den INHALT: Kennungen zählen nicht mit (kein Trainer kann sie
    ändern), eine fehlende Erklärung und fehlende englische Lernziele (goals_en)
    auch nicht. Damit hat ein Stand ohne Erklärungen/goals_en denselben Hash wie
    unter v1.42.0 — gespeicherte Hashes und sync_baseline.json bleiben gültig."""
    slim = {**{k: v for k, v in state.items() if k != "goals_en" or v},
            "blocks": [{k: v for k, v in b.items() if k != "uid"} for b in state["blocks"]],
            "quiz": [{k: v for k, v in q.items()
                      if k != "uid" and not (k.startswith("explanation_") and v is None)}
                     for q in state["quiz"]]}
    return hashlib.sha256(json.dumps(slim, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def load_all(db: Session, *, lock: bool = False
             ) -> dict[str, tuple[ContentModule, list[ContentBlock], list[ContentQuizQuestion]]]:
    """Alle Module mit ihren Zeilen, FRISCH aus der DB (populate_existing): ohne
    das behielten schon geladene Objekte ihre alten Werte, und ein inzwischen
    von einem anderen Prozess gespeicherter Stand bliebe unsichtbar.
    lock: Zeilensperre auf jede Modulzeile bis zum Commit (Postgres, FOR NO KEY
    UPDATE; SQLite ignoriert das) — dieselbe, die der Editor beim Speichern
    nimmt (routers/trainer_content.py, _locked_module)."""
    db.flush()  # SessionLocal läuft mit autoflush=False
    modules = db.query(ContentModule).populate_existing()
    if lock:
        modules = modules.with_for_update(key_share=True)
    modules = modules.all()  # zuerst: die Sperre steht, bevor Blöcke/Fragen gelesen werden
    blocks, questions = defaultdict(list), defaultdict(list)
    for b in db.query(ContentBlock).populate_existing().order_by(ContentBlock.position, ContentBlock.id):
        blocks[b.module_key].append(b)
    for q in (db.query(ContentQuizQuestion).populate_existing()
              .order_by(ContentQuizQuestion.position, ContentQuizQuestion.id)):
        questions[q.module_key].append(q)
    return {m.key: (m, blocks[m.key], questions[m.key]) for m in modules}


def _settings(db: Session, prefix: str) -> dict[str, str]:
    return {s.key[len(prefix):]: s.value
            for s in db.query(Setting).filter(Setting.key.startswith(prefix, autoescape=True))}


def _set(db: Session, key: str, value: str) -> None:
    row = db.get(Setting, key)
    if row is None:
        db.add(Setting(key=key, value=value))
    else:
        row.value = value


_OWN = "content_sync_own"  # Session.info: Modul-Keys, deren Zeilen diese Session selbst geschrieben hat


def _note_own_writes(session: Session, _context, _instances) -> None:
    for obj in (*session.new, *session.dirty, *session.deleted):
        if isinstance(obj, (ContentBlock, ContentQuizQuestion)):
            session.info[_OWN].add(obj.module_key)
        elif isinstance(obj, ContentModule):
            session.info[_OWN].add(obj.key)


def pristine_modules(db: Session) -> dict[str, str | None]:
    """Die ausgelieferten Module ohne Trainer-Änderung (siehe Modul-Docstring):
    Key -> Hash des dabei gesehenen Stands. Fehlende Module zählen dazu (Hash
    None) — sie werden in diesem Lauf frisch geseedet.

    Zwischen dieser Prüfung und dem Einspielen kann ein Trainer speichern
    (Rolling-Deploy: der alte Container bedient noch). Deshalb (a) sperrt die
    Prüfung die Modulzeilen bis zum Commit — ein Speichern mit diesem Code-Stand
    wartet und prüft danach seine base_version neu —, und (b) liest sync_content
    frisch und lässt jedes Modul aus, dessen Stand vom hier gesehenen abweicht,
    ohne dass diese Session selbst es geschrieben hat (ab jetzt mitgeschrieben)."""
    db.info[_OWN] = set()
    if not event.contains(db, "before_flush", _note_own_writes):
        event.listen(db, "before_flush", _note_own_writes)
    loaded = load_all(db, lock=True)
    stored = _settings(db, HASH_KEY)
    edited_once = {key for (key,) in db.query(ContentModuleSnapshot.module_key)}
    pristine: dict[str, str | None] = {}
    for key, seed in MODULES.items():
        if key not in loaded:
            pristine[key] = None
            continue
        state = db_state(*loaded[key])
        current = content_hash(state)
        if key in stored:
            unedited = current == stored[key]
        else:
            unedited = key not in edited_once or current in BASELINE.get(key, ())
        if unedited or current == content_hash(source_state(seed)):
            pristine[key] = current
    return pristine


def _assign_missing_uids(loaded: dict) -> None:
    """Bootstrap für Datenbanken bis v1.42.0: Zeilen ohne Kennung bekommen die
    des Stands v1.42.0 (STRUCTURE) — zugeordnet wie der Sync von v1.42.0 es tat:
    Widgets über ihre widget_id, alle anderen Blöcke als n-ter Block ihres Typs,
    Fragen über die Position (bei gleichem Fragetyp). Was sich so nicht zuordnen
    lässt (Trainer-Blöcke, eigene Module), bekommt eine neue Kennung. Läuft je
    Zeile einmal; danach gilt nur noch die Kennung."""
    for key, (_m, blocks, questions) in loaded.items():
        known = STRUCTURE.get(key, {"blocks": [], "quiz": []})
        taken = {b.uid for b in blocks if b.uid}
        pools: dict[tuple, list[str]] = defaultdict(list)
        for type_, uid in reversed(known["blocks"]):
            if uid not in taken:
                pools[(type_, uid if type_ == "widget" else None)].append(uid)
        for block in blocks:
            if block.uid is None:
                pool = pools[(block.type, block.widget_id if block.type == "widget" else None)]
                block.uid = pool.pop() if pool else new_uid()
        taken = {q.uid for q in questions if q.uid}
        for position, question in enumerate(questions):
            if question.uid is None:
                qtype, uid = known["quiz"][position] if position < len(known["quiz"]) else (None, None)
                question.uid = uid if qtype == question.qtype and uid not in taken else new_uid()
                taken.add(question.uid)


def _signature(item: dict, fields: tuple[str, ...]) -> str:
    return json.dumps([item[f] for f in fields], sort_keys=True)


def _match_rows(rows: list, items: list[dict], fields: tuple[str, ...]) -> list:
    """Ordnet jedem Eintrag der Vorgabe die vorhandene Zeile zu (None = neu):

    1. über die Kennung;
    2. sonst über identischen Inhalt — die Zeile übernimmt dann die Kennung der
       Vorgabe (z. B. im Editor gelöscht und inhaltsgleich neu angelegt);
    3. nur für Einträge OHNE Kennung (alte Snapshots, API-Aufrufe ohne uid):
       gleiche Position bei gleichem Typ, wie vor Einführung der Kennungen
       (die Textkorrektur an Ort und Stelle)."""
    by_uid = {row.uid: row for row in rows if row.uid}
    matched = [by_uid.pop(item["uid"], None) if item.get("uid") else None for item in items]
    free = {id(row) for row in rows} - {id(row) for row in matched if row is not None}
    by_content: dict[str, list] = defaultdict(list)
    for row in reversed(rows):
        if id(row) in free:
            by_content[_signature({f: getattr(row, f) for f in fields}, fields)].append(row)
    for i, item in enumerate(items):
        if matched[i] is None and by_content[_signature(item, fields)]:
            matched[i] = by_content[_signature(item, fields)].pop()
            free.discard(id(matched[i]))
    for i, item in enumerate(items):
        if (matched[i] is None and not item.get("uid") and i < len(rows) and id(rows[i]) in free
                and getattr(rows[i], fields[0]) == item[fields[0]]):
            matched[i] = rows[i]
            free.discard(id(rows[i]))
    return matched


def _moved(old: list | None, new: list | None) -> bool:
    """Steht ein Optionstext, den es weiter gibt, nicht mehr an seiner Stelle?"""
    return any(o in (new or []) and (new or [])[i:i + 1] != [o] for i, o in enumerate(old or []))


def _same_key(row: ContentQuizQuestion, item: dict) -> bool:
    """Darf die Fragezeile (und damit ihre DB-id, an der alte Abgaben hängen)
    bleiben? Nur wenn ein alter Options-Index gegen die neue Fassung noch
    dasselbe bedeutet: Typ gleich, Lösung gleich und kein weiter vorhandener
    Optionstext (de oder en) an eine andere Position gerückt. Sonst würden alte
    Abgaben gegen den neuen Schlüssel bewertet — Statistik und
    /practice?mode=wrong. Die Zeile BLEIBT bei Textkorrekturen an Prompt,
    Erklärung und am Wortlaut von Optionen sowie bei am Ende angefügten oder
    gestrichenen Optionen (die Indizes davor bedeuten dasselbe).
    ponytail: erkennt Umsortieren nur an unveränderten Texten; wer Optionen
    umsortiert UND alle umformuliert, vergibt eine neue Frage-id (Autorenregel)."""
    return (row.qtype == item["qtype"] and row.answer == item["answer"]
            and not _moved(row.options_de, item["options_de"])
            and not _moved(row.options_en, item["options_en"]))


def _write_rows(db: Session, model, key: str, existing: list, matched: list, items: list[dict],
                fields: tuple[str, ...]) -> None:
    """Schreibt items in die zugeordneten Zeilen (matched[i] gehört zu items[i],
    None = neu anlegen) und löscht nicht zugeordnete. Zugeordnete Zeilen behalten
    ihre DB-id."""
    taken = {row.uid for row, item in zip(matched, items, strict=True) if row is not None and not item.get("uid")}
    for position, (row, item) in enumerate(zip(matched, items, strict=True)):
        uid = item.get("uid") or (row.uid if row is not None else None)
        if not uid or (uid in taken and item.get("uid")):  # ohne oder mit doppelter Kennung geliefert
            uid = new_uid()
        taken.add(uid)
        if row is None:
            row = model(module_key=key)
            db.add(row)
        row.uid, row.position = uid, position
        for name in fields:
            setattr(row, name, item[name])
    kept = {id(row) for row in matched}
    for row in existing:
        if id(row) not in kept:
            db.delete(row)


def apply_state(db: Session, key: str, m: ContentModule, blocks: list[ContentBlock],
                questions: list[ContentQuizQuestion], state: dict, *, keep_comments: bool = False) -> int:
    """Bringt ein Modul in-place auf state (Form von serialize_module); blocks und
    questions sind seine Zeilen in Positionsreihenfolge. Zuordnung siehe
    Modul-Docstring und _match_rows.

    Kommentare hängen an der Blockposition und wandern mit ihrem Block mit.
    Entfällt der Block, wird der Kommentar gelöscht (Editor: der Trainer hat den
    Block bewusst entfernt) bzw. mit keep_comments an den nächsten davor
    verbliebenen Block gehängt (Sync: nie automatisch Teilnehmerbeiträge
    löschen). Gibt die Zahl der so umgehängten Kommentare zurück.

    Quiz-Abgaben (QuizResult) werden nie angefasst: Punktzahl und Gesamtzahl
    sind dort zum Abgabezeitpunkt gespeichert."""
    matched_blocks = _match_rows(blocks, state["blocks"], BLOCK_FIELDS)
    new_index = {id(row): position for position, row in enumerate(matched_blocks) if row is not None}
    moved = 0
    for comment in db.query(Comment).filter(Comment.module_key == key):
        if not 0 <= comment.block_index < len(blocks):
            continue
        survivors = [new_index[id(row)] for row in reversed(blocks[:comment.block_index + 1]) if id(row) in new_index]
        if id(blocks[comment.block_index]) in new_index:
            comment.block_index = survivors[0]
        elif keep_comments:
            comment.block_index = survivors[0] if survivors else 0
            moved += 1
        else:
            db.delete(comment)
    for name in _MODULE_FIELDS:
        setattr(m, name, state[name])
    _write_rows(db, ContentBlock, key, blocks, matched_blocks, state["blocks"], BLOCK_FIELDS)
    # Geänderter Lösungsschlüssel = neue Zeile, die alte fällt weg (siehe _same_key).
    matched_questions = [row if row is not None and _same_key(row, item) else None
                         for row, item in zip(_match_rows(questions, state["quiz"], QUESTION_FIELDS),
                                              state["quiz"], strict=True)]
    _write_rows(db, ContentQuizQuestion, key, questions, matched_questions, state["quiz"], QUESTION_FIELDS)
    return moved


def sync_content(db: Session, pristine: dict[str, str | None], fresh: frozenset[str] = frozenset()) -> dict:
    """Bringt die unveränderten Module auf den Quellstand und merkt sich dessen
    Hash. Je Modul ein Savepoint: ein Fehler rollt nur dieses Modul zurück.
    Committet nicht — das macht der Aufrufer zusammen mit dem Rest des Seeds.

    fresh: in diesem Lauf erst geseedete Module. Die Widget-Migrationen sortieren
    auch dort einzelne Blöcke um; das wird angeglichen, ist aber kein Update,
    das man melden müsste."""
    loaded = load_all(db)
    # Seit pristine_modules von jemand anderem gespeichert (dort (b)) -> Trainer-Stand.
    # ponytail: Module, die die Seed-Migrationen dieses Laufs selbst angefasst
    # haben, sind davon ausgenommen (ihr Hash hat sich ohnehin geändert). Soll
    # auch dort ein alter Container nichts überschreiben können: Versionsspalte
    # je Modul, die jeder Schreiber hochzählt.
    own = db.info.get(_OWN, set())
    changed_elsewhere = {key for key, seen in pristine.items()
                         if seen and key in loaded and key not in own
                         and content_hash(db_state(*loaded[key])) != seen}
    _assign_missing_uids(loaded)
    stored = _settings(db, HASH_KEY)
    reported = _settings(db, SKIPPED_KEY)
    updated, skipped, failed = [], {}, []
    for key, seed in MODULES.items():
        if key not in loaded:
            continue
        m, blocks, questions = loaded[key]
        src = source_state(seed)
        src_hash = content_hash(src)
        if key not in pristine or key in changed_elsewhere:
            if content_hash(db_state(m, blocks, questions)) != src_hash:
                skipped[key] = "vom Trainer geändert"
            continue
        try:
            with db.begin_nested():
                if db_state(m, blocks, questions) != src:
                    moved = apply_state(db, key, m, blocks, questions, src, keep_comments=True)
                    if moved:
                        log.warning("Content-Sync: Modul %s: %s Kommentar(e) an entfallenen Blöcken hängen "
                                    "jetzt am Block davor", key, moved)
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
