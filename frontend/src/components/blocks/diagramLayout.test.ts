import { describe, expect, it } from 'vitest'
import { diagramAlt, layoutFlow, layoutSequence, textWidth, wrapText, FLOW, SEQ } from './diagramLayout'
import type { FlowDiagram, SequenceDiagram } from './types'

const seq: SequenceDiagram = {
  kind: 'sequence', title: 'DORA',
  actors: [{ id: 'c', label: 'Client' }, { id: 'r', label: 'Relay' }, { id: 's', label: 'DHCP-Server mit sehr langem Namen' }],
  messages: [
    { from: 'c', to: 's', label: 'DHCPDISCOVER', style: 'broadcast', detail: 'Broadcast' },
    { from: 's', to: 'c', label: 'DHCPOFFER mit einer wirklich ausführlichen Beschriftung, die umbrechen muss' },
    { from: 's', to: 's', label: 'Lease in die Datenbank schreiben' },
    { from: 'c', to: 'r', label: 'DHCPREQUEST' },
  ],
}

const flow: FlowDiagram = {
  kind: 'flow', title: 'Topologie',
  nodes: [
    { id: 'pc', label: 'Client', shape: 'host', row: 0, col: 0 },
    { id: 'sw', label: 'Access-Switch mit langem Namen', shape: 'switch', row: 0, col: 1, detail: 'Authenticator' },
    { id: 'ok', label: 'Erlaubt?', shape: 'decision', row: 1, col: 1 },
    { id: 'srv', label: 'RADIUS', shape: 'server', row: 1, col: 3 },
  ],
  edges: [
    { from: 'pc', to: 'sw', label: 'EAPOL' },
    { id: 'hin', from: 'sw', to: 'ok', label: 'Access-Request' },
    { from: 'ok', to: 'sw' },
    { from: 'ok', to: 'srv', arrow: 'none' },
  ],
}

describe('wrapText', () => {
  it('bricht an Leerzeichen und hält jede Zeile in der Breite', () => {
    const lines = wrapText('Der Server bietet eine freie Adresse aus dem Pool an', 120, 14)
    expect(lines.length).toBeGreaterThan(1)
    expect(lines.join(' ')).toBe('Der Server bietet eine freie Adresse aus dem Pool an')
    for (const l of lines) expect(textWidth(l, 14)).toBeLessThanOrEqual(120)
  })
  it('teilt überlange Wörter hart, statt sie abzuschneiden', () => {
    const lines = wrapText('Donaudampfschifffahrtsgesellschaftskapitän', 80, 14)
    expect(lines.length).toBeGreaterThan(1)
    expect(lines.join('')).toBe('Donaudampfschifffahrtsgesellschaftskapitän')
    for (const l of lines) expect(textWidth(l, 14)).toBeLessThanOrEqual(80)
  })
  it('liefert für leeren Text genau eine leere Zeile', () => {
    expect(wrapText('', 100, 14)).toEqual([''])
  })
})

describe('layoutSequence', () => {
  const L = layoutSequence(seq)
  it('verteilt die Akteure gleichmäßig innerhalb der Breite', () => {
    expect(L.actors.map((a) => a.id)).toEqual(['c', 'r', 's'])
    for (const a of L.actors) {
      expect(a.x - a.w / 2).toBeGreaterThanOrEqual(0)
      expect(a.x + a.w / 2).toBeLessThanOrEqual(L.width)
      for (const line of a.lines) expect(textWidth(line, SEQ.actorFont)).toBeLessThanOrEqual(a.w)
    }
  })
  it('stapelt die Nachrichten ohne Überlappung unter den Köpfen', () => {
    let prev = L.headH
    for (const m of L.messages) {
      expect(m.top).toBeGreaterThan(prev)
      expect(m.y).toBeGreaterThanOrEqual(m.top + m.lines.length * SEQ.lineH)
      prev = m.y
    }
    expect(L.height).toBeGreaterThan(prev)
  })
  it('hält jede Beschriftung zwischen den beteiligten Lebenslinien', () => {
    for (const m of L.messages.filter((x) => !x.self)) {
      for (const line of m.lines) expect(textWidth(line, SEQ.labelFont)).toBeLessThanOrEqual(Math.abs(m.x2 - m.x1) - 24)
    }
    expect(L.messages[1].lines.length).toBeGreaterThan(1)
  })
  it('legt eine Nachricht an sich selbst als Box auf die eigene Lebenslinie', () => {
    const self = L.messages[2]
    expect(self.self).toBe(true)
    expect(self.cx + self.w / 2).toBeLessThanOrEqual(L.width)
    expect(self.cx - self.w / 2).toBeGreaterThanOrEqual(0)
  })
  it('bleibt bei fünf Akteuren lesbar breit', () => {
    const five = layoutSequence({ ...seq, actors: 'abcde'.split('').map((id) => ({ id, label: id })), messages: [{ from: 'a', to: 'e', label: 'x' }] })
    expect(five.width / 5).toBeGreaterThanOrEqual(150)
  })
})

