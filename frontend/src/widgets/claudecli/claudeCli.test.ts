import { describe, it, expect } from 'vitest'
import { createTerminalState, nextMode, runCommand, runTerminalCommand } from './claudeCli'

describe('runCommand', () => {
  it('/help lists commands', () => {
    expect(runCommand('/help', 'default', 'de').output).toContain('/context')
  })

  it('/clear signals a clear', () => {
    expect(runCommand('/clear', 'default', 'de').output).toBe('__CLEAR__')
  })

  it('unknown command hints /help', () => {
    expect(runCommand('/nope', 'default', 'de').output).toContain('/help')
  })

  it('non-slash input is treated as a task and mentions the mode', () => {
    expect(runCommand('fix the bug', 'plan', 'de').output).toContain('plan')
  })

  it('shows the config value default under its UI name Manual', () => {
    const out = runCommand('/status', 'default', 'en').output
    expect(out).toContain('manual mode on')
    expect(out).toContain('defaultMode: "default"')
  })

  it('knows auto mode and explains the classifier', () => {
    const out = runCommand('refactor auth', 'auto', 'en').output
    expect(out).toContain('auto mode on')
    expect(out).toContain('classifier')
  })

  it('cycles modes like Shift+Tab: auto → manual → accept edits → plan → auto', () => {
    expect(nextMode('auto')).toBe('default')
    expect(nextMode('default')).toBe('acceptEdits')
    expect(nextMode('acceptEdits')).toBe('plan')
    expect(nextMode('plan')).toBe('auto')
  })

  it('localizes output for en', () => {
    expect(runCommand('/status', 'default', 'en').output).toContain('Signed in')
  })

  it('keeps virtual files isolated in the terminal state', () => {
    const first = createTerminalState()
    const second = createTerminalState()
    const result = runTerminalCommand(first, 'echo hello > notes.txt', 'de')

    expect(runTerminalCommand(result.state, 'cat notes.txt', 'de').output).toBe('hello')
    expect(runTerminalCommand(second, 'cat notes.txt', 'de').output).toContain('nicht gefunden')
  })

  it('supports basic workspace inspection commands', () => {
    const result = runTerminalCommand(createTerminalState(), 'ls', 'en')

    expect(result.output).toContain('README.md')
    expect(runTerminalCommand(result.state, 'pwd', 'en').output).toBe('/workspace')
  })

  it('only shell commands go to the virtual shell; free text is a task for Claude (review 2026-10)', async () => {
    const { isTerminalCommand } = await import('./claudeCli')
    for (const cmd of ['ls', 'cat README.md', '  echo hi > a.txt', 'clear']) expect(isTerminalCommand(cmd)).toBe(true)
    for (const cmd of ['fix the failing test', '/context', '', 'lsx']) expect(isTerminalCommand(cmd)).toBe(false)
  })

  it('cat and touch ignore inherited object properties and survive extreme input', () => {
    const state = createTerminalState()
    for (const name of ['constructor', 'toString', '__proto__']) {
      expect(runTerminalCommand(state, 'cat ' + name, 'en').output).toBe('File not found: ' + name)
      expect(runTerminalCommand(state, 'touch ' + name, 'en').state.files[name]).toBe('')
    }
    expect(typeof runTerminalCommand(state, 'echo ' + 'x'.repeat(100_000), 'en').output).toBe('string')
    expect(runTerminalCommand(state, '   ', 'en').output).toBe('')
  })
})
