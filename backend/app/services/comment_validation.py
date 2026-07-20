from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.content import ContentBlock, ContentModule
from app.models.course import Course
from app.services.course_membership import active_module_keys


def require_course(db: Session, course_id: int) -> None:
    if not db.query(Course).filter(Course.id == course_id).first():
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")


def require_visible_module(db: Session, course_id: int, key: str) -> None:
    if not db.query(ContentModule).filter(ContentModule.key == key).first():
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    if key not in active_module_keys(db, course_id):
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")


def require_comment_target(db: Session, course_id: int, key: str, block_index: int,
                           *, require_active: bool = False) -> None:
    require_course(db, course_id)
    if require_active:
        require_visible_module(db, course_id, key)
    elif not db.query(ContentModule).filter(ContentModule.key == key).first():
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")

    block_count = db.query(ContentBlock).filter(ContentBlock.module_key == key).count()
    if not 0 <= block_index < block_count:
        raise HTTPException(status_code=422, detail="Ungültiger Block-Index")
