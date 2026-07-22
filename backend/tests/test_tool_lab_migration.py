"""openssl- und git-Lab muessen auch in Bestands-Datenbanken ankommen.

Gleiche Lage wie beim Ansible-Lab am 2026-07-21: seed_missing_content
ueberspringt Module, deren Schluessel schon existiert. Die beiden Zielmodule
sind mit ihren Lehrgaengen laengst ausgeliefert — ohne Migration erscheinen die
Labore auf bestehenden Servern nie, und zwar unbemerkt, weil lokal (frische DB)
alles richtig aussieht.
"""
import pytest
from fastapi.testclient import TestClient

from app.content.seed import TOOL_LABS_MIGRATION, _migrate_tool_labs
from app.database import SessionLocal
from app.main import app
from app.models.content import ContentBlock
from app.models.setting import Setting

# (Modul, Widget-Id) — beide Lehrgaenge auf einmal geprueft.
LABORE = [("tls-pruefen", "openssl-lab"), ("git-collaboration", "git-lab")]


@pytest.fixture(autouse=True)
def app_gestartet():
    with TestClient(app):
        yield


def _widget_bloecke(db, modul: str, widget_id: str):
    return [b for b in db.query(ContentBlock).filter(ContentBlock.module_key == modul).all()
            if b.widget_id == widget_id]


def _bestandszustand_herstellen(db):
    """Modul ohne Lab-Block und ohne Migrationsmarke — so sieht ein Server aus,
    der die Lehrgaenge vor dieser Version bekommen hat."""
    for modul, widget_id in LABORE:
        for block in _widget_bloecke(db, modul, widget_id):
            db.delete(block)
        for block in db.query(ContentBlock).filter(ContentBlock.module_key == modul):
            if block.type == "text" and block.value_de and "Selbst ausprobieren" in block.value_de:
                db.delete(block)
    marke = db.get(Setting, TOOL_LABS_MIGRATION)
    if marke:
        db.delete(marke)
    db.commit()


def test_migration_ergaenzt_beide_labore_in_bestandsmodulen():
    db = SessionLocal()
    try:
        _bestandszustand_herstellen(db)
        for modul, widget_id in LABORE:
            assert _widget_bloecke(db, modul, widget_id) == []

        _migrate_tool_labs(db)
        db.commit()

        for modul, widget_id in LABORE:
            assert len(_widget_bloecke(db, modul, widget_id)) == 1, f"{widget_id} fehlt in {modul}"
            alle = db.query(ContentBlock).filter(
                ContentBlock.module_key == modul).order_by(ContentBlock.position).all()
            stelle = next(i for i, b in enumerate(alle) if b.widget_id == widget_id)
            # Erklaertext direkt davor, damit das Lab nicht unvermittelt dasteht.
            assert alle[stelle - 1].type == "text"
            # Und das Ganze vor dem Quiz, also am Ende der Blockliste.
            assert stelle == len(alle) - 1
    finally:
        db.close()


def test_migration_laeuft_nicht_doppelt():
    """Zweiter Aufruf darf nichts verdoppeln — weder ueber die Marke noch ueber
    den Inhaltsabgleich."""
    db = SessionLocal()
    try:
        _migrate_tool_labs(db)
        db.commit()

        marke = db.get(Setting, TOOL_LABS_MIGRATION)
        if marke:
            db.delete(marke)  # jetzt schuetzt nur noch der Inhaltsabgleich
            db.commit()
        _migrate_tool_labs(db)
        db.commit()

        for modul, widget_id in LABORE:
            assert len(_widget_bloecke(db, modul, widget_id)) == 1
    finally:
        db.close()
