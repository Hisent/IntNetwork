// Reine Logik der Übungsblöcke match, cloze und scenario.
import type { ClozeData, ClozeGap, ScenarioData, ScenarioNode } from './types'

// --- match -------------------------------------------------------------------
// assignment[i] = Index der rechten Karte, die Begriff i zugeordnet ist (richtig: i).

export function assignPair(assignment: (number | null)[], left: number, right: number): (number | null)[] {
  // eine Beschreibung gehört höchstens zu einem Begriff
  return assignment.map((r, i) => (i === left ? right : r === right ? null : r))
}

export function matchResult(assignment: (number | null)[]): boolean[] {
  return assignment.map((r, i) => r === i)
}

// --- cloze -------------------------------------------------------------------

export type ClozePart = { text: string } | { gap: string }

/** Zerlegt `... [[id]] ...` in Text- und Lückenstücke. `[[…]]` statt `{{…}}`, weil
 * Jinja/Ansible-Beispiele selbst `{{ var }}` enthalten. Nur bekannte Lücken-ids zählen. */
export function parseCloze(text: string, ids?: ReadonlySet<string>): ClozePart[] {
  const parts: ClozePart[] = []
  let last = 0
  for (const m of text.matchAll(/\[\[([a-z0-9][a-z0-9_-]*)\]\]/g)) {
    if (ids && !ids.has(m[1])) continue
    if (m.index > last) parts.push({ text: text.slice(last, m.index) })
    parts.push({ gap: m[1] })
    last = m.index + m[0].length
  }
  if (last < text.length) parts.push({ text: text.slice(last) })
  return parts
}

/** Auswahl-Lücke: value = Options-Index als Text. Freitext: gegen `accept`, tolerant je Konfiguration. */
export function gapCorrect(gap: ClozeGap, value: string): boolean {
  if (gap.options) return value !== '' && Number(value) === gap.answer
  const norm = (s: string) => {
    const t = gap.strict_whitespace ? s : s.trim().replace(/\s+/g, ' ')
    return gap.case_sensitive ? t : t.toLowerCase()
  }
  return (gap.accept ?? []).some((a) => norm(a) === norm(value))
}

export function clozeResult(data: ClozeData, values: Record<string, string>): Record<string, boolean> {
  return Object.fromEntries(data.gaps.map((g) => [g.id, gapCorrect(g, values[g.id] ?? '')]))
}

/** Musterlösung einer Lücke für die Anzeige. */
export function gapSolution(gap: ClozeGap): string {
  return gap.options ? gap.options[gap.answer ?? 0] ?? '' : gap.accept?.[0] ?? ''
}

// --- scenario ----------------------------------------------------------------

/** Läuft die gewählten Optionen ab und liefert die besuchten Knoten (letzter = aktueller).
 * Ungültige Wahl/Referenz beendet den Lauf am letzten gültigen Knoten. */
export function walkScenario(data: ScenarioData, choices: number[]): ScenarioNode[] {
  const byId = new Map(data.nodes.map((n) => [n.id, n]))
  const start = byId.get(data.start)
  if (!start) return []
  const visited = [start]
  for (const choice of choices) {
    const next = byId.get(visited[visited.length - 1].options?.[choice]?.to ?? '')
    if (!next) break
    visited.push(next)
  }
  return visited
}
