// Lese-Haken (readProgress.ts) und Übungsstand (exerciseState.ts) je Modul auch auf
// dem Server, damit sie nach der Wiederaufnahme auf einem anderen Gerät da sind.
// localStorage bleibt der Arbeitsspeicher und Offline-Cache; diese Datei gleicht ab.
//
// cacheId = `<participantId>-<courseId>-<modul>` — derselbe Suffix wie in den
// Schlüsseln intnetwork-read-… und intnetwork-exercise-….
//
// Konfliktregel über eine Basisversion (keine Uhrzeiten verschiedener Rechner vergleichen):
// - Der Client merkt sich unter intnetwork-base-<cacheId> das updated_at des Servers,
//   das er zuletzt geladen oder selbst gespeichert hat — nur als Kennung, nie als Zeit.
// - Jede lokale Änderung setzt die Marke intnetwork-pending-<cacheId> und wird ~1,5 s
//   später (entprellt) als Ganzes gesendet; erst ein erfolgreicher Upload löscht die
//   Marke und merkt das neue updated_at als Basis.
// - Beim Öffnen des Moduls: hat der Server noch nichts, wird ein vorhandener lokaler
//   Stand hochgeladen. Liegt eine ungesendete lokale Änderung vor und ist der Server
//   noch auf der gemerkten Basis, gewinnt lokal (Upload). Sonst gewinnt der Server und
//   ersetzt den lokalen Cache (frisches Gerät, oder ein anderes Gerät hat inzwischen
//   gespeichert — dessen Stand geht vor, die ungesendete Änderung verfällt).
import { useEffect, useState } from 'react'
import { learnApi, type ModuleState } from '@/lib/learnApi'

export const DEBOUNCE_MS = 1500
const readKey = (cacheId: string) => `intnetwork-read-${cacheId}`
const exerciseKey = (cacheId: string) => `intnetwork-exercise-${cacheId}`
const pendingKey = (cacheId: string) => `intnetwork-pending-${cacheId}`
const baseKey = (cacheId: string) => `intnetwork-base-${cacheId}`
const moduleOf = (cacheId: string) => cacheId.match(/^\d+-\d+-(.+)$/)?.[1] ?? ''

function get(key: string): string | null {
  try { return localStorage.getItem(key) } catch { return null }
}
function set(key: string, value: string | null): void {
  try {
    if (value === null) localStorage.removeItem(key); else localStorage.setItem(key, value)
  } catch { /* Speicher voll/blockiert */ }
}
function parse<T>(raw: string | null, fallback: T, ok: (v: unknown) => boolean): T {
  try {
    const v: unknown = JSON.parse(raw ?? 'null')
    return ok(v) ? v as T : fallback
  } catch { return fallback }
}

function localState(cacheId: string): Pick<ModuleState, 'read' | 'exercises'> {
  return {
    read: parse<number[]>(get(readKey(cacheId)), [], Array.isArray).filter((x) => Number.isInteger(x) && x >= 0),
    exercises: parse(get(exerciseKey(cacheId)), {}, (v) => !!v && typeof v === 'object' && !Array.isArray(v)),
  }
}

const timers = new Map<string, ReturnType<typeof setTimeout>>()

async function push(cacheId: string): Promise<void> {
  const marker = get(pendingKey(cacheId))
  const { data } = await learnApi.putState(moduleOf(cacheId), localState(cacheId))
  set(baseKey(cacheId), data.updated_at)
  // Nur löschen, wenn seitdem nichts Neues dazukam (sonst sendet der nächste Timer).
  if (get(pendingKey(cacheId)) === marker) set(pendingKey(cacheId), null)
}

/** Nach jeder lokalen Änderung aufrufen (readProgress/exerciseState tun das). */
export function markChanged(cacheId: string): void {
  if (!moduleOf(cacheId)) return
  set(pendingKey(cacheId), String(Date.now()))  // nur Änderungsmarke, kein Vergleichszeitpunkt
  clearTimeout(timers.get(cacheId))
  timers.set(cacheId, setTimeout(() => { timers.delete(cacheId); push(cacheId).catch(() => {}) }, DEBOUNCE_MS))
}

/** Wartende Änderung sofort senden (Tab wird verborgen, Modul verlassen). */
export function flush(cacheId: string): void {
  if (!timers.has(cacheId)) return
  clearTimeout(timers.get(cacheId))
  timers.delete(cacheId)
  push(cacheId).catch(() => {})
}

/** Abgleich beim Öffnen eines Moduls (Regel oben). */
export async function syncOnOpen(cacheId: string): Promise<void> {
  const { data } = await learnApi.getState(moduleOf(cacheId))
  const pending = get(pendingKey(cacheId))
  const local = localState(cacheId)
  if (!data.updated_at) {
    if (pending || local.read.length || Object.keys(local.exercises).length) await push(cacheId)
    return
  }
  if (pending && get(baseKey(cacheId)) === data.updated_at) return push(cacheId)
  set(readKey(cacheId), JSON.stringify(data.read))
  set(exerciseKey(cacheId), JSON.stringify(data.exercises))
  set(pendingKey(cacheId), null)
  set(baseKey(cacheId), data.updated_at)
}

// Je Seitenaufruf nur einmal je Modul abgleichen: danach ist der lokale Cache aktuell
// (jede Änderung geht ohnehin hoch), und ein Zurückwechseln zeigt kein Lade-Skelett.
// ponytail: arbeitet jemand im selben Modul gleichzeitig auf zwei Geräten, sieht er
// die Änderungen des anderen erst nach dem Neuladen.
const syncedIds = new Set<string>()

/** true, sobald der Abgleich für dieses Modul durch ist (oder scheiterte — dann gilt
 *  der lokale Cache). Bis dahin noch keinen Stand aus localStorage anzeigen. */
export function useModuleStateSync(scope: string, moduleKey: string): boolean {
  const cacheId = scope && moduleKey ? `${scope}-${moduleKey}` : ''
  const [readyFor, setReadyFor] = useState('')
  useEffect(() => {
    if (!cacheId) return
    let live = true
    if (!syncedIds.has(cacheId)) {
      syncOnOpen(cacheId).then(() => syncedIds.add(cacheId), () => {}).finally(() => { if (live) setReadyFor(cacheId) })
    }
    const onHide = () => { if (document.hidden) flush(cacheId) }
    document.addEventListener('visibilitychange', onHide)
    return () => { live = false; document.removeEventListener('visibilitychange', onHide); flush(cacheId) }
  }, [cacheId])
  return !!cacheId && (readyFor === cacheId || syncedIds.has(cacheId))
}
