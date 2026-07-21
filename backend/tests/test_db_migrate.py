"""Sicherungen gegen den Startup-Hänger von v1.24: ein blockiertes ALTER TABLE
bzw. ein belegter Advisory-Lock darf den Start nicht still blockieren, sondern
muss nach begrenzter Zeit mit verwertbarer Meldung scheitern."""

import pytest
from sqlalchemy.exc import OperationalError

from app import db_migrate


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
