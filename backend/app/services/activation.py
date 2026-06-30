from app.models.module_disabled import ModuleDisabled


def disabled_keys(db, course_id: int) -> set[str]:
    rows = db.query(ModuleDisabled).filter(ModuleDisabled.course_id == course_id).all()
    return {r.module_key for r in rows}
