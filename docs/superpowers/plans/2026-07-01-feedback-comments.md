# Feedback-Kommentare pro Textabschnitt — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Kurs-Teilnehmer und Trainer können pro Text-Block eines Moduls Kommentare hinterlassen; alle im Kurs sehen sie inline, der Trainer moderiert je Kurs, und das ganze Feature ist per Laufzeit-Schalter abschaltbar.

**Architecture:** Neue DB-Tabellen `comment` (pro Kurs, an module_key+block_index) und `setting` (Feature-Flag). Getrennte Router für Teilnehmer- und Trainer-Kommentare plus ein Feature-Status/Toggle-Router. Frontend hängt eine Kommentar-Komponente unter Text-Blöcke (Teilnehmer) und bietet eine Feedback-Sammelansicht + Schalter (Trainer); ein pures Gruppierungs-/Snippet-Modul wird vitest-getestet.

**Tech Stack:** FastAPI + SQLAlchemy (Mapped/mapped_column), pytest; React 19 + TS + react-query + react-router, vitest.

## Global Constraints

- Kommentare sind **pro Kurs**; Teilnehmer-`course_id` kommt aus dem JWT, **nie** aus dem Request-Body.
- Löschen: Teilnehmer nur eigene (`participant_id`), Trainer jeden.
- Feature-Flag global in `setting`-Zeile `comments_enabled` (Default `True`); ist es aus, liefern **alle** Kommentar-Endpoints (lesen und schreiben) `403`.
- Kommentare nur an **Text**-Blöcken.
- Backend-Tests via venv: `./.venv/Scripts/python.exe -m pytest -q` (aus `backend/`). Frontend: `npm run test`, `npx tsc --noEmit`, `npm run build` (aus `frontend/`).
- API-Client-Prefix `/api`; Router-Pfade ohne `/api`.
- Deutsche Anführungszeichen typografisch, nie straight `"`. Frontend-Casing: Komponentendatei nicht namensgleich zu einer `.ts` daneben.

---

## File Structure

- `backend/app/models/setting.py` (CREATE) — Key/Value-Setting.
- `backend/app/models/comment.py` (CREATE) — Kommentar-Tabelle.
- `backend/app/services/features.py` (CREATE) — Flag lesen/setzen.
- `backend/app/routers/features.py` (CREATE) — `GET /features`, `PUT /trainer/features`.
- `backend/app/routers/comments.py` (CREATE) — Teilnehmer-Kommentare.
- `backend/app/routers/trainer_comments.py` (CREATE) — Trainer-Kommentare.
- `backend/app/main.py` (MODIFY) — Modelle importieren + Router einhängen.
- `backend/tests/test_features.py`, `test_comments.py`, `test_trainer_comments.py` (CREATE).
- `frontend/src/components/commentGroups.ts` (CREATE) — pure Gruppierung + Snippet.
- `frontend/src/components/commentGroups.test.ts` (CREATE).
- `frontend/src/lib/learnApi.ts` (MODIFY) — features/comments-Methoden.
- `frontend/src/lib/trainerApi.ts` (MODIFY) — features/trainer-comments-Methoden.
- `frontend/src/components/Blocks.tsx` (MODIFY) — optionales `footer`-Render pro Block.
- `frontend/src/components/BlockComments.tsx` (CREATE) — Teilnehmer-Kommentar-UI.
- `frontend/src/pages/ModulePage.tsx` (MODIFY) — Kommentare unter Text-Blöcke (feature-gated).
- `frontend/src/components/TrainerFeedback.tsx` (CREATE) — Trainer-Sammelansicht.
- `frontend/src/pages/TrainerPage.tsx` (MODIFY) — Feature-Schalter + Feedback pro Kurs.
- `backend/app/content/changelog.py` (MODIFY) — Eintrag.

---

### Task 1: Feature-Flag (Setting-Modell, Service, Router)

**Files:**
- Create: `backend/app/models/setting.py`, `backend/app/services/features.py`, `backend/app/routers/features.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_features.py`

**Interfaces:**
- Produces: `comments_enabled(db) -> bool`, `set_comments_enabled(db, value: bool) -> None`; `GET /features → {"comments": bool}`, `PUT /trainer/features {"comments": bool}`.

- [ ] **Step 1: Failing-Test schreiben**

`backend/tests/test_features.py`:

```python
from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_features_default_on_and_toggle():
    with TestClient(app) as c:
        assert c.get("/api/features").json() == {"comments": True}
        h = _trainer(c)
        assert c.put("/api/trainer/features", json={"comments": False}, headers=h).json() == {"comments": False}
        assert c.get("/api/features").json() == {"comments": False}
        c.put("/api/trainer/features", json={"comments": True}, headers=h)


def test_toggle_requires_trainer():
    with TestClient(app) as c:
        assert c.put("/api/trainer/features", json={"comments": False}).status_code in (401, 403)
```

