from datetime import timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.participant import Participant
from app.services.deps import get_trainer
from app.content.registry import module_meta
from app.utils import utc_now

router = APIRouter(tags=["presence"])

STALE_AFTER_SECONDS = 30


@router.get("/trainer/courses/{cid}/presence")
def course_presence(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    cutoff = utc_now() - timedelta(seconds=STALE_AFTER_SECONDS)
    titles = {m["key"]: m["title"] for m in module_meta()}
    rows = db.query(Participant).filter(
        Participant.course_id == cid,
        Participant.last_seen.isnot(None),
        Participant.last_seen >= cutoff,
        Participant.current_module_key.isnot(None),
    ).order_by(Participant.name).all()
    return [
        {"name": p.name, "module_key": p.current_module_key,
         "module_title": titles.get(p.current_module_key, p.current_module_key)}
        for p in rows
    ]
