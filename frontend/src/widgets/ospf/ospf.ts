// Reine OSPF-Kernlogik (keine UI-Abhängigkeiten, gut testbar).
//
// Modell: ein ungerichteter Graph aus Standorten (Knoten) und Leitungen
// (Kanten). Jede Leitung trägt eine Bandbreite in Mbit/s; daraus wird nach
// der klassischen OSPF-Formel eine Kosten-Metrik abgeleitet:
//   Kosten = Referenzbandbreite / Bandbreite, mindestens 1, abgerundet.
// Dijkstra liefert den kostengünstigsten Pfad (das ist echtes OSPF-Verhalten);
// eine separate Breitensuche liefert zusätzlich den Pfad mit den wenigsten
// Sprüngen (das wäre RIP-Verhalten) — der Unterschied zwischen beiden ist der
// zentrale Lerneffekt dieses Widgets.

export interface LinkSpec {
  a: string
  b: string
  mbit: number
}

export interface Edge extends LinkSpec {
  cost: number
}

export interface Graph {
  nodes: string[]
  edges: Edge[]
}

export interface CostPathResult {
  path: string[]
  cost: number
}

export interface HopPathResult {
  path: string[]
  hops: number
}

/** Klassische Nordwind-Testtopologie: 5 Standorte. */
export const NODES = ['Zentrale', 'Lager', 'FilialeNord', 'FilialeSued', 'Rechenzentrum'] as const

/**
 * Leitungen mit ihrer Bandbreite. Bewusst so gewählt, dass die
 * Zentrale-Rechenzentrum-Standleitung (10 Mbit/s) zwar den wenigsten Sprüngen
 * entspricht, aber wegen ihrer geringen Bandbreite (= hohe Kosten) NICHT der
 * kostengünstigste Weg ist — genau der Fall, an dem man OSPF (Kosten) von
 * RIP (Hop-Count) unterscheiden lernt.
 */
export const TOPOLOGY: LinkSpec[] = [
  { a: 'Zentrale', b: 'Lager', mbit: 1000 },
  { a: 'Zentrale', b: 'Rechenzentrum', mbit: 10 },
  { a: 'Zentrale', b: 'FilialeNord', mbit: 100 },
  { a: 'Lager', b: 'Rechenzentrum', mbit: 100 },
  { a: 'FilialeNord', b: 'FilialeSued', mbit: 100 },
  { a: 'FilialeSued', b: 'Rechenzentrum', mbit: 100 },
]

/** OSPF-Kostenformel: Referenzbandbreite / Bandbreite, abgerundet, mindestens 1. */
export function costFromBandwidth(mbit: number, referenceMbit: number): number {
  return Math.max(1, Math.floor(referenceMbit / mbit))
}

/** Baut den kostenbewerteten Graphen aus den rohen Bandbreiten. */
export function buildGraph(referenceMbit: number, links: LinkSpec[] = TOPOLOGY): Graph {
  const nodes = new Set<string>()
  for (const l of links) { nodes.add(l.a); nodes.add(l.b) }
  return {
    nodes: [...nodes],
    edges: links.map((l) => ({ ...l, cost: costFromBandwidth(l.mbit, referenceMbit) })),
  }
}

/** Neuer Graph ohne die Leitung a—b (Original bleibt unverändert). */
export function withoutLink(graph: Graph, a: string, b: string): Graph {
  return {
    nodes: [...graph.nodes],
    edges: graph.edges.filter((e) => !((e.a === a && e.b === b) || (e.a === b && e.b === a))),
  }
}

function neighborsOf(graph: Graph, node: string): { to: string; edge: Edge }[] {
  const out: { to: string; edge: Edge }[] = []
  for (const e of graph.edges) {
    if (e.a === node) out.push({ to: e.b, edge: e })
    else if (e.b === node) out.push({ to: e.a, edge: e })
  }
  return out
}

/** Dijkstra: kostengünstigster Pfad (Summe der OSPF-Kosten). */
export function shortestPath(graph: Graph, from: string, to: string): CostPathResult | null {
  if (!graph.nodes.includes(from) || !graph.nodes.includes(to)) return null
  const dist = new Map<string, number>(graph.nodes.map((n) => [n, Infinity]))
  const prev = new Map<string, string>()
  const visited = new Set<string>()
  dist.set(from, 0)

  while (true) {
    let u: string | null = null
    let best = Infinity
    for (const n of graph.nodes) {
      if (!visited.has(n) && dist.get(n)! < best) { best = dist.get(n)!; u = n }
    }
    if (u === null) break
    visited.add(u)
    if (u === to) break
    for (const { to: v, edge } of neighborsOf(graph, u)) {
      if (visited.has(v)) continue
      const nd = dist.get(u)! + edge.cost
      if (nd < dist.get(v)!) { dist.set(v, nd); prev.set(v, u) }
    }
  }

  if (dist.get(to) === Infinity || dist.get(to) === undefined) return null

  const path = [to]
  let cur = to
  while (cur !== from) {
    const p = prev.get(cur)
    if (p === undefined) return null
    path.unshift(p)
    cur = p
  }
  return { path, cost: dist.get(to)! }
}

/** Breitensuche: Pfad mit den wenigsten Sprüngen (RIP-artig, ignoriert Kosten). */
export function fewestHopsPath(graph: Graph, from: string, to: string): HopPathResult | null {
  if (!graph.nodes.includes(from) || !graph.nodes.includes(to)) return null
  if (from === to) return { path: [from], hops: 0 }
  const prev = new Map<string, string>()
  const visited = new Set<string>([from])
  const queue: string[] = [from]

  while (queue.length > 0) {
    const u = queue.shift()!
    for (const { to: v } of neighborsOf(graph, u)) {
      if (visited.has(v)) continue
      visited.add(v)
      prev.set(v, u)
      if (v === to) {
        const path = [to]
        let cur = to
        while (cur !== from) {
          const p = prev.get(cur)!
          path.unshift(p)
          cur = p
        }
        return { path, hops: path.length - 1 }
      }
      queue.push(v)
    }
  }
  return null
}
