// Lese-Fortschritt je Modul, nur im Browser (localStorage) — bewusst ohne
// Backend: persönliche Orientierung, der echte Abschluss bleibt das Quiz.
// ponytail: Indizes verschieben sich, wenn der Trainer Blöcke umsortiert —
// dann stimmen alte Haken nicht mehr; für einen Lese-Merker akzeptabel.
const storageKey = (moduleKey: string) => `intnetwork-read-${moduleKey}`

export function loadRead(moduleKey: string): number[] {
  try {
    const raw = JSON.parse(localStorage.getItem(storageKey(moduleKey)) ?? '[]')
    return Array.isArray(raw) ? raw.filter((x) => typeof x === 'number') : []
  } catch {
    return []
  }
}

export function toggleRead(moduleKey: string, current: number[], index: number): number[] {
  const next = current.includes(index) ? current.filter((x) => x !== index) : [...current, index]
  localStorage.setItem(storageKey(moduleKey), JSON.stringify(next))
  return next
}
