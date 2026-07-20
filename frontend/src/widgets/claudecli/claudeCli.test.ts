import { describe, it, expect } from 'vitest'
import { runCommand } from './claudeCli'

describe('runCommand', () => {
  it('/help lists commands', () => {
    expect(runCommand('/help', 'normal', 'de').output).toContain('/context')
  })

  it('/clear signals a clear', () => {
    expect(runCommand('/clear', 'normal', 'de').output).toBe('__CLEAR__')
  })

  it('unknown command hints /help', () => {
    expect(runCommand('/nope', 'normal', 'de').output).toContain('/help')
  })

  it('non-slash input is treated as a task and mentions the mode', () => {
    expect(runCommand('fix the bug', 'plan', 'de').output).toContain('plan')
  })

  it('localizes output for en', () => {
    expect(runCommand('/status', 'normal', 'en').output).toContain('Signed in')
  })
})
