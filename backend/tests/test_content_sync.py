"""Content-Sync (app/content/sync.py): geänderte Auslieferungsinhalte erreichen
Bestands-DBs, ohne Trainer-Stände zu überschreiben oder Teilnehmerdaten zu lösen.

Jeder Test bekommt eine eigene SQLite-Datei statt der gemeinsamen Test-DB —
die anderen Testdateien verbiegen dort Module, und hier zählt der exakte Stand.
"""
import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session

import app.main  # noqa: F401  (registriert alle Modelle an Base)
from app.content import sync
from app.content.registry import MODULES, public_module
from app.content.seed import seed_missing_content
from app.database import Base
from app.models.audit_log import AuditLog
from app.models.comment import Comment
from app.models.content import ContentBlock, ContentModuleSnapshot, ContentQuizQuestion
from app.services import grading
from app.models.course import Course
from app.models.course_module import CourseModule
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.models.setting import Setting
from app.routers.trainer_content import _apply, _seed_to_module_in

KEY = "playbooks-grundlagen"  # an_*-Modul mit debug-Block
REPO = Path(__file__).resolve().parents[2]
V1_41_1 = "93f88fe"
V1_42_0 = "d390453"  # letzter Stand ohne Kennungen (uid) in der DB


@pytest.fixture
def db(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'sync.db'}")
    Base.metadata.create_all(engine)
    with Session(engine, autoflush=False) as session:
        yield session
    engine.dispose()


def _blocks(db, key=KEY):
    return db.query(ContentBlock).filter(ContentBlock.module_key == key).order_by(ContentBlock.position).all()


def _questions(db, key=KEY):
    return db.query(ContentQuizQuestion).filter(
        ContentQuizQuestion.module_key == key).order_by(ContentQuizQuestion.position).all()


def _state(db, key=KEY):
    return sync.db_state(*sync.load_all(db)[key])


def _ship_new_source(monkeypatch, key=KEY):
    """Simuliert ein Release mit korrigiertem Inhalt: Text, Quiz-Prompt/-Optionen
    und der wrong-Index eines debug-Blocks (samt ergänzter Zeile) ändern sich,
    die Struktur nicht."""
    new = copy.deepcopy(MODULES[key])
    text = next(b for b in new["blocks"] if b["type"] == "text")
    text["value"] = {"de": text["value"]["de"] + " KORRIGIERT", "en": text["value"]["en"] + " FIXED"}
    for b in new["blocks"]:
        if b["type"] == "debug":
            for lang in ("de", "en"):
                b["payload"][f"lines_{lang}"] = [*b["payload"][f"lines_{lang}"], "# neu"]
            b["payload"]["wrong"] = [len(b["payload"]["lines_de"]) - 1]
    q = new["quiz"]["questions"][0]
    q["prompt"] = {"de": q["prompt"]["de"] + " (präzisiert)", "en": q["prompt"]["en"] + " (clarified)"}
    monkeypatch.setitem(MODULES, key, new)
    return new


def _trainer_edit(db, key=KEY, text="Vom Trainer umgeschrieben"):
    """Wie ein Speichern im Editor: Inhalt geändert, Snapshot vorhanden."""
    block = next(b for b in _blocks(db, key) if b.type == "text")
    block.value_de = text
    if not db.get(ContentModuleSnapshot, key):
        db.add(ContentModuleSnapshot(module_key=key, data={}))
    db.commit()


def _forget_sync_state(db):
    """Bestands-DB aus der Zeit vor dem Sync: keine gespeicherten Hashes."""
    db.query(Setting).filter(Setting.key.startswith("content-sync")).delete(synchronize_session=False)
    db.commit()


def test_fresh_seed_equals_source_and_second_start_is_noop(db):
    assert seed_missing_content(db) == {"updated": [], "skipped": {}, "failed": []}
    for key, seed in MODULES.items():
        assert _state(db, key) == sync.source_state(seed), key
        assert db.get(Setting, sync.HASH_KEY + key).value == sync.content_hash(sync.source_state(seed))

    audit_rows = db.query(AuditLog).count()
    result = seed_missing_content(db)
    assert result == {"updated": [], "skipped": {}, "failed": []}
    assert db.query(AuditLog).count() == audit_rows


