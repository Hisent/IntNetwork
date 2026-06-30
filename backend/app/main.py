import time

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.config import DEFAULT_SECRET_KEY, settings
from app.database import Base, engine
from app.models import course as _course  # noqa: F401
from app.models import participant as _participant  # noqa: F401
from app.models import progress as _progress  # noqa: F401
from app.models import quiz_result as _quiz_result  # noqa: F401

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
_api.include_router(auth_router.router)
_api.include_router(courses_router.router)
_api.include_router(join_router.router)
_api.include_router(modules_router.router)

app.include_router(_api)
