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
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import app.main  # noqa: F401  (registriert alle Modelle an Base)
from app.content import sync
from app.content.registry import MODULES, public_module
from app.content.seed import seed_missing_content
from app.database import Base
from app.models.audit_log import AuditLog
from app.models.comment import Comment
from app.models.content import ContentBlock, ContentModuleSnapshot, ContentQuizQuestion
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
    _apply(db, KEY, loaded[0], _seed_to_module_in(new), loaded[1])
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


def test_structural_change_with_participant_data_is_skipped_not_guessed(db, monkeypatch):
    seed_missing_content(db)
    course = Course(name="Kurs", join_code="SYNC03", workshop_key="network")
    db.add(course)
    db.flush()
    participant = Participant(course_id=course.id, name="Bo")
    db.add(participant)
    db.flush()
    db.add(Comment(course_id=course.id, module_key="arp", block_index=0, body="x",
                   author_kind="trainer", author_name="T"))
    db.add(QuizResult(participant_id=participant.id, module_key="dns", score=1, total=1, answers={}))
    db.commit()
    before = {key: _state(db, key) for key in ("arp", "dns", "vpn")}

    for key in ("arp", "vpn"):  # ein Block entfällt
        new = copy.deepcopy(MODULES[key])
        del new["blocks"][0]
        monkeypatch.setitem(MODULES, key, new)
    new_dns = copy.deepcopy(MODULES["dns"])  # eine Frage entfällt
    del new_dns["quiz"]["questions"][0]
    monkeypatch.setitem(MODULES, "dns", new_dns)
    result = seed_missing_content(db)

    assert sorted(result["skipped"]) == ["arp", "dns"]
    assert _state(db, "arp") == before["arp"] and _state(db, "dns") == before["dns"]
    # ohne Teilnehmerdaten am Modul darf die Struktur nachgezogen werden
    assert result["updated"] == ["vpn"]
    assert _state(db, "vpn") == sync.source_state(MODULES["vpn"])


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


def test_real_v1_41_1_database_matches_baseline_and_upgrades(tmp_path):
    """Beweis für den Bootstrap gegen den echten alten Stand: eine mit dem Code
    von v1.41.1 geseedete DB (inkl. der damaligen Migrationen) trifft je Modul
    die Baseline — ebenso der reine Quellstand von damals — und wird vom
    heutigen Start vollständig auf die aktuelle Quelle gezogen, mit denselben
    Frage-ids. Braucht die Git-Historie; in flachen Checkouts (CI) übersprungen."""
    try:
        archive = subprocess.run(["git", "-C", str(REPO), "archive", V1_41_1, "backend/app"],
                                 check=True, capture_output=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip(f"Commit {V1_41_1} nicht verfügbar (flacher Checkout)")
    subprocess.run(["tar", "-x", "-C", str(tmp_path)], input=archive, check=True)
    db_url = f"sqlite:///{tmp_path / 'old.db'}"
    old_modules = json.loads(subprocess.run(
        [sys.executable, "-c", _SEED_OLD_TREE], cwd=tmp_path / "backend", check=True,
        capture_output=True, text=True, env={**os.environ, "DATABASE_URL": db_url}).stdout)

    engine = create_engine(db_url)
    with Session(engine, autoflush=False) as db:
        assert not db.query(Setting).filter(Setting.key.startswith(sync.HASH_KEY)).count()
        for key, loaded in sync.load_all(db).items():
            assert sync.content_hash(sync.db_state(*loaded)) in sync.BASELINE[key], key
            assert sync.content_hash(sync.source_state(old_modules[key])) in sync.BASELINE[key], key
        # jedes Modul gilt als im Editor gespeichert -> nur die Baseline kann es freigeben
        db.add_all(ContentModuleSnapshot(module_key=key, data={}) for key in old_modules)
        db.commit()
        question_ids = {key: [q.id for q in _questions(db, key)] for key in old_modules}

        result = seed_missing_content(db)

        assert not result["skipped"] and not result["failed"]
        for key in old_modules:
            assert _state(db, key) == sync.source_state(MODULES[key]), key
            assert [q.id for q in _questions(db, key)] == question_ids[key], key
        assert seed_missing_content(db)["updated"] == []
    engine.dispose()
