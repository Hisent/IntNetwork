// Reine Layout-Funktionen für die SVG-Diagramme (sequence, flow). Kein DOM,
// keine Textmessung: Breiten werden aus Zeichenklassen geschätzt (bewusst
// großzügig), damit Text weder abgeschnitten wird noch überlappt — und damit
// das Layout in jsdom/Node testbar bleibt.
import type { DiagramData, FlowDiagram, FlowEdge, SequenceDiagram } from './types'

// ponytail: Schätzung statt canvas.measureText — reicht, weil jede Box aus der
// Schätzung heraus dimensioniert wird; bei exotischen Schriften measureText nachrüsten.
function charEm(ch: string): number {
  if (' .,:;!|\'`ijlt()[]/-'.includes(ch)) return 0.36
  if ('mwMW@%'.includes(ch)) return 0.92
  if (ch >= 'A' && ch <= 'Z') return 0.74
  if (ch >= '0' && ch <= '9') return 0.64
  return 0.6
}

export function textWidth(text: string, fontSize: number): number {
  let em = 0
  for (const ch of text) em += charEm(ch)
  return em * fontSize
}

/** Teilt ein zu breites Wort bevorzugt nach `-`, `/`, `_`; nur was dann noch zu breit ist, wird hart geschnitten.
 *  Liefert die vollen Zeilen und den Rest, der weiter in die laufende Zeile gehört. */
function splitLongWord(word: string, maxWidth: number, fontSize: number): { full: string[]; rest: string } {
  const full: string[] = []
  let cur = ''
  for (let seg of word.match(/[^-/_]*[-/_]+|[^-/_]+/g) ?? [word]) {
    if (cur && textWidth(cur + seg, fontSize) <= maxWidth) { cur += seg; continue }
    if (cur) { full.push(cur); cur = '' }
    // seg.length > 1: bei negativer/zu kleiner Breite bleibt sonst ein leerer Rest, der nie „passt“ (Endlosschleife)
    while (seg.length > 1 && textWidth(seg, fontSize) > maxWidth) {
      let cut = 1
      while (cut < seg.length && textWidth(seg.slice(0, cut + 1), fontSize) <= maxWidth) cut++
      full.push(seg.slice(0, cut))
      seg = seg.slice(cut)
    }
    cur = seg
  }
  return { full, rest: cur }
}

/** Bricht an Leerzeichen und `\n` um; Wörter, die allein zu breit sind, werden zuerst nach `-`, `/`, `_`, erst dann hart geteilt. */
export function wrapText(text: string, maxWidth: number, fontSize: number): string[] {
  const lines: string[] = []
  for (const para of text.split('\n')) {
    let line = ''
    for (let word of para.split(/\s+/).filter(Boolean)) {
      if (textWidth(word, fontSize) > maxWidth) {
        if (line) { lines.push(line); line = '' }
        const { full, rest } = splitLongWord(word, maxWidth, fontSize)
        lines.push(...full)
        word = rest
      }
      if (!word) continue
      const candidate = line ? `${line} ${word}` : word
      if (textWidth(candidate, fontSize) <= maxWidth) line = candidate
      else { if (line) lines.push(line); line = word }
    }
    if (line) lines.push(line)
  }
  return lines.length ? lines : ['']
}

// --- sequence ----------------------------------------------------------------

export const SEQ = { actorFont: 15, labelFont: 14, noteFont: 13, lineH: 18, pad: 12, atFont: 12, gutter: 60 }

export interface SeqActorBox { id: string; x: number; w: number; h: number; lines: string[] }
export interface SeqMessageBox {
  index: number
  self: boolean
  x1: number; x2: number
  /** x aller Empfänger (bei `to` als Liste mehrere; x2 ist der entfernteste) */
  xs: number[]
  /** Oberkante des Beschriftungsblocks bzw. der Notiz-Box */
  top: number
  /** y der Pfeillinie (bei self: Unterkante der Box) */
  y: number
  lines: string[]
  /** Mitte und Breite des Textblocks */
  cx: number; w: number
  /** y der Trennzeile NACH dieser Nachricht (`divider`) */
  dividerY?: number
}
export interface SeqLayout {
  width: number; height: number; headH: number; actors: SeqActorBox[]; messages: SeqMessageBox[]
  /** Breite der Zeitmarken-Spalte am linken Rand (0, wenn keine Nachricht `at` hat) */
  gutter: number
}

