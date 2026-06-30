# Modul „MAC & Switching" Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Inhalts-Modul `switching` (order 2) mit interaktivem MAC-Learning-Widget + Quiz; VLAN rückt logisch dahinter.

**Architecture:** Backend-Modul-Dict + Registry; Frontend pure `macLearning.ts` (Vitest) + `MacLearning.tsx`-Widget.

**Tech Stack:** FastAPI/SQLite/Pytest; React/TS/Vite/Tailwind/Vitest.

## Global Constraints

- `switching` order 2, prereq `["paket"]`; `vlan` prereq wird `["paket","switching"]`.
- Quiz-Lösungen serverseitig; Widget pure-Logik Vitest-getestet; strict TS.

---

### Task 1: Backend — Modul `switching` + VLAN-Prereq

**Files:** Create `backend/app/content/switching.py`; Modify `registry.py`, `vlan.py`, `tests/test_content.py`.

- [ ] **Step 1: `backend/app/content/switching.py`**

```python
SWITCHING_MODULE = {
    "key": "switching",
    "title": "MAC & Switching",
    "order": 2,
    "pass_threshold": 0.7,
    "prerequisites": ["paket"],
    "scenario": "Bei Nordwind hängen alle Geräte an einem flachen Switch — trotzdem "
                "landet nicht jeder Frame bei jedem. Wie findet der Switch heraus, an "
                "welchem Port ein Gerät hängt?",
    "blocks": [
        {"type": "text", "value": "## MAC-Adressen\n\nJede Netzwerkkarte hat eine "
            "eindeutige **MAC-Adresse** (Schicht 2). Ein Switch arbeitet mit diesen "
            "Adressen — nicht mit IPs."},
        {"type": "text", "value": "## Lernen & Weiterleiten\n\nDer Switch führt eine "
            "**MAC-Adresstabelle** (`MAC → Port`).\n\n"
            "- **Lernen:** aus jedem ankommenden Frame merkt er sich die **Quell-MAC** "
            "am **Eingangs-Port**.\n"
            "- **Bekanntes Ziel:** Frame nur an den passenden Port (**Unicast**).\n"
            "- **Unbekanntes Ziel:** Frame an **alle** anderen Ports (**Flooding**); "
            "antwortet das Ziel, ist es danach gelernt."},
        {"type": "widget", "id": "mac-learning"},
        {"type": "text", "value": "## Broadcast & der Haken\n\nEin **Broadcast** "
            "(`FF:FF:FF:FF:FF:FF`) geht **immer** an alle Ports. Ein flacher Switch "
            "**trennt nichts** — jedes Gerät kann jedes erreichen. Genau dieses Problem "
            "lösen als Nächstes die **VLANs**."},
    ],
    "quiz": {"questions": [
        {"id": "s1", "type": "single",
         "prompt": "Was lernt ein Switch aus einem ankommenden Frame?",
         "options": ["Die Ziel-IP", "Quell-MAC und Eingangs-Port", "Nichts", "Die VLAN-ID"],
         "answer": "Quell-MAC und Eingangs-Port"},
        {"id": "s2", "type": "single",
         "prompt": "Was macht der Switch, wenn die Ziel-MAC unbekannt ist?",
         "options": ["Frame verwerfen", "An alle anderen Ports fluten", "Nur an Port 1", "Zurück an den Absender"],
         "answer": "An alle anderen Ports fluten"},
        {"id": "s3", "type": "single",
         "prompt": "Auf welcher OSI-Schicht arbeitet ein klassischer Switch?",
         "options": ["Schicht 1 (Bitübertragung)", "Schicht 2 (Sicherung)", "Schicht 3 (Vermittlung)", "Schicht 4 (Transport)"],
         "answer": "Schicht 2 (Sicherung)"},
        {"id": "s4", "type": "single",
         "prompt": "Wohin geht ein Broadcast (FF:FF:FF:FF:FF:FF)?",
         "options": ["An keinen Port", "Nur an den Absender", "An alle Ports im selben Netz", "An den Router"],
         "answer": "An alle Ports im selben Netz"},
    ]},
}
```

- [ ] **Step 2: `registry.py`** — Import + MODULES:

```python
from app.content.paket import PAKET_MODULE
from app.content.switching import SWITCHING_MODULE
from app.content.vlan import VLAN_MODULE

MODULES = {m["key"]: m for m in (PAKET_MODULE, SWITCHING_MODULE, VLAN_MODULE)}
```
(alte paket/vlan-Import + MODULES-Zeile ersetzen.)

