from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    engine = create_engine(settings.database_url, connect_args=connect_args)

    @event.listens_for(engine, "connect")
    def _sqlite_fremdschluessel_einschalten(dbapi_connection, _connection_record) -> None:
        """SQLite prueft Fremdschluessel nur, wenn man es ausdruecklich verlangt.

        Ohne dieses PRAGMA sind ON DELETE CASCADE und jede FK-Bedingung in
        Entwicklung und Tests wirkungslos, waehrend Postgres in Produktion sie
        durchsetzt — die Umgebungen verhalten sich dann unterschiedlich, und
        zwar genau bei Loeschvorgaengen. Aufgefallen beim Passkey-Feature: Nach
        dem Loeschen eines Trainers blieben dessen Credential-Zeilen unter
        SQLite als Waisen stehen, statt mitgeloescht zu werden.
        """
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    # idle_in_transaction_session_timeout: eine Session, die eine Transaktion offen
    # liegen lässt, hält Tabellensperren und blockiert damit jedes ALTER TABLE beim
    # nächsten Deploy (genau so hing v1.24 beim Start). Postgres beendet solche
    # Sessions jetzt nach 60s selbst. pool_pre_ping fängt Connections ab, die ein
    # DB-Neustart unter uns geschlossen hat.
    # timezone=UTC: die DateTime-Spalten sind zeitzonenlos und sollen UTC enthalten
    # (utc_now). Postgres rechnet einen Wert MIT Zone beim Schreiben in die
    # Sitzungs-Zeitzone um — stünde der Server z.B. auf Europe/Berlin, landete
    # Ortszeit in der Spalte und die API (iso_utc) gäbe sie als UTC aus.
    engine = create_engine(
        settings.database_url,
        connect_args={"options": "-c idle_in_transaction_session_timeout=60000 -c timezone=UTC"},
        pool_pre_ping=True,
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