export function layoutSequence(d: SequenceDiagram): SeqLayout {
  const n = d.actors.length
  const colW = Math.min(280, Math.max(150, 760 / n))
  const gutter = d.messages.some((m) => m.at) ? SEQ.gutter : 0
  const width = gutter + colW * n
  const boxW = colW - 20
  const actors = d.actors.map((a, i) => {
    const lines = wrapText(a.label, boxW - 2 * SEQ.pad, SEQ.actorFont)
    return { id: a.id, x: gutter + colW * (i + 0.5), w: boxW, h: lines.length * SEQ.lineH + 14, lines }
  })
  const headH = Math.max(...actors.map((a) => a.h))
  for (const a of actors) a.h = headH
  const xOf = (id: string) => actors.find((a) => a.id === id)?.x ?? gutter + colW / 2

  let y = headH + 22
  const divide = (box: SeqMessageBox, text?: string) => {
    if (text) { box.dividerY = y + 4; y += 30 }
    return box
  }
  const messages = d.messages.map((m, index) => {
    const x1 = xOf(m.from)
    const xs = [m.to].flat().map(xOf)
    const x2 = xs.reduce((far, x) => (Math.abs(x - x1) > Math.abs(far - x1) ? x : far))
    if (m.from === m.to) {
      // Nachricht an sich selbst = Notiz-Box auf der Lebenslinie (interner Schritt)
      const w = Math.min(colW - 16, 230)
      const cx = Math.min(Math.max(x1, gutter + w / 2 + 4), width - w / 2 - 4)
      const lines = wrapText(m.label, w - 2 * SEQ.pad, SEQ.noteFont)
      const top = y
      y += lines.length * SEQ.lineH + 12
      const box = { index, self: true, x1, x2, xs, top, y, lines, cx, w }
      y += 20
      return divide(box, m.divider)
    }
    const lo = Math.min(x1, ...xs)
    const hi = Math.max(x1, ...xs)
    const w = hi - lo - 24
    const lines = wrapText(m.label, w, SEQ.labelFont)
    const top = y
    y += lines.length * SEQ.lineH + 6
    const box = { index, self: false, x1, x2, xs, top, y, lines, cx: (lo + hi) / 2, w }
    y += 24
    return divide(box, m.divider)
  })
  return { width, height: y + 4, headH, actors, messages, gutter }
}

// --- flow --------------------------------------------------------------------

export const FLOW = { nodeW: 136, font: 13, edgeFont: 12, lineH: 16, iconH: 24, pad: 16 }

export interface FlowNodeBox { id: string; cx: number; cy: number; w: number; h: number; lines: string[]; icon: boolean }
export interface FlowEdgeBox {
  key: string
  x1: number; y1: number; x2: number; y2: number
  /** nur bei Bogenführung um einen Knoten herum: Stützpunkte von (x1,y1) bis (x2,y2) */
  points?: [number, number][]
  label?: { cx: number; cy: number; w: number; h: number; lines: string[] }
}
export interface FlowLayout { width: number; height: number; nodes: FlowNodeBox[]; edges: FlowEdgeBox[] }

/** Stabile Kennung einer Kante: Autoren-id, sonst Position. */
export function edgeKey(e: { id?: string }, index: number): string {
  return e.id ?? `edge-${index}`
}

/** Schnittpunkt der Strecke Mitte→Ziel mit dem Rand der Box (plus Abstand). */
function clip(box: FlowNodeBox, towardX: number, towardY: number, gap: number): [number, number] {
  const dx = towardX - box.cx
  const dy = towardY - box.cy
  if (dx === 0 && dy === 0) return [box.cx, box.cy]
  const hw = box.w / 2 + gap
  const hh = box.h / 2 + gap
  const scale = Math.min(dx === 0 ? Infinity : hw / Math.abs(dx), dy === 0 ? Infinity : hh / Math.abs(dy))
  return [box.cx + dx * scale, box.cy + dy * scale]
}

type Pt = [number, number]
interface Box { cx: number; cy: number; w: number; h: number }
const inBox = (b: Box, [x, y]: Pt, margin: number) =>
  Math.abs(x - b.cx) < b.w / 2 + margin && Math.abs(y - b.cy) < b.h / 2 + margin
const hits = (pts: Pt[], boxes: Box[], margin: number) => pts.some((p) => boxes.some((b) => inBox(b, p, margin)))
const overlaps = (a: Box, b: Box, margin: number) =>
  Math.abs(a.cx - b.cx) < (a.w + b.w) / 2 + margin && Math.abs(a.cy - b.cy) < (a.h + b.h) / 2 + margin

