from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def sync_missing_columns() -> None:
    """create_all() legt nur neue Tabellen an, ändert nie bestehende. Deshalb
    hier beides von Hand: (1) Modell-Felder, die in der DB fehlen, per ADD
    COLUMN nachziehen — sonst crasht jede Query. (2) DB-Spalten, die das
    Modell nicht mehr kennt, DROPpen — alte NOT-NULL-Leichen (pass_threshold,
    saved_at) killen sonst jeden INSERT auf Postgres. Alle Tabellen gehören
    der App; unbekannte Spalten sind für den Code ohnehin unerreichbar."""
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
            model_cols = {c.name for c in table.columns}
            for col in table.columns:
                if col.name in existing_cols:
                    continue
                col_type = col.type.compile(dialect=engine.dialect)
                conn.exec_driver_sql(f'ALTER TABLE "{table.name}" ADD COLUMN "{col.name}" {col_type}')
            for col_name in sorted(existing_cols - model_cols):
                conn.exec_driver_sql(f'ALTER TABLE "{table.name}" DROP COLUMN "{col_name}"')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
