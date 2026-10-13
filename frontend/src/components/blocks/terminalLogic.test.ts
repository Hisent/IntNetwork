import { describe, expect, it } from 'vitest'
import { chipCommands, findCommand, helpText, runCommand, taskDone } from './terminalLogic'
import type { TerminalData } from './types'

const spec: TerminalData = {
  prompt: 'sw1#',
  abbreviations: true,
  unknown: "% Invalid input detected: '{cmd}'",
  commands: [
    { cmd: 'show vlan brief', aliases: ['show vlan'], output: 'VLAN 10', desc: 'VLANs' },
    { cmd: 'show version', output: 'IOS 15.2' },
    { cmd: 'configure terminal', output: '', prompt: 'sw1(config)#' },
    { cmd: 'dig * A', output: 'ANSWER', chip: true },
    { cmd: 'show secret', output: 'x', chip: false },
  ],
  tasks: [{ text: 'VLANs ansehen', command: 'show vlan' }, { text: 'Version?', answers: ['15.2', 'IOS 15.2'] }],
}

describe('findCommand', () => {
  it('trifft exakt, ohne Rücksicht auf Groß/Klein und Mehrfach-Leerzeichen', () => {
    expect(findCommand(spec, '  SHOW   vlan  Brief ')).toEqual({ kind: 'match', index: 0 })
  })
  it('kennt Aliasse', () => {
    expect(findCommand(spec, 'show vlan')).toEqual({ kind: 'match', index: 0 })
  })
  it('löst eindeutige Abkürzungen auf', () => {
    expect(findCommand(spec, 'sh ver')).toEqual({ kind: 'match', index: 1 })
    expect(findCommand(spec, 'conf t')).toEqual({ kind: 'match', index: 2 })
  })
  it('meldet mehrdeutige Abkürzungen', () => {
    expect(findCommand(spec, 'sh v')).toEqual({ kind: 'ambiguous' })
  })
  it('kürzt nur ab, wenn das Gerät es erlaubt', () => {
    expect(findCommand({ ...spec, abbreviations: false }, 'sh ver')).toEqual({ kind: 'none' })
  })
  it('behandelt * als Platzhalter für beliebigen Text', () => {
    expect(findCommand(spec, 'dig www.nordwind.example a')).toEqual({ kind: 'match', index: 3 })
    expect(findCommand(spec, 'dig a')).toEqual({ kind: 'none' })
  })
  it('achtet auf Groß/Klein, wenn case_sensitive gesetzt ist', () => {
    const cs = { ...spec, case_sensitive: true, abbreviations: false }
    expect(findCommand(cs, 'Show Version')).toEqual({ kind: 'none' })
    expect(findCommand(cs, 'show version')).toEqual({ kind: 'match', index: 1 })
  })
  it('nimmt Sonderzeichen im Befehl wörtlich', () => {
    const s: TerminalData = { prompt: '$', commands: [{ cmd: 'curl -k https://gm/wapi/v2.12/grid?_return_fields=name', output: '[]' }] }
    expect(findCommand(s, 'curl -k https://gm/wapi/v2.12/grid?_return_fields=name')).toEqual({ kind: 'match', index: 0 })
    expect(findCommand(s, 'curl -k https://gm/wapi/v2x12/grid?_return_fields=name')).toEqual({ kind: 'none' })
  })
})

describe('runCommand', () => {
  it('liefert Ausgabe, Index und neuen Prompt', () => {
    expect(runCommand(spec, 'conf t', 'de')).toEqual({ output: '', index: 2, prompt: 'sw1(config)#' })
  })
  it('listet bei ? und help die Befehle mit Beschreibung', () => {
    const out = runCommand(spec, '?', 'de').output
    expect(out).toBe(helpText(spec, 'de'))
    expect(out).toContain('Verfügbare Befehle:')
    expect(out).toContain('show vlan brief     VLANs')
    expect(runCommand(spec, 'help', 'en').output).toContain('Available commands:')
  })
  it('antwortet auf Unbekanntes mit der gerätetypischen Meldung', () => {
    expect(runCommand(spec, 'reload now', 'de').output).toBe("% Invalid input detected: 'reload now'")
    expect(runCommand({ ...spec, unknown: undefined }, 'reload', 'en').output).toContain('Unknown command: reload')
  })
  it('meldet Mehrdeutigkeit und ignoriert leere Eingaben', () => {
    expect(runCommand(spec, 'sh v', 'en').output).toContain('Ambiguous')
    expect(runCommand(spec, '   ', 'de')).toEqual({ output: '' })
  })
  it('lässt ein vom Autor definiertes help gewinnen', () => {
    expect(runCommand({ prompt: '>', commands: [{ cmd: 'help', output: 'eigene Hilfe' }] }, 'help', 'de').output).toBe('eigene Hilfe')
  })
})

