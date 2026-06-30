# Modul-Aktivierung + CLI-Simulator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Trainer können Module je Kurs aktivieren/deaktivieren (serverseitig durchgesetzt), und das VLAN-Switch-Widget bekommt ein IOS-artiges `show`-CLI, das die Port-Konfiguration spiegelt.

**Architecture:** Backend: `module_disabled`-Tabelle (pro Kurs), Teilnehmer-Modul-Endpunkte filtern danach, Trainer-Endpunkte togglen. Frontend: Trainer-Dashboard mit Modul-Checkboxen; ein generisches `DeviceCli`-Shell-Widget + pure `switchCli`-Logik (Vitest-getestet), eingebettet im `vlan-switch`-Widget.

**Tech Stack:** FastAPI/SQLite/Pytest; React/TS/Vite/Tailwind; **Vitest** (neu).

## Global Constraints

- Modul-Aktivierung **pro Kurs**, Default alles an, nur „aus"-Zeilen gespeichert; deaktiviertes Modul → 404 für Teilnehmer.
- CLI **read-only** (`show`-Befehle), gekoppelt an den Switch-Port-State.
- CLI-Kern erweiterbar: generische Shell + pro Gerät pure Logik (späterer Router dockt an).
- Backend-Tests venv: `.venv/Scripts/python.exe -m pytest`.
- Frontend strict TS, keine `any`.

---

### Task 1: Backend — Modul-Aktivierung pro Kurs

**Files:**
- Create: `backend/app/models/module_disabled.py`, `backend/app/services/activation.py`
- Modify: `backend/app/main.py` (Modell-Import), `backend/app/routers/modules.py` (Filter), `backend/app/routers/courses.py` (Trainer-Endpunkte)
- Create: `backend/tests/test_module_activation.py`

**Interfaces:**
- Produces: `ModuleDisabled(id, course_id, module_key)`; `activation.disabled_keys(db, course_id) -> set[str]`; Endpunkte `GET/PUT /courses/{id}/modules`; gefilterte Teilnehmer-Modul-Endpunkte.

- [ ] **Step 1: Modell** — `backend/app/models/module_disabled.py`:

```python
from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ModuleDisabled(Base):
    """Ein 'aus'-Eintrag für ein Modul in einem Kurs. Fehlt = aktiv."""
    __tablename__ = "module_disabled"
    __table_args__ = (UniqueConstraint("course_id", "module_key", name="uq_module_disabled"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    module_key: Mapped[str] = mapped_column(String, nullable=False)
```

- [ ] **Step 2: Modell-Import** — in `backend/app/main.py` bei den anderen `from app.models import …`:

```python
from app.models import module_disabled as _module_disabled  # noqa: F401
```

- [ ] **Step 3: Service** — `backend/app/services/activation.py`:

```python
from app.models.module_disabled import ModuleDisabled


def disabled_keys(db, course_id: int) -> set[str]:
    rows = db.query(ModuleDisabled).filter(ModuleDisabled.course_id == course_id).all()
    return {r.module_key for r in rows}
```

