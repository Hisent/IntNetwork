from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.content.registry import MODULES
from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion
from app.models.setting import Setting
from app.content.seed import (LEARNING_LABS_MIGRATION, NETWORK_VISUALS_MIGRATION,
                              seed_missing_content)


def test_seed_adds_missing_module_to_existing_db():
    """Neue Module müssen auch in bereits befüllte DBs nachgezogen werden
    (Deployment-Fall: Update bringt ein Modul mit, DB ist nicht leer)."""
    with TestClient(app):
        db = SessionLocal()
        try:
            key = "troubleshooting"
            db.query(ContentBlock).filter(ContentBlock.module_key == key).delete()
            db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key == key).delete()
            db.query(ContentModule).filter(ContentModule.key == key).delete()
            db.commit()
            assert db.query(ContentModule).count() == len(MODULES) - 1

            seed_missing_content(db)

            assert db.query(ContentModule).count() == len(MODULES)
            assert db.query(ContentBlock).filter(ContentBlock.module_key == key).count() > 0
            assert db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key == key).count() == 5
        finally:
            db.close()


def test_seed_populates_all_modules_once():
    with TestClient(app):
        db = SessionLocal()
        try:
            count = db.query(ContentModule).count()
            assert count == len(MODULES)
            vlan = db.query(ContentModule).filter(ContentModule.key == "vlan").first()
            assert vlan is not None
            assert vlan.title_de == "VLANs"
            blocks = db.query(ContentBlock).filter(ContentBlock.module_key == "vlan").count()
            assert blocks > 0
            questions = db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key == "vlan").count()
            assert questions == 4
        finally:
            db.close()


def test_seed_is_idempotent():
    with TestClient(app):
        db = SessionLocal()
        try:
            before = db.query(ContentModule).count()
            seed_missing_content(db)
            after = db.query(ContentModule).count()
            assert before == after
        finally:
            db.close()


def test_learning_lab_migration_runs_once_and_uses_anchor_position():
    with TestClient(app):
        db = SessionLocal()
        try:
            db.query(Setting).filter(Setting.key == LEARNING_LABS_MIGRATION).delete()
            db.query(ContentBlock).filter(ContentBlock.module_key == "routing",
                                          ContentBlock.widget_id == "learning-route").delete()
            db.commit()
            seed_missing_content(db)
            widgets = [b.widget_id for b in db.query(ContentBlock)
                       .filter(ContentBlock.module_key == "routing")
                       .order_by(ContentBlock.position)]
            assert widgets.index("learning-route") == widgets.index("routing-demo") + 1
            assert db.get(Setting, LEARNING_LABS_MIGRATION) is not None

            # Nach erfolgreicher Migration gilt die DB als Trainer-Inhalt:
            # bewusstes Entfernen darf beim nächsten Start nicht rückgängig werden.
            db.query(ContentBlock).filter(ContentBlock.module_key == "routing",
                                          ContentBlock.widget_id == "learning-route").delete()
            db.commit()
            seed_missing_content(db)
            assert db.query(ContentBlock).filter(ContentBlock.module_key == "routing",
                                                 ContentBlock.widget_id == "learning-route").count() == 0
        finally:
            db.query(Setting).filter(Setting.key == LEARNING_LABS_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()


def test_network_visual_migration_uses_anchor_and_respects_later_removal():
    with TestClient(app):
        db = SessionLocal()
        try:
            db.query(Setting).filter(Setting.key == NETWORK_VISUALS_MIGRATION).delete()
            db.query(ContentBlock).filter(ContentBlock.module_key == "dns",
                                          ContentBlock.widget_id == "visual-dns-tree").delete()
            db.commit()
            seed_missing_content(db)
            widgets = [b.widget_id for b in db.query(ContentBlock)
                       .filter(ContentBlock.module_key == "dns")
                       .order_by(ContentBlock.position)]
            assert widgets.index("visual-dns-tree") == widgets.index("dns-demo") + 1

            db.query(ContentBlock).filter(ContentBlock.module_key == "dns",
                                          ContentBlock.widget_id == "visual-dns-tree").delete()
            db.commit()
            seed_missing_content(db)
            assert db.query(ContentBlock).filter(ContentBlock.module_key == "dns",
                                                 ContentBlock.widget_id == "visual-dns-tree").count() == 0
        finally:
            db.query(Setting).filter(Setting.key == NETWORK_VISUALS_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()
