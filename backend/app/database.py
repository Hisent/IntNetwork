from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Spalten, die im Modell nicht mehr existieren, aber in alten DBs noch stehen.
# ADD COLUMN unten räumt nie ab — eine NOT-NULL-Leiche (pass_threshold, Modell
# 2026-07 entfernt) lässt sonst jeden INSERT neuer Module auf Postgres crashen.
DEAD_COLUMNS = {("content_module", "pass_threshold")}


def sync_missing_columns() -> None:
    """create_all() legt nur neue Tabellen an, ändert nie bestehende -> jedes
    Feld, das später an ein Modell einer schon existierenden Tabelle angehängt
    wird, fehlt sonst in der DB und lässt jede Query auf der Tabelle crashen."""
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    with engine.begin() as conn:
        for table in Base.metadata.sorted_tables:
            if table.name not in existing_tables:
                continue
            existing_cols = {c["name"] for c in inspector.get_columns(table.name)}
            for col in table.columns:
                if col.name in existing_cols:
                    continue
                col_type = col.type.compile(dialect=engine.dialect)
                conn.exec_driver_sql(f'ALTER TABLE "{table.name}" ADD COLUMN "{col.name}" {col_type}')
        # Guard-Reflection bewusst auf DIESER Connection: die gepoolte
        # SQLite-Connection hält sonst einen stale Schema-Cache und meldet
        # beim DROP fälschlich "no such column".
        conn_inspector = inspect(conn)
        for table_name, col_name in DEAD_COLUMNS:
            if table_name in existing_tables and any(
                    c["name"] == col_name for c in conn_inspector.get_columns(table_name)):
                conn.exec_driver_sql(f'ALTER TABLE "{table_name}" DROP COLUMN "{col_name}"')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