- [ ] **Step 4: Teilnehmer-Filter** — `backend/app/routers/modules.py` ersetzen:

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
from app.services.activation import disabled_keys
from app.content.registry import MODULES, module_meta, public_module
from app.utils import utc_now

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("")
def list_modules(db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    off = disabled_keys(db, p.course_id)
    return [m for m in module_meta() if m["key"] not in off]


@router.get("/{key}")
def get_module(key: str, db: Session = Depends(get_db), p: Participant = Depends(get_participant)):
    if key in disabled_keys(db, p.course_id):
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    pub = public_module(key)
    if not pub:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    return pub


class QuizSubmit(BaseModel):
    answers: dict


@router.post("/{key}/quiz")
def submit_quiz(key: str, data: QuizSubmit, db: Session = Depends(get_db),
                p: Participant = Depends(get_participant)):
    if key in disabled_keys(db, p.course_id):
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
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

- [ ] **Step 5: Trainer-Endpunkte** — in `backend/app/routers/courses.py` ergänzen
(Imports oben: `from app.models.module_disabled import ModuleDisabled` und
`from app.services.activation import disabled_keys`; `from pydantic import BaseModel`
ist bereits da), ans Dateiende:

```python
@router.get("/{course_id}/modules")
def course_modules(course_id: int, db: Session = Depends(get_db), _=Depends(get_trainer)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")
    off = disabled_keys(db, course_id)
    return [{"key": m["key"], "title": m["title"], "order": m["order"],
             "active": m["key"] not in off} for m in module_meta()]


class ModuleToggle(BaseModel):
    module_key: str
    active: bool


@router.put("/{course_id}/modules")
def set_course_module(course_id: int, data: ModuleToggle,
                      db: Session = Depends(get_db), _=Depends(get_trainer)):
    if not db.query(Course).filter(Course.id == course_id).first():
        raise HTTPException(status_code=404, detail="Kurs nicht gefunden")
    if data.module_key not in MODULES:
        raise HTTPException(status_code=422, detail="Unbekanntes Modul")
    row = db.query(ModuleDisabled).filter(
        ModuleDisabled.course_id == course_id,
        ModuleDisabled.module_key == data.module_key).first()
    if data.active:
        if row:
            db.delete(row)
    else:
        if not row:
            db.add(ModuleDisabled(course_id=course_id, module_key=data.module_key))
    db.commit()
    return {"ok": True}
```
(In `courses.py` zusätzlich `from app.content.registry import MODULES` ergänzen — bisher nur `module_meta` importiert.)

- [ ] **Step 6: Test** — `backend/tests/test_module_activation.py`:

```python
from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_per_course_activation():
    with TestClient(app) as c:
        h = _trainer(c)
        code_a = c.post("/api/courses", json={"name": "KursA"}, headers=h).json()["join_code"]
        code_b = c.post("/api/courses", json={"name": "KursB"}, headers=h).json()["join_code"]
        courses = {x["join_code"]: x["id"] for x in c.get("/api/courses", headers=h).json()}
        id_a = courses[code_a]

        # Default: alle aktiv
        mods = c.get(f"/api/courses/{id_a}/modules", headers=h).json()
        assert all(m["active"] for m in mods)

        # vlan in KursA deaktivieren
        assert c.put(f"/api/courses/{id_a}/modules", headers=h,
                     json={"module_key": "vlan", "active": False}).status_code == 200

        tok_a = c.post("/api/join", json={"code": code_a, "name": "A1"}).json()["access_token"]
        tok_b = c.post("/api/join", json={"code": code_b, "name": "B1"}).json()["access_token"]
        ha = {"Authorization": f"Bearer {tok_a}"}
        hb = {"Authorization": f"Bearer {tok_b}"}

        keys_a = [m["key"] for m in c.get("/api/modules", headers=ha).json()]
        assert "vlan" not in keys_a and "paket" in keys_a
        assert c.get("/api/modules/vlan", headers=ha).status_code == 404
        assert c.post("/api/modules/vlan/quiz", json={"answers": {}}, headers=ha).status_code == 404

        # KursB unberührt
        keys_b = [m["key"] for m in c.get("/api/modules", headers=hb).json()]
        assert "vlan" in keys_b

        # wieder aktivieren
        c.put(f"/api/courses/{id_a}/modules", headers=h, json={"module_key": "vlan", "active": True})
        assert "vlan" in [m["key"] for m in c.get("/api/modules", headers=ha).json()]

        # Teilnehmer darf nicht togglen
        assert c.put(f"/api/courses/{id_a}/modules", headers=ha,
                     json={"module_key": "vlan", "active": False}).status_code == 403
```

- [ ] **Step 7: Lauf + Commit**

```bash
cd backend && rm -f test_intnetwork.db && .venv/Scripts/python.exe -m pytest -q
```
Expected: alle grün.
```bash
git add backend/app/models/module_disabled.py backend/app/services/activation.py backend/app/main.py backend/app/routers/modules.py backend/app/routers/courses.py backend/tests/test_module_activation.py
git commit -m "feat(activation): Module pro Kurs aktivieren/deaktivieren (serverseitig)"
```

---

### Task 2: Frontend — Trainer-Modul-Schalter

**Files:**
- Modify: `frontend/src/lib/trainerApi.ts`
- Modify: `frontend/src/pages/TrainerPage.tsx`

**Interfaces:**
- Consumes: `GET/PUT /courses/{id}/modules`.
- Produces: `trainerApi.courseModules`, `trainerApi.setCourseModule`.

- [ ] **Step 1: `trainerApi`** — in `frontend/src/lib/trainerApi.ts` ergänzen:

```ts
export interface CourseModule { key: string; title: string; order: number; active: boolean }
```
und im `trainerApi`-Objekt:
```ts
  courseModules: (id: number) => api.get<CourseModule[]>(`/courses/${id}/modules`),
  setCourseModule: (id: number, module_key: string, active: boolean) =>
    api.put(`/courses/${id}/modules`, { module_key, active }),
```

- [ ] **Step 2: Dashboard-Abschnitt** — in `frontend/src/pages/TrainerPage.tsx` im
`TrainerDashboard` nach der `dash`-Query ergänzen:

```tsx
  const courseMods = useQuery({
    queryKey: ['course-modules', selected], enabled: selected !== null,
    queryFn: () => trainerApi.courseModules(selected as number).then((r) => r.data),
  })
  const toggleMod = useMutation({
    mutationFn: (v: { module_key: string; active: boolean }) =>
      trainerApi.setCourseModule(selected as number, v.module_key, v.active),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['course-modules', selected] }),
  })
```

und im JSX direkt **vor** dem Dashboard-`{dash.data && (...)}`-Block einfügen:

```tsx
        {courseMods.data && (
          <div className="rounded-xl border bg-white p-4 mb-6">
            <h3 className="text-sm font-semibold text-slate-700 mb-2">Module in diesem Kurs</h3>
            <div className="flex flex-col gap-1.5">
              {courseMods.data.map((m) => (
                <label key={m.key} className="flex items-center gap-2 text-sm text-slate-700">
                  <input type="checkbox" checked={m.active} disabled={toggleMod.isPending}
                    onChange={(e) => toggleMod.mutate({ module_key: m.key, active: e.target.checked })} />
                  {m.title}
                </label>
              ))}
            </div>
          </div>
        )}
```

- [ ] **Step 3: Build + Commit**

```bash
cd frontend && npx tsc -b && npm run build
```
Expected: Build ok.
```bash
git add frontend/src/lib/trainerApi.ts frontend/src/pages/TrainerPage.tsx
git commit -m "feat(activation): Trainer-Dashboard Modul-Schalter je Kurs"
```

---

### Task 3: Frontend — Vitest + Switch-CLI-Logik (pure)

**Files:**
- Modify: `frontend/package.json` (Vitest + Script)
- Create: `frontend/src/widgets/cli/switchCli.ts`, `frontend/src/widgets/cli/switchCli.test.ts`

**Interfaces:**
- Produces: `Port` Typ; `runSwitchCommand(ports: Port[], cmd: string) -> string`.

- [ ] **Step 1: Vitest installieren + Script**

```bash
cd frontend && npm install -D vitest
```
Dann in `frontend/package.json` unter `"scripts"` ergänzen: `"test": "vitest run"`.

- [ ] **Step 2: Test schreiben** — `frontend/src/widgets/cli/switchCli.test.ts`:

```ts
import { describe, it, expect } from 'vitest'
import { runSwitchCommand, type Port } from './switchCli'

const PORTS: Port[] = [
  { vlan: 10, mode: 'access' },
  { vlan: 10, mode: 'access' },
  { vlan: 20, mode: 'access' },
  { vlan: 10, mode: 'trunk' },
]

describe('runSwitchCommand', () => {
  it('show vlan listet Access-Ports je VLAN', () => {
    const out = runSwitchCommand(PORTS, 'show vlan')
    expect(out).toContain('10')
    expect(out).toContain('Gi0/1, Gi0/2')
    expect(out).toContain('Gi0/3')
  })

  it('show running-config zeigt access + trunk', () => {
    const out = runSwitchCommand(PORTS, 'show running-config')
    expect(out).toContain('interface Gi0/1')
    expect(out).toContain('switchport access vlan 10')
    expect(out).toContain('switchport mode trunk')
  })

  it('unbekannter Befehl', () => {
    expect(runSwitchCommand(PORTS, 'foobar')).toContain('% Invalid input')
  })
})
```

- [ ] **Step 3: Lauf, Fehlschlag**

Run: `cd frontend && npx vitest run src/widgets/cli/switchCli.test.ts`
Expected: FAIL (Modul fehlt).

- [ ] **Step 4: Implementieren** — `frontend/src/widgets/cli/switchCli.ts`:

```ts
export interface Port { vlan: number; mode: 'access' | 'trunk' }

const iface = (i: number) => `Gi0/${i + 1}`

function showVlan(ports: Port[]): string {
  const byVlan = new Map<number, string[]>()
  ports.forEach((p, i) => {
    if (p.mode === 'access') {
      const list = byVlan.get(p.vlan) ?? []
      list.push(iface(i))
      byVlan.set(p.vlan, list)
    }
  })
  const lines = ['VLAN Name             Status    Ports', '---- ---------------- --------- ------------------------------']
  for (const vlan of [...byVlan.keys()].sort((a, b) => a - b)) {
    const name = `VLAN${String(vlan).padStart(4, '0')}`
    lines.push(`${String(vlan).padEnd(4)} ${name.padEnd(16)} active    ${byVlan.get(vlan)!.join(', ')}`)
  }
  const trunks = ports.map((p, i) => (p.mode === 'trunk' ? iface(i) : null)).filter(Boolean)
  if (trunks.length) lines.push('', `Trunks: ${trunks.join(', ')}`)
  return lines.join('\n')
}

function showRunningConfig(ports: Port[]): string {
  const lines = ['!', 'hostname Nordwind-SW1', '!']
  ports.forEach((p, i) => {
    lines.push(`interface ${iface(i)}`)
    if (p.mode === 'trunk') {
      lines.push(' switchport mode trunk')
    } else {
      lines.push(' switchport mode access', ` switchport access vlan ${p.vlan}`)
    }
    lines.push('!')
  })
  lines.push('end')
  return lines.join('\n')
}

function showInterfacesStatus(ports: Port[]): string {
  const lines = ['Port      Status        Vlan       Mode']
  ports.forEach((p, i) => {
    const vlan = p.mode === 'trunk' ? 'trunk' : String(p.vlan)
    lines.push(`${iface(i).padEnd(10)}connected     ${vlan.padEnd(11)}${p.mode}`)
  })
  return lines.join('\n')
}

function showMacTable(ports: Port[]): string {
  const lines = ['Vlan    Mac Address       Ports', '----    -----------       -----']
  ports.forEach((p, i) => {
    if (p.mode === 'access') {
      const mac = `0011.22${String(i + 1).padStart(2, '0')}.00${String(p.vlan).padStart(2, '0')}`
      lines.push(`${String(p.vlan).padEnd(8)}${mac}    ${iface(i)}`)
    }
  })
  return lines.join('\n')
}

const HELP = [
  'Verfügbare Befehle:',
  '  show vlan',
  '  show running-config',
  '  show interfaces status',
  '  show mac address-table',
].join('\n')

export function runSwitchCommand(ports: Port[], raw: string): string {
  const cmd = raw.trim().toLowerCase().replace(/\s+/g, ' ')
  if (!cmd) return ''
  if (cmd === '?' || cmd === 'help') return HELP
  if (cmd === 'show vlan' || cmd === 'show vlan brief') return showVlan(ports)
  if (cmd === 'show running-config' || cmd === 'show run') return showRunningConfig(ports)
  if (cmd === 'show interfaces status' || cmd === 'show int status') return showInterfacesStatus(ports)
  if (cmd === 'show mac address-table') return showMacTable(ports)
  return '% Invalid input detected\nTippe ? für die Befehlsliste.'
}
```

- [ ] **Step 5: Lauf, grün + Commit**

Run: `cd frontend && npx vitest run src/widgets/cli/switchCli.test.ts`
Expected: 3 passed.
```bash
git add frontend/package.json frontend/package-lock.json frontend/src/widgets/cli/switchCli.ts frontend/src/widgets/cli/switchCli.test.ts
git commit -m "feat(cli): pure Switch-CLI-Logik (show-Befehle) + Vitest"
```

---

### Task 4: Frontend — DeviceCli-Shell + Einbindung im Switch-Widget

**Files:**
- Create: `frontend/src/widgets/cli/DeviceCli.tsx`
- Modify: `frontend/src/widgets/VlanSwitch.tsx`

**Interfaces:**
- Consumes: `runSwitchCommand`, `Port`.
- Produces: `DeviceCli`-Komponente (`prompt`, `run`).

- [ ] **Step 1: `frontend/src/widgets/cli/DeviceCli.tsx`**

```tsx
import { useState } from 'react'

export function DeviceCli({ prompt, run }: { prompt: string; run: (cmd: string) => string }) {
  const [lines, setLines] = useState<string[]>(['Tippe ? für die Befehlsliste.'])
  const [input, setInput] = useState('')
  const [hist, setHist] = useState<string[]>([])
  const [hi, setHi] = useState(-1)

  function submit() {
    const out = run(input)
    setLines((l) => [...l, `${prompt} ${input}`, ...(out ? out.split('\n') : [])])
    if (input.trim()) setHist((h) => [input, ...h])
    setHi(-1)
    setInput('')
  }

  function onKey(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter') submit()
    else if (e.key === 'ArrowUp') {
      e.preventDefault()
      const ni = Math.min(hi + 1, hist.length - 1)
      if (ni >= 0) { setHi(ni); setInput(hist[ni]) }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault()
      const ni = hi - 1
      setHi(ni)
      setInput(ni >= 0 ? hist[ni] : '')
    }
  }

  return (
    <div className="mt-4 rounded-lg bg-slate-900 p-3 font-mono text-xs text-slate-100">
      <div className="max-h-64 overflow-y-auto whitespace-pre-wrap">{lines.join('\n')}</div>
      <div className="mt-1 flex gap-2">
        <span className="text-green-400">{prompt}</span>
        <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={onKey}
          spellCheck={false} autoComplete="off"
          className="flex-1 bg-transparent text-slate-100 outline-none" />
      </div>
    </div>
  )
}
```

- [ ] **Step 2: Einbinden** — in `frontend/src/widgets/VlanSwitch.tsx`:

(a) Importe + `Port`-Typ aus der CLI-Logik nutzen. Oben ergänzen:
```tsx
import { DeviceCli } from '@/widgets/cli/DeviceCli'
import { runSwitchCommand, type Port } from '@/widgets/cli/switchCli'
```
und die **lokale** `interface Port { … }`-Zeile in `VlanSwitch.tsx` löschen (Typ kommt jetzt aus `switchCli`; Felder identisch: `vlan`, `mode`).

(b) Direkt vor dem schließenden `</div>` des Widgets (nach dem `source !== null`-Hinweisblock) einfügen:
```tsx
      <DeviceCli prompt="Nordwind-SW1#" run={(c) => runSwitchCommand(ports, c)} />
```

- [ ] **Step 3: Build + Commit**

```bash
cd frontend && npx tsc -b && npm run build
```
Expected: Build ok.
```bash
git add frontend/src/widgets/cli/DeviceCli.tsx frontend/src/widgets/VlanSwitch.tsx
git commit -m "feat(cli): DeviceCli-Terminal im VLAN-Switch-Widget (gekoppelt)"
```

---

### Task 5: Gesamt-Verifikation

- [ ] **Step 1: Backend-Tests**

```bash
cd backend && rm -f test_intnetwork.db && .venv/Scripts/python.exe -m pytest -q
```
Expected: alle grün.

- [ ] **Step 2: Frontend Tests + Build**

```bash
cd frontend && npx vitest run && npx tsc -b && npm run build
```
Expected: Vitest grün, Build ok.

- [ ] **Step 3: Manueller Smoke**

Trainer: Kurs wählen → „Module in diesem Kurs" → ein Modul abschalten → als
Teilnehmer dieses Kurses ist es weg (Direktaufruf 404). VLAN-Modul: im
Switch-Widget Ports ändern, dann im Terminal `show vlan` / `show running-config`
→ Ausgabe spiegelt die Ports; `?` zeigt Befehle; Unsinn → `% Invalid input`.

- [ ] **Step 4:** Keine weitere Commit nötig.
