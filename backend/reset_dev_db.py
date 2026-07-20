"""Reset the non-production database and seed the current workshop sources."""

import argparse

from app.config import settings
from app.database import Base, SessionLocal, engine, sync_missing_columns
from app.models import comment, content, course, course_module, module_disabled, participant  # noqa: F401
from app.models import progress, quiz_result, setting, trainer, workshop  # noqa: F401
from app.content.seed import seed_missing_content
from app.content.workshops import seed_workshops
from app.services.trainer_seed import seed_trainer_if_empty


def reset_database() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    sync_missing_columns()
    db = SessionLocal()
    try:
        seed_missing_content(db)
        seed_workshops(db)
        seed_trainer_if_empty(db)
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--yes", action="store_true", help="Datenbank unwiderruflich leeren")
    args = parser.parse_args()
    if not args.yes:
        parser.error("Reset ist destruktiv. Zum Bestätigen --yes angeben.")
    if not settings.database_url.startswith("sqlite:"):
        parser.error("Nur lokale SQLite-Datenbanken dürfen per Dev-Reset gelöscht werden.")
    reset_database()
    print("Lokale Dev-Datenbank neu geseedet.")


if __name__ == "__main__":
    main()
