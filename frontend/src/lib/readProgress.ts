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

// Alle participantId-tragenden Schlüsselarten (Lese-Fortschritt, Reflexionen,
// Live-CLI-Session — siehe Blocks.tsx / ClaudeCliWidget.tsx). Die participantId
// steht dabei immer als erstes Zahlen-Segment nach der Art.
const SCOPED_KEY = /^intnetwork-(?:read|reflect|cli)-(\d+)-/

// Räumt an geteilten Browsern die Reste anderer Teilnehmer auf: ruft man beim
// Bekanntwerden der aktuellen participantId auf, entfernt sie alle App-eigenen
// Keys, die erkennbar einer ANDEREN participantId gehören. Nicht zuordenbare
// App-Keys (z.B. das Theme) und fremde, nicht-App-Keys bleiben unangetastet.
export function pruneOtherParticipants(currentParticipantId: number): void {
  try {
    const stale: string[] = []
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      const match = key?.match(SCOPED_KEY)
      if (match && Number(match[1]) !== currentParticipantId) stale.push(key!)
    }
    stale.forEach((key) => localStorage.removeItem(key))
  } catch {
    // localStorage kann blockiert sein oder key()/length fehlen — dann nichts tun.
  }
}