def test_changed_source_updates_in_place_and_keeps_participant_data(db, monkeypatch):
    seed_missing_content(db)
    question_ids = [q.id for q in _questions(db)]
    debug_index = next(i for i, b in enumerate(_blocks(db)) if b.type == "debug")
    course = Course(name="Kurs", join_code="SYNC01", workshop_key="ansible")
    db.add(course)
    db.flush()
    participant = Participant(course_id=course.id, name="Ada")
    db.add(participant)
    db.flush()
    answers = {str(qid): 0 for qid in question_ids}
    db.add_all([
        CourseModule(course_id=course.id, module_key=KEY),
        Progress(participant_id=participant.id, module_key=KEY, done=True),
        QuizResult(participant_id=participant.id, module_key=KEY, score=3, total=len(answers), answers=answers),
        Comment(course_id=course.id, module_key=KEY, block_index=debug_index, body="Frage dazu",
                author_kind="participant", author_name="Ada", participant_id=participant.id),
    ])
    db.commit()

    new = _ship_new_source(monkeypatch)
    result = seed_missing_content(db)

    assert result["updated"] == [KEY] and not result["skipped"] and not result["failed"]
    assert _state(db) == sync.source_state(new)
    # (e) die wrong-Index-Korrektur des debug-Blocks ist in der DB und in der Auslieferung
    src_debug = next(b for b in new["blocks"] if b["type"] == "debug")
    assert _blocks(db)[debug_index].payload["wrong"] == src_debug["payload"]["wrong"]
    delivered = public_module(db, KEY)
    assert delivered["blocks"][debug_index]["wrong"] == src_debug["payload"]["wrong"]
    assert delivered["blocks"][debug_index]["lines"][-1] == "# neu"
    # Fragen sind dieselben Zeilen geblieben -> alte Abgaben passen weiter zu den Fragen
    assert [q.id for q in _questions(db)] == question_ids
    assert [q["id"] for q in delivered["quiz"]["questions"]] == list(answers)
    assert delivered["quiz"]["questions"][0]["prompt"].endswith("(präzisiert)")
    quiz_result = db.query(QuizResult).one()
    assert (quiz_result.score, quiz_result.total, quiz_result.answers) == (3, len(answers), answers)
    assert db.query(Progress).one().done is True
    assert db.query(CourseModule).filter(CourseModule.module_key == KEY).count() == 1
    assert db.query(Comment).one().block_index == debug_index
    assert db.query(AuditLog).filter(AuditLog.action == "content.sync").count() == 1

    # (c) zweiter Start: nichts mehr zu tun
    assert seed_missing_content(db) == {"updated": [], "skipped": {}, "failed": []}
    assert db.query(AuditLog).filter(AuditLog.action == "content.sync").count() == 1


def test_trainer_edited_module_is_left_alone_and_reported_once(db, monkeypatch):
    seed_missing_content(db)
    _trainer_edit(db)
    edited = _state(db)

    new = _ship_new_source(monkeypatch)
    result = seed_missing_content(db)

    assert result["updated"] == [] and list(result["skipped"]) == [KEY]
    assert _state(db) == edited
    skipped = db.query(AuditLog).filter(AuditLog.action == "content.sync.skipped")
    assert [a.target for a in skipped] == [f"module:{KEY}"]
    seed_missing_content(db)  # weiterer Start: unverändert, aber kein zweiter Audit-Eintrag
    assert _state(db) == edited and skipped.count() == 1

    # Trainer lädt im Editor den Auslieferungszustand -> Modul nimmt wieder am Sync teil.
    loaded = sync.load_all(db)[KEY]
    _apply(db, KEY, loaded[0], _seed_to_module_in(new), loaded[1], loaded[2])
    db.commit()
    assert seed_missing_content(db) == {"updated": [], "skipped": {}, "failed": []}
    newer = copy.deepcopy(new)
    newer["scenario"] = {"de": "Neues Szenario", "en": "New scenario"}
    monkeypatch.setitem(MODULES, KEY, newer)
    assert seed_missing_content(db)["updated"] == [KEY]
    assert _state(db) == sync.source_state(newer)


def test_bootstrap_without_stored_hash(db, monkeypatch):
    """Bestands-DB ohne gespeicherte Hashes: nie gespeicherte Module (kein
    Snapshot) und Module mit Baseline-Stand werden nachgezogen, ein editiertes nicht."""
    never_saved, saved_unchanged, edited = KEY, "arp", "dns"
    seed_missing_content(db)
    db.add(ContentModuleSnapshot(module_key=saved_unchanged, data={}))
    _trainer_edit(db, edited)
    _forget_sync_state(db)
    monkeypatch.setattr(sync, "BASELINE", {saved_unchanged: [sync.content_hash(_state(db, saved_unchanged))]})
    edited_state = _state(db, edited)

    new = {key: _ship_new_source(monkeypatch, key) for key in (never_saved, saved_unchanged, edited)}
    result = seed_missing_content(db)

    assert sorted(result["updated"]) == sorted([never_saved, saved_unchanged])
    assert list(result["skipped"]) == [edited]
    assert _state(db, never_saved) == sync.source_state(new[never_saved])
    assert _state(db, saved_unchanged) == sync.source_state(new[saved_unchanged])
    assert _state(db, edited) == edited_state
    assert seed_missing_content(db)["updated"] == []


