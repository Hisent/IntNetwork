import logging
import time

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError

from app.config import APP_VERSION, DEFAULT_SECRET_KEY, settings
from app.database import Base, SessionLocal, engine
from app.db_migrate import run_migrations
from app.models import course as _course  # noqa: F401
from app.models import course_module as _course_module  # noqa: F401
from app.models import participant as _participant  # noqa: F401
from app.models import progress as _progress  # noqa: F401
from app.models import quiz_result as _quiz_result  # noqa: F401
from app.models import module_disabled as _module_disabled  # noqa: F401
from app.models import setting as _setting  # noqa: F401
from app.models import comment as _comment  # noqa: F401
from app.models import content as _content  # noqa: F401
from app.models import workshop as _workshop  # noqa: F401
from app.models import trainer as _trainer  # noqa: F401
from app.models import certificate as _certificate  # noqa: F401
from app.models import audit_log as _audit_log  # noqa: F401
from app.models import trainer_credential as _trainer_credential  # noqa: F401

if not settings.debug and settings.secret_key == DEFAULT_SECRET_KEY:
    raise RuntimeError("SECRET_KEY ist nicht gesetzt (noch der Default).")


def _wait_for_db(retries: int = 30, delay: float = 2.0) -> None:
    """Wartet, bis die DB erreichbar ist (Postgres-Container-Start)."""
    for attempt in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except OperationalError:
            if attempt < retries - 1:
                time.sleep(delay)
    raise RuntimeError("Datenbank nicht erreichbar")


_wait_for_db()
# Schema wird von Alembic verwaltet (migrations/). create_all bleibt als
# Sicherheitsnetz danach: legt nur fehlende Tabellen an, ändert nie bestehende.
#
# ACHTUNG, teuer gelernt (Vorfall 22.07.2026): Wenn create_all hier wirklich
# etwas anlegt, ist das KEIN harmloser Normalfall, sondern bedeutet, dass
# Modelle und Migrationen auseinanderlaufen. Alembic weiß von so einer Tabelle
# nichts — die zugehörige Revision will sie beim nächsten Start erneut anlegen,
# scheitert an "relation already exists", der Prozess stirbt und die Plattform
# startet ihn endlos neu. Deshalb wird der Fall jetzt laut protokolliert statt
# still zu passieren; die betroffene Migration gehört dann idempotent gemacht
# (Muster: migrations/versions/7305d4053e50_add_trainer_credential.py).
run_migrations()
_fehlende_tabellen = sorted(
    set(Base.metadata.tables) - set(inspect(engine).get_table_names())
)
if _fehlende_tabellen:
    logging.getLogger(__name__).warning(
        "create_all legt Tabellen an, die keine Migration erzeugt hat: %s — "
        "Modelle und Migrationen laufen auseinander, siehe Kommentar in main.py.",
        ", ".join(_fehlende_tabellen),
    )
Base.metadata.create_all(bind=engine)

from app.content.seed import seed_missing_content  # noqa: E402
from app.content.workshops import seed_workshops  # noqa: E402
from app.services.trainer_seed import seed_trainer_if_empty  # noqa: E402

_seed_db = SessionLocal()
try:
    seed_missing_content(_seed_db)
    seed_workshops(_seed_db)
    seed_trainer_if_empty(_seed_db)
finally:
    _seed_db.close()

app = FastAPI(title="IntLab", version=APP_VERSION)


@app.middleware("http")
async def _security_headers(request, call_next):
    """Setzt Standard-Security-Header auf jede Response.

    Kein CSP hier: das Backend liefert nur JSON, keine HTML-Seiten. HSTS nur in
    Prod (debug=False) — auf lokalem HTTP würde der Browser sich sonst dauerhaft
    auf HTTPS festlegen.
    """
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    if not settings.debug:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


app.add_middleware(
    CORSMiddleware, allow_origins=settings.origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

_api = APIRouter(prefix="/api")


@_api.get("/health")
def health():
    return {"status": "ok", "version": APP_VERSION}


from app.routers import auth as auth_router  # noqa: E402
from app.routers import courses as courses_router  # noqa: E402
from app.routers import join as join_router  # noqa: E402
from app.routers import modules as modules_router  # noqa: E402
from app.routers import changelog as changelog_router  # noqa: E402
from app.routers import trainer_modules as trainer_modules_router  # noqa: E402
from app.routers import features as features_router  # noqa: E402
from app.routers import links as links_router  # noqa: E402
from app.routers import comments as comments_router  # noqa: E402
from app.routers import trainer_comments as trainer_comments_router  # noqa: E402
from app.routers import presence as presence_router  # noqa: E402
from app.routers import trainer_content as trainer_content_router  # noqa: E402
from app.routers import trainer_accounts as trainer_accounts_router  # noqa: E402
from app.routers import workshops as workshops_router  # noqa: E402
from app.routers import certificate as certificate_router  # noqa: E402
from app.routers import lab as lab_router  # noqa: E402
from app.routers import trainer_audit as trainer_audit_router  # noqa: E402
from app.routers import trainer_passkey as trainer_passkey_router  # noqa: E402
_api.include_router(auth_router.router)
_api.include_router(courses_router.router)
_api.include_router(join_router.router)
_api.include_router(modules_router.router)
_api.include_router(changelog_router.router)
_api.include_router(trainer_modules_router.router)
_api.include_router(features_router.router)
_api.include_router(links_router.router)
_api.include_router(comments_router.router)
_api.include_router(trainer_comments_router.router)
_api.include_router(presence_router.router)
_api.include_router(trainer_content_router.router)
_api.include_router(trainer_accounts_router.router)
_api.include_router(workshops_router.router)
_api.include_router(certificate_router.router)
_api.include_router(lab_router.router)
_api.include_router(trainer_audit_router.router)
_api.include_router(trainer_passkey_router.router)

app.include_router(_api)