- [ ] **Step 2: Test ausführen, Fehlschlag prüfen**

Run: `./.venv/Scripts/python.exe -m pytest tests/test_features.py -q`
Expected: FAIL (404 auf /api/features).

- [ ] **Step 3: Setting-Modell erstellen**

`backend/app/models/setting.py`:

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Setting(Base):
    __tablename__ = "setting"
    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[str] = mapped_column(String, nullable=False)
```

- [ ] **Step 4: Features-Service erstellen**

`backend/app/services/features.py`:

```python
from app.models.setting import Setting


def comments_enabled(db) -> bool:
    row = db.query(Setting).filter(Setting.key == "comments_enabled").first()
    return row.value == "1" if row else True


def set_comments_enabled(db, value: bool) -> None:
    row = db.query(Setting).filter(Setting.key == "comments_enabled").first()
    if row:
        row.value = "1" if value else "0"
    else:
        db.add(Setting(key="comments_enabled", value="1" if value else "0"))
    db.commit()
```

- [ ] **Step 5: Features-Router erstellen**

`backend/app/routers/features.py`:

```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.deps import get_trainer
from app.services.features import comments_enabled, set_comments_enabled

router = APIRouter(tags=["features"])


@router.get("/features")
def get_features(db: Session = Depends(get_db)):
    return {"comments": comments_enabled(db)}


class FeatureReq(BaseModel):
    comments: bool


