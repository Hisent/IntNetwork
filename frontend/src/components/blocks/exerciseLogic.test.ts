import { describe, expect, it } from 'vitest'
import { assignPair, clozeResult, gapCorrect, gapSolution, matchResult, parseCloze, walkScenario } from './exerciseLogic'
import type { ClozeData, ScenarioData } from './types'

describe('match', () => {
  it('ordnet zu und nimmt eine Beschreibung einem anderen Begriff wieder weg', () => {
    let a = assignPair([null, null, null], 0, 2)
    expect(a).toEqual([2, null, null])
    a = assignPair(a, 1, 2)
    expect(a).toEqual([null, 2, null])
  })
  it('wertet je Begriff aus', () => {
    expect(matchResult([0, 2, 1])).toEqual([true, false, false])
    expect(matchResult([0, 1, null])).toEqual([true, true, false])
  })
})

const cloze: ClozeData = {
  prompt: 'p', mono: true,
  text: 'interface Gi1/0/1\n switchport mode [[mode]]\n name: "{{ paket }}"\n vlan [[vlan]] [[unbekannt]]',
  gaps: [
    { id: 'mode', accept: ['access', 'mode access'] },
    { id: 'vlan', options: ['10', '20'], answer: 1 },
  ],
}

describe('cloze', () => {
  it('zerlegt den Text und lässt Jinja-Klammern sowie unbekannte Marken stehen', () => {
    const parts = parseCloze(cloze.text, new Set(['mode', 'vlan']))
    expect(parts.filter((p) => 'gap' in p)).toEqual([{ gap: 'mode' }, { gap: 'vlan' }])
    const text = parts.map((p) => ('text' in p ? p.text : `<${p.gap}>`)).join('')
    expect(text).toBe('interface Gi1/0/1\n switchport mode <mode>\n name: "{{ paket }}"\n vlan <vlan> [[unbekannt]]')
  })
  it('prüft Freitext tolerant gegen Groß/Klein und Leerraum', () => {
    expect(gapCorrect(cloze.gaps[0], '  ACCESS ')).toBe(true)
    expect(gapCorrect(cloze.gaps[0], 'mode   access')).toBe(true)
    expect(gapCorrect(cloze.gaps[0], 'trunk')).toBe(false)
    expect(gapCorrect(cloze.gaps[0], '')).toBe(false)
  })
  it('prüft streng, wenn konfiguriert', () => {
    const strict = { id: 'x', accept: ['Gi1/0/1'], case_sensitive: true, strict_whitespace: true }
    expect(gapCorrect(strict, 'Gi1/0/1')).toBe(true)
    expect(gapCorrect(strict, 'gi1/0/1')).toBe(false)
    expect(gapCorrect(strict, 'Gi1/0/1 ')).toBe(false)
  })
  it('prüft Auswahl-Lücken über den Index und wertet eine leere Auswahl nie als richtig', () => {
    expect(gapCorrect(cloze.gaps[1], '1')).toBe(true)
    expect(gapCorrect(cloze.gaps[1], '0')).toBe(false)
    expect(gapCorrect({ id: 'y', options: ['a', 'b'], answer: 0 }, '')).toBe(false)
  })
  it('liefert Ergebnis je Lücke und die Musterlösung', () => {
    expect(clozeResult(cloze, { mode: 'access' })).toEqual({ mode: true, vlan: false })
    expect(cloze.gaps.map(gapSolution)).toEqual(['access', '20'])
  })
})

const scenario: ScenarioData = {
  title: 't', start: 'a',
  nodes: [
    { id: 'a', text: 'A', options: [{ label: 'zu b', to: 'b' }, { label: 'Ende', to: 'gut' }] },
    { id: 'b', text: 'B', options: [{ label: 'zurück', to: 'a' }, { label: 'kaputt', to: 'fehlt' }] },
    { id: 'gut', text: 'gut', outcome: 'good' },
  ],
}

describe('scenario', () => {
  it('startet am Startknoten und folgt den Entscheidungen', () => {
    expect(walkScenario(scenario, []).map((n) => n.id)).toEqual(['a'])
    expect(walkScenario(scenario, [0, 0, 1]).map((n) => n.id)).toEqual(['a', 'b', 'a', 'gut'])
  })
  it('bleibt bei ungültiger Wahl oder fehlendem Ziel am letzten gültigen Knoten', () => {
    expect(walkScenario(scenario, [0, 1]).map((n) => n.id)).toEqual(['a', 'b'])
    expect(walkScenario(scenario, [7]).map((n) => n.id)).toEqual(['a'])
    expect(walkScenario(scenario, [1, 0]).map((n) => n.id)).toEqual(['a', 'gut'])
  })
  it('liefert nichts, wenn der Startknoten fehlt', () => {
    expect(walkScenario({ ...scenario, start: 'x' }, [])).toEqual([])
  })
})