- [ ] **Step 3: `vlan.py`** — Prereq erweitern: `"prerequisites": ["paket"],` → `"prerequisites": ["paket", "switching"],`.

- [ ] **Step 4: `tests/test_content.py`** — die vlan-Prereq-Assertions auf `["paket", "switching"]` ändern und Switching prüfen. Ersetze beide Tests:

```python
def test_public_module_strips_answers_keeps_scenario():
    pub = registry.public_module("vlan")
    assert pub is not None
    for q in pub["quiz"]["questions"]:
        assert "answer" not in q
    assert pub["prerequisites"] == ["paket", "switching"]
    assert "scenario" in pub
    assert registry.MODULES["vlan"]["quiz"]["questions"][0]["answer"]


def test_module_meta_has_prereqs_and_order():
    metas = registry.module_meta()
    assert metas[0]["key"] == "paket"
    assert any(m["key"] == "switching" and m["order"] == 2 for m in metas)
    vlan = next(m for m in metas if m["key"] == "vlan")
    assert vlan["prerequisites"] == ["paket", "switching"]
    assert registry.public_module("nope") is None
```

- [ ] **Step 5: Lauf + Commit**

```bash
cd backend && rm -f test_intnetwork.db && .venv/Scripts/python.exe -m pytest -q
git add backend/app/content/switching.py backend/app/content/registry.py backend/app/content/vlan.py backend/tests/test_content.py
git commit -m "feat(content): Modul MAC & Switching + VLAN-Prereq erweitert"
```

---

### Task 2: Frontend — MAC-Learning pure Logik + Vitest

**Files:** Create `frontend/src/widgets/switch/macLearning.ts`, `macLearning.test.ts`.

- [ ] **Step 1: Test** — `frontend/src/widgets/switch/macLearning.test.ts`:

```ts
import { describe, it, expect } from 'vitest'
import { learnStep, HOSTS } from './macLearning'

const macA = HOSTS[0].mac
const macB = HOSTS[1].mac

describe('learnStep', () => {
  it('unbekanntes Ziel -> Flooding an alle außer Quelle', () => {
    const r = learnStep({}, 1, macB)
    expect(r.flooded).toBe(true)
    expect(r.delivered).toEqual([2, 3, 4])
    expect(r.table[macA]).toBe(1)
  })

  it('bekanntes Ziel -> Unicast', () => {
    const r = learnStep({ [macA]: 1 }, 2, macA)
    expect(r.flooded).toBe(false)
    expect(r.delivered).toEqual([1])
    expect(r.table[macB]).toBe(2)
  })
})
```

- [ ] **Step 2: Implementieren** — `frontend/src/widgets/switch/macLearning.ts`:

```ts
export interface Host { port: number; name: string; mac: string }

export const HOSTS: Host[] = [
  { port: 1, name: 'PC-A', mac: 'AA:00:00:00:00:01' },
  { port: 2, name: 'PC-B', mac: 'AA:00:00:00:00:02' },
  { port: 3, name: 'Drucker', mac: 'AA:00:00:00:00:03' },
  { port: 4, name: 'Kamera', mac: 'AA:00:00:00:00:04' },
]

export interface LearnResult {
  table: Record<string, number>
  delivered: number[]
  flooded: boolean
  learnedMac: string
}

export function learnStep(table: Record<string, number>, srcPort: number, dstMac: string): LearnResult {
  const src = HOSTS.find((h) => h.port === srcPort)!
  const next = { ...table, [src.mac]: srcPort }
  const known = next[dstMac]
  if (known !== undefined && known !== srcPort) {
    return { table: next, delivered: [known], flooded: false, learnedMac: src.mac }
  }
  const delivered = HOSTS.map((h) => h.port).filter((p) => p !== srcPort)
  return { table: next, delivered, flooded: true, learnedMac: src.mac }
}
```

- [ ] **Step 3: Lauf + Commit**

```bash
cd frontend && npx vitest run src/widgets/switch/macLearning.test.ts
git add frontend/src/widgets/switch/macLearning.ts frontend/src/widgets/switch/macLearning.test.ts
git commit -m "feat(switching): pure MAC-Learning-Logik + Vitest"
```

---

### Task 3: Frontend — MacLearning-Widget + Registry

