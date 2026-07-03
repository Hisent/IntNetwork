from fastapi.testclient import TestClient
from sqlalchemy import inspect

from app.main import app
from app.database import engine, sync_missing_columns


def test_dead_columns_are_dropped():
    """Prod-Fall: alte DB hat noch content_module.pass_threshold NOT NULL
    (Feature 2026-07 entfernt) — jeder Seed-INSERT neuer Module crasht daran.
    sync_missing_columns muss bekannte tote Spalten wegräumen."""
    with TestClient(app):
        with engine.begin() as conn:
            conn.exec_driver_sql(
                "ALTER TABLE content_module ADD COLUMN pass_threshold FLOAT NOT NULL DEFAULT 0.7")
        sync_missing_columns()
        cols = {c["name"] for c in inspect(engine).get_columns("content_module")}
        assert "pass_threshold" not in cols
        # zweiter Lauf ist idempotent (Spalte schon weg)
        sync_missing_columns()