describe('layoutFlow', () => {
  const L = layoutFlow(flow)
  const overlap = (a: { cx: number; cy: number; w: number; h: number }, b: { cx: number; cy: number; w: number; h: number }) =>
    Math.abs(a.cx - b.cx) < (a.w + b.w) / 2 && Math.abs(a.cy - b.cy) < (a.h + b.h) / 2

  it('setzt Knoten überlappungsfrei ins Raster und innerhalb der Fläche', () => {
    for (const [i, a] of L.nodes.entries()) {
      expect(a.cx - a.w / 2).toBeGreaterThanOrEqual(0)
      expect(a.cx + a.w / 2).toBeLessThanOrEqual(L.width)
      expect(a.cy + a.h / 2).toBeLessThanOrEqual(L.height)
      for (const b of L.nodes.slice(i + 1)) expect(overlap(a, b)).toBe(false)
    }
    expect(L.nodes[0].cy).toBe(L.nodes[1].cy)
    expect(L.nodes[3].cx).toBeGreaterThan(L.nodes[2].cx)
  })
  it('macht Knoten so hoch, dass der umbrochene Text hineinpasst', () => {
    for (const n of L.nodes) {
      expect(n.h).toBeGreaterThanOrEqual(n.lines.length * FLOW.lineH + (n.icon ? FLOW.iconH : 0))
      for (const line of n.lines) expect(textWidth(line, FLOW.font)).toBeLessThanOrEqual(n.w)
    }
  })
  it('lässt Kanten am Knotenrand enden und Beschriftungen keinen Knoten überdecken', () => {
    expect(L.edges).toHaveLength(4)
    const first = L.edges[0]
    expect(first.x1).toBeGreaterThan(L.nodes[0].cx + L.nodes[0].w / 2)
    expect(first.x2).toBeLessThan(L.nodes[1].cx - L.nodes[1].w / 2)
    for (const e of L.edges) {
      if (!e.label) continue
      for (const n of L.nodes) expect(overlap(e.label, n)).toBe(false)
    }
  })
  it('versetzt Hin- und Rückkante gegeneinander', () => {
    const [hin, rueck] = [L.edges[1], L.edges[2]]
    expect(hin.key).toBe('hin')
    expect(rueck.key).toBe('edge-2')
    expect(hin.x1).not.toBe(rueck.x2)
  })
})

describe('diagramAlt', () => {
  it('beschreibt eine Sequenz Nachricht für Nachricht', () => {
    expect(diagramAlt(seq)[0]).toBe('1. Client → DHCP-Server mit sehr langem Namen: DHCPDISCOVER — Broadcast')
    expect(diagramAlt(seq)[2]).toContain('3. DHCP-Server mit sehr langem Namen: Lease')
  })
  it('beschreibt Knoten und Kanten eines Flussdiagramms', () => {
    const alt = diagramAlt(flow)
    expect(alt).toContain('Access-Switch mit langem Namen — Authenticator')
    expect(alt).toContain('Client → Access-Switch mit langem Namen: EAPOL')
    expect(alt).toContain('Erlaubt? — RADIUS')
  })
  it('beschreibt Schichten und Vergleichszeilen', () => {
    expect(diagramAlt({ kind: 'layers', title: 't', layers: [{ name: 'Transport', content: 'TCP', pdu: 'Segment' }] })).toEqual(['Transport — TCP — Segment'])
    expect(diagramAlt({ kind: 'compare', title: 't', columns: [{ title: 'A' }, { title: 'B' }], rows: [{ label: 'Port', values: ['1812', '49'] }] }))
      .toEqual(['Port: A = 1812; B = 49'])
  })
})
