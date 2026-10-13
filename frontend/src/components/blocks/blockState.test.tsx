// @vitest-environment jsdom
//
// Zustand der Blöcke gegen wechselnden Inhalt: Folienwechsel im Beamer-Modus,
// Content-Update bei offenem Modul, Sprachwechsel, unpassender gemerkter Stand.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { Blocks } from '@/components/Blocks'
import { TrainerBlocks } from '@/components/TrainerBlocks'
import { fingerprint } from '@/lib/exerciseState'
import { PrintContext } from '@/lib/printMode'
import type { Block } from '@/types'

const KEY = 'intnetwork-exercise-1-9-arp'
const FAILED = 'Dieses interaktive Element konnte nicht geladen werden.'
const seq = (title: string, n: number, uid?: string): Block => ({
  uid, type: 'diagram', kind: 'sequence', title,
  actors: [{ id: 'a', label: 'A' }, { id: 'b', label: 'B' }],
  messages: Array.from({ length: n }, (_, i) => ({ from: 'a', to: 'b', label: `${title}-${i + 1}` })),
})
const show = (blocks: Block[], lang: 'de' | 'en' = 'de') => <Blocks blocks={blocks} lang={lang} moduleKey="arp" keyScope="1-9" />
const store = (uid: string, block: Block, s: unknown, done = false) =>
  localStorage.setItem(KEY, JSON.stringify({ ...JSON.parse(localStorage.getItem(KEY) ?? '{}'), [uid]: { v: fingerprint(block), s, done } }))

beforeEach(() => { localStorage.clear(); vi.spyOn(console, 'error').mockImplementation(() => {}) })
afterEach(() => { cleanup(); vi.restoreAllMocks() })

describe('Folienwechsel (TrainerBlocks mit einem Block je Folie)', () => {
  it('zweites Sequenzdiagramm startet bei Schritt 1 statt mit dem Schritt der vorigen Folie abzustürzen', async () => {
    const { rerender } = render(<TrainerBlocks blocks={[seq('Lang', 6)]} />)
    const next = await screen.findByRole('button', { name: /Weiter/ })
    for (let i = 0; i < 5; i++) fireEvent.click(next)
    expect(screen.getByText('Schritt 6 / 6')).toBeTruthy()

    rerender(<TrainerBlocks blocks={[seq('Kurz', 2)]} />)
    expect(await screen.findByText('Schritt 1 / 2')).toBeTruthy()
    expect(screen.queryByText(FAILED)).toBeNull()
  })

  it('ein abgestürzter Block blockiert die nächste Folie nicht (ErrorBoundary setzt sich zurück)', async () => {
    const broken = { type: 'diagram', kind: 'sequence', title: 'Kaputt', actors: [], messages: null } as unknown as Block
    const { rerender } = render(<TrainerBlocks blocks={[broken]} />)
    expect(await screen.findByText(FAILED)).toBeTruthy()
    rerender(<TrainerBlocks blocks={[seq('Heil', 2)]} />)
    expect(await screen.findByText('Schritt 1 / 2')).toBeTruthy()
  })
})

describe('<Blocks> mit geändertem Inhalt neu gerendert', () => {
  it('ein anderer Check am selben Index übernimmt weder Antwort noch Speicherstand', () => {
    const a: Block = { type: 'check', prompt: 'A?', options: ['ja', 'nein'], answer: 0 }
    const b: Block = { type: 'check', prompt: 'B?', options: ['x', 'y', 'z'], answer: 0 }
    const { rerender } = render(show([a]))
    fireEvent.click(screen.getByRole('button', { name: 'ja' }))
    expect(screen.getByText('Richtig')).toBeTruthy()

    rerender(show([b]))
    expect(screen.queryByText('Richtig')).toBeNull()
    expect((screen.getByRole('button', { name: 'x' }) as HTMLButtonElement).disabled).toBe(false)
    expect(JSON.parse(localStorage.getItem(KEY)!)['check-0'].v).toBe(fingerprint(a))
  })

  it('gekürztes Diagramm und geänderte Zuordnung stürzen nicht ab', async () => {
    const match = (n: number): Block => ({ uid: 'm', type: 'match', prompt: 'Ordne zu', pairs: Array.from({ length: n }, (_, i) => ({ left: `L${i}`, right: `R${i}` })) })
    const { rerender } = render(show([seq('D', 6, 'd'), match(4)]))
    const next = await screen.findByRole('button', { name: /Weiter/ })
    for (let i = 0; i < 5; i++) fireEvent.click(next)
    fireEvent.click(await screen.findByRole('button', { name: /R3/ }))

    rerender(show([seq('D', 2, 'd'), match(2)]))
    expect(await screen.findByText('Schritt 1 / 2')).toBeTruthy()
    expect(await screen.findByRole('button', { name: /^L1/ })).toBeTruthy()
    expect(screen.queryByText(FAILED)).toBeNull()
  })

  it('Blöcke hängen an ihrer uid: ein davor eingefügter Block lässt den Zustand beim richtigen Block', () => {
    const c: Block = { uid: 'c1', type: 'check', prompt: 'A?', options: ['ja', 'nein'], answer: 0 }
    const { rerender, container } = render(show([c]))
    fireEvent.click(screen.getByRole('button', { name: 'ja' }))
    rerender(show([{ uid: 'c0', type: 'check', prompt: 'Neu?', options: ['u', 'v'], answer: 1 }, c]))
    expect(container.querySelector('[data-uid="c1"]')!.textContent).toContain('Richtig')
    expect(container.querySelector('[data-uid="c0"]')!.querySelectorAll('button:disabled')).toHaveLength(0)
  })
})