def test_reordered_blocks_follow_source_and_comments_move_with_their_block(db):
    """Die Widget-Migrationen haben Blöcke in Bestands-DBs teils anders einsortiert
    als die Quelle. Reine Umsortierung wird angeglichen, der Kommentar bleibt am Block."""
    seed_missing_content(db)
    blocks = _blocks(db, "arp")
    widget = next(i for i, b in enumerate(blocks) if b.type == "widget")
    other = next(i for i, b in enumerate(blocks) if b.type != "widget" and i > widget)
    blocks[widget].position, blocks[other].position = other, widget
    course = Course(name="Kurs", join_code="SYNC02", workshop_key="network")
    db.add(course)
    db.flush()
    db.add(Comment(course_id=course.id, module_key="arp", block_index=other, body="zum Widget",
                   author_kind="trainer", author_name="T"))
    db.commit()
    _forget_sync_state(db)

    assert seed_missing_content(db)["updated"] == ["arp"]
    assert _state(db, "arp") == sync.source_state(MODULES["arp"])
    assert db.query(Comment).one().block_index == widget


def _participant_data(db, key, workshop_key, join_code, comment_blocks):
    """Kurs mit einer Teilnehmerin: bestandene Abgabe zu allen Fragen des Moduls
    und je ein Kommentar an den genannten Blockpositionen. Gibt je Kommentar die
    DB-id des Blocks zurück, an dem er hängt."""
    course = Course(name="Kurs", join_code=join_code, workshop_key=workshop_key)
    db.add(course)
    db.flush()
    participant = Participant(course_id=course.id, name="Ada")
    db.add(participant)
    db.flush()
    questions, blocks = _questions(db, key), _blocks(db, key)
    db.add_all([
        Progress(participant_id=participant.id, module_key=key, done=True),
        QuizResult(participant_id=participant.id, module_key=key, score=len(questions), total=len(questions),
                   answers={str(q.id): q.answer for q in questions}),
        *(Comment(course_id=course.id, module_key=key, block_index=i, body=f"an Block {blocks[i].id}",
                  author_kind="participant", author_name="Ada", participant_id=participant.id)
          for i in comment_blocks),
    ])
    db.commit()
    return [blocks[i].id for i in comment_blocks]


def _extend_source(monkeypatch, key):
    """Simuliert den Ausbau eines Moduls: neuer Block ganz vorn (ein Typ, den der
    Sync nicht kennt, mit beliebigem Payload), neue Frage ganz vorn (mit
    Erklärung), Erklärung an der bisher ersten Frage."""
    new = copy.deepcopy(MODULES[key])
    new["blocks"].insert(0, {"type": "zukunft", "id": "zukunft-neu", "payload": {"x": [1, {"y": "z"}]}})
    new["quiz"]["questions"][0]["explanation"] = {"de": "Weil es so ist.", "en": "Because."}
    new["quiz"]["questions"].insert(0, {
        "id": "neu1", "type": "single", "prompt": {"de": "Neu?", "en": "New?"},
        "options": {"de": ["ja", "nein"], "en": ["yes", "no"]}, "answer": 0,
        "explanation": {"de": "Ja, neu.", "en": "Yes, new."}})
    monkeypatch.setitem(MODULES, key, new)
    return new


