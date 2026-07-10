from fastapi.testclient import TestClient
from sqlalchemy import inspect

from app.main import app
from app.database import engine, sync_missing_columns


def test_unknown_columns_are_preserved():
    """Der Start darf nie Schema oder Daten implizit zerstören."""
    with TestClient(app):
        with engine.begin() as conn:
            conn.exec_driver_sql(
                "ALTER TABLE content_module ADD COLUMN pass_threshold FLOAT NOT NULL DEFAULT 0.7")
            conn.exec_driver_sql(
                "ALTER TABLE content_module_snapshot ADD COLUMN saved_at TEXT")
        sync_missing_columns()
        insp = inspect(engine)
        assert "pass_threshold" in {c["name"] for c in insp.get_columns("content_module")}
        assert "saved_at" in {c["name"] for c in insp.get_columns("content_module_snapshot")}
        # zweiter Lauf ist idempotent.
        sync_missing_columns()
