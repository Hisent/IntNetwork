// Reine Logik der deklarativen CLI-Simulation (terminal-Block).
import type { Lang } from '@/lib/i18n'
import type { TerminalData, TerminalTask } from './types'

export function normalize(input: string, caseSensitive = false): string {
  const s = input.trim().replace(/\s+/g, ' ')
  return caseSensitive ? s : s.toLowerCase()
}

/** Exakter Vergleich; `*` im Muster steht für beliebigen nichtleeren Text. */
function patternMatches(pattern: string, input: string): boolean {
  if (!pattern.includes('*')) return pattern === input
  const re = pattern.split('*').map((part) => part.replace(/[.+?^${}()|[\]\\]/g, '\\$&')).join('.+')
  return new RegExp(`^${re}$`).test(input)
}

/** Geräte-typische Abkürzung: jedes Wort ist ein Präfix des Musterworts (`sh ip int br`). */
function abbrevMatches(pattern: string, input: string): boolean {
  const p = pattern.split(' ')
  const i = input.split(' ')
  return p.length === i.length && i.every((word, k) => p[k] === '*' || p[k].startsWith(word))
}

export type CommandMatch = { kind: 'match'; index: number } | { kind: 'ambiguous' } | { kind: 'none' }

export function findCommand(spec: TerminalData, raw: string): CommandMatch {
  const input = normalize(raw, spec.case_sensitive)
  const names = spec.commands.map((c) => [c.cmd, ...(c.aliases ?? [])].map((n) => normalize(n, spec.case_sensitive)))
  const exact = names.findIndex((list) => list.some((n) => patternMatches(n, input)))
  if (exact >= 0) return { kind: 'match', index: exact }
  if (!spec.abbreviations) return { kind: 'none' }
  const hits = names.flatMap((list, index) => (list.some((n) => abbrevMatches(n, input)) ? [index] : []))
  if (hits.length === 1) return { kind: 'match', index: hits[0] }
  return hits.length > 1 ? { kind: 'ambiguous' } : { kind: 'none' }
}

export function helpText(spec: TerminalData, lang: Lang): string {
  const width = Math.max(...spec.commands.map((c) => c.cmd.length))
  return [
    lang === 'de' ? 'Verfügbare Befehle:' : 'Available commands:',
    ...spec.commands.map((c) => `  ${c.cmd.padEnd(width)}${c.desc ? `  ${c.desc}` : ''}`.trimEnd()),
  ].join('\n')
}

export interface TerminalResult { output: string; index?: number; prompt?: string }

export function runCommand(spec: TerminalData, raw: string, lang: Lang): TerminalResult {
  if (!raw.trim()) return { output: '' }
  const m = findCommand(spec, raw)
  if (m.kind === 'match') {
    const c = spec.commands[m.index]
    return { output: c.output, index: m.index, prompt: c.prompt }
  }
  // ein vom Autor definiertes "help"/"?" gewinnt oben; sonst die generierte Liste
  if (['?', 'help'].includes(normalize(raw))) return { output: helpText(spec, lang) }
  if (m.kind === 'ambiguous') return { output: lang === 'de' ? '% Mehrdeutiger Befehl — ? zeigt die Befehlsliste.' : '% Ambiguous command — ? lists the commands.' }
  const fallback = lang === 'de' ? '% Unbekannter Befehl: {cmd} — ? zeigt die Befehlsliste.' : '% Unknown command: {cmd} — ? lists the commands.'
  return { output: (spec.unknown ?? fallback).replaceAll('{cmd}', raw.trim()) }
}

/** Befehle, die als Klick-Chip angeboten werden (Muster mit `*` sind nicht klickbar). */
export function chipCommands(spec: TerminalData): string[] {
  return spec.commands.filter((c) => c.chip !== false && !c.cmd.includes('*')).map((c) => c.cmd)
}

/** Aufgabe erledigt? `executed` = Indizes ausgeführter Befehle, `answer` = Texteingabe zur Aufgabe. */
export function taskDone(spec: TerminalData, task: TerminalTask, executed: ReadonlySet<number>, answer = ''): boolean {
  if (task.command !== undefined) {
    const m = findCommand({ ...spec, abbreviations: false }, task.command)
    return m.kind === 'match' && executed.has(m.index)
  }
  const given = normalize(answer)
  return given !== '' && (task.answers ?? []).some((a) => normalize(a) === given)
}