def test_structural_change_updates_in_place_and_keeps_participant_data(db, monkeypatch):
    """Blöcke und Fragen kommen hinzu, entfallen und wechseln den Platz, während
    Abgaben und Kommentare am Modul hängen: Zuordnung über die Kennung, nichts
    wird ausgelassen, nichts verliert seinen Bezug."""
    seed_missing_content(db)
    blocks, questions = _blocks(db), _questions(db)
    gone, kept, last = 1, 2, len(blocks) - 1
    block_ids = _participant_data(db, KEY, "ansible", "SYNC03", [gone, kept, last])
    quiz_result = db.query(QuizResult).one()
    stored = (quiz_result.score, quiz_result.total, dict(quiz_result.answers))

    new = _extend_source(monkeypatch, KEY)
    removed_block, removed_question = new["blocks"].pop(gone + 1), new["quiz"]["questions"].pop()  # +1: neuer Block vorn
    new["blocks"].append(new["blocks"].pop(2))  # der bisher dritte Block (Kommentar "kept") wandert ans Ende
    result = seed_missing_content(db)

    assert result == {"updated": [KEY], "skipped": {}, "failed": []}
    assert _state(db) == sync.source_state(new)
    by_uid = {q.uid: q.id for q in _questions(db)}
    assert by_uid.keys() == {q["id"] for q in new["quiz"]["questions"]}
    for old in questions[:-1]:  # verbliebene Fragen sind dieselben Zeilen
        assert by_uid[old.uid] == old.id
    assert by_uid["neu1"] not in {q.id for q in questions}
    assert removed_question["id"] not in by_uid and removed_block["id"] not in {b.uid for b in _blocks(db)}
    # Abgabe, Fortschritt: unverändert, nichts rückwirkend neu bewertet
    quiz_result = db.query(QuizResult).one()
    assert (quiz_result.score, quiz_result.total, quiz_result.answers) == stored
    assert db.query(Progress).one().done is True
    # Kommentare: wandern mit ihrem Block; der am entfallenen Block hängt am Block davor
    position = {b.id: b.position for b in _blocks(db)}
    comments = {c.body: c.block_index for c in db.query(Comment)}
    assert comments[f"an Block {block_ids[1]}"] == position[block_ids[1]] == len(position) - 1
    assert comments[f"an Block {block_ids[2]}"] == position[block_ids[2]]
    assert comments[f"an Block {block_ids[0]}"] == position[blocks[gone - 1].id]
    # Statistik: die alte Abgabe zählt für die neue Frage nicht als Fehlversuch
    stats = {s["id"]: s for s in grading.question_stats(
        {"questions": [{"id": str(q.id), "type": q.qtype, "answer": q.answer} for q in _questions(db)]},
        [quiz_result.answers])}
    assert stats[str(by_uid["neu1"])] == {"id": str(by_uid["neu1"]), "correct": 0, "attempts": 0}
    assert all(s["correct"] == s["attempts"] == 1 for qid, s in stats.items() if qid != str(by_uid["neu1"]))
    # Erklärungen sind in der DB, aber nicht in der Auslieferung vor der Abgabe
    assert _questions(db)[0].explanation_en == "Yes, new." and _questions(db)[1].explanation_de == "Weil es so ist."
    assert all("explanation" not in q and "answer" not in q for q in public_module(db, KEY)["quiz"]["questions"])

    assert seed_missing_content(db) == {"updated": [], "skipped": {}, "failed": []}


def test_hash_ignores_ids_and_missing_explanations(db):
    """Die "unediert"-Erkennung hängt am Inhalt: Kennungen zählen nicht, eine
    Erklärung schon. (Dass die Hashes denen von v1.42.0 entsprechen, belegt der
    Test gegen die echten alten Stände unten.)"""
    seed_missing_content(db)
    state = _state(db)
    without_ids = copy.deepcopy(state)
    for item in without_ids["blocks"] + without_ids["quiz"]:
        item["uid"] = None
    assert sync.content_hash(without_ids) == sync.content_hash(state)
    state["quiz"][0]["explanation_de"] = "x"
    assert sync.content_hash(without_ids) != sync.content_hash(state)


# Seedet mit dem Code des alten Stands (cwd = dessen backend/) eine leere DB.
_SEED_OLD_TREE = """
import importlib, json, pkgutil, sys
sys.path.insert(0, ".")
from app.database import Base, engine, SessionLocal
import app.models as models
for mod in pkgutil.iter_modules(models.__path__):
    importlib.import_module(f"app.models.{mod.name}")
Base.metadata.create_all(engine)
from app.content.registry import MODULES
from app.content.seed import seed_missing_content
seed_missing_content(SessionLocal())
print(json.dumps(MODULES))
"""


