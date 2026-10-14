// Stand der Mini-Übungen je Teilnehmer, Kurs, Modul und Block-Kennung — nur im
// Browser (localStorage), wie der Lese-Fortschritt (readProgress.ts): persönliche
// Orientierung ohne Bewertung; der echte Abschluss bleibt das Quiz.
// Ein Key je Modul (`intnetwork-exercise-<participantId>-<courseId>-<modul>`) mit
// { <block-uid>: { v, s, done } } — pruneOtherParticipants räumt ihn mit auf.
// Zusätzlich auf dem Server, geräteübergreifend: lib/moduleStateSync.ts (markChanged).
import { createContext, useContext, useEffect, useRef, useState, type Dispatch, type SetStateAction } from 'react'
import { markChanged } from '@/lib/moduleStateSync'

export interface ExerciseRecord {
  v: string // Fingerabdruck des Blockinhalts, zu dem der Stand gehört
  s: unknown
  done: boolean
}

const PREFIX = 'intnetwork-exercise-'
export const exerciseStorageKey = (keyScope: string, moduleKey: string) =>
  keyScope && moduleKey ? `${PREFIX}${keyScope}-${moduleKey}` : ''

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
    markChanged(storageKey.slice(PREFIX.length))
  } catch {
    // Speicher voll/blockiert — der Stand gilt dann nur für diese Sitzung.
  }
}

function hash(text: string): string {
  let h = 5381
  for (let i = 0; i < text.length; i++) h = ((h << 5) + h + text.charCodeAt(i)) | 0
  return `${text.length}.${h}`
}

// Anzeigetexte, die je Sprache anders ausgeliefert werden (backend/app/services/
// block_validation.py: alles, was als X_de/X_en im Payload stehen darf). Sie zählen
// nicht zum Fingerabdruck — nur ihre Anzahl (Textlisten wie options/items/lines).
const TEXT_KEYS = new Set([
  'title', 'caption', 'label', 'detail', 'at', 'divider', 'name', 'content', 'pdu', 'text', 'desc', 'intro',
  'unknown', 'explanation', 'prompt', 'left', 'right', 'output', 'value', 'teaser', 'note', 'options', 'items', 'lines',
])

// Der Stand gilt nur für die Struktur und Lösung, mit der er entstand (Typ, Anzahl,
// Indizes, ids, Befehle) — ändert sie sich (Content-Update), beginnt die Übung neu,
// statt alte Indizes auf neue Optionen zu legen. Reine Textänderungen und der
// Sprachwechsel lassen ihn stehen: gelöst bleibt in beiden Sprachen gelöst.
// ponytail: `accept` (Freitext-Lösungen) bleibt im Fingerabdruck — ist es je Sprache
// verschieden, gilt der Stand dieser einen Lücke weiterhin nur in seiner Sprache.
export function fingerprint(value: unknown): string {
  return hash(JSON.stringify(value, (key, v: unknown) => {
    if (!TEXT_KEYS.has(key)) return v
    if (typeof v === 'string') return ''
    return Array.isArray(v) && v.every((x) => typeof x === 'string') ? v.length : v
  }) ?? '')
}

/** Fingerabdruck bis v1.43 (ganzer, sprachabhängiger Blockinhalt): damit gespeicherte Stände bleiben gültig. */
export const legacyFingerprint = (value: unknown): string => hash(JSON.stringify(value) ?? '')

const fits = (saved: ExerciseRecord | undefined, v: string, legacy?: string): saved is ExerciseRecord =>
  !!saved && (saved.v === v || (legacy !== undefined && saved.v === legacy))

/** Welche gespeicherten Übungen sind erledigt (und passen noch zum Blockinhalt)? */
export function doneExercises(storageKey: string, versions: Record<string, string>, legacy: Record<string, string> = {}): Set<string> {
  const saved = loadExercises(storageKey)
  return new Set(Object.keys(versions).filter((uid) => fits(saved[uid], versions[uid], legacy[uid]) && saved[uid].done === true))
}

export interface ExerciseSlot {
  storageKey: string
  uid: string
  v: string
  /** alter Fingerabdruck desselben Blocks — nur zum Lesen bereits gespeicherter Stände */
  legacy?: string
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
    if (slot && fits(saved, slot.v, slot.legacy)) return saved.s as T
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