describe('gemerkter Stand, der nicht (mehr) zum Inhalt passt', () => {
  it('Diagramm: Schritt wird geklemmt', async () => {
    const d = seq('D', 2, 'd')
    store('d', d, 99)
    render(show([d]))
    expect(await screen.findByText('Schritt 2 / 2')).toBeTruthy()
  })

  it('Flow-Diagramm: Schritt wird geklemmt', async () => {
    const f: Block = {
      uid: 'f', type: 'diagram', kind: 'flow', title: 'F',
      nodes: [{ id: 'a', label: 'A', row: 0, col: 0 }, { id: 'b', label: 'B', row: 0, col: 1 }],
      steps: [{ highlight: ['a'], text: 'eins' }, { highlight: ['b'], text: 'zwei' }],
    }
    store('f', f, 7)
    render(show([f]))
    expect(await screen.findByText('zwei')).toBeTruthy()
  })

  it('Zuordnung: falsche Paarzahl -> Neustart', async () => {
    const m: Block = { uid: 'm', type: 'match', prompt: 'Ordne zu', pairs: [{ left: 'L0', right: 'R0' }, { left: 'L1', right: 'R1' }] }
    store('m', m, { order: [3, 2, 1, 0], assignment: [3, 2, 1, 0], active: null, checked: true })
    render(show([m]))
    expect(await screen.findByRole('button', { name: /R1/ })).toBeTruthy()
    expect((screen.getByRole('button', { name: 'Prüfen' }) as HTMLButtonElement).disabled).toBe(true)
  })

  it('Szenario: unbekannter Pfad -> Start', async () => {
    const s: Block = {
      uid: 's', type: 'scenario', title: 'Fall', start: 'a',
      nodes: [{ id: 'a', text: 'Ausgangslage', options: [{ label: 'weiter', to: 'b' }] }, { id: 'b', text: 'Ende', outcome: 'good' }],
    }
    store('s', s, [0, 4, 1])
    render(show([s]))
    expect(await screen.findByText('Ausgangslage')).toBeTruthy()
    expect(screen.queryByText('Einen Schritt zurück')).toBeNull()
  })

  it('Lückentext und Terminal: unbrauchbarer Stand -> Startzustand', async () => {
    const c: Block = { uid: 'c', type: 'cloze', prompt: 'Fülle', text: 'mode [[m]]', gaps: [{ id: 'm', accept: ['access'] }] }
    const t: Block = { uid: 't', type: 'terminal', prompt: 'PC>', commands: [{ cmd: 'ls', output: 'x' }], tasks: [{ text: 'Liste', command: 'ls' }] }
    store('c', c, 5)
    store('t', t, { executed: 'kaputt' })
    render(show([c, t]))
    expect(await screen.findByLabelText('Lücke 1')).toBeTruthy()
    expect(await screen.findByText('(offen)')).toBeTruthy()
    expect(screen.queryByText(FAILED)).toBeNull()
  })
})

describe('Terminal: Flags und Prompt gehören zum gemerkten Stand', () => {
  const arp: Block = {
    uid: 'terminal-arp-cache', type: 'terminal', prompt: 'PC>',
    commands: [
      { cmd: 'arp -a', output: 'Keine Einträge', variants: [{ when: 'pinged', output: '10.0.0.1 dynamisch' }] },
      { cmd: 'ping 10.0.0.1', output: 'Antwort', sets: ['pinged'], prompt: 'PC(ok)>' },
    ],
    tasks: [{ text: 'Pinge das Gateway', command: 'ping 10.0.0.1' }, { text: 'Was steht im Cache?', answers: ['dynamisch'] }],
  }
  it('nach dem Neuladen wirkt der frühere Ping weiter', async () => {
    render(show([arp]))
    fireEvent.click(await screen.findByRole('button', { name: 'ping 10.0.0.1' }))
    cleanup()  // „Neuladen“
    render(show([arp]))
    expect(await screen.findByText('(erledigt)')).toBeTruthy()
    expect(screen.getByText('PC(ok)>')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'arp -a' }))
    expect(screen.getByRole('log').textContent).toContain('10.0.0.1 dynamisch')
  })
})

