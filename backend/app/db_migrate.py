from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect

from app.database import engine

_BACKEND_DIR = Path(__file__).resolve().parent.parent  # .../backend
_ALEMBIC_INI = _BACKEND_DIR / "alembic.ini"
_BASELINE = "7a63b63c8cde"


def _config() -> Config:
    cfg = Config(str(_ALEMBIC_INI))
    cfg.set_main_option("script_location", str(_BACKEND_DIR / "migrations"))
    return cfg


def run_migrations() -> None:
    """Bringt das Schema mit Alembic auf head.

    Bestehende, früher per create_all gebaute DBs haben keine alembic_version-
    Tabelle. Die werden auf die Baseline *gestampt* (kein DDL — ihr Schema
    entspricht bereits der Baseline), danach laufen nur die Folge-Revisionen.
    So läuft auf laufenden Prod-DBs nie eine Baseline-DDL erneut, sondern nur die
    additiven Änderungen.
    """
    tables = set(inspect(engine).get_table_names())
    cfg = _config()
    if "alembic_version" not in tables and "participant" in tables:
        command.stamp(cfg, _BASELINE)
    command.upgrade(cfg, "head")
