// Reine Logik der deklarativen CLI-Simulation (terminal-Block).
import type { Lang } from '@/lib/i18n'
import type { TerminalData, TerminalTask } from './types'

export function normalize(input: string, caseSensitive = false): string {
  const s = input.trim().replace(/\s+/g, ' ')
  return caseSensitive ? s : s.toLowerCase()
}

// `\*` im Muster ist ein wörtlicher Stern (`clear ip nat translation \*`).
const STAR = '\u0000'
const hide = (pattern: string) => pattern.replaceAll('\\*', STAR)
/** Schreibweise eines Befehls, wie der Teilnehmer ihn tippt (ohne Escape). */
export const literal = (pattern: string) => pattern.replaceAll('\\*', '*')
const hasWildcard = (pattern: string) => hide(pattern).includes('*')

/** Exakter Vergleich; `*` im Muster steht für beliebigen nichtleeren Text. */
function patternMatches(pattern: string, input: string): boolean {
  if (!hasWildcard(pattern)) return literal(pattern) === input
  const re = hide(pattern).split('*').map((part) => part.replace(/[.+?^${}()|[\]\\]/g, '\\$&').replaceAll(STAR, '\\*')).join('.+')
  return new RegExp(`^${re}$`).test(input)
}

/** Geräte-typische Abkürzung: jedes Wort ist ein Präfix des Musterworts (`sh ip int br`). */
function abbrevMatches(pattern: string, input: string): boolean {
  const p = pattern.split(' ')
  const i = input.split(' ')
  return p.length === i.length && i.every((word, k) => p[k] === '*' || literal(p[k]).startsWith(word))
}

export type CommandMatch = { kind: 'match'; index: number } | { kind: 'ambiguous' } | { kind: 'none' }

export function findCommand(spec: TerminalData, raw: string): CommandMatch {
  const input = normalize(raw, spec.case_sensitive)
  const names = spec.commands.map((c) => [c.cmd, ...(c.aliases ?? [])].map((n) => normalize(n, spec.case_sensitive)))
  // wörtliche Schreibweisen vor Platzhalter-Mustern: `ping *` darf ein später stehendes `ping 10.0.0.1` nicht verdecken
  for (const wildcard of [false, true]) {
    const exact = names.findIndex((list) => list.some((n) => hasWildcard(n) === wildcard && patternMatches(n, input)))
    if (exact >= 0) return { kind: 'match', index: exact }
  }
  if (!spec.abbreviations) return { kind: 'none' }
  const hits = names.flatMap((list, index) => (list.some((n) => abbrevMatches(n, input)) ? [index] : []))
  if (hits.length === 1) return { kind: 'match', index: hits[0] }
  return hits.length > 1 ? { kind: 'ambiguous' } : { kind: 'none' }
}

export function helpText(spec: TerminalData, lang: Lang): string {
  const width = Math.max(...spec.commands.map((c) => literal(c.cmd).length))
  return [
    lang === 'de' ? 'Verfügbare Befehle:' : 'Available commands:',
    ...spec.commands.map((c) => `  ${literal(c.cmd).padEnd(width)}${c.desc ? `  ${c.desc}` : ''}`.trimEnd()),
  ].join('\n')
}

export interface TerminalResult { output: string; index?: number; prompt?: string; flags?: string[] }

const NO_FLAGS: readonly string[] = []

/** `flags` = bisher gesetzte Zustands-Flags. Die Ausgabe richtet sich nach dem Stand VOR dem
 * Befehl (erste `variants`-Zeile mit gesetztem `when`, sonst `output`); danach wirken
 * `clears`, dann `sets`. `flags` im Ergebnis nur, wenn der Befehl den Zustand ändert. */
export function runCommand(spec: TerminalData, raw: string, lang: Lang, flags: readonly string[] = NO_FLAGS): TerminalResult {
  if (!raw.trim()) return { output: '' }
  const m = findCommand(spec, raw)
  if (m.kind === 'match') {
    const c = spec.commands[m.index]
    const output = c.variants?.find((v) => flags.includes(v.when))?.output ?? c.output
    const result: TerminalResult = { output, index: m.index, prompt: c.prompt }
    if (c.sets || c.clears) result.flags = [...new Set([...flags.filter((f) => !c.clears?.includes(f)), ...(c.sets ?? [])])]
    return result
  }
  // ein vom Autor definiertes "help"/"?" gewinnt oben; sonst die generierte Liste
  if (['?', 'help'].includes(normalize(raw, spec.case_sensitive))) return { output: helpText(spec, lang) }
  if (m.kind === 'ambiguous') return { output: lang === 'de' ? '% Mehrdeutiger Befehl — ? zeigt die Befehlsliste.' : '% Ambiguous command — ? lists the commands.' }
  const fallback = lang === 'de' ? '% Unbekannter Befehl: {cmd} — ? zeigt die Befehlsliste.' : '% Unknown command: {cmd} — ? lists the commands.'
  return { output: (spec.unknown ?? fallback).replaceAll('{cmd}', raw.trim()) }
}

/** Befehle, die als Klick-Chip angeboten werden (Muster mit `*` sind nicht klickbar). */
export function chipCommands(spec: TerminalData): string[] {
  return spec.commands.filter((c) => c.chip !== false && !hasWildcard(c.cmd)).map((c) => literal(c.cmd))
}

/** Aufgabe erledigt? `executed` = Indizes ausgeführter Befehle, `answer` = Texteingabe zur Aufgabe. */
export function taskDone(spec: TerminalData, task: TerminalTask, executed: ReadonlySet<number>, answer = ''): boolean {
  if (task.command !== undefined) {
    const m = findCommand({ ...spec, abbreviations: false }, literal(task.command))
    return m.kind === 'match' && executed.has(m.index)
  }
  const given = normalize(answer)
  return given !== '' && (task.answers ?? []).some((a) => normalize(a) === given)
}