describe('Übungsstand und Sprache', () => {
  const de: Block = { uid: 'c1', type: 'check', prompt: 'Wie viele Bits?', options: ['acht', 'sechzehn'], answer: 0 }
  const en: Block = { uid: 'c1', type: 'check', prompt: 'How many bits?', options: ['eight', 'sixteen'], answer: 0 }
  const deR: Block = { uid: 'r1', type: 'reveal', teaser: 'Und dann?', value: 'Auflösung' }
  const enR: Block = { uid: 'r1', type: 'reveal', teaser: 'And then?', value: 'Solution' }

  it('der Fingerabdruck hängt an Struktur und Lösung, nicht an den Texten', () => {
    expect(fingerprint(de)).toBe(fingerprint(en))
    expect(fingerprint({ ...de, answer: 1 })).not.toBe(fingerprint(de))
    expect(fingerprint({ ...de, options: ['acht', 'sechzehn', 'vier'] })).not.toBe(fingerprint(de))
    const sc = (label: string, to: string) => ({ type: 'scenario', title: label, start: 'a', nodes: [{ id: 'a', text: label, options: [{ label, to }] }] })
    expect(fingerprint(sc('de', 'b'))).toBe(fingerprint(sc('en', 'b')))
    expect(fingerprint(sc('de', 'b'))).not.toBe(fingerprint(sc('de', 'c')))
  })

  it('DE gelöst -> EN -> dort weiterarbeiten -> zurück DE: der Stand bleibt', () => {
    const { rerender } = render(show([de, deR]))
    fireEvent.click(screen.getByRole('button', { name: 'acht' }))
    rerender(show([en, enR], 'en'))
    expect(screen.getByTestId('exercise-summary').textContent).toContain('1 of 2')
    expect(screen.getByText('Correct')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Reveal' }))
    cleanup()
    render(show([de, deR]))
    expect(screen.getByTestId('exercise-summary').textContent).toContain('2 von 2')
    expect(screen.getByText('Richtig')).toBeTruthy()
  })

  it('ein vor dem Update gespeicherter Stand (alter, sprachabhängiger Fingerabdruck) bleibt in seiner Sprache gültig', () => {
    const text = JSON.stringify(de)
    let hash = 5381
    for (let i = 0; i < text.length; i++) hash = ((hash << 5) + hash + text.charCodeAt(i)) | 0
    localStorage.setItem(KEY, JSON.stringify({ c1: { v: `${text.length}.${hash}`, s: 0, done: true } }))
    render(show([de]))
    expect(screen.getByTestId('exercise-summary').textContent).toContain('1 von 1')
    expect(screen.getByText('Richtig')).toBeTruthy()
  })
})

describe('Druck (Spickzettel) und Fokus der Diagramme', () => {
  const layers: Block = {
    uid: 'l', type: 'diagram', kind: 'layers', title: 'OSI',
    layers: [{ name: 'Transport', detail: 'TCP und UDP' }, { name: 'Netzwerk', detail: 'IP' }, { name: 'Bitübertragung' }],
  }
  it('layers: am Bildschirm ein Hinweis (im Druck ausgeblendet), im Druck alle Details', async () => {
    const { rerender } = render(<PrintContext.Provider value={false}>{show([layers])}</PrintContext.Provider>)
    expect((await screen.findByText('Schicht anklicken für Details.')).className).toContain('print:hidden')
    expect(screen.queryByText('TCP und UDP')).toBeNull()
    rerender(<PrintContext.Provider value={true}>{show([layers])}</PrintContext.Provider>)
    expect(screen.getByText('TCP und UDP')).toBeTruthy()
    expect(screen.getByText('IP')).toBeTruthy()
    expect(screen.queryByText('Schicht anklicken für Details.')).toBeNull()
  })

  it('fokussierbare SVG-Gruppen unterdrücken den Fokusrahmen nicht (kein outline-none)', async () => {
    const flow: Block = {
      uid: 'f', type: 'diagram', kind: 'flow', title: 'F',
      nodes: [{ id: 'a', label: 'A', row: 0, col: 0, detail: 'Knoten' }, { id: 'b', label: 'B', row: 0, col: 1 }],
      edges: [{ from: 'a', to: 'b', detail: 'Kante' }],
    }
    const { container } = render(show([seq('S', 2, 's'), flow]))
    await screen.findByRole('button', { name: 'A' })
    const focusable = [...container.querySelectorAll('svg [tabindex="0"]')]
    expect(focusable.length).toBeGreaterThanOrEqual(3)
    for (const g of focusable) expect(g.getAttribute('class')).not.toContain('outline-none')
  })
})