/** Strecke als Punktfolge im ~4px-Raster */
function segmentPoints(x1: number, y1: number, x2: number, y2: number): Pt[] {
  const steps = Math.max(1, Math.ceil(Math.hypot(x2 - x1, y2 - y1) / 4))
  return Array.from({ length: steps + 1 }, (_, i): Pt => [x1 + ((x2 - x1) * i) / steps, y1 + ((y2 - y1) * i) / steps])
}

/** Trifft die gerade Strecke einen der Knoten? */
export function segmentBlocked(x1: number, y1: number, x2: number, y2: number, boxes: Box[]): boolean {
  return hits(segmentPoints(x1, y1, x2, y2), boxes, 1)
}

/** Bogen von a nach b, der um `bulge` (mit Vorzeichen) seitlich ausweicht: kubische Kurve
 * Mitte→Mitte, beschnitten auf das Stück zwischen den beiden Knotenrändern. */
export function bowPoints(a: Box, b: Box, bulge: number, gapA: number, gapB: number): Pt[] {
  const len = Math.hypot(b.cx - a.cx, b.cy - a.cy) || 1
  const nx = (-(b.cy - a.cy) / len) * bulge
  const ny = ((b.cx - a.cx) / len) * bulge
  const pts: Pt[] = []
  for (let i = 0; i <= 64; i++) {
    const t = i / 64
    const k = 3 * t * (1 - t)  // Gewicht der beiden (gleich weit ausgelenkten) Kontrollpunkte
    const s = t * t * (3 - 2 * t)
    const p: Pt = [a.cx + (b.cx - a.cx) * s + nx * k, a.cy + (b.cy - a.cy) * s + ny * k]
    if (!inBox(a, p, gapA) && !inBox(b, p, gapB)) pts.push(p)
  }
  return pts
}

// ponytail: kein Router — probiert feste Auslenkungen auf beiden Seiten und nimmt die
// erste, die an allen fremden Knoten vorbeiführt und deren Beschriftung (am Scheitel)
// weder einen Knoten noch einen schon gelegten Bogen trifft — möglichst auch keine
// (kürzere, schon gelegte) gerade Kante. Bögen dürfen gerade Kanten kreuzen und deren
// Beschriftungen sind keine Hindernisse; wer das braucht, ordnet das Raster um.
const BULGES = [44, 64, 88, 116, 150, 190, 240, 300, 370]

