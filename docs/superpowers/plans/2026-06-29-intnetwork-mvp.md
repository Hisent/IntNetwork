# IntNetwork MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eine Full-Stack-Lernplattform (Trainer + Teilnehmer per Kurs-Code) mit serverseitig bewertetem Quiz, Fortschritt, Trainer-Dashboard und einem voll ausgebauten VLAN-Modul inkl. interaktivem Switch-Simulator.

**Architecture:** FastAPI-Backend (SQLite, JWT) hält Modul-Inhalte + Quiz-Lösungen serverseitig und bewertet Quizze; React/TS-Frontend rendert Modul-Blöcke und mappt `widget`-Blöcke auf Komponenten. Trainer = env-geseedetes Konto; Teilnehmer = (Kurs, Name) via Code.

**Tech Stack:** Backend: FastAPI, SQLAlchemy, pydantic-settings, python-jose, passlib/bcrypt, pytest. Frontend: React 18, TypeScript (strict), Vite, Tailwind, react-router, @tanstack/react-query, axios, zustand.

## Global Constraints

- TypeScript strict, keine `any`. Python snake_case, Logik in `services/`.
- Quiz-Lösungen (`answer`) verlassen den Server nie; Bewertung serverseitig.
- Secure-by-default: kein Start mit Default-`SECRET_KEY` in Prod; Trainer-Passwort nur aus `INTNETWORK_ADMIN_PASSWORD` (nicht hartkodiert).
- Teilnehmer-Identität unique `(course_id, name)`; gleicher Code+Name setzt fort.
- Modul „erledigt" = `score/total >= pass_threshold` (Default 0.7).
- API gemountet unter `/api`.
- Backend-Tests laufen mit `SECRET_KEY` aus Env (conftest setzt ihn).

---

### Task 1: Backend-Gerüst (App, Config, DB, Health)

**Files:**
- Create: `backend/requirements.txt`, `backend/app/__init__.py`, `backend/app/config.py`, `backend/app/database.py`, `backend/app/main.py`, `backend/app/utils.py`, `backend/tests/__init__.py`, `backend/tests/conftest.py`, `backend/tests/test_health.py`

**Interfaces:**
- Produces: `app.main:app` (FastAPI, API unter `/api`), `app.database.Base/engine/SessionLocal/get_db`, `app.config.settings` (`secret_key`, `admin_email`, `admin_password`, `database_url`), `app.utils.utc_now`.

- [ ] **Step 1: `backend/requirements.txt`**

```
fastapi>=0.138.0
uvicorn[standard]>=0.30.0
sqlalchemy>=2.0.0
pydantic-settings>=2.14.2
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
pytest>=8.0.0
httpx>=0.27.0
```

- [ ] **Step 2: Dependencies installieren**

```bash
cd backend && python -m venv .venv && .venv/Scripts/python -m pip install -r requirements.txt
```
Expected: Installation ohne Fehler.

- [ ] **Step 3: `backend/app/__init__.py`** — leer anlegen.

- [ ] **Step 4: `backend/app/utils.py`**

```python
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
```

- [ ] **Step 5: `backend/app/config.py`**

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SECRET_KEY = "change-me-intnetwork-default-secret"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    secret_key: str = DEFAULT_SECRET_KEY
    database_url: str = "sqlite:///./intnetwork.db"
    admin_email: str = "trainer@example.com"
    admin_password: str = ""  # leer = Trainer-Login deaktiviert (kein Hardcoded-PW)
    debug: bool = False


settings = Settings()
```

- [ ] **Step 6: `backend/app/database.py`**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 7: `backend/app/main.py`**

```python
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
```

- [ ] **Step 8: `backend/tests/__init__.py`** — leer.

- [ ] **Step 9: `backend/tests/conftest.py`**

```python
import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-not-the-default-0123456789")
os.environ.setdefault("ADMIN_EMAIL", "trainer@test.de")
os.environ.setdefault("ADMIN_PASSWORD", "trainerpass1")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_intnetwork.db")
```

- [ ] **Step 10: `backend/tests/test_health.py`**

```python
from fastapi.testclient import TestClient
from app.main import app


