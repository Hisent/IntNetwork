from sqlalchemy.orm import Session

from app.models.workshop import Workshop
from app.services.content_editor import EditorError


def publish_workshop(db: Session, key: str) -> Workshop:
    ws = db.get(Workshop, key)
    if ws is None:
        raise EditorError(404, f"Workshop/Modul ‚{key}‘ existiert nicht.")
    if ws.status != "published":
        ws.status = "published"
        db.commit()
    return ws