describe('Chips und Aufgaben', () => {
  it('bietet nur klickbare Befehle als Chip an', () => {
    expect(chipCommands(spec)).toEqual(['show vlan brief', 'show version', 'configure terminal'])
  })
  it('hakt eine Befehlsaufgabe ab, sobald der Befehl (auch per Alias) lief', () => {
    expect(taskDone(spec, spec.tasks![0], new Set())).toBe(false)
    expect(taskDone(spec, spec.tasks![0], new Set([1]))).toBe(false)
    expect(taskDone(spec, spec.tasks![0], new Set([0]))).toBe(true)
  })
  it('hakt eine Antwortaufgabe bei einer akzeptierten Eingabe ab', () => {
    expect(taskDone(spec, spec.tasks![1], new Set(), '')).toBe(false)
    expect(taskDone(spec, spec.tasks![1], new Set(), ' ios  15.2 ')).toBe(true)
    expect(taskDone(spec, spec.tasks![1], new Set(), '15.3')).toBe(false)
  })
})

describe('wörtlicher Stern (\\*)', () => {
  const nat: TerminalData = {
    prompt: 'r1#', abbreviations: true,
    commands: [
      { cmd: 'clear ip nat translation \\*', output: '' },
      { cmd: 'ls \\*.log *', output: 'x' },
    ],
    tasks: [{ text: 'Tabelle leeren', command: 'clear ip nat translation \\*' }],
  }
  it('trifft nur den getippten Stern, nicht beliebigen Text', () => {
    expect(findCommand(nat, 'clear ip nat translation *')).toEqual({ kind: 'match', index: 0 })
    expect(findCommand(nat, 'clear ip nat translation inside')).toEqual({ kind: 'none' })
    expect(findCommand(nat, 'cl ip nat tr *')).toEqual({ kind: 'match', index: 0 })
  })
  it('mischt wörtlichen Stern und Platzhalter in einem Muster', () => {
    expect(findCommand(nat, 'ls *.log /var')).toEqual({ kind: 'match', index: 1 })
    expect(findCommand(nat, 'ls a.log /var')).toEqual({ kind: 'none' })
  })
  it('zeigt Chip und Hilfe ohne Escape und hakt die Aufgabe ab', () => {
    expect(chipCommands(nat)).toEqual(['clear ip nat translation *'])
    expect(helpText(nat, 'de')).toContain('  clear ip nat translation *\n')
    expect(taskDone(nat, nat.tasks![0], new Set([0]))).toBe(true)
  })
})

describe('Zustand (sets / clears / variants)', () => {
  const pc: TerminalData = {
    prompt: 'PC>',
    commands: [
      { cmd: 'arp -a', output: 'leer', variants: [{ when: 'failed', output: 'kaputt' }, { when: 'pinged', output: '10.0.0.1' }] },
      { cmd: 'ping 10.0.0.1', output: 'Reply', sets: ['pinged'] },
      { cmd: 'arp -d', output: '', clears: ['pinged'] },
      { cmd: 'toggle', output: 'aus', sets: ['on'], clears: ['on'], variants: [{ when: 'on', output: 'an' }] },
    ],
  }
  it('liefert ohne Flags die Standardausgabe und meldet keine Zustandsänderung', () => {
    expect(runCommand(pc, 'arp -a', 'de')).toEqual({ output: 'leer', index: 0, prompt: undefined })
  })
  it('setzt Flags, wählt die erste passende Variante und löscht wieder', () => {
    const afterPing = runCommand(pc, 'ping 10.0.0.1', 'de', []).flags!
    expect(afterPing).toEqual(['pinged'])
    expect(runCommand(pc, 'arp -a', 'de', afterPing).output).toBe('10.0.0.1')
    expect(runCommand(pc, 'arp -a', 'de', ['pinged', 'failed']).output).toBe('kaputt')
    expect(runCommand(pc, 'ping 10.0.0.1', 'de', afterPing).flags).toEqual(['pinged'])
    expect(runCommand(pc, 'arp -d', 'de', ['other', 'pinged']).flags).toEqual(['other'])
  })
  it('wählt die Ausgabe nach dem Stand VOR dem Befehl; clears wirkt vor sets', () => {
    expect(runCommand(pc, 'toggle', 'de', [])).toMatchObject({ output: 'aus', flags: ['on'] })
    expect(runCommand(pc, 'toggle', 'de', ['on'])).toMatchObject({ output: 'an', flags: ['on'] })
  })
})
