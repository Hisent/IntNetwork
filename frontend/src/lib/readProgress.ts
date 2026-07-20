// Lese-Fortschritt je Teilnehmer, Kurs und Modul, nur im Browser (localStorage) —
// bewusst ohne Backend: persönliche Orientierung, der echte Abschluss bleibt das Quiz.
// participantId gehört zwingend in den Schlüssel, sonst sehen zwei Personen am
// selben Browser die Haken der jeweils anderen.
// ponytail: Indizes verschieben sich, wenn der Trainer Blöcke umsortiert —
// dann stimmen alte Haken nicht mehr; für einen Lese-Merker akzeptabel.
const storageKey = (participantId: number, courseId: number, moduleKey: string) =>
  `intnetwork-read-${participantId}-${courseId}-${moduleKey}`

export function loadRead(participantId: number, courseId: number, moduleKey: string): number[] {
  try {
    const raw = JSON.parse(localStorage.getItem(storageKey(participantId, courseId, moduleKey)) ?? '[]')
    return Array.isArray(raw) ? raw.filter((x) => typeof x === 'number') : []
  } catch {
    return []
  }
}

export function toggleRead(participantId: number, courseId: number, moduleKey: string, current: number[], index: number): number[] {
  const next = current.includes(index) ? current.filter((x) => x !== index) : [...current, index]
  localStorage.setItem(storageKey(participantId, courseId, moduleKey), JSON.stringify(next))
  return next
}
