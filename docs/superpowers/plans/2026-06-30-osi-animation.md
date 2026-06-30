# OSI-Schichtenmodell-Animation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ein animiertes, interaktives OSI-Widget im Paketaufbau-Modul, das Encapsulation (Senden) und Decapsulation (Empfangen) über 7 Schichten zeigt.

**Architecture:** Pure Schritt-Logik (`osiModel.ts`, Vitest-getestet) erzeugt die geordnete Animations-Schrittliste; die Komponente `OsiModel.tsx` rendert zwei Schicht-Stacks + wandernden PDU-Block + Steuerung. Im Backend wird der knappe Schichten-Text durch eine Einleitung + `widget id="osi-model"` ersetzt.

**Tech Stack:** React/TS/Vite/Tailwind, Vitest. Backend-Content (Python-Dict).

## Global Constraints

- Volle **7 OSI-Schichten**; Sender + Empfänger nebeneinander (schmal: untereinander).
- Pure Schritt-Logik ohne React/DOM → Vitest-testbar.
- Encapsulation: L4 +TCP (Segment), L3 +IP (Paket), L2 +ETH/+FCS (Frame); L7–5 = „Daten".
- Frontend strict TS, keine `any`.

---

### Task 1: Pure OSI-Schritt-Logik + Vitest

**Files:**
- Create: `frontend/src/widgets/osi/osiModel.ts`, `frontend/src/widgets/osi/osiModel.test.ts`

**Interfaces:**
- Produces: `Layer`, `LAYERS: Layer[]`, `Step` (`{side:'tx'|'rx'; layer:number; pieces:string[]; caption:string}`), `buildSteps(): Step[]`.

- [ ] **Step 1: Test** — `frontend/src/widgets/osi/osiModel.test.ts`:

```ts
import { describe, it, expect } from 'vitest'
import { buildSteps, LAYERS } from './osiModel'

describe('osiModel', () => {
  it('hat 7 Schichten', () => {
    expect(LAYERS.map((l) => l.nr)).toEqual([7, 6, 5, 4, 3, 2, 1])
  })

  it('buildSteps: 14 Schritte (7 tx + 7 rx)', () => {
    const s = buildSteps()
    expect(s).toHaveLength(14)
    expect(s.filter((x) => x.side === 'tx')).toHaveLength(7)
  })

  it('Start = Sender Schicht 7 mit nur Daten', () => {
    const s = buildSteps()[0]
    expect(s.side).toBe('tx')
    expect(s.layer).toBe(7)
    expect(s.pieces).toEqual(['Daten'])
  })

  it('Sender Schicht 2 ist ein vollständiger Frame', () => {
    const s = buildSteps().find((x) => x.side === 'tx' && x.layer === 2)!
    expect(s.pieces).toEqual(['ETH', 'IP', 'TCP', 'Daten', 'FCS'])
  })

  it('Empfänger Schicht 7 hat wieder nur Daten', () => {
    const s = buildSteps().at(-1)!
    expect(s.side).toBe('rx')
    expect(s.layer).toBe(7)
    expect(s.pieces).toEqual(['Daten'])
  })
})
```

- [ ] **Step 2: Lauf, Fehlschlag**

Run: `cd frontend && npx vitest run src/widgets/osi/osiModel.test.ts`
Expected: FAIL (Modul fehlt).

- [ ] **Step 3: Implementieren** — `frontend/src/widgets/osi/osiModel.ts`:

```ts
export interface Layer {
  nr: number; de: string; en: string; task: string; example: string; pdu: string
}

export const LAYERS: Layer[] = [
  { nr: 7, de: 'Anwendung', en: 'Application', task: 'Dienste für Anwendungen', example: 'HTTP, DNS', pdu: 'Daten' },
  { nr: 6, de: 'Darstellung', en: 'Presentation', task: 'Codierung, Verschlüsselung', example: 'TLS, UTF-8', pdu: 'Daten' },
  { nr: 5, de: 'Sitzung', en: 'Session', task: 'Sitzungen auf-/abbauen', example: 'Sessions', pdu: 'Daten' },
  { nr: 4, de: 'Transport', en: 'Transport', task: 'Ende-zu-Ende, Ports', example: 'TCP, UDP', pdu: 'Segment' },
  { nr: 3, de: 'Vermittlung', en: 'Network', task: 'Adressierung, Routing', example: 'IP', pdu: 'Paket' },
  { nr: 2, de: 'Sicherung', en: 'Data Link', task: 'Rahmen, MAC-Adressen', example: 'Ethernet, 802.1Q', pdu: 'Frame' },
  { nr: 1, de: 'Bitübertragung', en: 'Physical', task: 'Bits über das Medium', example: 'Kabel, Funk', pdu: 'Bits' },
]

export interface Step { side: 'tx' | 'rx'; layer: number; pieces: string[]; caption: string }

function txPieces(layer: number): string[] {
  if (layer >= 5) return ['Daten']
  if (layer === 4) return ['TCP', 'Daten']
  if (layer === 3) return ['IP', 'TCP', 'Daten']
  return ['ETH', 'IP', 'TCP', 'Daten', 'FCS'] // L2, L1
}

function rxPieces(layer: number): string[] {
  if (layer === 1) return ['ETH', 'IP', 'TCP', 'Daten', 'FCS']
  if (layer === 2) return ['IP', 'TCP', 'Daten']
  if (layer === 3) return ['TCP', 'Daten']
  return ['Daten'] // L4..L7
}

const TX_CAP: Record<number, string> = {
  7: 'Schicht 7: Anwendung erzeugt die Daten (z.B. HTTP-Anfrage).',
  6: 'Schicht 6: Darstellung — Codierung/Verschlüsselung.',
  5: 'Schicht 5: Sitzung verwaltet die Verbindung.',
  4: 'Schicht 4: Transport hängt den TCP-Header an → Segment.',
  3: 'Schicht 3: Vermittlung hängt den IP-Header an → Paket.',
  2: 'Schicht 2: Sicherung hängt Ethernet-Header + FCS an → Frame.',
  1: 'Schicht 1: Bitübertragung sendet die Bits über das Medium.',
}
const RX_CAP: Record<number, string> = {
  1: 'Empfänger Schicht 1: Bits kommen an.',
  2: 'Empfänger Schicht 2: Ethernet-Header/FCS entfernt → Paket.',
  3: 'Empfänger Schicht 3: IP-Header entfernt → Segment.',
  4: 'Empfänger Schicht 4: TCP-Header entfernt → Daten.',
  5: 'Empfänger Schicht 5: Sitzung übergibt nach oben.',
  6: 'Empfänger Schicht 6: Darstellung dekodiert.',
  7: 'Empfänger Schicht 7: Anwendung erhält die Daten.',
}

export function buildSteps(): Step[] {
  const steps: Step[] = []
  for (let nr = 7; nr >= 1; nr--) {
    steps.push({ side: 'tx', layer: nr, pieces: txPieces(nr), caption: TX_CAP[nr] })
  }
  for (let nr = 1; nr <= 7; nr++) {
    steps.push({ side: 'rx', layer: nr, pieces: rxPieces(nr), caption: RX_CAP[nr] })
  }
  return steps
}
```

- [ ] **Step 4: Lauf, grün + Commit**

Run: `cd frontend && npx vitest run src/widgets/osi/osiModel.test.ts`
Expected: 5 passed.
```bash
git add frontend/src/widgets/osi/osiModel.ts frontend/src/widgets/osi/osiModel.test.ts
git commit -m "feat(osi): pure Schritt-Logik (Encapsulation/Decapsulation) + Vitest"
```

---

### Task 2: OSI-Widget + Registry + Backend-Einbindung

**Files:**
- Create: `frontend/src/widgets/osi/OsiModel.tsx`
- Modify: `frontend/src/widgets/registry.tsx`
- Modify: `backend/app/content/paket.py`

**Interfaces:**
- Consumes: `LAYERS`, `buildSteps`, `Step`, `Layer`.
- Produces: Widget-Registry-Eintrag `'osi-model'`.

- [ ] **Step 1: `frontend/src/widgets/osi/OsiModel.tsx`**

```tsx
import { useEffect, useMemo, useState } from 'react'
import { LAYERS, buildSteps, type Layer } from '@/widgets/osi/osiModel'

const PIECE_COLOR: Record<string, string> = {
  Daten: 'bg-green-200 text-green-900',
  TCP: 'bg-amber-200 text-amber-900',
  IP: 'bg-sky-200 text-sky-900',
  ETH: 'bg-purple-200 text-purple-900',
  FCS: 'bg-slate-300 text-slate-700',
}

function Stack({ side, activeLayer, onPick }: {
  side: 'tx' | 'rx'; activeLayer: number | null; onPick: (l: Layer) => void
}) {
  return (
    <div className="flex flex-col gap-1">
      <p className="text-xs font-semibold text-slate-500 mb-1">{side === 'tx' ? 'Sender' : 'Empfänger'}</p>
      {LAYERS.map((l) => (
        <button key={l.nr} onClick={() => onPick(l)}
          className={`rounded-md border px-2 py-1.5 text-left text-xs transition-colors
            ${activeLayer === l.nr ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-slate-700 hover:bg-slate-50'}`}>
          <span className="font-mono">{l.nr}</span> {l.de}
        </button>
      ))}
    </div>
  )
}

