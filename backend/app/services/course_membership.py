from sqlalchemy.orm import Session

from app.models.course_module import CourseModule


def active_module_keys(db: Session, course_id: int) -> set[str]:
    return {key for (key,) in db.query(CourseModule.module_key)
            .filter(CourseModule.course_id == course_id).all()}
