# Story-Curriculum + Paketaufbau-Modul Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Den Kurs als Story der Firma „Nordwind Logistik GmbH" rahmen, Module mit sichtbaren Voraussetzungen versehen, und ein neues erstes Modul „Paketaufbau" (Ethernet-Frame + Lage des 802.1Q-Tags) mit interaktivem Frame-Builder-Widget hinzufügen.

**Architecture:** Backend-Modul-Dicts bekommen `prerequisites` + `scenario`; `module_meta` liefert Prereqs mit, `public_module` liefert Scenario mit (weiterhin ohne Quiz-Lösungen). Ein statischer Firmen-Steckbrief über `GET /company`. Frontend zeigt Firmen-Karte + „setzt voraus" + Scenario-Intro und rendert das neue `frame-builder`-Widget.

**Tech Stack:** FastAPI/SQLite/Pytest (Backend); React/TS/Vite/Tailwind/react-markdown (Frontend).

## Global Constraints

- Quiz-Lösungen (`answer`) verlassen den Server nie.
- „Empfohlene Reihenfolge": Module frei navigierbar, Voraussetzungen nur angezeigt (keine Sperre).
- `prerequisites` verweisen nur auf existierende Module (`vlan` → `["paket"]`).
- Backend-Tests mit venv: `.venv/Scripts/python.exe -m pytest`.
- Frontend strict TS, keine `any`.

---

### Task 1: Backend — Modul-Felder (prerequisites/scenario) + Firmen-Steckbrief + VLAN-Retrofit

**Files:**
- Create: `backend/app/content/company.py`
- Modify: `backend/app/content/registry.py` (meta um `prerequisites`)
- Modify: `backend/app/content/vlan.py` (order/prerequisites/scenario)
- Modify: `backend/app/routers/join.py` (`GET /company`)
- Modify: `backend/tests/test_content.py`

**Interfaces:**
- Produces: `company.COMPANY` (`name, blurb, sites, devices`); `module_meta()` Einträge mit `prerequisites`; `public_module` liefert `scenario` + `prerequisites` (vorhanden via deepcopy); `GET /company` → COMPANY.

- [ ] **Step 1: `backend/app/content/company.py`**

```python
COMPANY = {
    "name": "Nordwind Logistik GmbH",
    "blurb": "Mittelständischer Logistiker mit Zentrale und Lager-Standort. "
             "Über die Jahre gewachsen — das Netzwerk ist historisch flach und "
             "muss Stück für Stück sauber strukturiert werden.",
    "sites": ["Zentrale", "Lager"],
    "devices": [
        "Büro-PCs (Verwaltung)",
        "Drucker",
        "Mitarbeiter-WLAN (Lager-Scanner, Tablets)",
        "Gäste-WLAN (Empfang)",
        "IP-Überwachungskameras (Lager, Eingang)",
        "VoIP-Telefone",
        "Server (ERP, Datei)",
        "Internet-Router",
    ],
}
```

- [ ] **Step 2: `module_meta` um `prerequisites` erweitern** — in `backend/app/content/registry.py`:

```python
def module_meta() -> list[dict]:
    metas = [{"key": m["key"], "title": m["title"], "order": m["order"],
              "prerequisites": m.get("prerequisites", [])} for m in MODULES.values()]
    return sorted(metas, key=lambda m: m["order"])
```

- [ ] **Step 3: VLAN-Retrofit** — in `backend/app/content/vlan.py` die Kopf-Felder anpassen
(`"order": 1` → `3`) und direkt nach `"pass_threshold": 0.7,` ergänzen:

```python
    "order": 3,
    "pass_threshold": 0.7,
    "prerequisites": ["paket"],
    "scenario": "Im Lager hängen Kameras, Gäste-WLAN, Büro-PCs und Drucker am "
                "selben Switch und sehen sich gegenseitig. Das ist ein Sicherheits- "
                "und Broadcast-Problem. Trennen wir sie mit VLANs — der **802.1Q-Tag** "
                "aus dem Modul Paketaufbau macht das möglich.",
```
(Die bestehende Zeile `"order": 1,` entfernen; `order` darf nur einmal vorkommen.)

- [ ] **Step 4: `GET /company`** — in `backend/app/routers/join.py` ergänzen
(Import oben: `from app.content.company import COMPANY`), neue Route ans Dateiende:

```python
@router.get("/company")
def company(p: Participant = Depends(get_participant)):
    return COMPANY
```

- [ ] **Step 5: Tests anpassen** — `backend/tests/test_content.py` ersetzen:

