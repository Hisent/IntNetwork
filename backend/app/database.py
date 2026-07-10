from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
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
