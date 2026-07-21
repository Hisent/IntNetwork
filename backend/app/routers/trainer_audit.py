from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.audit_log import AuditLog
from app.services.deps import get_trainer

router = APIRouter(prefix="/trainer/audit", tags=["trainer-audit"])


def _serialize(a: AuditLog) -> dict:
    return {"id": a.id, "created_at": a.created_at.isoformat(), "trainer_email": a.trainer_email,
            "action": a.action, "target": a.target, "detail": a.detail}


@router.get("")
def list_audit(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
              action: str | None = None,
              db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    q = db.query(AuditLog)
    if action:
        q = q.filter(AuditLog.action == action)
    rows = q.order_by(AuditLog.created_at.desc(), AuditLog.id.desc()).offset(offset).limit(limit).all()
    return [_serialize(a) for a in rows]
