import { openPrerequisites } from '@/lib/lockedModules'
import type { Follow, ModuleMeta, ProgressItem } from '@/types'

/** Modul, zu dem der „Folgt mir“-Hinweis führen soll — oder null: kein geteilter
 *  Stand, Teilnehmer ist schon dort, Hinweis für dieses Modul weggeklickt, oder
 *  das Modul steht ihm (noch) nicht offen (nicht im Kurs bzw. Voraussetzung offen). */
export function followTarget(
  follow: Follow | null | undefined,
  current: string | null,
  modules: ModuleMeta[],
  progress: ProgressItem[],
  dismissed: string[],
): ModuleMeta | null {
  if (!follow || follow.module_key === current || dismissed.includes(follow.module_key)) return null
  const target = modules.find((m) => m.key === follow.module_key)
  return target && openPrerequisites(target, progress, modules).length === 0 ? target : null
}

/** Ziel-Adresse; mit Block springt ModulePage über #b-<uid> dorthin (wie ein Suchtreffer). */
export function followHref(follow: Follow): string {
  return `/lernen/${follow.module_key}${follow.block_uid ? `#b-${encodeURIComponent(follow.block_uid)}` : ''}`
}

// Weggeklickte Module je Browser-Tab; Speicher kann gesperrt sein (privater Modus).
const DISMISSED_KEY = 'intlab-follow-dismissed'

export function loadDismissed(): string[] {
  try {
    const raw = JSON.parse(sessionStorage.getItem(DISMISSED_KEY) ?? '[]')
    return Array.isArray(raw) ? raw.filter((k): k is string => typeof k === 'string') : []
  } catch {
    return []
  }
}

export function dismiss(dismissed: string[], key: string): string[] {
  const next = [...new Set([...dismissed, key])]
  try {
    sessionStorage.setItem(DISMISSED_KEY, JSON.stringify(next))
  } catch { /* nur für diese Seite gemerkt */ }
  return next
}
