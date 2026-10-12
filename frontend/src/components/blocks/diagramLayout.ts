// Reine Layout-Funktionen für die SVG-Diagramme (sequence, flow). Kein DOM,
// keine Textmessung: Breiten werden aus Zeichenklassen geschätzt (bewusst
// großzügig), damit Text weder abgeschnitten wird noch überlappt — und damit
// das Layout in jsdom/Node testbar bleibt.
import type { DiagramData, FlowDiagram, SequenceDiagram } from './types'

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

/** Bricht an Leerzeichen um; Wörter, die allein zu breit sind, werden hart geteilt. */
export function wrapText(text: string, maxWidth: number, fontSize: number): string[] {
  const lines: string[] = []
  for (const para of text.split('\n')) {
    let line = ''
    for (let word of para.split(/\s+/).filter(Boolean)) {
      while (textWidth(word, fontSize) > maxWidth) {
        if (line) { lines.push(line); line = '' }
        let cut = 1
        while (cut < word.length && textWidth(word.slice(0, cut + 1), fontSize) <= maxWidth) cut++
        lines.push(word.slice(0, cut))
        word = word.slice(cut)
      }
      if (!word) continue
      const candidate = line ? `${line} ${word}` : word
      if (textWidth(candidate, fontSize) <= maxWidth) line = candidate
      else { lines.push(line); line = word }
    }
    if (line) lines.push(line)
  }
  return lines.length ? lines : ['']
}

// --- sequence ----------------------------------------------------------------

export const SEQ = { actorFont: 15, labelFont: 14, noteFont: 13, lineH: 18, pad: 12 }

export interface SeqActorBox { id: string; x: number; w: number; h: number; lines: string[] }
export interface SeqMessageBox {
  index: number
  self: boolean
  x1: number; x2: number
  /** Oberkante des Beschriftungsblocks bzw. der Notiz-Box */
  top: number
  /** y der Pfeillinie (bei self: Unterkante der Box) */
  y: number
  lines: string[]
  /** Mitte und Breite des Textblocks */
  cx: number; w: number
}
export interface SeqLayout { width: number; height: number; headH: number; actors: SeqActorBox[]; messages: SeqMessageBox[] }

export function layoutSequence(d: SequenceDiagram): SeqLayout {
  const n = d.actors.length
  const colW = Math.min(280, Math.max(150, 760 / n))
  const width = colW * n
  const boxW = colW - 20
  const actors = d.actors.map((a, i) => {
    const lines = wrapText(a.label, boxW - 2 * SEQ.pad, SEQ.actorFont)
    return { id: a.id, x: colW * (i + 0.5), w: boxW, h: lines.length * SEQ.lineH + 14, lines }
  })
  const headH = Math.max(...actors.map((a) => a.h))
  for (const a of actors) a.h = headH
  const xOf = (id: string) => actors.find((a) => a.id === id)?.x ?? colW / 2

  let y = headH + 22
  const messages = d.messages.map((m, index) => {
    const x1 = xOf(m.from)
    const x2 = xOf(m.to)
    if (m.from === m.to) {
      // Nachricht an sich selbst = Notiz-Box auf der Lebenslinie (interner Schritt)
      const w = Math.min(colW - 16, 230)
      const cx = Math.min(Math.max(x1, w / 2 + 4), width - w / 2 - 4)
      const lines = wrapText(m.label, w - 2 * SEQ.pad, SEQ.noteFont)
      const top = y
      y += lines.length * SEQ.lineH + 12
      const box = { index, self: true, x1, x2, top, y, lines, cx, w }
      y += 20
      return box
    }
    const span = Math.abs(x2 - x1)
    const w = span - 24
    const lines = wrapText(m.label, w, SEQ.labelFont)
    const top = y
    y += lines.length * SEQ.lineH + 6
    const box = { index, self: false, x1, x2, top, y, lines, cx: (x1 + x2) / 2, w }
    y += 24
    return box
  })
  return { width, height: y + 4, headH, actors, messages }
}

// --- flow --------------------------------------------------------------------

export const FLOW = { nodeW: 136, font: 13, edgeFont: 12, lineH: 16, iconH: 24, pad: 16 }

export interface FlowNodeBox { id: string; cx: number; cy: number; w: number; h: number; lines: string[]; icon: boolean }
export interface FlowEdgeBox {
  key: string
  x1: number; y1: number; x2: number; y2: number
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
  const height = y - gapY + FLOW.pad
  const width = cols * FLOW.nodeW + (cols - 1) * gapX + 2 * FLOW.pad

  const nodes: FlowNodeBox[] = measured.map(({ n, lines, icon, h }) => {
    const r = n.row - minRow
    return {
      id: n.id, lines, icon, w: FLOW.nodeW, h,
      cx: FLOW.pad + (n.col - minCol) * (FLOW.nodeW + gapX) + FLOW.nodeW / 2,
      cy: rowTop[r] + rowH[r] / 2,
    }
  })
  const byId = new Map(nodes.map((b) => [b.id, b]))

  const edgeBoxes: FlowEdgeBox[] = edges.flatMap((e, i) => {
    const a = byId.get(e.from)
    const b = byId.get(e.to)
    if (!a || !b) return []
    let [x1, y1] = clip(a, b.cx, b.cy, e.arrow === 'both' ? 5 : 2)
    let [x2, y2] = clip(b, a.cx, a.cy, e.arrow === 'none' ? 2 : 5)
    // Hin- und Rückkante zwischen denselben Knoten: seitlich versetzen statt überdecken
    const twin = edges.some((o, oi) => oi !== i && o.from === e.to && o.to === e.from)
    const len = Math.hypot(x2 - x1, y2 - y1) || 1
    const nx = -(y2 - y1) / len
    const ny = (x2 - x1) / len
    if (twin) { x1 += nx * 9; y1 += ny * 9; x2 += nx * 9; y2 += ny * 9 }
    const lines = edgeLabels[i]
    let label: FlowEdgeBox['label']
    if (lines) {
      const w = Math.max(...lines.map((s) => textWidth(s, FLOW.edgeFont))) + 12
      const h = lines.length * FLOW.lineH + 6
      // bei Zwillingskanten die Beschriftung ganz neben die (schon versetzte) Linie schieben
      const off = twin ? (Math.abs(nx) * w + Math.abs(ny) * h) / 2 + 3 : 0
      label = { cx: (x1 + x2) / 2 + nx * off, cy: (y1 + y2) / 2 + ny * off, w, h, lines }
    }
    return [{ key: edgeKey(e, i), x1, y1, x2, y2, label }]
  })
  return { width, height, nodes, edges: edgeBoxes }
}

// --- Textalternative ---------------------------------------------------------

/** Aus den Daten erzeugte Textalternative: eine Zeile je Nachricht/Schicht/Knoten/Zeile. */
export function diagramAlt(d: DiagramData): string[] {
  if (d.kind === 'sequence') {
    const name = (id: string) => d.actors.find((a) => a.id === id)?.label ?? id
    return d.messages.map((m, i) =>
      `${i + 1}. ${m.from === m.to ? name(m.from) : `${name(m.from)} → ${name(m.to)}`}: ${m.label}${m.detail ? ` — ${m.detail}` : ''}`)
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
  return d.rows.map((r) => `${r.label}: ${r.values.map((v, i) => `${d.columns[i]?.title ?? ''} = ${v}`).join('; ')}`)
}
