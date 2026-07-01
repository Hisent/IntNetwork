from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.content.registry import MODULES
from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion
from app.content.seed import seed_content_if_empty


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
            seed_content_if_empty(db)
            after = db.query(ContentModule).count()
            assert before == after
        finally:
            db.close()
