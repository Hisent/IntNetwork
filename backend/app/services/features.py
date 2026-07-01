from app.models.setting import Setting


def comments_enabled(db) -> bool:
    row = db.query(Setting).filter(Setting.key == "comments_enabled").first()
    return row.value == "1" if row else True


def set_comments_enabled(db, value: bool) -> None:
    row = db.query(Setting).filter(Setting.key == "comments_enabled").first()
    if row:
        row.value = "1" if value else "0"
    else:
        db.add(Setting(key="comments_enabled", value="1" if value else "0"))
    db.commit()