def test_health():
    with TestClient(app) as c:
        r = c.get("/api/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}
```

- [ ] **Step 11: Lauf + Commit**

```bash
cd backend && .venv/Scripts/python -m pytest tests/test_health.py -q
```
Expected: 1 passed.
```bash
git add backend
git commit -m "feat(backend): FastAPI-Gerüst, Config, DB, Health"
```

---

### Task 2: Datenmodelle

**Files:**
- Create: `backend/app/models/__init__.py`, `backend/app/models/course.py`, `backend/app/models/participant.py`, `backend/app/models/progress.py`, `backend/app/models/quiz_result.py`
- Modify: `backend/app/main.py` (Modelle importieren)

**Interfaces:**
- Produces: `Course(id, name, join_code, created_at)`, `Participant(id, course_id, name, created_at)`, `Progress(id, participant_id, module_key, done, completed_at)`, `QuizResult(id, participant_id, module_key, score, total, answers, created_at)`.

- [ ] **Step 1: `backend/app/models/__init__.py`** — leer.

- [ ] **Step 2: `backend/app/models/course.py`**

```python
from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils import utc_now


class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    join_code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
```

- [ ] **Step 3: `backend/app/models/participant.py`**

```python
from datetime import datetime
from sqlalchemy import DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils import utc_now


class Participant(Base):
    __tablename__ = "participant"
    __table_args__ = (UniqueConstraint("course_id", "name", name="uq_participant"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
```

- [ ] **Step 4: `backend/app/models/progress.py`**

```python
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Progress(Base):
    __tablename__ = "progress"
    __table_args__ = (UniqueConstraint("participant_id", "module_key", name="uq_progress"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    participant_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    module_key: Mapped[str] = mapped_column(String, nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
```

- [ ] **Step 5: `backend/app/models/quiz_result.py`**

```python
from datetime import datetime
from sqlalchemy import DateTime, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils import utc_now


class QuizResult(Base):
    __tablename__ = "quiz_result"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    participant_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    module_key: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    answers: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
```

- [ ] **Step 6: `backend/app/main.py`** — nach den `database`-Imports ergänzen (vor `create_all`):

```python
from app.models import course as _course  # noqa: F401
from app.models import participant as _participant  # noqa: F401
from app.models import progress as _progress  # noqa: F401
from app.models import quiz_result as _quiz_result  # noqa: F401
```

- [ ] **Step 7: Import-Check + Commit**

```bash
cd backend && SECRET_KEY=test-secret-key-not-the-default-0123456789 .venv/Scripts/python -c "import app.main; print('ok')"
```
Expected: `ok`.
```bash
git add backend/app
git commit -m "feat(backend): Modelle Course/Participant/Progress/QuizResult"
```

---

### Task 3: Auth (Trainer-Login + JWT + Deps)

**Files:**
- Create: `backend/app/services/__init__.py`, `backend/app/services/security.py`, `backend/app/services/deps.py`, `backend/app/routers/__init__.py`, `backend/app/routers/auth.py`, `backend/tests/test_auth.py`
- Modify: `backend/app/main.py` (Router einbinden)

**Interfaces:**
- Produces:
  - `security.create_token(sub: str, role: str, extra: dict | None) -> str`, `security.decode_token(token) -> dict`.
  - `deps.get_trainer()` (403 wenn nicht Trainer), `deps.get_participant(db)` → `Participant` (403 sonst).
  - `POST /api/trainer/login {email, password}` → `{access_token}`.

- [ ] **Step 1: `backend/app/services/__init__.py`** — leer.

- [ ] **Step 2: `backend/app/services/security.py`**

```python
from datetime import timedelta

from jose import JWTError, jwt

from app.config import settings
from app.utils import utc_now

ALGORITHM = "HS256"


def create_token(sub: str, role: str, extra: dict | None = None) -> str:
    payload = {"sub": sub, "role": role, "exp": utc_now() + timedelta(days=30)}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except JWTError:
        return None
```

- [ ] **Step 3: `backend/app/services/deps.py`**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.participant import Participant
from app.services.security import decode_token

bearer = HTTPBearer()


def _payload(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    data = decode_token(creds.credentials)
    if not data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ungültiges Token")
    return data


def get_trainer(payload: dict = Depends(_payload)) -> dict:
    if payload.get("role") != "trainer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nur Trainer")
    return payload


def get_participant(payload: dict = Depends(_payload), db: Session = Depends(get_db)) -> Participant:
    if payload.get("role") != "participant":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nur Teilnehmer")
    p = db.query(Participant).filter(Participant.id == payload.get("participant_id")).first()
    if not p:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Teilnehmer nicht gefunden")
    return p
```

- [ ] **Step 4: `backend/app/routers/__init__.py`** — leer.

- [ ] **Step 5: `backend/app/routers/auth.py`**

```python
import hmac

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.config import settings
from app.services.security import create_token

router = APIRouter(tags=["auth"])


class TrainerLogin(BaseModel):
    email: str
    password: str


@router.post("/trainer/login")
def trainer_login(data: TrainerLogin):
    if not settings.admin_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Trainer-Login nicht konfiguriert")
    ok_mail = hmac.compare_digest(data.email.lower(), settings.admin_email.lower())
    ok_pw = hmac.compare_digest(data.password, settings.admin_password)
    if not (ok_mail and ok_pw):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login fehlgeschlagen")
    return {"access_token": create_token(sub=settings.admin_email, role="trainer")}
```

- [ ] **Step 6: `backend/app/main.py`** — Router einbinden (nach Health):

```python
from app.routers import auth as auth_router
_api.include_router(auth_router.router)
```

- [ ] **Step 7: `backend/tests/test_auth.py`**

```python
from fastapi.testclient import TestClient
from app.main import app


def test_trainer_login_ok_and_bad():
    with TestClient(app) as c:
        r = c.post("/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"})
        assert r.status_code == 200
        assert r.json()["access_token"]

        bad = c.post("/api/trainer/login", json={"email": "trainer@test.de", "password": "wrong"})
        assert bad.status_code == 401
```

- [ ] **Step 8: Lauf + Commit**

```bash
cd backend && .venv/Scripts/python -m pytest tests/test_auth.py -q
```
Expected: 1 passed.
```bash
git add backend/app backend/tests/test_auth.py
git commit -m "feat(backend): Trainer-Login, JWT, Auth-Deps"
```

---

### Task 4: Modul-Inhalte + Quiz-Bewertung (pure) + Tests

**Files:**
- Create: `backend/app/content/__init__.py`, `backend/app/content/vlan.py`, `backend/app/content/registry.py`, `backend/app/services/grading.py`, `backend/tests/test_grading.py`, `backend/tests/test_content.py`

**Interfaces:**
- Produces:
  - `registry.MODULES: dict[str, dict]` (jeder Modul-Dict: `key, title, order, pass_threshold, blocks, quiz`).
  - `registry.public_module(key) -> dict | None` (Blöcke + Quizfragen **ohne** `answer`).
  - `registry.module_meta() -> list[dict]` (`key, title, order`, sortiert).
  - `grading.grade(quiz: dict, answers: dict) -> tuple[int, int]`, `grading.passed(score, total, threshold) -> bool`.

- [ ] **Step 1: Test schreiben** — `backend/tests/test_grading.py`:

```python
from app.services import grading

QUIZ = {"questions": [
    {"id": "q1", "type": "single", "prompt": "?", "options": ["a", "b"], "answer": "b"},
    {"id": "q2", "type": "multi", "prompt": "?", "options": ["a", "b", "c"], "answer": ["a", "c"]},
    {"id": "q3", "type": "number", "prompt": "?", "answer": 10},
]}


def test_grade_all_correct():
    score, total = grading.grade(QUIZ, {"q1": "b", "q2": ["c", "a"], "q3": 10})
    assert (score, total) == (3, 3)


def test_grade_partial_and_wrong_types():
    score, total = grading.grade(QUIZ, {"q1": "a", "q2": ["a"], "q3": 10})
    assert (score, total) == (1, 3)  # nur q3


def test_passed_threshold():
    assert grading.passed(2, 3, 0.7) is False
    assert grading.passed(3, 3, 0.7) is True
    assert grading.passed(0, 0, 0.7) is False
```

- [ ] **Step 2: Lauf, Fehlschlag**

Run: `cd backend && .venv/Scripts/python -m pytest tests/test_grading.py -q`
Expected: FAIL (kein `grading`).

- [ ] **Step 3: `backend/app/services/grading.py`**

```python
def _correct(question: dict, answer) -> bool:
    t = question["type"]
    if t == "single":
        return answer == question["answer"]
    if t == "multi":
        if not isinstance(answer, list):
            return False
        return sorted(answer) == sorted(question["answer"])
    if t == "number":
        try:
            return float(answer) == float(question["answer"])
        except (TypeError, ValueError):
            return False
    return False


def grade(quiz: dict, answers: dict) -> tuple[int, int]:
    questions = quiz["questions"]
    score = sum(1 for q in questions if _correct(q, (answers or {}).get(q["id"])))
    return score, len(questions)


def passed(score: int, total: int, threshold: float) -> bool:
    return total > 0 and (score / total) >= threshold
```

- [ ] **Step 4: Lauf, grün**

Run: `cd backend && .venv/Scripts/python -m pytest tests/test_grading.py -q`
Expected: 3 passed.

- [ ] **Step 5: `backend/app/content/__init__.py`** — leer.

- [ ] **Step 6: `backend/app/content/vlan.py`**

```python
VLAN_MODULE = {
    "key": "vlan",
    "title": "VLANs",
    "order": 1,
    "pass_threshold": 0.7,
    "blocks": [
        {"type": "text", "value": "## Was ist ein VLAN?\n\nEin VLAN (Virtual LAN) "
            "teilt einen physischen Switch in mehrere getrennte Broadcast-Domänen. "
            "Geräte in verschiedenen VLANs können ohne Router nicht miteinander reden."},
        {"type": "text", "value": "## Access- vs. Trunk-Port\n\n- **Access-Port**: "
            "gehört zu genau einem VLAN, sendet/empfängt **ungetaggte** Frames (Endgeräte).\n"
            "- **Trunk-Port**: trägt mehrere VLANs, markiert Frames mit einem "
            "**802.1Q-Tag** (VLAN-ID), Verbindung zwischen Switches."},
        {"type": "widget", "id": "vlan-switch"},
        {"type": "text", "value": "## Broadcast-Domänen\n\nJedes VLAN ist eine eigene "
            "Broadcast-Domäne. Ein Broadcast aus VLAN 10 erreicht nur Ports in VLAN 10."},
    ],
    "quiz": {"questions": [
        {"id": "v1", "type": "single",
         "prompt": "Wie viele VLANs trägt ein Access-Port?",
         "options": ["0", "genau 1", "mehrere", "alle"], "answer": "genau 1"},
        {"id": "v2", "type": "single",
         "prompt": "Womit markiert ein Trunk Frames für ein VLAN?",
         "options": ["MAC-Adresse", "802.1Q-Tag", "IP-Header", "Portnummer"],
         "answer": "802.1Q-Tag"},
        {"id": "v3", "type": "multi",
         "prompt": "Was stimmt über VLANs? (mehrere)",
         "options": ["Eigene Broadcast-Domäne", "Brauchen Router für VLAN-übergreifend",
                     "Access-Port taggt Frames", "Trennen Geräte logisch"],
         "answer": ["Eigene Broadcast-Domäne", "Brauchen Router für VLAN-übergreifend",
                    "Trennen Geräte logisch"]},
        {"id": "v4", "type": "number",
         "prompt": "Ein Host in VLAN 20 sendet über einen Trunk. Welche VLAN-ID steht im Tag?",
         "answer": 20},
    ]},
}
```

- [ ] **Step 7: `backend/app/content/registry.py`**

```python
from copy import deepcopy

from app.content.vlan import VLAN_MODULE

MODULES = {VLAN_MODULE["key"]: VLAN_MODULE}


def module_meta() -> list[dict]:
    metas = [{"key": m["key"], "title": m["title"], "order": m["order"]} for m in MODULES.values()]
    return sorted(metas, key=lambda m: m["order"])


def public_module(key: str) -> dict | None:
    m = MODULES.get(key)
    if not m:
        return None
    pub = deepcopy(m)
    for q in pub["quiz"]["questions"]:
        q.pop("answer", None)
    return pub
```

- [ ] **Step 8: `backend/tests/test_content.py`**

```python
from app.content import registry


def test_public_module_strips_answers():
    pub = registry.public_module("vlan")
    assert pub is not None
    for q in pub["quiz"]["questions"]:
        assert "answer" not in q
    # Original bleibt vollständig
    assert registry.MODULES["vlan"]["quiz"]["questions"][0]["answer"]


def test_module_meta_sorted():
    metas = registry.module_meta()
    assert metas[0]["key"] == "vlan"
    assert registry.public_module("nope") is None
```

- [ ] **Step 9: Lauf + Commit**

```bash
cd backend && .venv/Scripts/python -m pytest tests/test_grading.py tests/test_content.py -q
```
Expected: 5 passed.
```bash
git add backend/app/content backend/app/services/grading.py backend/tests/test_grading.py backend/tests/test_content.py
git commit -m "feat(content): VLAN-Modul + Quiz-Bewertung (pure) + Tests"
```

---

### Task 5: Kurse + Beitritt (Endpoints)

**Files:**
- Create: `backend/app/services/codes.py`, `backend/app/routers/courses.py`, `backend/app/routers/join.py`, `backend/tests/test_courses_join.py`
- Modify: `backend/app/main.py` (Router einbinden)

**Interfaces:**
- Consumes: `get_trainer`, `get_participant`, Modelle, `create_token`, `module_meta`.
- Produces:
  - `codes.new_code(db) -> str` (6 Zeichen, im Kurs unique).
  - `POST /api/courses` (Trainer) → `{id, name, join_code}`; `GET /api/courses` (Trainer) → Liste.
  - `POST /api/join {code, name}` → `{access_token, course_name, name}`.
  - `GET /api/me` (Teilnehmer) → `{name, course_id, progress: [{module_key, done, best}]}`.

- [ ] **Step 1: `backend/app/services/codes.py`**

```python
import secrets
import string

from app.models.course import Course

_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # ohne verwechselbare Zeichen


def new_code(db) -> str:
    while True:
        code = "".join(secrets.choice(_ALPHABET) for _ in range(6))
        if not db.query(Course).filter(Course.join_code == code).first():
            return code
```

- [ ] **Step 2: `backend/app/routers/courses.py`**

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.course import Course
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.services.codes import new_code
from app.services.deps import get_trainer
from app.content.registry import module_meta

router = APIRouter(prefix="/courses", tags=["courses"])


class CourseCreate(BaseModel):
    name: str


@router.post("")
def create_course(data: CourseCreate, db: Session = Depends(get_db), _=Depends(get_trainer)):
    if not data.name.strip():
        raise HTTPException(status_code=422, detail="Name fehlt")
    c = Course(name=data.name.strip(), join_code=new_code(db))
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "name": c.name, "join_code": c.join_code}


@router.get("")
def list_courses(db: Session = Depends(get_db), _=Depends(get_trainer)):
    return [{"id": c.id, "name": c.name, "join_code": c.join_code}
            for c in db.query(Course).order_by(Course.created_at.desc()).all()]


@router.get("/{course_id}/dashboard")
def dashboard(course_id: int, db: Session = Depends(get_db), _=Depends(get_trainer)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")
    metas = module_meta()
    participants = db.query(Participant).filter(Participant.course_id == course_id).all()
    rows = []
    for p in participants:
        cells = {}
        for m in metas:
            prog = db.query(Progress).filter(
                Progress.participant_id == p.id, Progress.module_key == m["key"]).first()
            best = db.query(QuizResult).filter(
                QuizResult.participant_id == p.id, QuizResult.module_key == m["key"]).all()
            best_pct = max((r.score / r.total for r in best if r.total), default=None)
            cells[m["key"]] = {"done": bool(prog and prog.done),
                               "best": round(best_pct * 100) if best_pct is not None else None}
        rows.append({"name": p.name, "cells": cells})
    return {"course": {"id": course.id, "name": course.name, "join_code": course.join_code},
            "modules": metas, "participants": rows}
```

- [ ] **Step 3: `backend/app/routers/join.py`**

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.course import Course
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.services.deps import get_participant
from app.services.security import create_token
from app.content.registry import module_meta

router = APIRouter(tags=["join"])


class JoinReq(BaseModel):
    code: str
    name: str


@router.post("/join")
def join(data: JoinReq, db: Session = Depends(get_db)):
    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Name fehlt")
    course = db.query(Course).filter(Course.join_code == data.code.strip().upper()).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs-Code ungültig")
    p = db.query(Participant).filter(
        Participant.course_id == course.id, Participant.name == name).first()
    if not p:
        p = Participant(course_id=course.id, name=name)
        db.add(p)
        db.commit()
        db.refresh(p)
    token = create_token(sub=name, role="participant",
                         extra={"participant_id": p.id, "course_id": course.id})
    return {"access_token": token, "course_name": course.name, "name": name}


@router.get("/me")
def me(db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    progress = []
    for m in module_meta():
        prog = db.query(Progress).filter(
            Progress.participant_id == p.id, Progress.module_key == m["key"]).first()
        best = db.query(QuizResult).filter(
            QuizResult.participant_id == p.id, QuizResult.module_key == m["key"]).all()
        best_pct = max((r.score / r.total for r in best if r.total), default=None)
        progress.append({"module_key": m["key"], "done": bool(prog and prog.done),
                         "best": round(best_pct * 100) if best_pct is not None else None})
    return {"name": p.name, "course_id": p.course_id, "progress": progress}
```

- [ ] **Step 4: `backend/app/main.py`** — Router einbinden:

```python
from app.routers import courses as courses_router
from app.routers import join as join_router
_api.include_router(courses_router.router)
_api.include_router(join_router.router)
```

- [ ] **Step 5: `backend/tests/test_courses_join.py`**

```python
from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_course_and_join_flow():
    with TestClient(app) as c:
        h = _trainer(c)
        code = c.post("/api/courses", json={"name": "Netzwerk Q3"}, headers=h).json()["join_code"]

        # Beitritt legt Teilnehmer an
        r = c.post("/api/join", json={"code": code, "name": "Anna"})
        assert r.status_code == 200
        tok = r.json()["access_token"]

        # gleicher Code+Name -> kein Duplikat (Token erneut, gleicher Teilnehmer)
        r2 = c.post("/api/join", json={"code": code, "name": "Anna"})
        assert r2.status_code == 200

        # /me
        me = c.get("/api/me", headers={"Authorization": f"Bearer {tok}"})
        assert me.status_code == 200
        assert me.json()["name"] == "Anna"
        assert any(p["module_key"] == "vlan" for p in me.json()["progress"])

        # ungültiger Code
        assert c.post("/api/join", json={"code": "ZZZZZZ", "name": "X"}).status_code == 404
        # Teilnehmer darf keine Kurse anlegen
        assert c.post("/api/courses", json={"name": "x"},
                      headers={"Authorization": f"Bearer {tok}"}).status_code == 403
```

- [ ] **Step 6: Lauf + Commit**

```bash
cd backend && .venv/Scripts/python -m pytest tests/test_courses_join.py -q
```
Expected: 1 passed.
```bash
git add backend/app backend/tests/test_courses_join.py
git commit -m "feat(backend): Kurse anlegen, Beitritt per Code, Dashboard-Endpoint"
```

---

### Task 6: Module + Quiz-Abgabe (Endpoints)

**Files:**
- Create: `backend/app/routers/modules.py`, `backend/tests/test_modules_quiz.py`
- Modify: `backend/app/main.py` (Router einbinden)

**Interfaces:**
- Consumes: `get_participant`, `registry.module_meta/public_module/MODULES`, `grading.grade/passed`, Modelle.
- Produces:
  - `GET /api/modules` (Teilnehmer) → Meta-Liste.
  - `GET /api/modules/{key}` (Teilnehmer) → Blöcke + Quizfragen ohne Lösung.
  - `POST /api/modules/{key}/quiz {answers}` (Teilnehmer) → `{score, total, passed, best}`; speichert Versuch + aktualisiert Progress.

- [ ] **Step 1: `backend/app/routers/modules.py`**

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.participant import Participant
from app.models.progress import Progress
from app.models.quiz_result import QuizResult
from app.services.deps import get_participant
from app.services import grading
from app.content.registry import MODULES, module_meta, public_module
from app.utils import utc_now

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("")
def list_modules(_: Participant = Depends(get_participant)):
    return module_meta()


@router.get("/{key}")
def get_module(key: str, _: Participant = Depends(get_participant)):
    pub = public_module(key)
    if not pub:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    return pub


class QuizSubmit(BaseModel):
    answers: dict


@router.post("/{key}/quiz")
def submit_quiz(key: str, data: QuizSubmit, db: Session = Depends(get_db),
                p: Participant = Depends(get_participant)):
    module = MODULES.get(key)
    if not module:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    score, total = grading.grade(module["quiz"], data.answers)
    is_passed = grading.passed(score, total, module["pass_threshold"])

    db.add(QuizResult(participant_id=p.id, module_key=key, score=score,
                      total=total, answers=data.answers))

    prog = db.query(Progress).filter(
        Progress.participant_id == p.id, Progress.module_key == key).first()
    if not prog:
        prog = Progress(participant_id=p.id, module_key=key, done=False)
        db.add(prog)
    if is_passed and not prog.done:
        prog.done = True
        prog.completed_at = utc_now()
    db.commit()

    results = db.query(QuizResult).filter(
        QuizResult.participant_id == p.id, QuizResult.module_key == key).all()
    best_pct = max((r.score / r.total for r in results if r.total), default=0)
    return {"score": score, "total": total, "passed": is_passed, "best": round(best_pct * 100)}
```

- [ ] **Step 2: `backend/app/main.py`** — Router einbinden:

```python
from app.routers import modules as modules_router
_api.include_router(modules_router.router)
```

- [ ] **Step 3: `backend/tests/test_modules_quiz.py`**

```python
from fastapi.testclient import TestClient
from app.main import app


def _participant_token(c):
    h = {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}
    code = c.post("/api/courses", json={"name": "QuizKurs"}, headers=h).json()["join_code"]
    return c.post("/api/join", json={"code": code, "name": "Bob"}).json()["access_token"]


def test_module_delivery_hides_answers_and_grades():
    with TestClient(app) as c:
        tok = _participant_token(c)
        h = {"Authorization": f"Bearer {tok}"}

        mod = c.get("/api/modules/vlan", headers=h).json()
        for q in mod["quiz"]["questions"]:
            assert "answer" not in q

        # alles richtig -> passed, done
        good = {"v1": "genau 1", "v2": "802.1Q-Tag",
                "v3": ["Eigene Broadcast-Domäne", "Brauchen Router für VLAN-übergreifend", "Trennen Geräte logisch"],
                "v4": 20}
        r = c.post("/api/modules/vlan/quiz", json={"answers": good}, headers=h).json()
        assert r["score"] == 4 and r["total"] == 4 and r["passed"] is True

        me = c.get("/api/me", headers=h).json()
        vlan = next(p for p in me["progress"] if p["module_key"] == "vlan")
        assert vlan["done"] is True and vlan["best"] == 100

        # schlechterer Versuch senkt best NICHT
        c.post("/api/modules/vlan/quiz", json={"answers": {"v1": "0"}}, headers=h)
        me2 = c.get("/api/me", headers=h).json()
        assert next(p for p in me2["progress"] if p["module_key"] == "vlan")["best"] == 100

        # unbekanntes Modul
        assert c.get("/api/modules/nope", headers=h).status_code == 404
```

- [ ] **Step 4: Lauf + Commit**

```bash
cd backend && .venv/Scripts/python -m pytest -q
```
Expected: alle grün.
```bash
git add backend/app/routers/modules.py backend/app/main.py backend/tests/test_modules_quiz.py
git commit -m "feat(backend): Modul-Auslieferung + serverseitige Quiz-Abgabe"
```

---

### Task 7: Frontend-Gerüst (Vite, Tailwind, Auth-Store, Landing)

**Files:**
- Create: `frontend/` (Vite React-TS), `frontend/tailwind.config.js`, `frontend/src/index.css`, `frontend/src/lib/api.ts`, `frontend/src/store/auth.ts`, `frontend/src/App.tsx`, `frontend/src/main.tsx`, `frontend/src/pages/LandingPage.tsx`

**Interfaces:**
- Produces: axios-Client mit Token-Interceptor; `useAuthStore` (`token`, `role`, `setAuth`, `logout`); Router mit `/` (Landing), `/lernen`, `/trainer`.

- [ ] **Step 1: Vite-Projekt + Deps**

```bash
cd frontend && npm create vite@latest . -- --template react-ts
npm install
npm install react-router-dom @tanstack/react-query axios zustand
npm install -D tailwindcss @tailwindcss/vite
```

- [ ] **Step 2: `frontend/vite.config.ts`** ersetzen

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { proxy: { '/api': 'http://localhost:8000' } },
})
```

- [ ] **Step 3: `frontend/src/index.css`** ersetzen

```css
@import "tailwindcss";
```

- [ ] **Step 4: `frontend/src/store/auth.ts`**

```ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

type Role = 'trainer' | 'participant' | null

interface AuthState {
  token: string | null
  role: Role
  displayName: string | null
  setAuth: (token: string, role: Role, displayName?: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      role: null,
      displayName: null,
      setAuth: (token, role, displayName) => set({ token, role, displayName: displayName ?? null }),
      logout: () => set({ token: null, role: null, displayName: null }),
    }),
    { name: 'intnetwork-auth' },
  ),
)
```

- [ ] **Step 5: `frontend/src/lib/api.ts`**

```ts
import axios from 'axios'
import { useAuthStore } from '@/store/auth'

export const api = axios.create({ baseURL: '/api' })

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const authApi = {
  trainerLogin: (email: string, password: string) =>
    api.post<{ access_token: string }>('/trainer/login', { email, password }),
  join: (code: string, name: string) =>
    api.post<{ access_token: string; course_name: string; name: string }>('/join', { code, name }),
}
```

(Hinweis: `@`-Alias in `tsconfig.json` + `vite.config.ts` setzen — `paths: { "@/*": ["src/*"] }` und `resolve.alias`. Falls Vite-Template das nicht hat, in Step 2 `resolve: { alias: { '@': '/src' } }` ergänzen und in `tsconfig.app.json` `"baseUrl": ".", "paths": {"@/*": ["src/*"]}`.)

- [ ] **Step 6: `frontend/src/pages/LandingPage.tsx`**

```tsx
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authApi } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

export function LandingPage() {
  const nav = useNavigate()
  const setAuth = useAuthStore((s) => s.setAuth)
  const [code, setCode] = useState('')
  const [name, setName] = useState('')
  const [err, setErr] = useState('')

  async function join(e: React.FormEvent) {
    e.preventDefault()
    setErr('')
    try {
      const r = await authApi.join(code, name)
      setAuth(r.data.access_token, 'participant', r.data.name)
      nav('/lernen')
    } catch {
      setErr('Kurs-Code ungültig oder Name fehlt.')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <div className="w-full max-w-sm rounded-2xl bg-white shadow p-8">
        <h1 className="text-2xl font-bold text-slate-900">IntNetwork</h1>
        <p className="text-slate-500 text-sm mb-6">Netzwerk-Grundlagen — Kurs beitreten</p>
        <form onSubmit={join} className="flex flex-col gap-3">
          <input className="border rounded-lg px-3 py-2 uppercase" placeholder="Kurs-Code"
            value={code} onChange={(e) => setCode(e.target.value.toUpperCase())} />
          <input className="border rounded-lg px-3 py-2" placeholder="Dein Name"
            value={name} onChange={(e) => setName(e.target.value)} />
          {err && <p className="text-sm text-red-600">{err}</p>}
          <button className="rounded-lg bg-indigo-600 text-white py-2 font-medium">Beitreten</button>
        </form>
        <button onClick={() => nav('/trainer')} className="mt-4 text-xs text-slate-400 hover:text-slate-600">
          Trainer-Login
        </button>
      </div>
    </div>
  )
}
```

- [ ] **Step 7: `frontend/src/App.tsx`**

```tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { LandingPage } from '@/pages/LandingPage'
import { LearnPage } from '@/pages/LearnPage'
import { ModulePage } from '@/pages/ModulePage'
import { TrainerPage } from '@/pages/TrainerPage'

const qc = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={qc}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/lernen" element={<LearnPage />} />
          <Route path="/lernen/:key" element={<ModulePage />} />
          <Route path="/trainer" element={<TrainerPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
```

(`main.tsx` aus dem Vite-Template behalten, nur sicherstellen dass `./index.css` importiert wird.)

- [ ] **Step 8: Platzhalter-Seiten** anlegen, damit es baut — `frontend/src/pages/LearnPage.tsx`, `ModulePage.tsx`, `TrainerPage.tsx` je mit `export function <Name>() { return <div className="p-8">…</div> }` (werden in Tasks 8–10 ersetzt).

- [ ] **Step 9: Build + Commit**

```bash
cd frontend && npx tsc -b && npm run build
```
Expected: Build ok.
```bash
git add frontend
git commit -m "feat(frontend): Vite/Tailwind-Gerüst, Auth-Store, Landing"
```

---

### Task 8: Teilnehmer — Modul-Liste + Block-Renderer + Quiz

**Files:**
- Create: `frontend/src/lib/learnApi.ts`, `frontend/src/pages/LearnPage.tsx` (ersetzen), `frontend/src/pages/ModulePage.tsx` (ersetzen), `frontend/src/components/Blocks.tsx`, `frontend/src/components/Quiz.tsx`, `frontend/src/widgets/registry.tsx`, `frontend/src/types.ts`

**Interfaces:**
- Consumes: `api`, Auth-Store.
- Produces: `learnApi` (`me`, `listModules`, `getModule`, `submitQuiz`); `WIDGETS` Registry (`{ 'vlan-switch': Component }`); Typen `Block`, `Question`, `ModuleDetail`.

- [ ] **Step 1: `frontend/src/types.ts`**

```ts
export type Block =
  | { type: 'text'; value: string }
  | { type: 'image'; url: string; alt?: string }
  | { type: 'widget'; id: string }

export type Question =
  | { id: string; type: 'single'; prompt: string; options: string[] }
  | { id: string; type: 'multi'; prompt: string; options: string[] }
  | { id: string; type: 'number'; prompt: string }

export interface ModuleDetail {
  key: string
  title: string
  blocks: Block[]
  quiz: { questions: Question[] }
}

export interface ModuleMeta { key: string; title: string; order: number }
export interface ProgressItem { module_key: string; done: boolean; best: number | null }
```

- [ ] **Step 2: `frontend/src/lib/learnApi.ts`**

```ts
import { api } from '@/lib/api'
import type { ModuleDetail, ModuleMeta, ProgressItem } from '@/types'

export const learnApi = {
  me: () => api.get<{ name: string; course_id: number; progress: ProgressItem[] }>('/me'),
  listModules: () => api.get<ModuleMeta[]>('/modules'),
  getModule: (key: string) => api.get<ModuleDetail>(`/modules/${key}`),
  submitQuiz: (key: string, answers: Record<string, unknown>) =>
    api.post<{ score: number; total: number; passed: boolean; best: number }>(
      `/modules/${key}/quiz`, { answers }),
}
```

- [ ] **Step 3: `frontend/src/widgets/registry.tsx`**

```tsx
import type { ComponentType } from 'react'
import { VlanSwitch } from '@/widgets/VlanSwitch'

export const WIDGETS: Record<string, ComponentType> = {
  'vlan-switch': VlanSwitch,
}
```

(Bis Task 9 existiert `VlanSwitch` noch nicht — lege in diesem Schritt einen Stub
`frontend/src/widgets/VlanSwitch.tsx` mit `export function VlanSwitch() { return <div className="rounded-lg border p-4 text-sm text-slate-500">Switch-Simulator folgt…</div> }` an, der in Task 9 ersetzt wird.)

- [ ] **Step 4: `frontend/src/components/Blocks.tsx`**

```tsx
import type { Block } from '@/types'
import { WIDGETS } from '@/widgets/registry'

export function Blocks({ blocks }: { blocks: Block[] }) {
  return (
    <div className="flex flex-col gap-6">
      {blocks.map((b, i) => {
        if (b.type === 'text') {
          return <div key={i} className="prose prose-slate max-w-none whitespace-pre-wrap text-slate-700">{b.value}</div>
        }
        if (b.type === 'image') {
          return <img key={i} src={b.url} alt={b.alt ?? ''} className="rounded-lg border" />
        }
        const W = WIDGETS[b.id]
        return W ? <W key={i} /> : <div key={i} className="text-sm text-red-500">Unbekanntes Widget: {b.id}</div>
      })}
    </div>
  )
}
```

- [ ] **Step 5: `frontend/src/components/Quiz.tsx`**

```tsx
import { useState } from 'react'
import type { Question } from '@/types'
import { learnApi } from '@/lib/learnApi'

export function Quiz({ moduleKey, questions }: { moduleKey: string; questions: Question[] }) {
  const [answers, setAnswers] = useState<Record<string, unknown>>({})
  const [result, setResult] = useState<{ score: number; total: number; passed: boolean } | null>(null)

  const set = (id: string, value: unknown) => setAnswers((a) => ({ ...a, [id]: value }))
  const toggleMulti = (id: string, opt: string) =>
    setAnswers((a) => {
      const cur = (a[id] as string[]) ?? []
      return { ...a, [id]: cur.includes(opt) ? cur.filter((o) => o !== opt) : [...cur, opt] }
    })

  async function submit() {
    const r = await learnApi.submitQuiz(moduleKey, answers)
    setResult(r.data)
  }

  return (
    <div className="mt-8 rounded-2xl border bg-white p-6">
      <h3 className="text-lg font-semibold text-slate-900 mb-4">Quiz</h3>
      <div className="flex flex-col gap-5">
        {questions.map((q) => (
          <div key={q.id}>
            <p className="font-medium text-slate-800 mb-2">{q.prompt}</p>
            {q.type === 'number' ? (
              <input type="number" className="border rounded-lg px-3 py-1.5 w-32"
                onChange={(e) => set(q.id, Number(e.target.value))} />
            ) : (
              <div className="flex flex-col gap-1.5">
                {q.options.map((opt) => (
                  <label key={opt} className="flex items-center gap-2 text-slate-700">
                    <input
                      type={q.type === 'single' ? 'radio' : 'checkbox'}
                      name={q.id}
                      checked={q.type === 'single' ? answers[q.id] === opt : ((answers[q.id] as string[]) ?? []).includes(opt)}
                      onChange={() => (q.type === 'single' ? set(q.id, opt) : toggleMulti(q.id, opt))}
                    />
                    {opt}
                  </label>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
      <button onClick={submit} className="mt-5 rounded-lg bg-indigo-600 text-white px-4 py-2 font-medium">
        Auswerten
      </button>
      {result && (
        <p className={`mt-4 font-medium ${result.passed ? 'text-green-600' : 'text-amber-600'}`}>
          {result.score} / {result.total} richtig — {result.passed ? 'bestanden ✓' : 'noch nicht bestanden'}
        </p>
      )}
    </div>
  )
}
```

- [ ] **Step 6: `frontend/src/pages/LearnPage.tsx`** (ersetzen)

```tsx
import { useQuery } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { useAuthStore } from '@/store/auth'

export function LearnPage() {
  const nav = useNavigate()
  const { role, displayName } = useAuthStore()
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data) })
  const mods = useQuery({ queryKey: ['modules'], queryFn: () => learnApi.listModules().then((r) => r.data) })

  if (role !== 'participant') { nav('/'); return null }

  const progressOf = (key: string) => me.data?.progress.find((p) => p.module_key === key)

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-slate-900">Hallo {displayName}</h1>
        <p className="text-slate-500 text-sm mb-6">Wähle ein Modul.</p>
        <div className="flex flex-col gap-3">
          {mods.data?.map((m) => {
            const p = progressOf(m.key)
            return (
              <Link key={m.key} to={`/lernen/${m.key}`}
                className="rounded-xl border bg-white p-4 flex items-center justify-between hover:shadow">
                <span className="font-medium text-slate-800">{m.title}</span>
                <span className="text-sm text-slate-500">
                  {p?.done ? '✓ erledigt' : 'offen'}{p?.best != null ? ` · best ${p.best}%` : ''}
                </span>
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 7: `frontend/src/pages/ModulePage.tsx`** (ersetzen)

```tsx
import { useQuery } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { Blocks } from '@/components/Blocks'
import { Quiz } from '@/components/Quiz'

export function ModulePage() {
  const { key = '' } = useParams()
  const mod = useQuery({ queryKey: ['module', key], queryFn: () => learnApi.getModule(key).then((r) => r.data) })

  if (mod.isLoading || !mod.data) return <div className="p-10">Lädt…</div>

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <Link to="/lernen" className="text-sm text-slate-400 hover:text-slate-600">← Module</Link>
        <h1 className="text-2xl font-bold text-slate-900 mt-2 mb-6">{mod.data.title}</h1>
        <Blocks blocks={mod.data.blocks} />
        <Quiz moduleKey={key} questions={mod.data.quiz.questions} />
      </div>
    </div>
  )
}
```

- [ ] **Step 8: Build + Commit**

```bash
cd frontend && npx tsc -b && npm run build
```
Expected: Build ok.
```bash
git add frontend/src
git commit -m "feat(frontend): Modul-Liste, Block-Renderer, Quiz"
```

---

### Task 9: VLAN-Switch-Widget

**Files:**
- Create: `frontend/src/widgets/VlanSwitch.tsx` (ersetzt den Stub)

**Interfaces:**
- Produces: `VlanSwitch`-Komponente (clientseitig, keine API).

**Modell:** 6 Ports. Jeder Port: `vlan` (Zahl) + `mode` (`access` | `trunk`). Ein Host hängt an jedem Access-Port. „Frame senden" von einem gewählten Quell-Port → alle Ports in derselben Broadcast-Domäne (gleiches VLAN) leuchten; Trunk-Ports zeigen das Tag `802.1Q VLAN <id>`.

- [ ] **Step 1: `frontend/src/widgets/VlanSwitch.tsx`**

```tsx
import { useMemo, useState } from 'react'

interface Port { vlan: number; mode: 'access' | 'trunk' }

const INITIAL: Port[] = [
  { vlan: 10, mode: 'access' },
  { vlan: 10, mode: 'access' },
  { vlan: 20, mode: 'access' },
  { vlan: 20, mode: 'access' },
  { vlan: 30, mode: 'access' },
  { vlan: 10, mode: 'trunk' },
]
const VLAN_COLORS: Record<number, string> = {
  10: 'bg-blue-100 border-blue-400 text-blue-700',
  20: 'bg-green-100 border-green-400 text-green-700',
  30: 'bg-purple-100 border-purple-400 text-purple-700',
}

export function VlanSwitch() {
  const [ports, setPorts] = useState<Port[]>(INITIAL)
  const [source, setSource] = useState<number | null>(null)

  const reached = useMemo(() => {
    if (source === null) return new Set<number>()
    const vlan = ports[source].vlan
    const set = new Set<number>()
    ports.forEach((p, i) => {
      if (i !== source && (p.vlan === vlan || p.mode === 'trunk')) set.add(i)
    })
    return set
  }, [source, ports])

  const update = (i: number, patch: Partial<Port>) =>
    setPorts((ps) => ps.map((p, idx) => (idx === i ? { ...p, ...patch } : p)))

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">Switch-Simulator</p>
      <div className="grid grid-cols-3 gap-3">
        {ports.map((p, i) => {
          const active = source === i
          const lit = reached.has(i)
          return (
            <div key={i}
              className={`rounded-xl border-2 p-3 text-sm ${VLAN_COLORS[p.vlan] ?? 'bg-slate-100 border-slate-300'} ${active ? 'ring-2 ring-indigo-500' : ''} ${lit ? 'outline outline-2 outline-amber-400' : ''}`}>
              <div className="font-semibold mb-1">Port {i + 1}</div>
              <label className="block text-xs">VLAN
                <input type="number" value={p.vlan} min={1}
                  onChange={(e) => update(i, { vlan: Number(e.target.value) })}
                  className="ml-1 w-14 border rounded px-1" />
              </label>
              <label className="block text-xs mt-1">Modus
                <select value={p.mode} onChange={(e) => update(i, { mode: e.target.value as Port['mode'] })}
                  className="ml-1 border rounded px-1">
                  <option value="access">Access</option>
                  <option value="trunk">Trunk</option>
                </select>
              </label>
              <button onClick={() => setSource(i)}
                className="mt-2 text-xs rounded bg-indigo-600 text-white px-2 py-0.5">Frame senden</button>
              {lit && p.mode === 'trunk' && source !== null && (
                <div className="mt-1 text-[10px] font-mono text-amber-700">802.1Q VLAN {ports[source].vlan}</div>
              )}
            </div>
          )
        })}
      </div>
      {source !== null && (
        <p className="mt-3 text-xs text-slate-500">
          Frame aus Port {source + 1} (VLAN {ports[source].vlan}) erreicht die hervorgehobenen Ports.
          Andere VLANs bleiben getrennt (eigene Broadcast-Domäne).
        </p>
      )}
    </div>
  )
}
```

- [ ] **Step 2: Build + Commit**

```bash
cd frontend && npx tsc -b && npm run build
```
Expected: Build ok.
```bash
git add frontend/src/widgets/VlanSwitch.tsx
git commit -m "feat(frontend): interaktives VLAN-Switch-Widget"
```

---

### Task 10: Trainer — Login, Kurse, Dashboard

**Files:**
- Create: `frontend/src/lib/trainerApi.ts`, `frontend/src/pages/TrainerPage.tsx` (ersetzen)

**Interfaces:**
- Consumes: `api`, Auth-Store.
- Produces: `trainerApi` (`listCourses`, `createCourse`, `dashboard`).

- [ ] **Step 1: `frontend/src/lib/trainerApi.ts`**

```ts
import { api } from '@/lib/api'

export interface Course { id: number; name: string; join_code: string }
export interface Dashboard {
  course: Course
  modules: { key: string; title: string; order: number }[]
  participants: { name: string; cells: Record<string, { done: boolean; best: number | null }> }[]
}

export const trainerApi = {
  listCourses: () => api.get<Course[]>('/courses'),
  createCourse: (name: string) => api.post<Course>('/courses', { name }),
  dashboard: (id: number) => api.get<Dashboard>(`/courses/${id}/dashboard`),
}
```

- [ ] **Step 2: `frontend/src/pages/TrainerPage.tsx`** (ersetzen)

```tsx
import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { authApi } from '@/lib/api'
import { trainerApi } from '@/lib/trainerApi'
import { useAuthStore } from '@/store/auth'

export function TrainerPage() {
  const { token, role, setAuth, logout } = useAuthStore()
  if (role !== 'trainer' || !token) return <TrainerLogin onLogin={(t) => setAuth(t, 'trainer')} />
  return <TrainerDashboard onLogout={logout} />
}

function TrainerLogin({ onLogin }: { onLogin: (t: string) => void }) {
  const [email, setEmail] = useState('')
  const [pw, setPw] = useState('')
  const [err, setErr] = useState('')
  async function submit(e: React.FormEvent) {
    e.preventDefault(); setErr('')
    try { onLogin((await authApi.trainerLogin(email, pw)).data.access_token) }
    catch { setErr('Login fehlgeschlagen.') }
  }
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <form onSubmit={submit} className="w-full max-w-sm rounded-2xl bg-white shadow p-8 flex flex-col gap-3">
        <h1 className="text-xl font-bold text-slate-900">Trainer-Login</h1>
        <input className="border rounded-lg px-3 py-2" placeholder="E-Mail" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="border rounded-lg px-3 py-2" type="password" placeholder="Passwort" value={pw} onChange={(e) => setPw(e.target.value)} />
        {err && <p className="text-sm text-red-600">{err}</p>}
        <button className="rounded-lg bg-indigo-600 text-white py-2 font-medium">Anmelden</button>
      </form>
    </div>
  )
}

function TrainerDashboard({ onLogout }: { onLogout: () => void }) {
  const qc = useQueryClient()
  const [name, setName] = useState('')
  const [selected, setSelected] = useState<number | null>(null)
  const courses = useQuery({ queryKey: ['courses'], queryFn: () => trainerApi.listCourses().then((r) => r.data) })
  const create = useMutation({
    mutationFn: () => trainerApi.createCourse(name).then((r) => r.data),
    onSuccess: () => { setName(''); qc.invalidateQueries({ queryKey: ['courses'] }) },
  })
  const dash = useQuery({
    queryKey: ['dashboard', selected], enabled: selected !== null,
    queryFn: () => trainerApi.dashboard(selected as number).then((r) => r.data),
  })

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-slate-900">Trainer</h1>
          <button onClick={onLogout} className="text-sm text-slate-400 hover:text-slate-600">Abmelden</button>
        </div>

        <div className="flex gap-2 mb-6">
          <input className="border rounded-lg px-3 py-2" placeholder="Neuer Kurs-Name" value={name} onChange={(e) => setName(e.target.value)} />
          <button onClick={() => name.trim() && create.mutate()} className="rounded-lg bg-indigo-600 text-white px-4 font-medium">Kurs anlegen</button>
        </div>

        <div className="flex flex-col gap-2 mb-8">
          {courses.data?.map((c) => (
            <button key={c.id} onClick={() => setSelected(c.id)}
              className={`rounded-xl border bg-white p-4 text-left flex justify-between ${selected === c.id ? 'ring-2 ring-indigo-500' : ''}`}>
              <span className="font-medium text-slate-800">{c.name}</span>
              <span className="font-mono text-indigo-600">{c.join_code}</span>
            </button>
          ))}
        </div>

        {dash.data && (
          <div className="overflow-x-auto rounded-xl border bg-white">
            <table className="w-full text-sm">
              <thead className="bg-slate-50">
                <tr>
                  <th className="text-left px-3 py-2">Teilnehmer</th>
                  {dash.data.modules.map((m) => <th key={m.key} className="px-3 py-2">{m.title}</th>)}
                </tr>
              </thead>
              <tbody>
                {dash.data.participants.map((p) => (
                  <tr key={p.name} className="border-t">
                    <td className="px-3 py-2 font-medium text-slate-700">{p.name}</td>
                    {dash.data!.modules.map((m) => {
                      const cell = p.cells[m.key]
                      return <td key={m.key} className="px-3 py-2 text-center">
                        {cell?.done ? '✓' : '–'}{cell?.best != null ? ` ${cell.best}%` : ''}
                      </td>
                    })}
                  </tr>
                ))}
                {dash.data.participants.length === 0 && (
                  <tr><td colSpan={dash.data.modules.length + 1} className="px-3 py-6 text-center text-slate-400">Noch keine Teilnehmer.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Build + Commit**

```bash
cd frontend && npx tsc -b && npm run build
```
Expected: Build ok.
```bash
git add frontend/src
git commit -m "feat(frontend): Trainer-Login, Kurse, Dashboard"
```

---

### Task 11: README + End-to-End-Verifikation

**Files:**
- Create: `README.md`, `backend/.env.example`

- [ ] **Step 1: `backend/.env.example`**

```
SECRET_KEY=change-me-openssl-rand-hex-32
ADMIN_EMAIL=trainer@firma.de
ADMIN_PASSWORD=setze-ein-starkes-passwort
DATABASE_URL=sqlite:///./intnetwork.db
```

- [ ] **Step 2: `README.md`**

```markdown
# IntNetwork

Interaktiver Netzwerk-Grundlagenkurs (Trainer + Teilnehmer per Kurs-Code).
MVP: Plattform + VLAN-Modul mit Switch-Simulator und serverseitig bewertetem Quiz.

## Backend

    cd backend
    python -m venv .venv && .venv/Scripts/activate
    pip install -r requirements.txt
    cp .env.example .env   # SECRET_KEY + ADMIN_PASSWORD setzen
    uvicorn app.main:app --reload   # http://localhost:8000

## Frontend

    cd frontend
    npm install
    npm run dev   # http://localhost:5173

## Nutzung

1. Trainer: `/trainer` → Login (ADMIN_EMAIL/PASSWORD) → Kurs anlegen → Code merken.
2. Teilnehmer: `/` → Kurs-Code + Name → Modul „VLANs" → Theorie + Switch-Simulator + Quiz.
3. Trainer-Dashboard zeigt Fortschritt + besten Quiz-Score je Teilnehmer.

## Tests

    cd backend && pytest

## Weitere Module andocken

Backend: `ModuleDef` in `app/content/` ergänzen + in `registry.MODULES` registrieren.
Frontend: optionales Widget unter `src/widgets/` + in `widgets/registry.tsx` eintragen.
```

- [ ] **Step 3: Backend-Tests komplett**

```bash
cd backend && .venv/Scripts/python -m pytest -q
```
Expected: alle grün.

- [ ] **Step 4: Frontend-Build**

```bash
cd frontend && npx tsc -b && npm run build
```
Expected: Build ok.

- [ ] **Step 5: Manueller End-to-End-Smoke (lokal)**

Backend (`uvicorn`, mit gesetztem `SECRET_KEY`+`ADMIN_PASSWORD`) + Frontend (`npm run dev`) starten:
Trainer-Login → Kurs anlegen → Code → als Teilnehmer beitreten → VLAN-Modul: Switch-Simulator „Frame senden" hebt gleiche VLAN-Ports hervor, Trunk zeigt Tag → Quiz bestehen → Dashboard zeigt ✓ + Score.

- [ ] **Step 6: Commit**

```bash
git add README.md backend/.env.example
git commit -m "docs: README + .env.example"
```
