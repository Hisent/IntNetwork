"""Reset the non-production database and seed the current workshop sources."""

import argparse

from sqlalchemy import text

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.db_migrate import run_migrations
from app.models import comment, content, course, course_module, module_disabled, participant  # noqa: F401
from app.models import progress, quiz_result, setting, trainer, workshop  # noqa: F401
from app.content.seed import seed_missing_content
from app.content.workshops import seed_workshops
from app.services.trainer_seed import seed_trainer_if_empty


def reset_database() -> None:
    """Leert die Dev-DB und baut sie wieder auf.

    Nutzt dieselbe Autoritaet wie main.py fuer den Schemaaufbau: Alembic ueber
    run_migrations(), NICHT Base.metadata.create_all(). Grund (siehe main.py-
    Kommentar zum Crashloop vom 22.07.2026): create_all legt Tabellen an, ohne
    alembic_version zu setzen. Der naechste normale App-Start sieht dann "keine
    alembic_version, aber participant existiert bereits", stampt die Baseline
    und spielt anschliessend Folgemigrationen erneut ein -- die versuchen
    bereits vorhandene Spalten/Tabellen nochmal anzulegen und crashen mit
    "duplicate column name". run_migrations() baut das Schema per Alembic UND
    setzt alembic_version korrekt, sodass ein anschliessender App-Start keine
    Migrationen mehr wiederholt.

    alembic_version selbst ist keine ORM-Tabelle (nicht Teil von Base.metadata)
    und ueberlebt daher drop_all() unveraendert -- staende dort noch "head",
    wuerde run_migrations() faelschlich annehmen, das Schema sei bereits
    aktuell, und gar keine Migration mehr ausfuehren, obwohl alle Tabellen
    gerade gedroppt wurden. Deshalb explizit mitloeschen, damit Alembic von
    Grund auf neu baut."""
    Base.metadata.drop_all(bind=engine)
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
    run_migrations()
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