```python
from app.content import registry


def test_public_module_strips_answers_keeps_scenario():
    pub = registry.public_module("vlan")
    assert pub is not None
    for q in pub["quiz"]["questions"]:
        assert "answer" not in q
    assert pub["prerequisites"] == ["paket"]
    assert "scenario" in pub
    assert registry.MODULES["vlan"]["quiz"]["questions"][0]["answer"]


def test_module_meta_has_prereqs_and_order():
    metas = registry.module_meta()
    assert metas[0]["key"] == "paket"
    vlan = next(m for m in metas if m["key"] == "vlan")
    assert vlan["prerequisites"] == ["paket"]
    assert registry.public_module("nope") is None
```

(Dieser Test referenziert bereits `paket` — er wird erst nach Task 2 grün. Schritt 6
führt daher nur `vlan`-bezogene Teile aus; die volle Suite läuft am Ende von Task 2.)

- [ ] **Step 6: Teilprüfung + Commit**

```bash
cd backend && .venv/Scripts/python.exe -c "from app.content import registry; m=registry.module_meta(); print([x['key'] for x in m]); from app.content.company import COMPANY; print(COMPANY['name'])"
```
Expected: Ausgabe enthält `vlan` mit prereqs; `Nordwind Logistik GmbH`.
```bash
git add backend/app/content/company.py backend/app/content/registry.py backend/app/content/vlan.py backend/app/routers/join.py backend/tests/test_content.py
git commit -m "feat(content): Modul-Prerequisites/Scenario, Firmen-Steckbrief, VLAN-Retrofit"
```

---

### Task 2: Backend — Modul „Paketaufbau" (`paket`)

**Files:**
- Create: `backend/app/content/paket.py`
- Modify: `backend/app/content/registry.py` (registrieren)
- Modify: `backend/tests/test_courses_join.py` (Company-Test ergänzen)

**Interfaces:**
- Produces: Modul `paket` (order 1) mit Blöcken inkl. `widget id="frame-builder"` und 4-Fragen-Quiz; in `registry.MODULES` registriert.

- [ ] **Step 1: `backend/app/content/paket.py`**

```python
PAKET_MODULE = {
    "key": "paket",
    "title": "Paketaufbau / Frames",
    "order": 1,
    "pass_threshold": 0.7,
    "prerequisites": [],
    "scenario": "Bevor Nordwind die Geräte sauber trennen kann, müssen wir "
                "verstehen, wie zwei Geräte im Netz überhaupt miteinander reden — "
                "nämlich als **Frame** über das Kabel.",
    "blocks": [
        {"type": "text", "value": "## Schichten (ganz kurz)\n\nDaten reisen in "
            "Schichten: **Bitübertragung** (Kabel/Funk) → **Sicherung** (Ethernet, "
            "MAC-Adressen, *Frames*) → **Vermittlung** (IP, Routing) → **Transport** "
            "(TCP/UDP). Hier schauen wir auf die Sicherungsschicht: den **Ethernet-Frame**."},
        {"type": "text", "value": "## Der Ethernet-Frame\n\nEin Frame hat einen festen "
            "Aufbau. Die wichtigsten Felder:\n\n"
            "- **Ziel-MAC** (6 B): an wen geht der Frame.\n"
            "- **Quell-MAC** (6 B): von wem.\n"
            "- **EtherType** (2 B): was steckt im Payload (z.B. 0x0800 = IPv4).\n"
            "- **Payload** (46–1500 B): die Nutzdaten (z.B. ein IP-Paket).\n"
            "- **FCS** (4 B): Prüfsumme zur Fehlererkennung."},
        {"type": "widget", "id": "frame-builder"},
        {"type": "text", "value": "## Wo steckt das VLAN drin?\n\nEin VLAN wird über "
            "einen **802.1Q-Tag** markiert: 4 Byte, die **zwischen Quell-MAC und "
            "EtherType** eingefügt werden. Der Tag enthält die Kennung **0x8100** "
            "(TPID) und die **VLAN-ID**. So weiß jeder Switch, zu welchem VLAN ein "
            "Frame gehört — die Grundlage fürs nächste Problem bei Nordwind."},
    ],
    "quiz": {"questions": [
        {"id": "p1", "type": "single",
         "prompt": "Welches Feld steht im Ethernet-Frame ganz vorne (nach der Präambel)?",
         "options": ["Quell-MAC", "Ziel-MAC", "EtherType", "FCS"], "answer": "Ziel-MAC"},
        {"id": "p2", "type": "single",
         "prompt": "Wie groß ist eine MAC-Adresse?",
         "options": ["2 Byte", "4 Byte", "6 Byte", "8 Byte"], "answer": "6 Byte"},
        {"id": "p3", "type": "single",
         "prompt": "Wo wird der 802.1Q-VLAN-Tag eingefügt?",
         "options": ["vor der Ziel-MAC", "zwischen Quell-MAC und EtherType",
                     "im Payload", "im FCS"],
         "answer": "zwischen Quell-MAC und EtherType"},
        {"id": "p4", "type": "number",
         "prompt": "Wie viele Byte ist der 802.1Q-Tag groß?",
         "answer": 4},
    ]},
}
```

