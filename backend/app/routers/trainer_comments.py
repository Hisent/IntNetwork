from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.comment import Comment
from app.services.deps import get_trainer
from app.services.features import comments_enabled

router = APIRouter(tags=["trainer-comments"])


def _guard(db: Session) -> None:
    if not comments_enabled(db):
        raise HTTPException(status_code=403, detail="Feedback ist deaktiviert")


def _serialize(c: Comment) -> dict:
    return {"id": c.id, "module_key": c.module_key, "block_index": c.block_index,
            "body": c.body, "author_kind": c.author_kind, "author_name": c.author_name,
            "created_at": c.created_at.isoformat(), "own": c.author_kind == "trainer"}


class TComReq(BaseModel):
    block_index: int
    body: str = Field(max_length=2000)


@router.get("/trainer/courses/{cid}/comments")
def course_comments(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    _guard(db)
    rows = db.query(Comment).filter(Comment.course_id == cid).order_by(
        Comment.module_key, Comment.block_index, Comment.created_at).all()
    return [_serialize(c) for c in rows]


@router.post("/trainer/courses/{cid}/modules/{key}/comments")
def add_trainer_comment(cid: int, key: str, data: TComReq, db: Session = Depends(get_db),
                        _t: dict = Depends(get_trainer)):
    _guard(db)
    body = data.body.strip()
    if not body:
        raise HTTPException(status_code=400, detail="Kommentar ist leer")
    c = Comment(course_id=cid, module_key=key, block_index=data.block_index,
                body=body, author_kind="trainer", author_name="Trainer", participant_id=None)
    db.add(c)
    db.commit()
    db.refresh(c)
    return _serialize(c)


@router.delete("/trainer/comments/{cid}")
def delete_trainer_comment(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    _guard(db)
    c = db.query(Comment).filter(Comment.id == cid).first()
    if not c:
        raise HTTPException(status_code=404, detail="Kommentar nicht gefunden")
    db.delete(c)
    db.commit()
    return {"ok": True}
