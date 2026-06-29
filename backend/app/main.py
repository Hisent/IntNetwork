from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import DEFAULT_SECRET_KEY, settings
from app.database import Base, engine

if not settings.debug and settings.secret_key == DEFAULT_SECRET_KEY:
    raise RuntimeError("SECRET_KEY ist nicht gesetzt (noch der Default).")

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


app.include_router(_api)