- [ ] **Step 2: registrieren** — in `backend/app/content/registry.py` Import + MODULES:

```python
from app.content.paket import PAKET_MODULE
from app.content.vlan import VLAN_MODULE

MODULES = {m["key"]: m for m in (PAKET_MODULE, VLAN_MODULE)}
```
(die alte `MODULES = {VLAN_MODULE["key"]: VLAN_MODULE}`-Zeile + den alten einzelnen Import ersetzen.)

- [ ] **Step 3: Company-Test ergänzen** — am Ende von `backend/tests/test_courses_join.py`:

```python
def test_company_endpoint():
    with TestClient(app) as c:
        h = _trainer(c)
        code = c.post("/api/courses", json={"name": "CoKurs"}, headers=h).json()["join_code"]
        tok = c.post("/api/join", json={"code": code, "name": "Cara"}).json()["access_token"]
        r = c.get("/api/company", headers={"Authorization": f"Bearer {tok}"})
        assert r.status_code == 200
        assert r.json()["name"] == "Nordwind Logistik GmbH"
```

- [ ] **Step 4: Volle Suite + Commit**

```bash
cd backend && rm -f test_intnetwork.db && .venv/Scripts/python.exe -m pytest -q
```
Expected: alle grün (test_content erwartet jetzt `paket` als erstes Modul).
```bash
git add backend/app/content/paket.py backend/app/content/registry.py backend/tests/test_courses_join.py
git commit -m "feat(content): Modul Paketaufbau (Frame + 802.1Q-Lage) + Company-Test"
```

---

### Task 3: Frontend — Firmen-Karte, Voraussetzungen, Scenario-Intro

**Files:**
- Modify: `frontend/src/types.ts` (Prereqs, scenario, Company)
- Modify: `frontend/src/lib/learnApi.ts` (`company`)
- Modify: `frontend/src/pages/LearnPage.tsx` (Firmen-Karte + „setzt voraus")
- Modify: `frontend/src/pages/ModulePage.tsx` (Scenario-Intro)

**Interfaces:**
- Consumes: `GET /company`, erweitertes `/modules` + `/modules/{key}`.
- Produces: `learnApi.company()`; Typen `Company`, `ModuleMeta.prerequisites`, `ModuleDetail.scenario`.

- [ ] **Step 1: `frontend/src/types.ts`** — Typen erweitern:

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
  scenario?: string
  prerequisites: string[]
  blocks: Block[]
  quiz: { questions: Question[] }
}

export interface ModuleMeta { key: string; title: string; order: number; prerequisites: string[] }
export interface ProgressItem { module_key: string; done: boolean; best: number | null }
export interface Company { name: string; blurb: string; sites: string[]; devices: string[] }
```

- [ ] **Step 2: `frontend/src/lib/learnApi.ts`** — `company` ergänzen:

```ts
import { api } from '@/lib/api'
import type { Company, ModuleDetail, ModuleMeta, ProgressItem } from '@/types'

