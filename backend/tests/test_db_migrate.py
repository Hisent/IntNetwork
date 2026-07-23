"""Sicherungen gegen den Startup-Hänger von v1.24: ein blockiertes ALTER TABLE
bzw. ein belegter Advisory-Lock darf den Start nicht still blockieren, sondern
muss nach begrenzter Zeit mit verwertbarer Meldung scheitern."""

import pytest
from alembic import command
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError

from app import db_migrate
from app.config import settings
from app.database import Base, engine
from app.main import app

_HEAD = "75aeb8d5399c"        # trainer_token_version_and_core_fk_cascades
_VORGAENGER = "7305d4053e50"  # add_trainer_credential


def _blocked() -> OperationalError:
    return OperationalError("ALTER TABLE participant", {}, Exception("lock timeout"))


def test_migration_wird_nach_fremder_sperre_wiederholt(monkeypatch):
    versuche = []

    def fake_migrate():
        versuche.append(1)
        if len(versuche) < 3:
            raise _blocked()

    monkeypatch.setattr(db_migrate, "_do_migrate", fake_migrate)
    monkeypatch.setattr(db_migrate.time, "sleep", lambda _s: None)

    db_migrate._migrate_with_retry()

    assert len(versuche) == 3


def test_dauerhafte_sperre_scheitert_mit_hinweis(monkeypatch):
    def fake_migrate():
        raise _blocked()

    monkeypatch.setattr(db_migrate, "_do_migrate", fake_migrate)
    monkeypatch.setattr(db_migrate.time, "sleep", lambda _s: None)

    with pytest.raises(RuntimeError, match="idle in transaction"):
        db_migrate._migrate_with_retry()


def test_belegter_lock_haengt_nicht_endlos(monkeypatch):
    class FakeResult:
        def scalar(self):
            return False

    class FakeConn:
        def __init__(self):
            self.aufrufe = 0

        def execute(self, *_args, **_kwargs):
            self.aufrufe += 1
            return FakeResult()

    monkeypatch.setattr(db_migrate, "_LOCK_WAIT_SECONDS", 0.0)
    monkeypatch.setattr(db_migrate.time, "sleep", lambda _s: None)
    conn = FakeConn()

    with pytest.raises(RuntimeError, match="Migrations-Lock"):
        db_migrate._acquire_lock(conn)

    assert conn.aufrufe >= 1


def test_migrationen_allein_erzeugen_das_vollstaendige_schema():
    """F: Base.metadata.create_all() läuft in main.py nicht mehr -- Alembic ist
    jetzt allein autoritativ. Auf einer frischen SQLite-DB (siehe conftest.py,
    die Datei wird je Testlauf neu angelegt) müssen die Migrationen daher
    bereits jede Tabelle anlegen, die die Modelle kennen. Fehlte hier eine,
    gäbe es keinen create_all-Fallback mehr, der das kaschiert."""
    with TestClient(app):
        pass
    fehlende = set(Base.metadata.tables) - set(inspect(engine).get_table_names())
    assert fehlende == set()


def test_75aeb8d5399c_ist_idempotent_wenn_objekte_schon_existieren(tmp_path, monkeypatch):
    """Regression zum Prod-Crashloop vom 2026-07-23.

    Die Prod-DB war urspruenglich per create_all gebaut (vor v1.35, als das noch
    in main.py lief) und ihr alembic_version stand hinter Head. Beim Redeploy
    lief 75aeb8d5399c auf einer DB, in der Spalte/FKs/Index TEILS SCHON
    existierten -- add_column/create_foreign_key/create_index scheiterten an
    "already exists" -> Startup-Crashloop.

    Genau diese Konstellation stellt der Test nach: Schema einmal auf Head
    bringen (alle Objekte existieren), alembic_version auf den Vorgaenger
    zuruecksetzen, dann erneut auf Head migrieren. Ohne die Idempotenz-Guards
    (fix ffcfb73) wirft der zweite Lauf; mit ihnen laeuft er sauber durch.

    Bewusst eigene tmp-DB statt der conftest-DB: der Test manipuliert
    alembic_version und darf den geteilten Zustand nicht verschmutzen.
    """
    db_url = f"sqlite:///{tmp_path / 'legacy.db'}"
    monkeypatch.setattr(settings, "database_url", db_url)
    cfg = db_migrate._config()

    # 1. Volles Schema: alle Objekte aus 75aeb8d5399c existieren jetzt.
    command.upgrade(cfg, "head")

    legacy_engine = create_engine(db_url)
    # alembic_version auf den Vorgaenger zuruecksetzen -> Alembic "vergisst",
    # dass 75aeb8d5399c schon lief, die Objekte bleiben aber in der DB.
    with legacy_engine.begin() as conn:
        conn.execute(text("UPDATE alembic_version SET version_num = :v"), {"v": _VORGAENGER})

    # 2. Der eigentliche Test: erneuter upgrade auf Head darf NICHT an
    #    "already exists"/"duplicate column" scheitern.
    command.upgrade(cfg, "head")

    with legacy_engine.connect() as conn:
        version = conn.execute(text("SELECT version_num FROM alembic_version")).scalar()
    legacy_engine.dispose()
    assert version == _HEAD
