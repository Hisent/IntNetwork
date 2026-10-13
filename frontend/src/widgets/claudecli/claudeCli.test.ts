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
})
