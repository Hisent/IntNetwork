from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.comment import Comment
from app.models.participant import Participant
from app.services.deps import get_participant
from app.services.features import comments_enabled

router = APIRouter(tags=["comments"])


def _guard(db: Session) -> None:
    if not comments_enabled(db):
        raise HTTPException(status_code=403, detail="Feedback ist deaktiviert")


def _serialize(c: Comment, own: bool) -> dict:
    return {"id": c.id, "block_index": c.block_index, "body": c.body,
            "author_kind": c.author_kind, "author_name": c.author_name,
            "created_at": c.created_at.isoformat(), "own": own}


class CommentReq(BaseModel):
    block_index: int
    body: str = Field(max_length=2000)


@router.get("/modules/{key}/comments")
def list_comments(key: str, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    _guard(db)
    rows = db.query(Comment).filter(
        Comment.course_id == p.course_id, Comment.module_key == key
    ).order_by(Comment.created_at).all()
    return [_serialize(c, c.author_kind == "participant" and c.participant_id == p.id) for c in rows]


@router.post("/modules/{key}/comments")
def add_comment(key: str, data: CommentReq, db: Session = Depends(get_db),
                p: Participant = Depends(get_participant)):
    _guard(db)
    body = data.body.strip()
    if not body:
        raise HTTPException(status_code=400, detail="Kommentar ist leer")
    c = Comment(course_id=p.course_id, module_key=key, block_index=data.block_index,
                body=body, author_kind="participant", author_name=p.name, participant_id=p.id)
    db.add(c)
    db.commit()
    db.refresh(c)
    return _serialize(c, True)


@router.delete("/comments/{cid}")
def delete_comment(cid: int, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    _guard(db)
    c = db.query(Comment).filter(Comment.id == cid).first()
    if not c:
        raise HTTPException(status_code=404, detail="Kommentar nicht gefunden")
    if not (c.author_kind == "participant" and c.participant_id == p.id):
        raise HTTPException(status_code=403, detail="Nicht erlaubt")
    db.delete(c)
    db.commit()
    return {"ok": True}
