import logging
import time
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError

from app.database import engine

log = logging.getLogger(__name__)

_BACKEND_DIR = Path(__file__).resolve().parent.parent  # .../backend
_ALEMBIC_INI = _BACKEND_DIR / "alembic.ini"
_BASELINE = "7a63b63c8cde"

# Feste, frei gewählte Konstante für den Postgres-Advisory-Lock. Verhindert bei
# mehreren uvicorn-Workern, dass "alembic upgrade" parallel läuft (Race auf
# alembic_version). Der Wert hat keine weitere Bedeutung, muss nur projektweit
# eindeutig sein.
_MIGRATION_LOCK_ID = 872_364_501
# Wartegrenzen: lieber laut scheitern als still hängen (siehe _acquire_lock).
_LOCK_WAIT_SECONDS = 60.0
_DDL_ATTEMPTS = 3
_DDL_RETRY_DELAY = 5.0


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


def _acquire_lock(conn) -> None:
    """Holt den Advisory-Lock, wartet dabei aber nur begrenzt.

    Bewusst pg_try_advisory_lock in einer Schleife statt des blockierenden
    pg_advisory_lock: hängt ein anderer Prozess mit dem Lock, soll der Start
    nach _LOCK_WAIT_SECONDS mit klarer Meldung scheitern statt still zu warten
    (ein stiller Hänger sieht am Proxy wie "no available server" aus).
    """
    deadline = time.monotonic() + _LOCK_WAIT_SECONDS
    while True:
        if conn.execute(text("SELECT pg_try_advisory_lock(:id)"), {"id": _MIGRATION_LOCK_ID}).scalar():
            return
        if time.monotonic() >= deadline:
            raise RuntimeError(
                f"Migrations-Lock seit {_LOCK_WAIT_SECONDS}s belegt — ein anderer "
                "Prozess migriert noch oder ist dabei abgestürzt. Prüfen: "
                "SELECT * FROM pg_locks WHERE locktype = 'advisory';"
            )
        time.sleep(1.0)


def _migrate_with_retry() -> None:
    """Führt die Migration aus und wiederholt sie bei fremder Tabellensperre.

    lock_timeout (gesetzt in migrations/env.py) lässt ein blockiertes ALTER TABLE
    nach 10s scheitern. Typischer Auslöser ist der noch laufende alte Container
    beim rollenden Deploy — dessen Sessions sind Sekunden später weg, deshalb
    lohnt der Wiederholungsversuch.
    """
    for attempt in range(1, _DDL_ATTEMPTS + 1):
        try:
            _do_migrate()
            return
        except OperationalError as exc:
            if attempt == _DDL_ATTEMPTS:
                raise RuntimeError(
                    "Migration blockiert: eine andere Postgres-Session hält eine "
                    "Sperre auf einer zu ändernden Tabelle (oft eine offene "
                    "Transaktion des alten Containers). Prüfen: SELECT pid, state, "
                    "query FROM pg_stat_activity WHERE state LIKE 'idle in transaction%';"
                ) from exc
            log.warning("Migration blockiert (Versuch %s/%s), neuer Versuch in %ss: %s",
                        attempt, _DDL_ATTEMPTS, _DDL_RETRY_DELAY, exc)
            time.sleep(_DDL_RETRY_DELAY)


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
        _acquire_lock(conn)
        try:
            _migrate_with_retry()
        finally:
            conn.execute(text("SELECT pg_advisory_unlock(:id)"), {"id": _MIGRATION_LOCK_ID})