export const learnApi = {
  me: () => api.get<{ name: string; course_id: number; progress: ProgressItem[] }>('/me'),
  company: () => api.get<Company>('/company'),
  listModules: () => api.get<ModuleMeta[]>('/modules'),
  getModule: (key: string) => api.get<ModuleDetail>(`/modules/${key}`),
  submitQuiz: (key: string, answers: Record<string, unknown>) =>
    api.post<{ score: number; total: number; passed: boolean; best: number }>(
      `/modules/${key}/quiz`, { answers }),
}
```

- [ ] **Step 3: `frontend/src/pages/LearnPage.tsx`** ersetzen:

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
  const company = useQuery({ queryKey: ['company'], queryFn: () => learnApi.company().then((r) => r.data) })

  if (role !== 'participant') { nav('/'); return null }

  const titleOf = (key: string) => mods.data?.find((m) => m.key === key)?.title ?? key
  const progressOf = (key: string) => me.data?.progress.find((p) => p.module_key === key)

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-slate-900">Hallo {displayName}</h1>
        <p className="text-slate-500 text-sm mb-6">Netzwerk-Grundlagen — am Beispiel einer echten Firma.</p>

        {company.data && (
          <div className="rounded-2xl border bg-white p-5 mb-8">
            <h2 className="font-semibold text-slate-900">{company.data.name}</h2>
            <p className="text-sm text-slate-600 mt-1">{company.data.blurb}</p>
            <p className="text-xs text-slate-500 mt-3">Standorte: {company.data.sites.join(', ')}</p>
            <div className="mt-2 flex flex-wrap gap-1.5">
              {company.data.devices.map((d) => (
                <span key={d} className="text-xs rounded-full bg-slate-100 text-slate-600 px-2 py-0.5">{d}</span>
              ))}
            </div>
          </div>
        )}

        <div className="flex flex-col gap-3">
          {mods.data?.map((m) => {
            const p = progressOf(m.key)
            return (
              <Link key={m.key} to={`/lernen/${m.key}`}
                className="rounded-xl border bg-white p-4 hover:shadow block">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-800">{m.title}</span>
                  <span className="text-sm text-slate-500">
                    {p?.done ? '✓ erledigt' : 'offen'}{p?.best != null ? ` · best ${p.best}%` : ''}
                  </span>
                </div>
                {m.prerequisites.length > 0 && (
                  <p className="text-xs text-slate-400 mt-1">setzt voraus: {m.prerequisites.map(titleOf).join(', ')}</p>
                )}
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 4: `frontend/src/pages/ModulePage.tsx`** ersetzen (Scenario-Intro):

```tsx
import { useQuery } from '@tanstack/react-query'
import Markdown from 'react-markdown'
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
        <h1 className="text-2xl font-bold text-slate-900 mt-2 mb-4">{mod.data.title}</h1>
        {mod.data.scenario && (
          <div className="rounded-xl border-l-4 border-indigo-400 bg-indigo-50 px-4 py-3 mb-6 text-sm text-slate-700">
            <Markdown>{mod.data.scenario}</Markdown>
          </div>
        )}
        <Blocks blocks={mod.data.blocks} />
        <Quiz moduleKey={key} questions={mod.data.quiz.questions} />
      </div>
    </div>
  )
}
```

- [ ] **Step 5: Build + Commit**

```bash
cd frontend && npx tsc -b && npm run build
```
Expected: Build ok.
```bash
git add frontend/src/types.ts frontend/src/lib/learnApi.ts frontend/src/pages/LearnPage.tsx frontend/src/pages/ModulePage.tsx
git commit -m "feat(frontend): Firmen-Karte, Voraussetzungen, Scenario-Intro"
```

---

### Task 4: Frontend — Frame-Builder-Widget

**Files:**
- Create: `frontend/src/widgets/FrameBuilder.tsx`
- Modify: `frontend/src/widgets/registry.tsx` (registrieren)

**Interfaces:**
- Produces: `FrameBuilder`-Komponente; Registry-Eintrag `'frame-builder'`.

- [ ] **Step 1: `frontend/src/widgets/FrameBuilder.tsx`**

```tsx
import { useMemo, useState } from 'react'

interface Field { key: string; name: string; bytes: string; desc: string; color: string }

const BASE: Field[] = [
  { key: 'dst', name: 'Ziel-MAC', bytes: '6 B', color: 'bg-blue-100 border-blue-400 text-blue-800',
    desc: 'Hardware-Adresse des Empfängers. Der Switch entscheidet anhand dieser Adresse, wohin der Frame geht.' },
  { key: 'src', name: 'Quell-MAC', bytes: '6 B', color: 'bg-sky-100 border-sky-400 text-sky-800',
    desc: 'Hardware-Adresse des Absenders.' },
  { key: 'type', name: 'EtherType', bytes: '2 B', color: 'bg-amber-100 border-amber-400 text-amber-800',
    desc: 'Welches Protokoll steckt im Payload? z.B. 0x0800 = IPv4, 0x0806 = ARP.' },
  { key: 'payload', name: 'Payload', bytes: '46–1500 B', color: 'bg-green-100 border-green-400 text-green-800',
    desc: 'Die Nutzdaten — typischerweise ein komplettes IP-Paket.' },
  { key: 'fcs', name: 'FCS', bytes: '4 B', color: 'bg-slate-100 border-slate-400 text-slate-700',
    desc: 'Frame Check Sequence: Prüfsumme zur Fehlererkennung.' },
]

