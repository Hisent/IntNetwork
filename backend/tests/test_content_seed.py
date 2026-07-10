from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.content.registry import MODULES
from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion
from app.content.seed import seed_missing_content


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


def test_seed_adds_new_widgets_to_existing_modules_without_duplicates():
    with TestClient(app):
        db = SessionLocal()
        try:
            seed_missing_content(db)
            seed_missing_content(db)
            for key in ("routing", "subnetting", "troubleshooting"):
                widgets = [b.widget_id for b in db.query(ContentBlock)
                           .filter(ContentBlock.module_key == key, ContentBlock.type == "widget")]
                assert sum(w == {"routing": "learning-route", "subnetting": "learning-subnet", "troubleshooting": "learning-evidence"}[key] for w in widgets) == 1
        finally:
            db.close()