**Files:** Create `frontend/src/widgets/switch/MacLearning.tsx`; Modify `registry.tsx`.

- [ ] **Step 1: `frontend/src/widgets/switch/MacLearning.tsx`**

```tsx
import { useState } from 'react'
import { HOSTS, learnStep, type LearnResult } from '@/widgets/switch/macLearning'

export function MacLearning() {
  const [table, setTable] = useState<Record<string, number>>({})
  const [src, setSrc] = useState(1)
  const [dst, setDst] = useState(2)
  const [last, setLast] = useState<LearnResult | null>(null)

  function send() {
    if (src === dst) return
    const dstMac = HOSTS.find((h) => h.port === dst)!.mac
    const r = learnStep(table, src, dstMac)
    setTable(r.table)
    setLast(r)
  }

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">Switch — MAC-Lernen</p>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4">
        {HOSTS.map((h) => {
          const lit = last?.delivered.includes(h.port)
          const isSrc = last && src === h.port
          return (
            <div key={h.port}
              className={`rounded-xl border-2 p-2 text-xs ${isSrc ? 'border-teal-500 bg-teal-50' : lit ? 'border-amber-400 bg-amber-50' : 'border-slate-200 bg-white'}`}>
              <div className="font-semibold text-slate-700">Port {h.port} · {h.name}</div>
              <div className="font-mono text-[10px] text-slate-500">{h.mac}</div>
            </div>
          )
        })}
      </div>

      <div className="flex flex-wrap items-end gap-2">
        <label className="text-xs text-slate-600">Von
          <select value={src} onChange={(e) => setSrc(Number(e.target.value))} className="ml-1 border rounded px-1 py-0.5">
            {HOSTS.map((h) => <option key={h.port} value={h.port}>{h.name}</option>)}
          </select>
        </label>
        <label className="text-xs text-slate-600">An
          <select value={dst} onChange={(e) => setDst(Number(e.target.value))} className="ml-1 border rounded px-1 py-0.5">
            {HOSTS.map((h) => <option key={h.port} value={h.port}>{h.name}</option>)}
          </select>
        </label>
        <button onClick={send} disabled={src === dst}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium disabled:opacity-50">
          Frame senden
        </button>
        <button onClick={() => { setTable({}); setLast(null) }}
          className="rounded-lg border px-3 py-1.5 text-sm">Tabelle leeren</button>
      </div>

      {last && (
        <p className="mt-3 text-xs text-slate-600">
          {last.flooded
            ? `Ziel unbekannt → Flooding an Ports ${last.delivered.join(', ')}. Quell-MAC am Port ${src} gelernt.`
            : `Ziel bekannt → Unicast an Port ${last.delivered[0]}.`}
        </p>
      )}

      <div className="mt-4">
        <p className="text-xs font-semibold text-slate-500 mb-1">MAC-Adresstabelle</p>
        <div className="rounded-lg border divide-y text-xs font-mono">
          {Object.keys(table).length === 0
            ? <div className="px-3 py-2 text-slate-400">leer</div>
            : Object.entries(table).map(([mac, port]) => (
              <div key={mac} className="flex justify-between px-3 py-1.5">
                <span className="text-slate-700">{mac}</span><span className="text-slate-500">Port {port}</span>
              </div>
            ))}
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 2: `registry.tsx`** ergänzen:

```tsx
import { MacLearning } from '@/widgets/switch/MacLearning'
```
und im `WIDGETS`-Objekt `'mac-learning': MacLearning,` hinzufügen.

- [ ] **Step 3: Build + Commit**

```bash
cd frontend && npx tsc -b && npm run build
git add frontend/src/widgets/switch/MacLearning.tsx frontend/src/widgets/registry.tsx
git commit -m "feat(switching): MAC-Learning-Widget + Registry"
```

---

### Task 4: Verifikation

- [ ] **Step 1:** `cd backend && rm -f test_intnetwork.db && .venv/Scripts/python.exe -m pytest -q` → grün.
- [ ] **Step 2:** `cd frontend && npx vitest run && npx tsc -b && npm run build` → grün.
- [ ] **Step 3:** Manueller Smoke: Modul-Liste zeigt Paketaufbau → **MAC & Switching** → VLANs (VLAN „setzt voraus: Paketaufbau, MAC & Switching"). Widget: „Frame senden" an unbekanntes Ziel flutet, Tabelle füllt sich, danach Unicast.
