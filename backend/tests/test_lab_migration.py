"""Der Lab-Block muss auch in Bestands-Datenbanken ankommen.

seed_missing_content ueberspringt Module, deren Schluessel schon existiert (Schutz
fuer Trainer-Bearbeitungen). Das Lab kam nach dem Ausliefern des Ansible-Lehrgangs
dazu — ohne Migration erscheint es auf bestehenden Servern nie. Genau das ist am
2026-07-21 beim Aktivieren passiert.
"""
import pytest
from fastapi.testclient import TestClient

from app.content.seed import ANSIBLE_LAB_MIGRATION, _migrate_ansible_lab
from app.database import SessionLocal
from app.main import app
from app.models.content import ContentBlock
from app.models.setting import Setting

MODULE = "fehlerbehandlung-idempotenz"


@pytest.fixture(autouse=True)
def app_gestartet():
    """Startet die App einmal, damit Schema und Seed stehen (wie in den anderen
    Tests) — sonst gibt es die Tabellen noch gar nicht."""
    with TestClient(app):
        yield


def _lab_bloecke(db):
    return [b for b in db.query(ContentBlock).filter(ContentBlock.module_key == MODULE).all()
            if b.widget_id == "ansible-lab"]


def test_migration_ergaenzt_lab_in_bestandsmodul():
    db = SessionLocal()
    try:
        # Bestandszustand nachstellen: Lab-Block weg, Migration nie gelaufen.
        for block in _lab_bloecke(db):
            db.delete(block)
        marke = db.get(Setting, ANSIBLE_LAB_MIGRATION)
        if marke:
            db.delete(marke)
        db.commit()
        assert _lab_bloecke(db) == []

        _migrate_ansible_lab(db)
        db.commit()

        nachher = _lab_bloecke(db)
        assert len(nachher) == 1, "Lab-Widget fehlt nach der Migration"

        # Der Erklaertext steht direkt davor.
        alle = db.query(ContentBlock).filter(
            ContentBlock.module_key == MODULE).order_by(ContentBlock.position).all()
        stelle = next(i for i, b in enumerate(alle) if b.widget_id == "ansible-lab")
        assert alle[stelle - 1].type == "text"
    finally:
        db.close()


def test_migration_laeuft_nicht_doppelt():
    """Zweiter Aufruf darf nichts verdoppeln — weder ueber die Marke noch ueber
    den Inhaltsabgleich."""
    db = SessionLocal()
    try:
        _migrate_ansible_lab(db)
        db.commit()
        vorher = len(_lab_bloecke(db))

        marke = db.get(Setting, ANSIBLE_LAB_MIGRATION)
        if marke:
            db.delete(marke)  # Marke entfernen: jetzt schuetzt nur noch der Inhaltsabgleich
            db.commit()
        _migrate_ansible_lab(db)
        db.commit()

        assert len(_lab_bloecke(db)) == vorher == 1
    finally:
        db.close()