export function FrameBuilder() {
  const [tagOn, setTagOn] = useState(false)
  const [vlanId, setVlanId] = useState(10)
  const [sel, setSel] = useState<string | null>(null)

  const fields = useMemo<Field[]>(() => {
    if (!tagOn) return BASE
    const tag: Field = {
      key: 'tag', name: '802.1Q-Tag', bytes: '4 B', color: 'bg-purple-100 border-purple-500 text-purple-800',
      desc: `Markiert den Frame für ein VLAN. Enthält TPID 0x8100 und die VLAN-ID (${vlanId}). ` +
            'Wird genau zwischen Quell-MAC und EtherType eingefügt.',
    }
    return [BASE[0], BASE[1], tag, ...BASE.slice(2)]
  }, [tagOn, vlanId])

  const selected = fields.find((f) => f.key === sel)

  return (
    <div className="rounded-2xl border bg-white p-5">
      <div className="flex items-center justify-between mb-3">
        <p className="text-sm font-semibold text-slate-700">Ethernet-Frame</p>
        <label className="flex items-center gap-2 text-xs text-slate-600">
          <input type="checkbox" checked={tagOn} onChange={(e) => setTagOn(e.target.checked)} />
          802.1Q-VLAN-Tag
        </label>
      </div>

      <div className="flex flex-wrap gap-1">
        {fields.map((f) => (
          <button key={f.key} onClick={() => setSel(f.key)}
            className={`rounded-lg border-2 px-3 py-2 text-xs font-medium ${f.color} ${sel === f.key ? 'ring-2 ring-indigo-500' : ''}`}>
            <div>{f.name}</div>
            <div className="opacity-70">{f.bytes}</div>
          </button>
        ))}
      </div>

      {tagOn && (
        <label className="block mt-3 text-xs text-slate-600">VLAN-ID:
          <input type="number" min={1} value={vlanId} onChange={(e) => setVlanId(Number(e.target.value))}
            className="ml-2 w-20 border rounded px-1" />
        </label>
      )}

      <div className="mt-4 rounded-lg bg-slate-50 border p-3 text-sm text-slate-700 min-h-[3.5rem]">
        {selected
          ? <><b>{selected.name}</b> ({selected.bytes}) — {selected.desc}</>
          : 'Klick auf ein Feld für die Erklärung. Schalte den 802.1Q-Tag ein, um zu sehen, wo das VLAN im Frame steht.'}
      </div>
    </div>
  )
}
```

- [ ] **Step 2: `frontend/src/widgets/registry.tsx`** ersetzen:

```tsx
import type { ComponentType } from 'react'
import { VlanSwitch } from '@/widgets/VlanSwitch'
import { FrameBuilder } from '@/widgets/FrameBuilder'

export const WIDGETS: Record<string, ComponentType> = {
  'vlan-switch': VlanSwitch,
  'frame-builder': FrameBuilder,
}
```

- [ ] **Step 3: Build + Commit**

```bash
cd frontend && npx tsc -b && npm run build
```
Expected: Build ok.
```bash
git add frontend/src/widgets/FrameBuilder.tsx frontend/src/widgets/registry.tsx
git commit -m "feat(frontend): Frame-Builder-Widget (Ethernet-Frame + 802.1Q-Tag)"
```

---

### Task 5: Gesamt-Verifikation

- [ ] **Step 1: Backend-Tests**

```bash
cd backend && rm -f test_intnetwork.db && .venv/Scripts/python.exe -m pytest -q
```
Expected: alle grün.

- [ ] **Step 2: Frontend Build**

```bash
cd frontend && npx tsc -b && npm run build
```
Expected: Build ok.

- [ ] **Step 3: Manueller Smoke (lokal)**

Backend (uvicorn, `SECRET_KEY`+`ADMIN_PASSWORD` gesetzt) + Frontend (`npm run dev`):
Als Teilnehmer beitreten → Lern-Startseite zeigt **Nordwind-Karte**; Modul-Liste:
zuerst **Paketaufbau**, dann **VLANs** mit „setzt voraus: Paketaufbau". Modul
Paketaufbau: Story-Intro, Frame-Builder (Feld anklicken erklärt, 802.1Q-Schalter
fügt Tag zwischen Quell-MAC und EtherType ein), Quiz bestehen. VLAN-Modul zeigt
sein Scenario.

- [ ] **Step 4:** Keine weitere Commit nötig (Tasks haben committet).
