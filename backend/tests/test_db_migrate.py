"""Sicherungen gegen den Startup-Hänger von v1.24: ein blockiertes ALTER TABLE
bzw. ein belegter Advisory-Lock darf den Start nicht still blockieren, sondern
muss nach begrenzter Zeit mit verwertbarer Meldung scheitern."""

import re
import subprocess
import sys
from pathlib import Path

import pytest
from alembic import command
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app import db_migrate
from app.config import settings
from app.database import Base, engine
from app.main import app

_HEAD = "c8d9e0f1a2b3"        # add_live_poll
_VORGAENGER = "7305d4053e50"  # add_trainer_credential (danach laufen 75aeb8d5399c, a6b7c8d9e0f1, b7c8d9e0f1a2 und c8d9e0f1a2b3 erneut)


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


def test_migration_schaltet_bestehende_logger_nicht_stumm():
    """fileConfig() in migrations/env.py deaktivierte mit dem Standard
    disable_existing_loggers=True alle schon angelegten Logger — die Warnung
    "Migration blockiert (Versuch x/3)" und jedes spaetere App-Log (z.B.
    fehlgeschlagene Audit-Eintraege) verschwanden danach lautlos."""
    import logging

    db_migrate._do_migrate()  # DB ist schon auf head: laedt nur env.py

    assert logging.getLogger("app.db_migrate").disabled is False
    assert logging.getLogger("app.services.audit").disabled is False


@pytest.fixture
def leere_db(tmp_path):
    """URL einer leeren Wegwerf-DB auf demselben System wie die Suite: unter
    Postgres eine eigene Datenbank (Downgrade/DDL darf die geteilte nicht
    anfassen), sonst eine SQLite-Datei."""
    if engine.dialect.name != "postgresql":
        yield f"sqlite:///{tmp_path / 'leer.db'}"
        return
    name = "intlab_test_downgrade"
    admin = create_engine(settings.database_url, isolation_level="AUTOCOMMIT")
    with admin.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {name}"))
        conn.execute(text(f"CREATE DATABASE {name}"))
    yield make_url(settings.database_url).set(database=name).render_as_string(hide_password=False)
    with admin.connect() as conn:
        conn.execute(text(f"DROP DATABASE {name} WITH (FORCE)"))
    admin.dispose()


def test_downgrade_und_erneutes_upgrade_laesst_module_unediert(leere_db, monkeypatch):
    """Der Downgrade von a6b7c8d9e0f1/b7c8d9e0f1a2 entfernt Spalten samt Inhalt
    (Erklärungen, goals_en). Blieben die gespeicherten Sync-Hashes stehen, gälte
    danach jedes Modul dauerhaft als "vom Trainer geändert" und bekäme nie
    wieder ein Inhalts-Update."""
    from app.content import sync
    from app.content.registry import MODULES
    from app.content.seed import seed_missing_content
    from app.models.setting import Setting

    monkeypatch.setattr(settings, "database_url", leere_db)
    cfg = db_migrate._config()
    eigene = create_engine(leere_db)

    def start():
        command.upgrade(cfg, "head")
        with Session(eigene, autoflush=False) as db:
            return seed_missing_content(db)

    assert start()["skipped"] == {}
    with Session(eigene) as db:
        assert db.query(Setting).filter(Setting.key.startswith(sync.HASH_KEY)).count() == len(MODULES)

    command.downgrade(cfg, "75aeb8d5399c")
    assert "uid" not in {c["name"] for c in inspect(eigene).get_columns("content_block")}
    command.upgrade(cfg, "head")

    with Session(eigene, autoflush=False) as db:
        assert set(sync.pristine_modules(db)) == set(MODULES)
    ergebnis = start()
    eigene.dispose()
    assert ergebnis["skipped"] == {} and ergebnis["failed"] == []
    assert "arp" in ergebnis["updated"]  # Erklärungen/goals_en sind wieder da


def test_env_py_importiert_alle_modelle():
    """`alembic revision --autogenerate` vergleicht die DB mit Base.metadata, wie
    migrations/env.py es lädt (bewusst ohne app.main). Fehlt dort ein Modell,
    schlägt autogenerate DROP TABLE für dessen Tabelle vor."""
    backend = Path(__file__).resolve().parents[1]
    imports = re.findall(r"^from app\.models import \w+", (backend / "migrations" / "env.py").read_text(), re.M)
    out = subprocess.run(
        [sys.executable, "-c", "\n".join([*imports, "from app.database import Base",
                                          "print(*sorted(Base.metadata.tables))"])],
        cwd=backend, check=True, capture_output=True, text=True).stdout.split()
    with TestClient(app):
        pass
    assert set(out) == set(inspect(engine).get_table_names()) - {"alembic_version"}