def _run_old_seed(tmp_path, commit, db_url):
    """Startet den Seed (samt damaliger Migrationen/Sync) mit dem Code von commit."""
    tree = tmp_path / commit
    tree.mkdir()
    try:
        archive = subprocess.run(["git", "-C", str(REPO), "archive", commit, "backend/app"],
                                 check=True, capture_output=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip(f"Commit {commit} nicht verfügbar (flacher Checkout)")
    subprocess.run(["tar", "-x", "-C", str(tree)], input=archive, check=True)
    return json.loads(subprocess.run(
        [sys.executable, "-c", _SEED_OLD_TREE], cwd=tree / "backend", check=True,
        capture_output=True, text=True, env={**os.environ, "DATABASE_URL": db_url}).stdout)


def _add_new_columns(engine):
    """Was im Betrieb Alembic erledigt: Spalten, die das alte Schema nicht kennt."""
    with engine.begin() as conn:
        for table in Base.metadata.sorted_tables:
            have = {col["name"] for col in inspect(conn).get_columns(table.name)}
            for col in table.columns:
                if col.name not in have:
                    conn.execute(text(f'ALTER TABLE {table.name} ADD COLUMN "{col.name}" '
                                      f'{col.type.compile(engine.dialect)}'))


@pytest.mark.parametrize("history", [(V1_41_1,), (V1_41_1, V1_42_0)], ids=["von-v1.41.1", "ueber-v1.42.0"])
def test_real_old_database_gets_ids_and_structural_update(tmp_path, monkeypatch, history):
    """Beweis gegen die echten alten Stände, MIT Teilnehmerdaten: eine mit dem
    Code von v1.41.1 geseedete DB — direkt oder nachdem v1.42.0 (erster Sync,
    speichert Hashes) darauf lief — gilt je Modul als unediert, bekommt beim
    ersten Start die Kennungen des Stands v1.42.0 und wird danach auf eine
    Quelle mit eingefügten Blöcken/Fragen gezogen: alte Zeilen bleiben dieselben
    (Frage-ids, Abgaben, Kommentare), neue kommen dazu. Braucht die
    Git-Historie; in flachen Checkouts (CI) übersprungen."""
    db_url = f"sqlite:///{tmp_path / 'old.db'}"
    extended = ("arp", "dns", KEY, "krypto-grundlagen")
    old_modules = _run_old_seed(tmp_path, history[0], db_url)
    engine = create_engine(db_url)
    _add_new_columns(engine)
    with Session(engine, autoflush=False) as db:
        assert not db.query(Setting).filter(Setting.key.startswith(sync.HASH_KEY)).count()
        for key, loaded in sync.load_all(db).items():
            assert sync.content_hash(sync.db_state(*loaded)) in sync.BASELINE[key], key
            assert sync.content_hash(sync.source_state(old_modules[key])) in sync.BASELINE[key], key
        # jedes Modul gilt als im Editor gespeichert -> nur Baseline/gespeicherter Hash kann es freigeben
        db.add_all(ContentModuleSnapshot(module_key=key, data={}) for key in old_modules)
        commented = {key: _participant_data(db, key, "network", f"OLD{i}", [0, len(_blocks(db, key)) - 1])
                     for i, key in enumerate(extended)}
        question_ids = {key: [q.id for q in _questions(db, key)] for key in old_modules}
        block_ids = {key: {b.id for b in _blocks(db, key)} for key in old_modules}
        results = {r.module_key: (r.score, r.total, dict(r.answers)) for r in db.query(QuizResult)}

    for commit in history[1:]:  # v1.42.0 läuft auf der DB: sein Sync, seine Hashes
        newer_modules = _run_old_seed(tmp_path, commit, db_url)
        with Session(engine, autoflush=False) as db:
            for key, loaded in sync.load_all(db).items():
                assert sync.content_hash(sync.db_state(*loaded)) in sync.BASELINE[key], key
                assert sync.db_state(*loaded)["blocks"][0]["uid"] is None  # v1.42.0 kennt keine Kennungen
                assert sync.STRUCTURE[key]["quiz"] == [[q["type"], q["id"]] for q in newer_modules[key]["quiz"]["questions"]]

    with Session(engine, autoflush=False) as db:
        for key in extended:
            _extend_source(monkeypatch, key)
        result = seed_missing_content(db)

        assert not result["skipped"] and not result["failed"]
        for key in old_modules:
            assert _state(db, key) == sync.source_state(MODULES[key]), key
            # alle alten Fragen sind dieselben Zeilen geblieben, in derselben Reihenfolge
            assert [q.id for q in _questions(db, key) if q.uid != "neu1"] == question_ids[key], key
            assert block_ids[key] <= {b.id for b in _blocks(db, key)}, key  # keine alte Blockzeile ersetzt
        for key in extended:
            assert _questions(db, key)[0].uid == "neu1" and _blocks(db, key)[0].uid == "zukunft-neu"
            position = {b.id: b.position for b in _blocks(db, key)}
            comments = {c.body: c.block_index for c in db.query(Comment).filter(Comment.module_key == key)}
            assert comments == {f"an Block {bid}": position[bid] for bid in commented[key]}, key
            assert min(comments.values()) == 1  # der Kommentar am bisher ersten Block steht hinter dem neuen
        assert {r.module_key: (r.score, r.total, r.answers) for r in db.query(QuizResult)} == results
        assert db.query(Progress).filter(Progress.done).count() == len(extended)
        assert seed_missing_content(db)["updated"] == []
    engine.dispose()
