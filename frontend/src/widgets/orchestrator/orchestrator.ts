export interface Task {
  de: string
  en: string
  cost: number
}

export const TASKS: Task[] = [
  { de: 'Frontend auf Zugänglichkeit prüfen', en: 'check frontend accessibility', cost: 4 },
  { de: 'Backend auf fehlende Fehlerbehandlung prüfen', en: 'check backend error handling', cost: 6 },
  { de: 'Tests auf Lücken prüfen', en: 'check tests for gaps', cost: 3 },
]

// Wall-Clock-Zeit: nacheinander = Summe, parallel = das langsamste Einzelstück
// (unabhängige Subagents laufen gleichzeitig).
export function wallClock(tasks: Task[], mode: 'sequential' | 'parallel'): number {
  const costs = tasks.map((t) => t.cost)
  if (costs.length === 0) return 0
  return mode === 'parallel' ? Math.max(...costs) : costs.reduce((a, b) => a + b, 0)
}
