from sqlalchemy import create_engine, event, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    engine = create_engine(settings.database_url, connect_args=connect_args)

    @event.listens_for(engine, "connect")
    def _sqlite_fremdschluessel_einschalten(dbapi_connection, _connection_record) -> None:
        """SQLite prueft Fremdschluessel nur, wenn man es ausdruecklich verlangt.

        Ohne dieses PRAGMA sind ON DELETE CASCADE und jede FK-Bedingung in
        Entwicklung und Tests wirkungslos, waehrend Postgres in Produktion sie
        durchsetzt — die Umgebungen verhalten sich dann unterschiedlich, und
        zwar genau bei Loeschvorgaengen. Aufgefallen beim Passkey-Feature: Nach
        dem Loeschen eines Trainers blieben dessen Credential-Zeilen unter
        SQLite als Waisen stehen, statt mitgeloescht zu werden.
        """
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    # idle_in_transaction_session_timeout: eine Session, die eine Transaktion offen
    # liegen lässt, hält Tabellensperren und blockiert damit jedes ALTER TABLE beim
    # nächsten Deploy (genau so hing v1.24 beim Start). Postgres beendet solche
    # Sessions jetzt nach 60s selbst. pool_pre_ping fängt Connections ab, die ein
    # DB-Neustart unter uns geschlossen hat.
    engine = create_engine(
        settings.database_url,
        connect_args={"options": "-c idle_in_transaction_session_timeout=60000"},
        pool_pre_ping=True,
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def sync_missing_columns() -> None:
    """Fügt fehlende Spalten nur additiv hinzu.

    Schemaänderungen, die Daten entfernen oder bestehende Spalten verändern,
    brauchen eine explizite, versionierte Migration. Ein automatisches
    ``DROP COLUMN`` beim App-Start wäre sonst ein Datenverlust-Risiko.
    """
    with engine.begin() as conn:
        # Reflection bewusst auf DIESER Connection: eine andere gepoolte
        # SQLite-Connection hält sonst einen stale Schema-Cache und meldet
        # beim DROP fälschlich "no such column".
        inspector = inspect(conn)
        existing_tables = set(inspector.get_table_names())
        for table in Base.metadata.sorted_tables:
            if table.name not in existing_tables:
                continue
            existing_cols = {c["name"] for c in inspector.get_columns(table.name)}
            for col in table.columns:
                if col.name in existing_cols:
                    continue
                col_type = col.type.compile(dialect=engine.dialect)
                conn.exec_driver_sql(f'ALTER TABLE "{table.name}" ADD COLUMN "{col.name}" {col_type}')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
