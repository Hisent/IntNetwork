import logging

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog

logger = logging.getLogger(__name__)


def log_action(db: Session, trainer: dict, action: str,
               target: str | None = None, detail: str | None = None) -> None:
    """Schreibt einen Audit-Eintrag für eine mutierende Trainer-Aktion.

    `trainer` ist das Payload-Dict aus get_trainer (enthält "sub" = E-Mail und
    "trainer_id"). Wird immer NACH dem Commit der eigentlichen Aktion
    aufgerufen -> zu diesem Zeitpunkt hängt an der Session nichts anderes mehr
    Ungeschriebenes, daher trifft ein Rollback hier nur den Audit-Eintrag
    selbst und kann die eigentliche Aktion nicht mehr gefährden.

    Audit ist best-effort: ein Fehlschlag hier darf die eigentliche Aktion
    (die schon committed ist) nicht nachtraeglich scheitern lassen, deshalb
    wird die Exception nicht weitergeworfen -- aber sie muss sichtbar bleiben
    (Schema-Drift, DB-Problem), sonst faellt ein kaputter Audit-Trail nie auf.
    """
    try:
        db.add(AuditLog(
            trainer_id=trainer.get("trainer_id"),
            trainer_email=trainer.get("sub") or "?",
            action=action, target=target, detail=detail,
        ))
        db.commit()
    except Exception:
        logger.exception("Audit-Eintrag fehlgeschlagen: action=%s target=%s", action, target)
        db.rollback()