export function layoutFlow(d: FlowDiagram): FlowLayout {
  const edges = d.edges ?? []
  const minRow = Math.min(...d.nodes.map((n) => n.row))
  const minCol = Math.min(...d.nodes.map((n) => n.col))
  const rows = Math.max(...d.nodes.map((n) => n.row)) - minRow + 1
  const cols = Math.max(...d.nodes.map((n) => n.col)) - minCol + 1

  const edgeLabels = edges.map((e) => (e.label ? wrapText(e.label, 92, FLOW.edgeFont) : null))
  const maxLabelW = Math.max(0, ...edgeLabels.flatMap((l) => (l ?? []).map((s) => textWidth(s, FLOW.edgeFont))))
  const maxLabelLines = Math.max(0, ...edgeLabels.map((l) => l?.length ?? 0))
  // Lücken so groß, dass die längste Kantenbeschriftung zwischen zwei Nachbarn passt
  const gapX = Math.max(64, maxLabelW + 40)
  const gapY = Math.max(52, maxLabelLines * FLOW.lineH + 40)

  const measured = d.nodes.map((n) => {
    const diamond = n.shape === 'decision'
    const icon = !diamond && n.shape !== 'process' && n.shape !== undefined
    const lines = wrapText(n.label, diamond ? FLOW.nodeW * 0.62 : FLOW.nodeW - 16, FLOW.font)
    const text = lines.length * FLOW.lineH
    const h = diamond ? Math.max(76, text * 2 + 20) : text + (icon ? FLOW.iconH : 0) + 18
    return { n, lines, icon, h }
  })
  const rowH = Array.from({ length: rows }, (_, r) =>
    Math.max(40, ...measured.filter((m) => m.n.row - minRow === r).map((m) => m.h)))
  const rowTop: number[] = []
  let y = FLOW.pad
  for (let r = 0; r < rows; r++) { rowTop.push(y); y += rowH[r] + gapY }
  let height = y - gapY + FLOW.pad
  let width = cols * FLOW.nodeW + (cols - 1) * gapX + 2 * FLOW.pad

  const nodes: FlowNodeBox[] = measured.map(({ n, lines, icon, h }) => {
    const r = n.row - minRow
    return {
      id: n.id, lines, icon, w: FLOW.nodeW, h,
      cx: FLOW.pad + (n.col - minCol) * (FLOW.nodeW + gapX) + FLOW.nodeW / 2,
      cy: rowTop[r] + rowH[r] / 2,
    }
  })
  const byId = new Map(nodes.map((b) => [b.id, b]))
  const centerX = nodes.reduce((sum, b) => sum + b.cx, 0) / nodes.length
  const centerY = nodes.reduce((sum, b) => sum + b.cy, 0) / nodes.length

  const bows: { points: Pt[]; label?: Box }[] = []
  const straight: Pt[] = []
  const layoutEdge = (e: FlowEdge, i: number): FlowEdgeBox | null => {
    const a = byId.get(e.from)
    const b = byId.get(e.to)
    if (!a || !b) return null
    const gapA = e.arrow === 'both' ? 5 : 2
    const gapB = e.arrow === 'none' ? 2 : 5
    let [x1, y1] = clip(a, b.cx, b.cy, gapA)
    let [x2, y2] = clip(b, a.cx, a.cy, gapB)
    // Mehrere Kanten zwischen denselben zwei Knoten (Hin/Rück oder doppelt): parallel versetzen
    // statt überdecken. `side` = Versatz in 18px-Spuren entlang der eigenen Normalen; ein
    // Hin-/Rück-Paar landet so je 9px rechts der eigenen Laufrichtung.
    const group = edges.flatMap((o, oi) => ((o.from === e.from && o.to === e.to) || (o.from === e.to && o.to === e.from) ? [oi] : []))
    const lane = (group.length - 1) / 2 - group.indexOf(i)
    const side = edges[group[0]].from === e.from ? lane : -lane
    const len = Math.hypot(x2 - x1, y2 - y1) || 1
    const nx = -(y2 - y1) / len
    const ny = (x2 - x1) / len
    x1 += nx * side * 18; y1 += ny * side * 18; x2 += nx * side * 18; y2 += ny * side * 18
    const lines = edgeLabels[i]
    const w = lines ? Math.max(...lines.map((s) => textWidth(s, FLOW.edgeFont))) + 12 : 0
    const h = lines ? lines.length * FLOW.lineH + 6 : 0
    // Beschriftung ganz neben die (versetzte) Linie schieben (dir = ±1), sonst mittig darauf
    const beside = (dir: number) => dir * ((Math.abs(nx) * w + Math.abs(ny) * h) / 2 + 3)

    // Läge ein fremder Knoten auf der Geraden, führt ein Bogen um ihn herum.
    const others = nodes.filter((o) => o !== a && o !== b)
    if (segmentBlocked(x1, y1, x2, y2, others)) {
      // bevorzugt nach außen (weg vom Schwerpunkt), bei einer einzelnen Zeile/Spalte nach oben/links
      const out = ((a.cx + b.cx) / 2 - centerX) * nx + ((a.cy + b.cy) / 2 - centerY) * ny
      const first = Math.abs(out) > 1 ? Math.sign(out) : ny !== 0 ? -Math.sign(ny) : -Math.sign(nx)
      const free = BULGES.flatMap((bulge) => [first * bulge, -first * bulge]).flatMap((bulge) => {
        const points = bowPoints(a, b, bulge, gapA, gapB)
        if (points.length < 2 || hits(points, others, 8) || hits(points, bows.flatMap((o) => (o.label ? [o.label] : [])), 2)) return []
        const [cx, cy] = points[Math.floor(points.length / 2)]
        const label = lines ? { cx, cy, w, h, lines } : undefined
        if (label && (nodes.some((n) => overlaps(label, n, 4)) || bows.some((o) => (o.label && overlaps(label, o.label, 4)) || hits(o.points, [label], 2)))) return []
        return [{ points, label }]
      })
      // lieber ein größerer Bogen als eine Beschriftung auf einer geraden Kante
      const calm = free.filter((c) => !c.label || !hits(straight, [c.label], 2))
      const pool = calm.length ? calm : free
      // weitere Kanten desselben Paars nehmen den nächstgrößeren freien Bogen
      const pick = pool[Math.min(group.indexOf(i), pool.length - 1)]
      if (pick) {
        const { points, label } = pick
        bows.push(pick)
        return { key: edgeKey(e, i), points, x1: points[0][0], y1: points[0][1], x2: points[points.length - 1][0], y2: points[points.length - 1][1], label }
      }
    }
    const off = side ? beside(Math.sign(side)) : 0
    const label = lines ? { cx: (x1 + x2) / 2 + nx * off, cy: (y1 + y2) / 2 + ny * off, w, h, lines } : undefined
    straight.push(...segmentPoints(x1, y1, x2, y2))
    return { key: edgeKey(e, i), x1, y1, x2, y2, label }
  }
  // kurze Kanten zuerst: so liegen verschachtelte Bögen ineinander statt sich zu kreuzen
  const span = (e: { from: string; to: string }) => {
    const a = byId.get(e.from)
    const b = byId.get(e.to)
    return a && b ? Math.hypot(b.cx - a.cx, b.cy - a.cy) : 0
  }
  const laid: (FlowEdgeBox | null)[] = []
  for (const i of edges.map((_, k) => k).sort((p, q) => span(edges[p]) - span(edges[q]))) laid[i] = layoutEdge(edges[i], i)
  const edgeBoxes = laid.filter((b): b is FlowEdgeBox => b !== null)

  // Bögen ragen über das Raster hinaus: Fläche erweitern und alles mitverschieben.
  const bowed = edgeBoxes.filter((e) => e.points)
  if (bowed.length) {
    const xs = bowed.flatMap((e) => [...e.points!.map((p) => p[0]), ...(e.label ? [e.label.cx - e.label.w / 2, e.label.cx + e.label.w / 2] : [])])
    const ys = bowed.flatMap((e) => [...e.points!.map((p) => p[1]), ...(e.label ? [e.label.cy - e.label.h / 2, e.label.cy + e.label.h / 2] : [])])
    const dx = Math.max(0, 8 - Math.min(...xs))
    const dy = Math.max(0, 8 - Math.min(...ys))
    width = Math.max(width, Math.max(...xs) + 8) + dx
    height = Math.max(height, Math.max(...ys) + 8) + dy
    if (dx || dy) {
      for (const n of nodes) { n.cx += dx; n.cy += dy }
      for (const e of edgeBoxes) {
        e.x1 += dx; e.y1 += dy; e.x2 += dx; e.y2 += dy
        if (e.label) { e.label.cx += dx; e.label.cy += dy }
        e.points = e.points?.map(([px, py]) => [px + dx, py + dy])
      }
    }
  }
  return { width, height, nodes, edges: edgeBoxes }
}

