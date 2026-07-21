from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def log_action(db: Session, trainer: dict, action: str,
               target: str | None = None, detail: str | None = None) -> None:
    """Schreibt einen Audit-Eintrag für eine mutierende Trainer-Aktion.

    `trainer` ist das Payload-Dict aus get_trainer (enthält "sub" = E-Mail und
    "trainer_id"). Wird immer NACH dem Commit der eigentlichen Aktion
    aufgerufen -> zu diesem Zeitpunkt hängt an der Session nichts anderes mehr
    Ungeschriebenes, daher trifft ein Rollback hier nur den Audit-Eintrag
    selbst und kann die eigentliche Aktion nicht mehr gefährden.
    """
    try:
        db.add(AuditLog(
            trainer_id=trainer.get("trainer_id"),
            trainer_email=trainer.get("sub") or "?",
            action=action, target=target, detail=detail,
        ))
        db.commit()
    except Exception:
        db.rollback()