export function OsiModel() {
  const steps = useMemo(() => buildSteps(), [])
  const [i, setI] = useState(0)
  const [playing, setPlaying] = useState(false)
  const [pick, setPick] = useState<Layer | null>(null)

  const cur = steps[i]

  useEffect(() => {
    if (!playing) return
    if (i >= steps.length - 1) { setPlaying(false); return }
    const t = setTimeout(() => setI((x) => x + 1), 1200)
    return () => clearTimeout(t)
  }, [playing, i, steps.length])

  return (
    <div className="rounded-2xl border bg-white p-5">
      <div className="grid grid-cols-1 sm:grid-cols-[1fr_auto_1fr] gap-4 items-start">
        <Stack side="tx" activeLayer={cur.side === 'tx' ? cur.layer : null} onPick={setPick} />

        <div className="flex flex-col items-center justify-center min-h-[10rem] px-2">
          <div className="flex gap-0.5">
            {cur.pieces.map((p, idx) => (
              <span key={idx} className={`rounded px-1.5 py-1 text-[10px] font-mono font-semibold ${PIECE_COLOR[p] ?? 'bg-slate-200'}`}>{p}</span>
            ))}
          </div>
          <p className="text-[11px] text-slate-400 mt-2">{cur.side === 'tx' ? '↓ Encapsulation' : '↑ Decapsulation'}</p>
        </div>

        <Stack side="rx" activeLayer={cur.side === 'rx' ? cur.layer : null} onPick={setPick} />
      </div>

      <p className="mt-4 rounded-lg bg-slate-50 border px-3 py-2 text-sm text-slate-700">{cur.caption}</p>

      <div className="mt-3 flex items-center gap-2">
        <button onClick={() => setPlaying((p) => !p)} disabled={i >= steps.length - 1 && !playing}
          className="rounded-lg bg-indigo-600 text-white px-3 py-1.5 text-sm font-medium disabled:opacity-50">
          {playing ? 'Pause' : 'Abspielen'}
        </button>
        <button onClick={() => { setPlaying(false); setI((x) => Math.min(x + 1, steps.length - 1)) }}
          className="rounded-lg border px-3 py-1.5 text-sm">Schritt</button>
        <button onClick={() => { setPlaying(false); setI(0) }}
          className="rounded-lg border px-3 py-1.5 text-sm">Zurücksetzen</button>
        <span className="text-xs text-slate-400">Schritt {i + 1}/{steps.length}</span>
      </div>

      {pick && (
        <div className="mt-3 rounded-lg border-l-4 border-indigo-400 bg-indigo-50 px-3 py-2 text-sm text-slate-700">
          <b>Schicht {pick.nr}: {pick.de}</b> ({pick.en}) — {pick.task}. Beispiel: {pick.example}. PDU: {pick.pdu}.
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 2: Registry** — `frontend/src/widgets/registry.tsx` ersetzen:

```tsx
import type { ComponentType } from 'react'
import { VlanSwitch } from '@/widgets/VlanSwitch'
import { FrameBuilder } from '@/widgets/FrameBuilder'
import { OsiModel } from '@/widgets/osi/OsiModel'

export const WIDGETS: Record<string, ComponentType> = {
  'vlan-switch': VlanSwitch,
  'frame-builder': FrameBuilder,
  'osi-model': OsiModel,
}
```

- [ ] **Step 3: Backend-Einbindung** — in `backend/app/content/paket.py` den ersten
Block (`## Schichten (ganz kurz)` …) ersetzen durch Einleitung + Widget:

```python
        {"type": "text", "value": "## Das OSI-Schichtenmodell\n\nNetzwerk-Kommunikation "
            "ist in **7 Schichten** organisiert. Beim Senden wandern die Daten von oben "
            "nach unten — jede Schicht hängt ihre Information an (*Encapsulation*); beim "
            "Empfänger wird Schicht für Schicht wieder ausgepackt. Spiel es durch und "
            "klick auf die Schichten:"},
        {"type": "widget", "id": "osi-model"},
```

- [ ] **Step 4: Build + Commit**

```bash
cd frontend && npx tsc -b && npm run build
```
Expected: Build ok.
```bash
git add frontend/src/widgets/osi/OsiModel.tsx frontend/src/widgets/registry.tsx backend/app/content/paket.py
git commit -m "feat(osi): animiertes OSI-Widget + Einbindung im Paketaufbau-Modul"
```

---

### Task 3: Verifikation

- [ ] **Step 1: Frontend Tests + Build**

```bash
cd frontend && npx vitest run && npx tsc -b && npm run build
```
Expected: Vitest grün (alt + osiModel), Build ok.

- [ ] **Step 2: Backend-Sanity** (Content lädt)

```bash
cd backend && SECRET_KEY=test-secret-key-not-the-default-0123456789 .venv/Scripts/python.exe -c "from app.content.registry import public_module; m=public_module('paket'); print([b.get('id') or b['type'] for b in m['blocks']])"
```
Expected: Liste enthält `osi-model` und `frame-builder`.

- [ ] **Step 3: Manueller Smoke**

Paketaufbau-Modul öffnen → OSI-Widget: „Abspielen" lässt den PDU-Block beim
Sender wachsen (Daten → +TCP → +IP → +ETH/FCS), nach unten, dann beim Empfänger
schrumpfen; aktive Schicht hervorgehoben, Caption passt; Klick auf eine Schicht
zeigt Details. „Schritt" und „Zurücksetzen" funktionieren.

- [ ] **Step 4:** Keine weitere Commit nötig.