// --- Textalternative ---------------------------------------------------------

/** „A → B“, bei mehreren Empfängern „A → B, C“, bei einer Notiz an sich selbst nur „A“. */
export function seqRoute(m: { from: string; to: string | string[] }, name: (id: string) => string): string {
  return m.from === m.to ? name(m.from) : `${name(m.from)} → ${[m.to].flat().map(name).join(', ')}`
}

/** Aus den Daten erzeugte Textalternative: eine Zeile je Nachricht/Schicht/Knoten/Zeile. */
export function diagramAlt(d: DiagramData): string[] {
  if (d.kind === 'sequence') {
    const name = (id: string) => d.actors.find((a) => a.id === id)?.label ?? id
    return d.messages.map((m, i) =>
      `${i + 1}. ${m.at ? `[${m.at}] ` : ''}${seqRoute(m, name)}: ${m.label}${m.detail ? ` — ${m.detail}` : ''}${m.divider ? ` — ${m.divider}` : ''}`)
  }
  if (d.kind === 'layers') {
    return d.layers.map((l) => [l.name, l.content, l.pdu].filter(Boolean).join(' — '))
  }
  if (d.kind === 'flow') {
    const name = (id: string) => d.nodes.find((n) => n.id === id)?.label ?? id
    return [
      ...d.nodes.map((n) => `${n.label}${n.detail ? ` — ${n.detail}` : ''}`),
      ...(d.edges ?? []).map((e) => `${name(e.from)} ${e.arrow === 'none' ? '—' : e.arrow === 'both' ? '↔' : '→'} ${name(e.to)}${e.label ? `: ${e.label}` : ''}`),
    ]
  }
  return d.rows.map((r) => `${r.label}: ${r.values.map((v, i) => `${d.columns[i]?.title ?? ''} = ${v}`).join('; ')}${r.detail ? ` — ${r.detail}` : ''}`)
}