@router.put("/trainer/features")
def put_features(data: FeatureReq, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    set_comments_enabled(db, data.comments)
    return {"comments": comments_enabled(db)}
```

- [ ] **Step 6: Modell + Router in main.py einhängen**

In `backend/app/main.py` nach `from app.models import module_disabled as _module_disabled  # noqa: F401` einfügen:

```python
from app.models import setting as _setting  # noqa: F401
```

Nach `from app.routers import changelog as changelog_router  # noqa: E402` (bzw. der letzten Router-Import-Zeile) einfügen:

```python
from app.routers import features as features_router  # noqa: E402
```

und nach der letzten `_api.include_router(...)`-Zeile:

```python
_api.include_router(features_router.router)
```

- [ ] **Step 7: Tests grün**

Run: `./.venv/Scripts/python.exe -m pytest -q`
Expected: PASS (alle).

- [ ] **Step 8: Commit**

```bash
git add backend/app/models/setting.py backend/app/services/features.py backend/app/routers/features.py backend/app/main.py backend/tests/test_features.py
git commit -m "feat(feedback): Feature-Flag comments_enabled + Trainer-Toggle"
```

---

### Task 2: Teilnehmer-Kommentare (Modell + Router)

**Files:**
- Create: `backend/app/models/comment.py`, `backend/app/routers/comments.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_comments.py`

**Interfaces:**
- Consumes: `comments_enabled` (Task 1), `get_participant`.
- Produces: `Comment`-Modell; `GET/POST /modules/{key}/comments`, `DELETE /comments/{cid}`. Serialisiertes Kommentar-Dict: `{id, block_index, body, author_kind, author_name, created_at, own}`.

- [ ] **Step 1: Failing-Test schreiben**

`backend/tests/test_comments.py`:

```python
from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _course(c, h, name):
    return c.post("/api/courses", json={"name": name}, headers=h).json()["join_code"]


def _join(c, code, name):
    return {"Authorization": "Bearer " + c.post(
        "/api/join", json={"code": code, "name": name}).json()["access_token"]}


def test_participant_comment_flow():
    with TestClient(app) as c:
        h = _trainer(c)
        code_a = _course(c, h, "KursA")
        code_b = _course(c, h, "KursB")
        a1 = _join(c, code_a, "A1")
        a2 = _join(c, code_a, "A2")
        b1 = _join(c, code_b, "B1")

        r = c.post("/api/modules/switching/comments",
                   json={"block_index": 0, "body": "Guter Abschnitt"}, headers=a1)
        assert r.status_code == 200
        cid = r.json()["id"]

        # A1 sieht ihn als own, A2 (gleicher Kurs) als nicht-own
        assert c.get("/api/modules/switching/comments", headers=a1).json()[0]["own"] is True
        assert c.get("/api/modules/switching/comments", headers=a2).json()[0]["own"] is False
        # B1 (anderer Kurs) sieht ihn nicht
        assert c.get("/api/modules/switching/comments", headers=b1).json() == []

        # leerer Body -> 400
        assert c.post("/api/modules/switching/comments",
                      json={"block_index": 0, "body": "   "}, headers=a1).status_code == 400
        # A2 darf A1s Kommentar nicht löschen, A1 schon
        assert c.delete(f"/api/comments/{cid}", headers=a2).status_code == 403
        assert c.delete(f"/api/comments/{cid}", headers=a1).status_code == 200
        assert c.delete(f"/api/comments/{cid}", headers=a1).status_code == 404


def test_comments_gated_by_feature():
    with TestClient(app) as c:
        h = _trainer(c)
        code = _course(c, h, "KursGate")
        p = _join(c, code, "P1")
        c.put("/api/trainer/features", json={"comments": False}, headers=h)
        assert c.get("/api/modules/switching/comments", headers=p).status_code == 403
        assert c.post("/api/modules/switching/comments",
                      json={"block_index": 0, "body": "x"}, headers=p).status_code == 403
        c.put("/api/trainer/features", json={"comments": True}, headers=h)
```

- [ ] **Step 2: Test ausführen, Fehlschlag prüfen**

Run: `./.venv/Scripts/python.exe -m pytest tests/test_comments.py -q`
Expected: FAIL (404 auf Kommentar-Pfaden).

- [ ] **Step 3: Comment-Modell erstellen**

`backend/app/models/comment.py`:

```python
from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils import utc_now


class Comment(Base):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    module_key: Mapped[str] = mapped_column(String, index=True, nullable=False)
    block_index: Mapped[int] = mapped_column(Integer, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_kind: Mapped[str] = mapped_column(String, nullable=False)
    author_name: Mapped[str] = mapped_column(String, nullable=False)
    participant_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
```

- [ ] **Step 4: Teilnehmer-Router erstellen**

`backend/app/routers/comments.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.comment import Comment
from app.models.participant import Participant
from app.services.deps import get_participant
from app.services.features import comments_enabled

router = APIRouter(tags=["comments"])


def _guard(db: Session) -> None:
    if not comments_enabled(db):
        raise HTTPException(status_code=403, detail="Feedback ist deaktiviert")


def _serialize(c: Comment, own: bool) -> dict:
    return {"id": c.id, "block_index": c.block_index, "body": c.body,
            "author_kind": c.author_kind, "author_name": c.author_name,
            "created_at": c.created_at.isoformat(), "own": own}


class CommentReq(BaseModel):
    block_index: int
    body: str


@router.get("/modules/{key}/comments")
def list_comments(key: str, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    _guard(db)
    rows = db.query(Comment).filter(
        Comment.course_id == p.course_id, Comment.module_key == key
    ).order_by(Comment.created_at).all()
    return [_serialize(c, c.author_kind == "participant" and c.participant_id == p.id) for c in rows]


@router.post("/modules/{key}/comments")
def add_comment(key: str, data: CommentReq, db: Session = Depends(get_db),
                p: Participant = Depends(get_participant)):
    _guard(db)
    body = data.body.strip()
    if not body:
        raise HTTPException(status_code=400, detail="Kommentar ist leer")
    c = Comment(course_id=p.course_id, module_key=key, block_index=data.block_index,
                body=body, author_kind="participant", author_name=p.name, participant_id=p.id)
    db.add(c)
    db.commit()
    db.refresh(c)
    return _serialize(c, True)


@router.delete("/comments/{cid}")
def delete_comment(cid: int, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    _guard(db)
    c = db.query(Comment).filter(Comment.id == cid).first()
    if not c:
        raise HTTPException(status_code=404, detail="Kommentar nicht gefunden")
    if not (c.author_kind == "participant" and c.participant_id == p.id):
        raise HTTPException(status_code=403, detail="Nicht erlaubt")
    db.delete(c)
    db.commit()
    return {"ok": True}
```

- [ ] **Step 5: Modell + Router in main.py einhängen**

In `backend/app/main.py` nach der `setting`-Import-Zeile einfügen:

```python
from app.models import comment as _comment  # noqa: F401
```

Nach der `features`-Router-Import-Zeile:

```python
from app.routers import comments as comments_router  # noqa: E402
```

und nach `_api.include_router(features_router.router)`:

```python
_api.include_router(comments_router.router)
```

- [ ] **Step 6: Tests grün**

Run: `./.venv/Scripts/python.exe -m pytest -q`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add backend/app/models/comment.py backend/app/routers/comments.py backend/app/main.py backend/tests/test_comments.py
git commit -m "feat(feedback): Teilnehmer-Kommentare pro Block (kursgescoped)"
```

---

### Task 3: Trainer-Kommentare (Router)

**Files:**
- Create: `backend/app/routers/trainer_comments.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_trainer_comments.py`

**Interfaces:**
- Consumes: `Comment` (Task 2), `comments_enabled`, `get_trainer`.
- Produces: `GET /trainer/courses/{cid}/comments`, `POST /trainer/courses/{cid}/modules/{key}/comments`, `DELETE /trainer/comments/{cid}`. Serialisiertes Dict wie Teilnehmer, zusätzlich `module_key`.

- [ ] **Step 1: Failing-Test schreiben**

`backend/tests/test_trainer_comments.py`:

```python
from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _join(c, code, name):
    return {"Authorization": "Bearer " + c.post(
        "/api/join", json={"code": code, "name": name}).json()["access_token"]}


def test_trainer_comment_flow():
    with TestClient(app) as c:
        h = _trainer(c)
        course = c.post("/api/courses", json={"name": "KursT"}, headers=h).json()
        cid = c.get("/api/courses", headers=h).json()
        cid = next(x["id"] for x in cid if x["join_code"] == course["join_code"])
        p = _join(c, course["join_code"], "P1")

        # Teilnehmer-Kommentar
        c.post("/api/modules/vlan/comments", json={"block_index": 1, "body": "Frage dazu"}, headers=p)
        # Trainer-Kommentar
        r = c.post(f"/api/trainer/courses/{cid}/modules/vlan/comments",
                   json={"block_index": 1, "body": "Antwort vom Trainer"}, headers=h)
        assert r.status_code == 200 and r.json()["author_kind"] == "trainer"
        tid = r.json()["id"]

        allc = c.get(f"/api/trainer/courses/{cid}/comments", headers=h).json()
        assert len(allc) == 2
        assert all("module_key" in x for x in allc)

        # Trainer löscht den Teilnehmer-Kommentar (Moderation)
        part_id = next(x["id"] for x in allc if x["author_kind"] == "participant")
        assert c.delete(f"/api/trainer/comments/{part_id}", headers=h).status_code == 200
        assert c.delete(f"/api/trainer/comments/{tid}", headers=h).status_code == 200
        assert c.delete(f"/api/trainer/comments/{tid}", headers=h).status_code == 404
```

- [ ] **Step 2: Test ausführen, Fehlschlag prüfen**

Run: `./.venv/Scripts/python.exe -m pytest tests/test_trainer_comments.py -q`
Expected: FAIL (404 auf Trainer-Kommentar-Pfaden).

- [ ] **Step 3: Trainer-Router erstellen**

`backend/app/routers/trainer_comments.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.comment import Comment
from app.services.deps import get_trainer
from app.services.features import comments_enabled

router = APIRouter(tags=["trainer-comments"])


def _guard(db: Session) -> None:
    if not comments_enabled(db):
        raise HTTPException(status_code=403, detail="Feedback ist deaktiviert")


def _serialize(c: Comment) -> dict:
    return {"id": c.id, "module_key": c.module_key, "block_index": c.block_index,
            "body": c.body, "author_kind": c.author_kind, "author_name": c.author_name,
            "created_at": c.created_at.isoformat(), "own": c.author_kind == "trainer"}


class TComReq(BaseModel):
    block_index: int
    body: str


@router.get("/trainer/courses/{cid}/comments")
def course_comments(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    _guard(db)
    rows = db.query(Comment).filter(Comment.course_id == cid).order_by(
        Comment.module_key, Comment.block_index, Comment.created_at).all()
    return [_serialize(c) for c in rows]


@router.post("/trainer/courses/{cid}/modules/{key}/comments")
def add_trainer_comment(cid: int, key: str, data: TComReq, db: Session = Depends(get_db),
                        _t: dict = Depends(get_trainer)):
    _guard(db)
    body = data.body.strip()
    if not body:
        raise HTTPException(status_code=400, detail="Kommentar ist leer")
    c = Comment(course_id=cid, module_key=key, block_index=data.block_index,
                body=body, author_kind="trainer", author_name="Trainer", participant_id=None)
    db.add(c)
    db.commit()
    db.refresh(c)
    return _serialize(c)


@router.delete("/trainer/comments/{cid}")
def delete_trainer_comment(cid: int, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    _guard(db)
    c = db.query(Comment).filter(Comment.id == cid).first()
    if not c:
        raise HTTPException(status_code=404, detail="Kommentar nicht gefunden")
    db.delete(c)
    db.commit()
    return {"ok": True}
```

- [ ] **Step 4: Router in main.py einhängen**

In `backend/app/main.py` nach der `comments`-Router-Import-Zeile:

```python
from app.routers import trainer_comments as trainer_comments_router  # noqa: E402
```

und nach `_api.include_router(comments_router.router)`:

```python
_api.include_router(trainer_comments_router.router)
```

- [ ] **Step 5: Tests grün**

Run: `./.venv/Scripts/python.exe -m pytest -q`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add backend/app/routers/trainer_comments.py backend/app/main.py backend/tests/test_trainer_comments.py
git commit -m "feat(feedback): Trainer-Kommentare + Moderation je Kurs"
```

---

### Task 4: Pure Frontend-Logik (Gruppierung + Snippet)

**Files:**
- Create: `frontend/src/components/commentGroups.ts`, `frontend/src/components/commentGroups.test.ts`

**Interfaces:**
- Produces: Typ `TrainerComment`; `groupByModuleBlock(comments) -> CommentGroup[]`; `blockSnippet(block, maxLen?) -> string`.

- [ ] **Step 1: Failing-Test schreiben**

`frontend/src/components/commentGroups.test.ts`:

```ts
import { describe, it, expect } from 'vitest'
import { groupByModuleBlock, blockSnippet, type TrainerComment } from './commentGroups'
import type { Block } from '@/types'

const mk = (id: number, module_key: string, block_index: number): TrainerComment => ({
  id, module_key, block_index, body: 'x', author_kind: 'participant', author_name: 'A',
  created_at: '2026-07-01T10:00:00', own: false,
})

describe('groupByModuleBlock', () => {
  it('gruppiert nach Modul + Block', () => {
    const g = groupByModuleBlock([mk(1, 'vlan', 0), mk(2, 'vlan', 0), mk(3, 'vlan', 2)])
    expect(g).toHaveLength(2)
    expect(g[0]).toMatchObject({ moduleKey: 'vlan', blockIndex: 0 })
    expect(g[0].items).toHaveLength(2)
    expect(g[1].blockIndex).toBe(2)
  })
})

describe('blockSnippet', () => {
  it('kürzt Text-Blöcke und entfernt Markdown-Zeichen', () => {
    const b: Block = { type: 'text', value: '## Titel\n\nEin **langer** Satz zum Thema Netzwerk und Switching hier.' }
    const s = blockSnippet(b, 20)
    expect(s.length).toBeLessThanOrEqual(21)
    expect(s).not.toContain('#')
    expect(s.endsWith('…')).toBe(true)
  })
  it('leer für Nicht-Text-Blöcke', () => {
    expect(blockSnippet({ type: 'widget', id: 'x' })).toBe('')
    expect(blockSnippet(undefined)).toBe('')
  })
})
```

- [ ] **Step 2: Test ausführen, Fehlschlag prüfen**

Run (aus `frontend/`): `npm run test`
Expected: FAIL (Modul fehlt).

- [ ] **Step 3: Implementieren**

`frontend/src/components/commentGroups.ts`:

```ts
import type { Block } from '@/types'

export interface TrainerComment {
  id: number
  module_key: string
  block_index: number
  body: string
  author_kind: string
  author_name: string
  created_at: string
  own: boolean
}

export interface CommentGroup {
  moduleKey: string
  blockIndex: number
  items: TrainerComment[]
}

export function groupByModuleBlock(comments: TrainerComment[]): CommentGroup[] {
  const map = new Map<string, CommentGroup>()
  for (const c of comments) {
    const k = `${c.module_key}#${c.block_index}`
    let g = map.get(k)
    if (!g) {
      g = { moduleKey: c.module_key, blockIndex: c.block_index, items: [] }
      map.set(k, g)
    }
    g.items.push(c)
  }
  return [...map.values()]
}

export function blockSnippet(block: Block | undefined, maxLen = 60): string {
  if (!block || block.type !== 'text') return ''
  const text = block.value.replace(/[#*`]/g, ' ').replace(/\s+/g, ' ').trim()
  return text.length > maxLen ? text.slice(0, maxLen) + '…' : text
}
```

- [ ] **Step 4: Test grün**

Run (aus `frontend/`): `npm run test`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/commentGroups.ts frontend/src/components/commentGroups.test.ts
git commit -m "feat(feedback): pure Kommentar-Gruppierung + Block-Snippet"
```

---

### Task 5: Teilnehmer-UI (API, Blocks-Footer, BlockComments, ModulePage)

**Files:**
- Modify: `frontend/src/lib/learnApi.ts`, `frontend/src/components/Blocks.tsx`, `frontend/src/pages/ModulePage.tsx`
- Create: `frontend/src/components/BlockComments.tsx`

**Interfaces:**
- Consumes: react-query, `learnApi`.
- Produces: `learnApi.features/listComments/addComment/deleteComment`; `<Blocks footer>`; `<BlockComments moduleKey blockIndex>`.

- [ ] **Step 1: learnApi erweitern**

In `frontend/src/lib/learnApi.ts` innerhalb des `learnApi`-Objekts (nach `submitQuiz`) ergänzen und den `Comment`-Typ am Dateiende hinzufügen:

```ts
  features: () => api.get<{ comments: boolean }>('/features'),
  listComments: (key: string) => api.get<Comment[]>(`/modules/${key}/comments`),
  addComment: (key: string, block_index: number, body: string) =>
    api.post<Comment>(`/modules/${key}/comments`, { block_index, body }),
  deleteComment: (id: number) => api.delete(`/comments/${id}`),
```

Am Dateiende:

```ts
export interface Comment {
  id: number
  block_index: number
  body: string
  author_kind: string
  author_name: string
  created_at: string
  own: boolean
}
```

- [ ] **Step 2: Blocks um optionales footer-Render erweitern**

`frontend/src/components/Blocks.tsx` — Import-Kopf und Signatur/Body ersetzen (MD_COMPONENTS bleibt unverändert):

```tsx
import type { ReactNode } from 'react'
import Markdown from 'react-markdown'
import type { Block } from '@/types'
import { WIDGETS } from '@/widgets/registry'

// ... MD_COMPONENTS unverändert ...

export function Blocks({
  blocks,
  footer,
}: {
  blocks: Block[]
  footer?: (block: Block, index: number) => ReactNode
}) {
  return (
    <div className="flex flex-col gap-6">
      {blocks.map((b, i) => (
        <div key={i} className="flex flex-col gap-1">
          {b.type === 'text' && <Markdown components={MD_COMPONENTS}>{b.value}</Markdown>}
          {b.type === 'image' && <img src={b.url} alt={b.alt ?? ''} className="rounded-lg border" />}
          {b.type === 'widget' &&
            (WIDGETS[b.id] ? (
              (() => {
                const W = WIDGETS[b.id]
                return <W />
              })()
            ) : (
              <div className="text-sm text-red-500">Unbekanntes Widget: {b.id}</div>
            ))}
          {footer?.(b, i)}
        </div>
      ))}
    </div>
  )
}
```

- [ ] **Step 3: BlockComments-Komponente erstellen**

`frontend/src/components/BlockComments.tsx`:

```tsx
import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { learnApi } from '@/lib/learnApi'

export function BlockComments({ moduleKey, blockIndex }: { moduleKey: string; blockIndex: number }) {
  const qc = useQueryClient()
  const [open, setOpen] = useState(false)
  const [text, setText] = useState('')

  const comments = useQuery({
    queryKey: ['comments', moduleKey],
    queryFn: () => learnApi.listComments(moduleKey).then((r) => r.data),
  })
  const add = useMutation({
    mutationFn: () => learnApi.addComment(moduleKey, blockIndex, text),
    onSuccess: () => {
      setText('')
      qc.invalidateQueries({ queryKey: ['comments', moduleKey] })
    },
  })
  const del = useMutation({
    mutationFn: (id: number) => learnApi.deleteComment(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['comments', moduleKey] }),
  })

  const items = (comments.data ?? []).filter((c) => c.block_index === blockIndex)

  return (
    <div className="mt-1">
      <button
        onClick={() => setOpen((o) => !o)}
        className="text-xs font-medium text-teal-700 hover:text-teal-800"
      >
        {open ? '▾' : '▸'} 💬 Kommentare ({items.length})
      </button>
      {open && (
        <div className="mt-2 rounded-lg border bg-slate-50 p-3">
          <div className="flex flex-col gap-2 mb-2">
            {items.length === 0 && <p className="text-xs text-slate-400">Noch keine Kommentare.</p>}
            {items.map((c) => (
              <div key={c.id} className="text-sm">
                <span className="font-medium text-slate-700">{c.author_name}</span>
                <span className="text-xs text-slate-400"> · {c.created_at.slice(0, 16).replace('T', ' ')}</span>
                {c.own && (
                  <button
                    onClick={() => del.mutate(c.id)}
                    className="ml-2 text-xs text-rose-600 hover:text-rose-700"
                  >
                    löschen
                  </button>
                )}
                <p className="text-slate-700">{c.body}</p>
              </div>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Kommentar…"
              className="flex-1 border rounded-lg px-2 py-1 text-sm"
            />
            <button
              onClick={() => text.trim() && add.mutate()}
              disabled={add.isPending}
              className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 text-sm font-medium disabled:opacity-60"
            >
              Senden
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 4: ModulePage einbinden (feature-gated)**

`frontend/src/pages/ModulePage.tsx` vollständig ersetzen durch:

```tsx
import { useQuery } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, useParams } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { Blocks } from '@/components/Blocks'
import { BlockComments } from '@/components/BlockComments'
import { Quiz } from '@/components/Quiz'

export function ModulePage() {
  const { key = '' } = useParams()
  const mod = useQuery({ queryKey: ['module', key], queryFn: () => learnApi.getModule(key).then((r) => r.data) })
  const features = useQuery({ queryKey: ['features'], queryFn: () => learnApi.features().then((r) => r.data) })

  if (mod.isLoading || !mod.data) return <div className="p-10">Lädt…</div>

  const commentsOn = features.data?.comments ?? false

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <Link to="/lernen" className="text-sm text-slate-400 hover:text-slate-600">← Module</Link>
        <h1 className="text-2xl font-bold text-slate-900 mt-2 mb-4">{mod.data.title}</h1>
        {mod.data.scenario && (
          <div className="rounded-xl border-l-4 border-teal-400 bg-teal-50 px-4 py-3 mb-6 text-sm text-slate-700">
            <Markdown>{mod.data.scenario}</Markdown>
          </div>
        )}
        <Blocks
          blocks={mod.data.blocks}
          footer={
            commentsOn
              ? (b, i) => (b.type === 'text' ? <BlockComments moduleKey={key} blockIndex={i} /> : null)
              : undefined
          }
        />
        <Quiz moduleKey={key} questions={mod.data.quiz.questions} />
      </div>
    </div>
  )
}
```

- [ ] **Step 5: Typecheck + Build**

Run (aus `frontend/`): `npx tsc --noEmit && npm run build`
Expected: kein Fehler, Build erfolgreich.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/lib/learnApi.ts frontend/src/components/Blocks.tsx frontend/src/components/BlockComments.tsx frontend/src/pages/ModulePage.tsx
git commit -m "feat(feedback): Teilnehmer-Kommentare inline unter Text-Blöcken"
```

---

### Task 6: Trainer-UI (API, Feedback-Ansicht, Schalter)

**Files:**
- Modify: `frontend/src/lib/trainerApi.ts`, `frontend/src/pages/TrainerPage.tsx`
- Create: `frontend/src/components/TrainerFeedback.tsx`

**Interfaces:**
- Consumes: `trainerApi`, `groupByModuleBlock`, `blockSnippet`, `TrainerComment` (Task 4).
- Produces: `trainerApi.features/setFeature/courseComments/addTrainerComment/deleteTrainerComment`; `<TrainerFeedback courseId>`.

- [ ] **Step 1: trainerApi erweitern**

In `frontend/src/lib/trainerApi.ts` den Import-Kopf ergänzen:

```ts
import type { TrainerComment } from '@/components/commentGroups'
```

Innerhalb des `trainerApi`-Objekts (nach `trainerModule`) ergänzen:

```ts
  features: () => api.get<{ comments: boolean }>('/features'),
  setFeature: (comments: boolean) => api.put<{ comments: boolean }>('/trainer/features', { comments }),
  courseComments: (cid: number) => api.get<TrainerComment[]>(`/trainer/courses/${cid}/comments`),
  addTrainerComment: (cid: number, key: string, block_index: number, body: string) =>
    api.post(`/trainer/courses/${cid}/modules/${key}/comments`, { block_index, body }),
  deleteTrainerComment: (id: number) => api.delete(`/trainer/comments/${id}`),
```

- [ ] **Step 2: TrainerFeedback-Komponente erstellen**

`frontend/src/components/TrainerFeedback.tsx`:

```tsx
import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { trainerApi } from '@/lib/trainerApi'
import { groupByModuleBlock, blockSnippet, type TrainerComment } from '@/components/commentGroups'

export function TrainerFeedback({ courseId }: { courseId: number }) {
  const comments = useQuery({
    queryKey: ['course-comments', courseId],
    queryFn: () => trainerApi.courseComments(courseId).then((r) => r.data),
  })

  const byModule = new Map<string, TrainerComment[]>()
  for (const c of comments.data ?? []) {
    const list = byModule.get(c.module_key) ?? []
    list.push(c)
    byModule.set(c.module_key, list)
  }

  if (!comments.data) return null
  if (comments.data.length === 0)
    return <p className="text-sm text-slate-400">Noch kein Feedback in diesem Kurs.</p>

  return (
    <div className="flex flex-col gap-4">
      {[...byModule.keys()].map((key) => (
        <FeedbackModule key={key} courseId={courseId} moduleKey={key} comments={byModule.get(key)!} />
      ))}
    </div>
  )
}

function FeedbackModule({
  courseId,
  moduleKey,
  comments,
}: {
  courseId: number
  moduleKey: string
  comments: TrainerComment[]
}) {
  const qc = useQueryClient()
  const mod = useQuery({
    queryKey: ['trainer-module', moduleKey],
    queryFn: () => trainerApi.trainerModule(moduleKey).then((r) => r.data),
  })
  const [drafts, setDrafts] = useState<Record<number, string>>({})

  const add = useMutation({
    mutationFn: (v: { blockIndex: number; body: string }) =>
      trainerApi.addTrainerComment(courseId, moduleKey, v.blockIndex, v.body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['course-comments', courseId] }),
  })
  const del = useMutation({
    mutationFn: (id: number) => trainerApi.deleteTrainerComment(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['course-comments', courseId] }),
  })

  const groups = groupByModuleBlock(comments)

  return (
    <div className="rounded-xl border bg-white p-4">
      <h4 className="text-sm font-semibold text-slate-800 mb-2">{mod.data?.title ?? moduleKey}</h4>
      <div className="flex flex-col gap-3">
        {groups.map((g) => {
          const snippet = blockSnippet(mod.data?.blocks[g.blockIndex])
          return (
            <div key={g.blockIndex} className="border-t pt-2">
              <p className="text-xs text-slate-400">
                Block {g.blockIndex + 1}
                {snippet && <span> · „{snippet}"</span>}
              </p>
              {g.items.map((c) => (
                <div key={c.id} className="text-sm mt-1">
                  <span className="font-medium text-slate-700">{c.author_name}</span>
                  <button
                    onClick={() => del.mutate(c.id)}
                    className="ml-2 text-xs text-rose-600 hover:text-rose-700"
                  >
                    löschen
                  </button>
                  <p className="text-slate-700">{c.body}</p>
                </div>
              ))}
              <div className="flex gap-2 mt-2">
                <input
                  value={drafts[g.blockIndex] ?? ''}
                  onChange={(e) => setDrafts((d) => ({ ...d, [g.blockIndex]: e.target.value }))}
                  placeholder="Antwort…"
                  className="flex-1 border rounded-lg px-2 py-1 text-sm"
                />
                <button
                  onClick={() => {
                    const body = (drafts[g.blockIndex] ?? '').trim()
                    if (body) {
                      add.mutate({ blockIndex: g.blockIndex, body })
                      setDrafts((d) => ({ ...d, [g.blockIndex]: '' }))
                    }
                  }}
                  className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 text-sm font-medium"
                >
                  Antworten
                </button>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
```

- [ ] **Step 3: TrainerPage — Schalter + Feedback einbinden**

In `frontend/src/pages/TrainerPage.tsx` den Import ergänzen:

```tsx
import { TrainerFeedback } from '@/components/TrainerFeedback'
```

In `TrainerDashboard` nach der `presentMods`-Query-Zeile einfügen:

```tsx
  const features = useQuery({ queryKey: ['features'], queryFn: () => trainerApi.features().then((r) => r.data) })
  const toggleFeature = useMutation({
    mutationFn: (v: boolean) => trainerApi.setFeature(v),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['features'] }),
  })
```

Im JSX unmittelbar vor `{presentMods.data && (` einfügen:

```tsx
        {features.data && (
          <label className="flex items-center gap-2 text-sm text-slate-700 mb-6">
            <input
              type="checkbox"
              checked={features.data.comments}
              disabled={toggleFeature.isPending}
              onChange={(e) => toggleFeature.mutate(e.target.checked)}
            />
            Feedback-Kommentare aktiv
          </label>
        )}
```

Im JSX direkt nach dem `{courseMods.data && ( … )}`-Block (Modul-Aktivierung) einfügen:

```tsx
        {selected !== null && features.data?.comments && (
          <div className="rounded-xl border bg-white p-4 mb-6">
            <h3 className="text-sm font-semibold text-slate-700 mb-3">Feedback</h3>
            <TrainerFeedback courseId={selected} />
          </div>
        )}
```

- [ ] **Step 4: Typecheck + Build**

Run (aus `frontend/`): `npx tsc --noEmit && npm run build`
Expected: kein Fehler, Build erfolgreich.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/lib/trainerApi.ts frontend/src/components/TrainerFeedback.tsx frontend/src/pages/TrainerPage.tsx
git commit -m "feat(feedback): Trainer-Feedbackansicht + Feature-Schalter"
```

---

### Task 7: Changelog + Gesamt-Verifikation

**Files:**
- Modify: `backend/app/content/changelog.py`

- [ ] **Step 1: Changelog-Eintrag ergänzen**

In `backend/app/content/changelog.py` als **ersten** Eintrag nach `CHANGELOG = [` einfügen:

```python
    {"date": "2026-07-01", "title": "Feedback-Kommentare",
     "text": "Teilnehmer und Trainer können pro Textabschnitt Kommentare "
             "hinterlassen (kursweit sichtbar); der Trainer moderiert je Kurs und "
             "kann das Feature per Schalter an- und ausschalten."},
```

- [ ] **Step 2: Gesamt-Verifikation Backend**

Run (aus `backend/`): `./.venv/Scripts/python.exe -m pytest -q`
Expected: alle Tests PASS.

- [ ] **Step 3: Gesamt-Verifikation Frontend**

Run (aus `frontend/`): `npm run test && npx tsc --noEmit && npm run build`
Expected: Tests PASS, kein tsc-Fehler, Build erfolgreich.

- [ ] **Step 4: Commit**

```bash
git add backend/app/content/changelog.py
git commit -m "docs(changelog): Feedback-Kommentare"
```

---

## Self-Review-Notiz

- Spec-Abdeckung: Datenmodell (T1/T2), Endpoints Teilnehmer (T2) + Trainer (T3), Feature-Flag/Toggle (T1) + Gate in allen Kommentar-Routen (T2/T3), Teilnehmer-UI (T5), Trainer-UI + Schalter (T6), pure Gruppierung/Snippet + Tests (T4), Changelog (T7).
- Sicherheit: course_id aus JWT (T2), Löschrechte serverseitig (T2/T3), 403 bei deaktiviert inkl. Schreibzugriff (T2/T3-Tests).
- Typkonsistenz: `TrainerComment` (T4) von `trainerApi`/`TrainerFeedback` genutzt (T6); `Comment` (T5) von `BlockComments`; Serialisierungs-Felder identisch zwischen Backend (T2/T3) und Frontend-Typen.
- Casing: `commentGroups.ts`, `BlockComments.tsx`, `TrainerFeedback.tsx` — keine Namensgleichheit mit `.ts`/`.tsx`-Nachbarn.
