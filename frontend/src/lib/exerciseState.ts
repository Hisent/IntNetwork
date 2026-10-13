// Stand der Mini-Übungen je Teilnehmer, Kurs, Modul und Block-Kennung — nur im
// Browser (localStorage), wie der Lese-Fortschritt (readProgress.ts): persönliche
// Orientierung ohne Bewertung; der echte Abschluss bleibt das Quiz.
// Ein Key je Modul (`intnetwork-exercise-<participantId>-<courseId>-<modul>`) mit
// { <block-uid>: { v, s, done } } — pruneOtherParticipants räumt ihn mit auf.
import { createContext, useContext, useEffect, useRef, useState, type Dispatch, type SetStateAction } from 'react'

export interface ExerciseRecord {
  v: string // Fingerabdruck des Blockinhalts, zu dem der Stand gehört
  s: unknown
  done: boolean
}

export const exerciseStorageKey = (keyScope: string, moduleKey: string) =>
  keyScope && moduleKey ? `intnetwork-exercise-${keyScope}-${moduleKey}` : ''

export function loadExercises(storageKey: string): Record<string, ExerciseRecord> {
  if (!storageKey) return {}
  try {
    const raw: unknown = JSON.parse(localStorage.getItem(storageKey) ?? '{}')
    return raw && typeof raw === 'object' && !Array.isArray(raw) ? raw as Record<string, ExerciseRecord> : {}
  } catch {
    return {}
  }
}

function saveExercise(storageKey: string, uid: string, record: ExerciseRecord): void {
  try {
    localStorage.setItem(storageKey, JSON.stringify({ ...loadExercises(storageKey), [uid]: record }))
  } catch {
    // Speicher voll/blockiert — der Stand gilt dann nur für diese Sitzung.
  }
}

// ponytail: Der Stand gilt nur für exakt den Blockinhalt, mit dem er entstand —
// ändert sich der Block (Content-Update, Sprachwechsel), beginnt die Übung neu,
// statt alte Indizes auf neue Optionen zu legen. Wer den Stand über Sprachen
// hinweg halten will, braucht je Blocktyp einen sprachneutralen Fingerabdruck.
export function fingerprint(value: unknown): string {
  const text = JSON.stringify(value) ?? ''
  let hash = 5381
  for (let i = 0; i < text.length; i++) hash = ((hash << 5) + hash + text.charCodeAt(i)) | 0
  return `${text.length}.${hash}`
}

/** Welche gespeicherten Übungen sind erledigt (und passen noch zum Blockinhalt)? */
export function doneExercises(storageKey: string, versions: Record<string, string>): Set<string> {
  const saved = loadExercises(storageKey)
  return new Set(Object.keys(versions).filter((uid) => saved[uid]?.done === true && saved[uid].v === versions[uid]))
}

export interface ExerciseSlot {
  storageKey: string
  uid: string
  v: string
  onDone: (uid: string, done: boolean) => void
}

// Von `Blocks` je Block bereitgestellt. Ohne Slot (Trainer-Vorschau, noch kein
// Teilnehmerkontext) verhält sich useExercise wie useState.
export const ExerciseSlotContext = createContext<ExerciseSlot | null>(null)

/** useState, dessen Wert je Block gemerkt wird. `isDone` entscheidet, ob die Übung als erledigt zählt. */
export function useExercise<T>(initial: T | (() => T), isDone: (state: T) => boolean): [T, Dispatch<SetStateAction<T>>] {
  const slot = useContext(ExerciseSlotContext)
  const [state, setState] = useState<T>(() => {
    const saved = slot ? loadExercises(slot.storageKey)[slot.uid] : undefined
    if (saved && saved.v === slot!.v) return saved.s as T
    return typeof initial === 'function' ? (initial as () => T)() : initial
  })
  const untouched = useRef(state)
  useEffect(() => {
    if (!slot || untouched.current === state) return  // nur echte Änderungen speichern, nicht den Startwert
    untouched.current = undefined as T
    const done = isDone(state)
    saveExercise(slot.storageKey, slot.uid, { v: slot.v, s: state, done })
    slot.onDone(slot.uid, done)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- isDone/slot sind je Block stabil genug; gespeichert wird bei Zustandswechsel
  }, [state])
  return [state, setState]
}
