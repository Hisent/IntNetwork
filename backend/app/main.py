import time

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.config import DEFAULT_SECRET_KEY, settings
from app.database import Base, SessionLocal, engine
from app.models import course as _course  # noqa: F401
from app.models import participant as _participant  # noqa: F401
from app.models import progress as _progress  # noqa: F401
from app.models import quiz_result as _quiz_result  # noqa: F401
from app.models import module_disabled as _module_disabled  # noqa: F401
from app.models import setting as _setting  # noqa: F401
from app.models import comment as _comment  # noqa: F401
from app.models import content as _content  # noqa: F401

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
Base.metadata.create_all(bind=engine)

from app.content.seed import seed_content_if_empty  # noqa: E402

_seed_db = SessionLocal()
try:
    seed_content_if_empty(_seed_db)
finally:
    _seed_db.close()

app = FastAPI(title="IntNetwork")
app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

_api = APIRouter(prefix="/api")


@_api.get("/health")
def health():
    return {"status": "ok"}


from app.routers import auth as auth_router  # noqa: E402
from app.routers import courses as courses_router  # noqa: E402
from app.routers import join as join_router  # noqa: E402
from app.routers import modules as modules_router  # noqa: E402
from app.routers import changelog as changelog_router  # noqa: E402
from app.routers import trainer_modules as trainer_modules_router  # noqa: E402
from app.routers import features as features_router  # noqa: E402
from app.routers import comments as comments_router  # noqa: E402
from app.routers import trainer_comments as trainer_comments_router  # noqa: E402
from app.routers import presence as presence_router  # noqa: E402
_api.include_router(auth_router.router)
_api.include_router(courses_router.router)
_api.include_router(join_router.router)
_api.include_router(modules_router.router)
_api.include_router(changelog_router.router)
_api.include_router(trainer_modules_router.router)
_api.include_router(features_router.router)
_api.include_router(comments_router.router)
_api.include_router(trainer_comments_router.router)
_api.include_router(presence_router.router)

app.include_router(_api)
