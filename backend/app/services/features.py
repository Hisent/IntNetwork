from fastapi import HTTPException

from app.models.setting import Setting


def comments_enabled(db) -> bool:
    row = db.query(Setting).filter(Setting.key == "comments_enabled").first()
    return row.value == "1" if row else True


def require_comments_enabled(db) -> None:
    if not comments_enabled(db):
        raise HTTPException(status_code=403, detail="Feedback ist deaktiviert")


def set_comments_enabled(db, value: bool) -> None:
    row = db.query(Setting).filter(Setting.key == "comments_enabled").first()
    if row:
        row.value = "1" if value else "0"
    else:
        db.add(Setting(key="comments_enabled", value="1" if value else "0"))
    db.commit()
