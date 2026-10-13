import { describe, expect, it } from 'vitest'
import { diagramAlt, layoutFlow, layoutSequence, segmentBlocked, textWidth, wrapText, FLOW, SEQ } from './diagramLayout'
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
  it('trennt deutsche Komposita mit Bindestrich am Bindestrich, nicht im Wort', () => {
    const lines = wrapText('Ethernet-Frame-Header-Prüfsumme', 100, 14)
    expect(lines.length).toBeGreaterThan(1)
    expect(lines.join('')).toBe('Ethernet-Frame-Header-Prüfsumme')
    for (const l of lines.slice(0, -1)) expect(l.endsWith('-')).toBe(true)
    for (const l of lines) expect(textWidth(l, 14)).toBeLessThanOrEqual(100)
  })
  it('trennt Pfade nach dem Schrägstrich', () => {
    const lines = wrapText('/etc/ssl/private/server.key', 100, 14)
    expect(lines).toEqual(['/etc/ssl/', 'private/', 'server.key'])
  })
  it('trennt snake_case nach dem Unterstrich', () => {
    const lines = wrapText('max_connections_per_host', 110, 14)
    expect(lines.join('')).toBe('max_connections_per_host')
    for (const l of lines.slice(0, -1)) expect(l.endsWith('_')).toBe(true)
  })
  it('hält vorhandene Zeilenumbrüche ein', () => {
    expect(wrapText('Access\nRequest', 300, 14)).toEqual(['Access', 'Request'])
  })
  it('schneidet nur dann hart, wenn auch ein Segment zu breit ist', () => {
    const lines = wrapText('kurz-Donaudampfschifffahrtsgesellschaft-ok', 80, 14)
    expect(lines.join('')).toBe('kurz-Donaudampfschifffahrtsgesellschaft-ok')
    expect(lines[0]).toBe('kurz-')
    for (const l of lines) expect(textWidth(l, 14)).toBeLessThanOrEqual(80)
  })
  it('lässt Wörter unverändert, die in eine Zeile passen', () => {
    expect(wrapText('Ethernet-Frame', 300, 14)).toEqual(['Ethernet-Frame'])
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

describe('layoutSequence: Zeitmarken, Trennzeilen, mehrere Empfänger', () => {
  const base = layoutSequence(seq)
  it('lässt Diagramme ohne die neuen Felder unverändert', () => {
    expect(base.gutter).toBe(0)
    expect(base.messages.every((m) => m.dividerY === undefined && m.xs.length === 1 && m.xs[0] === m.x2)).toBe(true)
  })
  it('reserviert für Zeitmarken links eine Spalte und schiebt alles andere nach rechts', () => {
    const L = layoutSequence({ ...seq, messages: seq.messages.map((m, i) => (i === 0 ? { ...m, at: '30 s' } : m)) })
    expect(L.gutter).toBeGreaterThanOrEqual(textWidth('120 ms', SEQ.atFont) + 12)
    expect(L.width).toBe(base.width + L.gutter)
    L.actors.forEach((a, i) => expect(a.x).toBe(base.actors[i].x + L.gutter))
    for (const m of L.messages) expect(m.cx - m.w / 2).toBeGreaterThanOrEqual(L.gutter)
    expect(L.height).toBe(base.height)
  })
  it('legt die Trennzeile zwischen zwei Nachrichten, ohne etwas zu überlappen', () => {
    const L = layoutSequence({ ...seq, messages: seq.messages.map((m, i) => (i === 0 || i === 3 ? { ...m, divider: 'Timeout' } : m)) })
    expect(L.messages[0].dividerY!).toBeGreaterThan(L.messages[0].y + 8)
    expect(L.messages[1].top).toBeGreaterThanOrEqual(L.messages[0].dividerY! + 18)
    expect(L.messages[1].dividerY).toBeUndefined()
    // auch nach der letzten Nachricht ist Platz
    expect(L.height).toBeGreaterThanOrEqual(L.messages[3].dividerY! + 18)
    expect(L.height).toBeGreaterThan(base.height)
  })
  it('zeichnet eine Nachricht an mehrere Empfänger in einer Zeile, Beschriftung über die ganze Spanne', () => {
    const L = layoutSequence({ ...seq, messages: [{ from: 'r', to: ['c', 's'], label: 'Hello an alle' }, { from: 'c', to: ['r', 's'], label: 'x' }] })
    const [c, r, s] = L.actors.map((a) => a.x)
    expect(L.messages[0]).toMatchObject({ self: false, x1: r, xs: [c, s], cx: (c + s) / 2, w: s - c - 24 })
    expect(L.messages[1]).toMatchObject({ x1: c, xs: [r, s], x2: s })
    expect(diagramAlt({ ...seq, messages: [{ from: 'r', to: ['c', 's'], label: 'Hello', at: '0 s', divider: 'Timeout' }] }))
      .toEqual(['1. [0 s] Relay → Client, DHCP-Server mit sehr langem Namen: Hello — Timeout'])
  })
})

describe('layoutFlow: mehrere Kanten je Knotenpaar', () => {
  const pair = (edges: FlowDiagram['edges']): FlowDiagram => ({
    kind: 'flow', title: 't',
    nodes: [{ id: 'a', label: 'A', row: 0, col: 0 }, { id: 'b', label: 'B', row: 0, col: 1 }], edges,
  })
  const boxOverlap = (a: { cx: number; cy: number; w: number; h: number }, b: { cx: number; cy: number; w: number; h: number }) =>
    Math.abs(a.cx - b.cx) < (a.w + b.w) / 2 && Math.abs(a.cy - b.cy) < (a.h + b.h) / 2

  it('lässt eine einzelne Kante gerade durch die Knotenmitten laufen', () => {
    const L = layoutFlow(pair([{ from: 'a', to: 'b', label: 'x' }]))
    expect(L.edges[0].y1).toBe(L.nodes[0].cy)
    expect(L.edges[0].points).toBeUndefined()
    expect(L.edges[0].label!.cy).toBe(L.nodes[0].cy)
  })
  it('versetzt Hin- und Rückkante um je 9px und stellt die Beschriftungen auf verschiedene Seiten', () => {
    const L = layoutFlow(pair([{ from: 'a', to: 'b', label: 'hin' }, { from: 'b', to: 'a', label: 'zurück' }]))
    const cy = L.nodes[0].cy
    expect(L.edges.map((e) => e.y1 - cy)).toEqual([9, -9])
    expect(L.edges[0].label!.cy).toBeGreaterThan(cy + 9)
    expect(L.edges[1].label!.cy).toBeLessThan(cy - 9)
    expect(boxOverlap(L.edges[0].label!, L.edges[1].label!)).toBe(false)
  })
  it('trennt zwei gleichgerichtete Kanten genauso', () => {
    const L = layoutFlow(pair([{ from: 'a', to: 'b', label: 'HTTP' }, { from: 'a', to: 'b', label: 'DNS' }]))
    const cy = L.nodes[0].cy
    expect(L.edges.map((e) => e.y1 - cy)).toEqual([9, -9])
    expect(boxOverlap(L.edges[0].label!, L.edges[1].label!)).toBe(false)
  })
  it('legt bei drei Kanten die mittlere auf die Gerade', () => {
    const L = layoutFlow(pair([{ from: 'a', to: 'b' }, { from: 'b', to: 'a' }, { from: 'a', to: 'b' }]))
    const cy = L.nodes[0].cy
    expect(L.edges.map((e) => e.y1 - cy).sort((x, y) => x - y)).toEqual([-18, 0, 18])
  })
})

describe('layoutFlow: Bogen um besetzte Zellen', () => {
  const row = (n: number, edges: FlowDiagram['edges'], extra: FlowDiagram['nodes'] = []): FlowDiagram => ({
    kind: 'flow', title: 't',
    nodes: [...Array.from({ length: n }, (_, i) => ({ id: `n${i}`, label: `Knoten ${i}`, shape: 'server' as const, row: 0, col: i })), ...extra],
    edges,
  })
  const inside = (b: { cx: number; cy: number; w: number; h: number }, [x, y]: [number, number], m = 0) =>
    Math.abs(x - b.cx) < b.w / 2 + m && Math.abs(y - b.cy) < b.h / 2 + m
  const expectClear = (L: ReturnType<typeof layoutFlow>, edge: number, ends: string[]) => {
    const e = L.edges[edge]
    expect(e.points!.length).toBeGreaterThan(8)
    for (const n of L.nodes.filter((x) => !ends.includes(x.id))) {
      for (const p of e.points!) expect(inside(n, p, 6)).toBe(false)
      if (e.label) expect(Math.abs(e.label.cx - n.cx) < (e.label.w + n.w) / 2 && Math.abs(e.label.cy - n.cy) < (e.label.h + n.h) / 2).toBe(false)
    }
    for (const [x, y] of e.points!) {
      expect(x).toBeGreaterThanOrEqual(0); expect(x).toBeLessThanOrEqual(L.width)
      expect(y).toBeGreaterThanOrEqual(0); expect(y).toBeLessThanOrEqual(L.height)
    }
    if (e.label) {
      expect(e.label.cy - e.label.h / 2).toBeGreaterThanOrEqual(0)
      expect(e.label.cy + e.label.h / 2).toBeLessThanOrEqual(L.height)
    }
  }

  it('erkennt, ob eine Gerade einen Knoten trifft', () => {
    const box = [{ id: 'x', cx: 100, cy: 100, w: 40, h: 20, lines: [], icon: false }]
    expect(segmentBlocked(0, 100, 200, 100, box)).toBe(true)
    expect(segmentBlocked(0, 0, 200, 200, box)).toBe(true)
    expect(segmentBlocked(0, 80, 200, 80, box)).toBe(false)
    expect(segmentBlocked(0, 100, 70, 100, box)).toBe(false)
  })
  it('führt eine Kante über eine besetzte Zelle im Bogen herum und vergrößert dafür die Fläche', () => {
    const plain = layoutFlow(row(3, [{ from: 'n0', to: 'n1' }]))
    const L = layoutFlow(row(3, [{ from: 'n0', to: 'n1' }, { id: 'weit', from: 'n0', to: 'n2', label: 'Replikation' }]))
    expect(L.edges[0].points).toBeUndefined()
    expectClear(L, 1, ['n0', 'n2'])
    expect(L.height).toBeGreaterThan(plain.height)
    // einzelne Zeile: Bogen nach oben, Start/Ende an der Oberkante der Knoten
    const e = L.edges[1]
    expect(Math.min(...e.points!.map((p) => p[1]))).toBeLessThan(L.nodes[1].cy - L.nodes[1].h / 2)
    expect(e.y1).toBeLessThan(L.nodes[0].cy - L.nodes[0].h / 2)
    expect([e.x1, e.y1]).toEqual(e.points![0])
    expect([e.x2, e.y2]).toEqual(e.points![e.points!.length - 1])
  })
  it('schafft auch fünf Spalten und eine besetzte Spalte (senkrecht)', () => {
    expectClear(layoutFlow(row(5, [{ from: 'n0', to: 'n4', label: 'über alle' }])), 0, ['n0', 'n4'])
    const col: FlowDiagram = {
      kind: 'flow', title: 't',
      nodes: [0, 1, 2].map((r) => ({ id: `n${r}`, label: `K${r}`, row: r, col: 0 })),
      edges: [{ from: 'n2', to: 'n0', label: 'zurück' }],
    }
    const L = layoutFlow(col)
    expectClear(L, 0, ['n2', 'n0'])
    expect(L.width).toBeGreaterThan(layoutFlow({ ...col, edges: [] }).width)
  })
  it('weicht in einem mehrzeiligen Raster nach außen aus und trennt Hin- und Rückbogen', () => {
    const L = layoutFlow(row(3, [{ from: 'n0', to: 'n2', label: 'hin' }, { from: 'n2', to: 'n0', label: 'her' }],
      [{ id: 'u', label: 'unten', row: 1, col: 1 }]))
    expectClear(L, 0, ['n0', 'n2'])
    expectClear(L, 1, ['n0', 'n2'])
    const peak = (i: number) => Math.min(...L.edges[i].points!.map((p) => p[1]))
    expect(peak(0)).toBeLessThan(L.nodes[1].cy)
    expect(Math.abs(peak(0) - peak(1))).toBeGreaterThan(10)
  })
  it('führt verschachtelte Bögen kreuzungsfrei und hält ihre Beschriftungen auseinander', () => {
    const L = layoutFlow({ kind: 'flow', title: 't',
      nodes: [0, 1, 2, 3, 4].map((r) => ({ id: `n${r}`, label: `Knoten ${r}`, row: r, col: 0 })),
      edges: [{ from: 'n4', to: 'n0', label: 'Feedback' }, { from: 'n3', to: 'n1', label: 'Rollback' }] })
    expectClear(L, 0, ['n4', 'n0'])
    expectClear(L, 1, ['n3', 'n1'])
    const [long, short] = L.edges
    // die Bögen kreuzen und berühren sich nicht (ineinander oder auf verschiedenen Seiten)
    for (const p of long.points!) for (const q of short.points!) expect(Math.hypot(p[0] - q[0], p[1] - q[1])).toBeGreaterThan(8)
    expect(Math.abs(long.label!.cx - short.label!.cx)).toBeGreaterThanOrEqual((long.label!.w + short.label!.w) / 2)
    for (const p of long.points!) expect(inside(short.label!, p)).toBe(false)
    for (const n of L.nodes) expect(Math.abs(short.label!.cx - n.cx)).toBeGreaterThanOrEqual((short.label!.w + n.w) / 2)
  })
  it('lässt freie Diagonalen und Kanten über leere Zellen gerade', () => {
    const L = layoutFlow({ kind: 'flow', title: 't',
      nodes: [{ id: 'a', label: 'A', row: 0, col: 0 }, { id: 'b', label: 'B', row: 0, col: 2 }, { id: 'c', label: 'C', row: 1, col: 1 }],
      edges: [{ from: 'a', to: 'b' }, { from: 'a', to: 'c' }, { from: 'c', to: 'b' }] })
    expect(L.edges.every((e) => e.points === undefined)).toBe(true)
  })
})
