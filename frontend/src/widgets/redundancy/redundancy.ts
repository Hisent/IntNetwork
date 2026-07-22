// Reine Logik für die drei Redundanzmechanismen (keine UI-Abhängigkeiten).
//
// Teil A: STP-Root-Wahl — vereinfacht auf die zwei tatsächlich
// entscheidenden Kriterien reduziert (Priorität, dann MAC), ohne den vollen
// Bridge-ID-Formalismus (Priorität + erweiterte System-ID) nachzubilden.
// Teil B: Link-Aggregation — Summenbandbreite vs. Einzelfluss-Bandbreite.

export interface SwitchSpec {
  name: string
  priority: number
  mac: string
}

export interface RootElection {
  root: string
  reason: 'priority' | 'mac'
}

/** Vergleicht zwei MAC-Adressen ("AA:BB:CC:DD:EE:FF") oktett-weise numerisch. */
function macCompare(a: string, b: string): number {
  const pa = a.split(':').map((h) => parseInt(h, 16))
  const pb = b.split(':').map((h) => parseInt(h, 16))
  for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
    const diff = (pa[i] ?? 0) - (pb[i] ?? 0)
    if (diff !== 0) return diff
  }
  return 0
}

/**
 * Bestimmt die Root-Bridge nach der echten STP-Regel: niedrigste Priorität
 * gewinnt; bei Gleichstand entscheidet die niedrigste MAC-Adresse.
 */
export function electRoot(switches: SwitchSpec[]): RootElection {
  const minPriority = Math.min(...switches.map((s) => s.priority))
  const candidates = switches.filter((s) => s.priority === minPriority)
  if (candidates.length === 1) {
    return { root: candidates[0].name, reason: 'priority' }
  }
  const winner = candidates.reduce((best, cur) => (macCompare(cur.mac, best.mac) < 0 ? cur : best))
  return { root: winner.name, reason: 'mac' }
}

/** Summenbandbreite des Bündels: steigt linear mit jeder Leitung. */
export function aggregateBandwidth(links: number, linkMbit: number): number {
  return links * linkMbit
}

/**
 * Bandbreite EINES einzelnen Datenflusses: der Verteilungs-Hash bindet einen
 * Fluss fest an eine Leitung — mehr Leitungen im Bündel helfen einem
 * einzelnen Fluss darum nicht.
 */
export function singleFlowBandwidth(linkMbit: number): number {
  return linkMbit
}
