from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text

from app.database import engine

_BACKEND_DIR = Path(__file__).resolve().parent.parent  # .../backend
_ALEMBIC_INI = _BACKEND_DIR / "alembic.ini"
_BASELINE = "7a63b63c8cde"

# Feste, frei gewählte Konstante für den Postgres-Advisory-Lock. Verhindert bei
# mehreren uvicorn-Workern, dass "alembic upgrade" parallel läuft (Race auf
# alembic_version). Der Wert hat keine weitere Bedeutung, muss nur projektweit
# eindeutig sein.
_MIGRATION_LOCK_ID = 872_364_501


def _config() -> Config:
    cfg = Config(str(_ALEMBIC_INI))
    cfg.set_main_option("script_location", str(_BACKEND_DIR / "migrations"))
    return cfg


def _do_migrate() -> None:
    tables = set(inspect(engine).get_table_names())
    cfg = _config()
    if "alembic_version" not in tables and "participant" in tables:
        command.stamp(cfg, _BASELINE)
    command.upgrade(cfg, "head")


def run_migrations() -> None:
    """Bringt das Schema mit Alembic auf head.

    Bestehende, früher per create_all gebaute DBs haben keine alembic_version-
    Tabelle. Die werden auf die Baseline *gestampt* (kein DDL — ihr Schema
    entspricht bereits der Baseline), danach laufen nur die Folge-Revisionen.
    So läuft auf laufenden Prod-DBs nie eine Baseline-DDL erneut, sondern nur die
    additiven Änderungen.

    Bei Postgres (Multi-Worker-Deploy) läuft die Migration unter einem
    Advisory-Lock auf einer dedizierten Connection: mehrere uvicorn-Worker
    starten gleichzeitig, aber nur einer darf "alembic upgrade" ausführen.
    SQLite ist Single-Prozess-Dev, dort ist kein Lock nötig.
    """
    if engine.dialect.name != "postgresql":
        _do_migrate()
        return

    with engine.connect() as conn:
        conn.execute(text("SELECT pg_advisory_lock(:id)"), {"id": _MIGRATION_LOCK_ID})
        try:
            _do_migrate()
        finally:
            conn.execute(text("SELECT pg_advisory_unlock(:id)"), {"id": _MIGRATION_LOCK_ID})
