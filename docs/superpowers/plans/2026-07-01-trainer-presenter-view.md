# Trainer-Modulansicht mit Präsentationsnotizen — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Trainer bekommen pro Modul eine read-only Präsentationsansicht mit einklappbaren Block-Notizen, Kurzübersicht und sichtbaren Quiz-Lösungen.

**Architecture:** Content-Blöcke tragen optionales `note`, Module optionales `goals` (dev-authored). Ein neuer trainer-geschützter Endpoint liefert das volle Modul; der Teilnehmer-Endpoint strippt `note`/`answer`/`goals`. Frontend rendert die Trainer-Ansicht über eigene Komponenten, die die bestehende Markdown-/Widget-Darstellung teilen.

**Tech Stack:** FastAPI + SQLAlchemy (Backend), React 19 + TS + Vite + react-query + react-router (Frontend), pytest + vitest.

## Global Constraints

- Notizen und Quiz-Lösungen dürfen nur über den `get_trainer`-geschützten Endpoint erreichbar sein; `public_module` strippt `note`, `answer` und `goals`.
- Deutsche Anführungszeichen in Python-Content nur typografisch („…"), nie straight `"` (schließt den String).
- Frontend-Casing-Falle: Komponentendatei nicht namensgleich zu einer `.ts` daneben.
- Backend-Tests via venv: `./.venv/Scripts/python.exe -m pytest -q` (aus `backend/`).
- Frontend-Verifikation: `npm run test`, `npx tsc --noEmit`, `npm run build` (aus `frontend/`).
- API-Client hat Basis-Prefix `/api`; Router-Pfade daher ohne `/api` definieren.

---

## File Structure

- `backend/app/content/registry.py` (MODIFY) — `public_module` strippt zusätzlich note/goals; neue `trainer_module`.
- `backend/app/content/switching.py` (MODIFY) — Notizen + goals als Test-Fixture (Task 1).
- `backend/app/routers/trainer_modules.py` (CREATE) — trainer-geschützte Endpoints.
- `backend/app/main.py` (MODIFY) — Router einhängen.
- `backend/tests/test_content.py` (MODIFY) — Strip-/Trainer-Tests.
- `backend/tests/test_trainer_modules.py` (CREATE) — Endpoint-/Auth-Tests.
- restliche `backend/app/content/*.py` (MODIFY, Task 3) — Notizen + goals.
- `frontend/src/types.ts` (MODIFY) — Block.note, Question.answer, TrainerModuleDetail.
- `frontend/src/lib/trainerApi.ts` (MODIFY) — trainerModules/trainerModule.
- `frontend/src/components/Blocks.tsx` (MODIFY) — `MD_COMPONENTS` exportieren.
- `frontend/src/components/trainerQuiz.ts` (CREATE) — pure `isCorrect`.
- `frontend/src/components/trainerQuiz.test.ts` (CREATE) — vitest.
- `frontend/src/components/TrainerBlocks.tsx` (CREATE) — Blöcke + einklappbare Notiz.
- `frontend/src/components/TrainerQuiz.tsx` (CREATE) — read-only Quiz mit Lösungen.
- `frontend/src/pages/TrainerModulePage.tsx` (CREATE) — Trainer-Modulseite.
- `frontend/src/App.tsx` (MODIFY) — Route `/trainer/modul/:key`.
- `frontend/src/pages/TrainerPage.tsx` (MODIFY) — „Präsentieren"-Links.
- `backend/app/content/changelog.py` (MODIFY, Task 7) — Eintrag.

---

### Task 1: Backend-Registry + Switching-Fixture

**Files:**
- Modify: `backend/app/content/registry.py`
- Modify: `backend/app/content/switching.py`
- Test: `backend/tests/test_content.py`

**Interfaces:**
- Produces: `trainer_module(key: str) -> dict | None` (voller Deepcopy, nichts gestrippt); `public_module` strippt nun zusätzlich `note` (je Block) und `goals` (Modul).

- [ ] **Step 1: Switching um goals + eine Block-Notiz erweitern**

In `backend/app/content/switching.py`: direkt nach der Zeile `"prerequisites": ["paket"],` einfügen:

```python
    "goals": [
        "MAC-Adressen als Schicht-2-Kennung verstehen",
        "Lernen, Weiterleiten und Flooding am Switch erklären",
        "Broadcast-Domäne als Motivation für VLANs einordnen",
    ],
```

Im ersten Block (der mit `## MAC-Adressen`) das Dict um einen `note`-Schlüssel ergänzen, sodass er so aussieht:

```python
        {"type": "text", "value": "## MAC-Adressen\n\nJede Netzwerkkarte hat eine "
            "eindeutige **MAC-Adresse** (Schicht 2). Ein Switch arbeitet mit diesen "
            "Adressen — nicht mit IPs.",
         "note": "Analogie: MAC = fest eingebaute Seriennummer der Netzwerkkarte, "
                 "IP = die verhandelbare Postadresse. Kurz die 48-Bit-Schreibweise zeigen."},
```

- [ ] **Step 2: Failing-Tests schreiben**

In `backend/tests/test_content.py` ans Ende anhängen:

```python
def test_public_module_strips_notes_and_goals():
    pub = registry.public_module("switching")
    assert "goals" not in pub
    for b in pub["blocks"]:
        assert "note" not in b
    for q in pub["quiz"]["questions"]:
        assert "answer" not in q


def test_trainer_module_keeps_notes_answers_goals():
    m = registry.trainer_module("switching")
    assert m["goals"]
    assert any("note" in b for b in m["blocks"])
    assert m["quiz"]["questions"][0]["answer"]
    assert registry.trainer_module("nope") is None
```

- [ ] **Step 3: Test ausführen, Fehlschlag prüfen**

Run: `./.venv/Scripts/python.exe -m pytest tests/test_content.py -q`
Expected: FAIL (`trainer_module` existiert nicht / `note` noch in public).

- [ ] **Step 4: Registry anpassen**

`backend/app/content/registry.py` vollständig ersetzen durch:

```python
from copy import deepcopy

from app.content.paket import PAKET_MODULE
from app.content.switching import SWITCHING_MODULE
from app.content.subnetting import SUBNETTING_MODULE
from app.content.arp import ARP_MODULE
from app.content.routing import ROUTING_MODULE
from app.content.nat import NAT_MODULE
from app.content.dns import DNS_MODULE
from app.content.dhcp import DHCP_MODULE
from app.content.ports import PORTS_MODULE
from app.content.icmp import ICMP_MODULE
from app.content.firewall import FIREWALL_MODULE
from app.content.ipv6 import IPV6_MODULE
from app.content.wlan import WLAN_MODULE
from app.content.vpn import VPN_MODULE
from app.content.vlan import VLAN_MODULE

MODULES = {m["key"]: m for m in (PAKET_MODULE, SWITCHING_MODULE, VLAN_MODULE, SUBNETTING_MODULE, ARP_MODULE, ROUTING_MODULE, NAT_MODULE, DNS_MODULE, DHCP_MODULE, PORTS_MODULE, ICMP_MODULE, FIREWALL_MODULE, IPV6_MODULE, WLAN_MODULE, VPN_MODULE)}


def module_meta() -> list[dict]:
    metas = [{"key": m["key"], "title": m["title"], "order": m["order"],
              "prerequisites": m.get("prerequisites", [])} for m in MODULES.values()]
    return sorted(metas, key=lambda m: m["order"])


def public_module(key: str) -> dict | None:
    m = MODULES.get(key)
    if not m:
        return None
    pub = deepcopy(m)
    pub.pop("goals", None)
    for b in pub["blocks"]:
        b.pop("note", None)
    for q in pub["quiz"]["questions"]:
        q.pop("answer", None)
    return pub


def trainer_module(key: str) -> dict | None:
    m = MODULES.get(key)
    return deepcopy(m) if m else None
```

- [ ] **Step 5: Tests grün**

Run: `./.venv/Scripts/python.exe -m pytest -q`
Expected: PASS (alle, weiterhin inkl. bestehender Content-/Aktivierungs-Tests).

- [ ] **Step 6: Commit**

```bash
git add backend/app/content/registry.py backend/app/content/switching.py backend/tests/test_content.py
git commit -m "feat(trainer): registry trainer_module + note/goals-Stripping"
```

---

### Task 2: Trainer-Modul-Endpoint

**Files:**
- Create: `backend/app/routers/trainer_modules.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_trainer_modules.py`

**Interfaces:**
- Consumes: `trainer_module`, `module_meta` (Task 1), `get_trainer` (vorhanden in `app/services/deps.py`).
- Produces: `GET /api/trainer/modules`, `GET /api/trainer/modules/{key}`.

- [ ] **Step 1: Failing-Tests schreiben**

`backend/tests/test_trainer_modules.py` erstellen:

```python
from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_trainer_module_requires_trainer():
    with TestClient(app) as c:
        assert c.get("/api/trainer/modules/switching").status_code in (401, 403)


def test_trainer_module_returns_notes_answers_goals():
    with TestClient(app) as c:
        h = _trainer(c)
        r = c.get("/api/trainer/modules/switching", headers=h)
        assert r.status_code == 200
        data = r.json()
        assert data["goals"]
        assert any("note" in b for b in data["blocks"])
        assert data["quiz"]["questions"][0]["answer"]
        assert c.get("/api/trainer/modules", headers=h).status_code == 200
        assert c.get("/api/trainer/modules/nope", headers=h).status_code == 404
```

- [ ] **Step 2: Test ausführen, Fehlschlag prüfen**

Run: `./.venv/Scripts/python.exe -m pytest tests/test_trainer_modules.py -q`
Expected: FAIL (404 auf allen Trainer-Modul-Pfaden — Router fehlt).

- [ ] **Step 3: Router erstellen**

`backend/app/routers/trainer_modules.py`:

```python
from fastapi import APIRouter, Depends, HTTPException

from app.services.deps import get_trainer
from app.content.registry import module_meta, trainer_module

router = APIRouter(prefix="/trainer/modules", tags=["trainer-modules"])


@router.get("")
def list_trainer_modules(_t: dict = Depends(get_trainer)):
    return module_meta()


@router.get("/{key}")
def get_trainer_module(key: str, _t: dict = Depends(get_trainer)):
    m = trainer_module(key)
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    return m
```

- [ ] **Step 4: Router einhängen**

In `backend/app/main.py` nach der Zeile `from app.routers import changelog as changelog_router  # noqa: E402` ergänzen:

```python
from app.routers import trainer_modules as trainer_modules_router  # noqa: E402
```

und nach `_api.include_router(changelog_router.router)`:

```python
_api.include_router(trainer_modules_router.router)
```

- [ ] **Step 5: Tests grün**

Run: `./.venv/Scripts/python.exe -m pytest -q`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add backend/app/routers/trainer_modules.py backend/app/main.py backend/tests/test_trainer_modules.py
git commit -m "feat(trainer): trainer-geschützter Modul-Endpoint mit Notizen/Lösungen"
```

---

### Task 3: Notizen + Lernziele für alle übrigen Module

**Files:**
- Modify: `backend/app/content/{paket,vlan,subnetting,arp,routing,nat,dns,dhcp,ports,icmp,firewall,ipv6,wlan,vpn}.py`
- Test: `backend/tests/test_content.py`

**Interfaces:**
- Consumes: nichts Neues. Ergänzt `goals` je Modul + `note` je Text-Block.

- [ ] **Step 1: Failing-Test schreiben**

In `backend/tests/test_content.py` anhängen:

```python
def test_every_module_has_goals_and_notes():
    for key, m in registry.MODULES.items():
        assert m.get("goals"), f"{key} ohne goals"
        assert any("note" in b for b in m["blocks"]), f"{key} ohne Block-Notiz"
```

- [ ] **Step 2: Test ausführen, Fehlschlag prüfen**

Run: `./.venv/Scripts/python.exe -m pytest tests/test_content.py::test_every_module_has_goals_and_notes -q`
Expected: FAIL (Module ohne goals/notes).

- [ ] **Step 3: goals + Notizen ergänzen**

Für **jedes** der 14 Module: (a) direkt nach der `"prerequisites"`-Zeile ein `"goals": [...]` mit 2–4 Lernzielen einfügen; (b) mindestens die ersten **zwei** Text-Blöcke sowie den Widget-Block um einen `"note"`-Schlüssel ergänzen (1–2 Sätze: Analogie / Reihenfolge im Widget / typische Rückfrage). Muster (am Beispiel `arp.py`, `goals` + eine Widget-Notiz):

```python
    # nach "prerequisites": ["subnetting"],
    "goals": [
        "Die Lücke zwischen IP (Schicht 3) und MAC (Schicht 2) benennen",
        "Den ARP-Ablauf Broadcast → Reply → Cache erklären",
        "Verstehen, warum ARP am Router endet (Gateway-MAC)",
    ],
```

Und beim Widget-Block:

```python
        {"type": "widget", "id": "arp-demo",
         "note": "Erst Cache leeren, dann eine unbekannte IP anfragen → Broadcast + "
                 "Reply zeigen. Danach dieselbe IP erneut → jetzt Cache-Treffer, kein Broadcast."},
```

Notizen für Widget-Blöcke sollen die **Vorführ-Reihenfolge** beschreiben. Anführungszeichen typografisch. Für die restlichen 13 Module analog vorgehen; Inhalte am jeweiligen Modul-Thema ausrichten.

- [ ] **Step 4: Test grün**

Run: `./.venv/Scripts/python.exe -m pytest -q`
Expected: PASS (inkl. `test_every_module_has_goals_and_notes`).

- [ ] **Step 5: Commit**

```bash
git add backend/app/content/
git commit -m "content(trainer): Präsentationsnotizen + Lernziele für alle Module"
```

---

### Task 4: Frontend-Typen, API, MD-Export

**Files:**
- Modify: `frontend/src/types.ts`
- Modify: `frontend/src/lib/trainerApi.ts`
- Modify: `frontend/src/components/Blocks.tsx`

**Interfaces:**
- Produces: `Block` mit optionalem `note`; `Question` mit optionalem `answer`; `TrainerModuleDetail`; `trainerApi.trainerModules()`, `trainerApi.trainerModule(key)`; exportiertes `MD_COMPONENTS`.

- [ ] **Step 1: Typen erweitern**

In `frontend/src/types.ts` `Block` und `Question` ersetzen und `TrainerModuleDetail` ergänzen:

```ts
export type Block =
  | { type: 'text'; value: string; note?: string }
  | { type: 'image'; url: string; alt?: string; note?: string }
  | { type: 'widget'; id: string; note?: string }

export type Question =
  | { id: string; type: 'single'; prompt: string; options: string[]; answer?: string }
  | { id: string; type: 'multi'; prompt: string; options: string[]; answer?: string[] }
  | { id: string; type: 'number'; prompt: string; answer?: number }
```

Nach `ModuleDetail` einfügen:

```ts
export interface TrainerModuleDetail extends ModuleDetail { goals?: string[] }
```

- [ ] **Step 2: MD_COMPONENTS exportieren**

In `frontend/src/components/Blocks.tsx` `const MD_COMPONENTS` zu `export const MD_COMPONENTS` ändern (nur das Schlüsselwort `export` voranstellen).

- [ ] **Step 3: trainerApi erweitern**

In `frontend/src/lib/trainerApi.ts` den Import-Kopf und die zwei Methoden ergänzen. Import-Zeile am Dateianfang hinzufügen:

```ts
import type { ModuleMeta, TrainerModuleDetail } from '@/types'
```

Innerhalb des `trainerApi`-Objekts (nach `setCourseModule`) einfügen:

```ts
  trainerModules: () => api.get<ModuleMeta[]>('/trainer/modules'),
  trainerModule: (key: string) => api.get<TrainerModuleDetail>(`/trainer/modules/${key}`),
```

- [ ] **Step 4: Typecheck**

Run (aus `frontend/`): `npx tsc --noEmit`
Expected: keine Fehler.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/types.ts frontend/src/lib/trainerApi.ts frontend/src/components/Blocks.tsx
git commit -m "feat(trainer): Frontend-Typen, trainerApi-Endpoints, MD_COMPONENTS-Export"
```

---

### Task 5: Trainer-Komponenten (Blocks + Quiz)

**Files:**
- Create: `frontend/src/components/trainerQuiz.ts`
- Create: `frontend/src/components/trainerQuiz.test.ts`
- Create: `frontend/src/components/TrainerBlocks.tsx`
- Create: `frontend/src/components/TrainerQuiz.tsx`

**Interfaces:**
- Consumes: `MD_COMPONENTS`, `WIDGETS`, Typen aus Task 4.
- Produces: `isCorrect(q, opt)`, `<TrainerBlocks blocks>`, `<TrainerQuiz questions>`.

- [ ] **Step 1: Failing-Test für isCorrect**

`frontend/src/components/trainerQuiz.test.ts`:

```ts
import { describe, it, expect } from 'vitest'
import { isCorrect } from './trainerQuiz'
import type { Question } from '@/types'

const single: Question = { id: 's', type: 'single', prompt: '', options: ['a', 'b'], answer: 'b' }
const multi: Question = { id: 'm', type: 'multi', prompt: '', options: ['a', 'b', 'c'], answer: ['a', 'c'] }
const num: Question = { id: 'n', type: 'number', prompt: '', answer: 42 }

describe('isCorrect', () => {
  it('single: nur die Antwort ist korrekt', () => {
    expect(isCorrect(single, 'b')).toBe(true)
    expect(isCorrect(single, 'a')).toBe(false)
  })
  it('multi: alle Antwort-Optionen korrekt', () => {
    expect(isCorrect(multi, 'a')).toBe(true)
    expect(isCorrect(multi, 'b')).toBe(false)
  })
  it('number: Optionen gibt es nicht -> false', () => {
    expect(isCorrect(num, '42')).toBe(false)
  })
})
```

- [ ] **Step 2: Test ausführen, Fehlschlag prüfen**

Run (aus `frontend/`): `npm run test`
Expected: FAIL (`isCorrect` nicht definiert).

- [ ] **Step 3: isCorrect implementieren**

`frontend/src/components/trainerQuiz.ts`:

```ts
import type { Question } from '@/types'

export function isCorrect(q: Question, opt: string): boolean {
  if (q.type === 'single') return q.answer === opt
  if (q.type === 'multi') return (q.answer ?? []).includes(opt)
  return false
}
```

- [ ] **Step 4: Test grün**

Run (aus `frontend/`): `npm run test`
Expected: PASS

- [ ] **Step 5: TrainerBlocks erstellen**

`frontend/src/components/TrainerBlocks.tsx`:

```tsx
import { useState } from 'react'
import Markdown from 'react-markdown'
import type { Block } from '@/types'
import { WIDGETS } from '@/widgets/registry'
import { MD_COMPONENTS } from '@/components/Blocks'

function WidgetBlock({ id }: { id: string }) {
  const W = WIDGETS[id]
  return W ? <W /> : <div className="text-sm text-red-500">Unbekanntes Widget: {id}</div>
}

function NoteBox({ note }: { note: string }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="mt-1">
      <button
        onClick={() => setOpen((o) => !o)}
        className="text-xs font-medium text-teal-700 hover:text-teal-800"
      >
        {open ? '▾' : '▸'} 💬 Notiz
      </button>
      {open && (
        <div className="mt-1 rounded-lg border-l-4 border-amber-300 bg-amber-50 px-3 py-2 text-sm text-slate-700">
          {note}
        </div>
      )}
    </div>
  )
}

export function TrainerBlocks({ blocks }: { blocks: Block[] }) {
  return (
    <div className="flex flex-col gap-6">
      {blocks.map((b, i) => (
        <div key={i} className="flex flex-col gap-1">
          {b.type === 'text' && <Markdown components={MD_COMPONENTS}>{b.value}</Markdown>}
          {b.type === 'image' && <img src={b.url} alt={b.alt ?? ''} className="rounded-lg border" />}
          {b.type === 'widget' && <WidgetBlock id={b.id} />}
          {b.note && <NoteBox note={b.note} />}
        </div>
      ))}
    </div>
  )
}
```

- [ ] **Step 6: TrainerQuiz erstellen**

`frontend/src/components/TrainerQuiz.tsx`:

```tsx
import type { Question } from '@/types'
import { isCorrect } from '@/components/trainerQuiz'

export function TrainerQuiz({ questions }: { questions: Question[] }) {
  return (
    <div className="mt-8 rounded-2xl border bg-white p-6">
      <h3 className="text-lg font-semibold text-slate-900 mb-4">Quiz — mit Lösungen</h3>
      <div className="flex flex-col gap-5">
        {questions.map((q) => (
          <div key={q.id}>
            <p className="font-medium text-slate-800 mb-2">{q.prompt}</p>
            {q.type === 'number' ? (
              <p className="text-sm">
                <span className="text-slate-500">Antwort: </span>
                <span className="font-mono font-semibold text-teal-700">{q.answer}</span>
              </p>
            ) : (
              <div className="flex flex-col gap-1.5">
                {q.options.map((opt) => {
                  const ok = isCorrect(q, opt)
                  return (
                    <div
                      key={opt}
                      className={`flex items-center gap-2 text-sm ${ok ? 'text-teal-700 font-medium' : 'text-slate-600'}`}
                    >
                      <span>{ok ? '✓' : '○'}</span>
                      {opt}
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
```

- [ ] **Step 7: Typecheck + Test grün**

Run (aus `frontend/`): `npx tsc --noEmit && npm run test`
Expected: keine Fehler, Tests PASS.

- [ ] **Step 8: Commit**

```bash
git add frontend/src/components/trainerQuiz.ts frontend/src/components/trainerQuiz.test.ts frontend/src/components/TrainerBlocks.tsx frontend/src/components/TrainerQuiz.tsx
git commit -m "feat(trainer): TrainerBlocks (Notizen) + TrainerQuiz (Lösungen)"
```

---

### Task 6: Trainer-Modulseite + Route + Links

**Files:**
- Create: `frontend/src/pages/TrainerModulePage.tsx`
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/pages/TrainerPage.tsx`

**Interfaces:**
- Consumes: `trainerApi.trainerModule`, `trainerApi.trainerModules`, `TrainerBlocks`, `TrainerQuiz`, `useAuthStore` (liefert `{ token, role }`).

- [ ] **Step 1: TrainerModulePage erstellen**

`frontend/src/pages/TrainerModulePage.tsx`:

```tsx
import { useQuery } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, useParams } from 'react-router-dom'
import { trainerApi } from '@/lib/trainerApi'
import { TrainerBlocks } from '@/components/TrainerBlocks'
import { TrainerQuiz } from '@/components/TrainerQuiz'
import { useAuthStore } from '@/store/auth'

export function TrainerModulePage() {
  const { key = '' } = useParams()
  const { token, role } = useAuthStore()
  const mod = useQuery({
    queryKey: ['trainer-module', key],
    queryFn: () => trainerApi.trainerModule(key).then((r) => r.data),
    enabled: role === 'trainer' && !!token,
  })

  if (role !== 'trainer' || !token)
    return (
      <div className="p-10 text-slate-600">
        Nur für Trainer. <Link to="/trainer" className="text-teal-600">Zum Login</Link>
      </div>
    )
  if (mod.isLoading || !mod.data) return <div className="p-10">Lädt…</div>
  const m = mod.data

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <Link to="/trainer" className="text-sm text-slate-400 hover:text-slate-600">← Trainer</Link>
        <h1 className="text-2xl font-bold text-slate-900 mt-2 mb-4">
          {m.title} <span className="text-sm font-normal text-slate-400">· Trainer-Ansicht</span>
        </h1>

        <div className="rounded-xl border bg-white p-4 mb-6 text-sm">
          <div className="flex flex-wrap gap-x-6 gap-y-1 text-slate-600">
            <span>Voraussetzungen: {m.prerequisites.length ? m.prerequisites.join(', ') : '—'}</span>
            <span>{m.blocks.length} Blöcke</span>
            <span>{m.quiz.questions.length} Quiz-Fragen</span>
          </div>
          {m.goals && m.goals.length > 0 && (
            <div className="mt-2">
              <p className="font-semibold text-slate-700">Lernziele</p>
              <ul className="list-disc pl-5 text-slate-600">
                {m.goals.map((g, i) => <li key={i}>{g}</li>)}
              </ul>
            </div>
          )}
        </div>

        {m.scenario && (
          <div className="rounded-xl border-l-4 border-teal-400 bg-teal-50 px-4 py-3 mb-6 text-sm text-slate-700">
            <Markdown>{m.scenario}</Markdown>
          </div>
        )}

        <TrainerBlocks blocks={m.blocks} />
        <TrainerQuiz questions={m.quiz.questions} />
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Route ergänzen**

In `frontend/src/App.tsx` den Import ergänzen:

```tsx
import { TrainerModulePage } from '@/pages/TrainerModulePage'
```

und vor der `<Route path="*" ...>`-Zeile einfügen:

```tsx
          <Route path="/trainer/modul/:key" element={<TrainerModulePage />} />
```

- [ ] **Step 3: „Präsentieren"-Links im Dashboard**

In `frontend/src/pages/TrainerPage.tsx`: Import-Zeile am Dateianfang ergänzen:

```tsx
import { Link } from 'react-router-dom'
```

In `TrainerDashboard` nach der `changelog`-Query-Zeile (`const changelog = useQuery(...)`) einfügen:

```tsx
  const presentMods = useQuery({ queryKey: ['trainer-modules'], queryFn: () => trainerApi.trainerModules().then((r) => r.data) })
```

Im JSX direkt nach dem öffnenden `<div className="flex flex-col gap-2 mb-8">…</div>`-Block (Kursliste) — konkret unmittelbar vor `{courseMods.data && (` — einfügen:

```tsx
        {presentMods.data && (
          <div className="rounded-xl border bg-white p-4 mb-6">
            <h3 className="text-sm font-semibold text-slate-700 mb-2">Module präsentieren</h3>
            <div className="flex flex-wrap gap-2">
              {presentMods.data.map((m) => (
                <Link key={m.key} to={`/trainer/modul/${m.key}`}
                  className="rounded-lg border px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-50">
                  {m.title}
                </Link>
              ))}
            </div>
          </div>
        )}
```

- [ ] **Step 4: Typecheck + Build**

Run (aus `frontend/`): `npx tsc --noEmit && npm run build`
Expected: kein Fehler, Build erfolgreich.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/pages/TrainerModulePage.tsx frontend/src/App.tsx frontend/src/pages/TrainerPage.tsx
git commit -m "feat(trainer): Modul-Präsentationsseite + Route + Dashboard-Links"
```

---

### Task 7: Changelog + Gesamt-Verifikation

**Files:**
- Modify: `backend/app/content/changelog.py`

- [ ] **Step 1: Changelog-Eintrag ergänzen**

In `backend/app/content/changelog.py` als **ersten** Eintrag der `CHANGELOG`-Liste (direkt nach `CHANGELOG = [`) einfügen:

```python
    {"date": "2026-07-01", "title": "Trainer-Präsentationsansicht",
     "text": "Trainer haben pro Modul eine eigene Ansicht mit einklappbaren "
             "Präsentationsnotizen je Block, einer Kurzübersicht (Voraussetzungen, "
             "Lernziele) und sichtbaren Quiz-Lösungen."},
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
git commit -m "docs(changelog): Trainer-Präsentationsansicht"
```

---

## Self-Review-Notiz

- Sicherheit: `public_module` strippt note/answer/goals (Task 1), Endpoint `get_trainer`-geschützt (Task 2) — durch Tests abgedeckt.
- Typen konsistent: `note?`/`answer?`/`goals?` (Task 4) matchen Backend-Felder (Task 1/3) und Nutzung in `TrainerBlocks`/`TrainerQuiz`/`TrainerModulePage` (Task 5/6).
- Reuse statt Duplikat: `MD_COMPONENTS` exportiert, `<Blocks>`/`<Quiz>` für Teilnehmer unverändert.
