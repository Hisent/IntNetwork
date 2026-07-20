import { describe, it, expect } from 'vitest'
import { timeline } from './hookLifecycle'

describe('hook lifecycle timeline', () => {
  it('edit: PostToolUse fires, PreToolUse does not, correct order', () => {
    const steps = timeline('edit', 'de')
    expect(steps.map((s) => s.event)).toEqual(['UserPromptSubmit', 'PreToolUse', 'PostToolUse', 'Stop'])
    const pre = steps.find((s) => s.event === 'PreToolUse')
    const post = steps.find((s) => s.event === 'PostToolUse')
    expect(pre?.fires).toBe(false)
    expect(post?.fires).toBe(true)
  })

  it('bash: PreToolUse fires', () => {
    const pre = timeline('bash', 'de').find((s) => s.event === 'PreToolUse')
    expect(pre?.fires).toBe(true)
  })

  it('session starts with SessionStart and fires', () => {
    const steps = timeline('session', 'de')
    expect(steps[0].event).toBe('SessionStart')
    expect(steps[0].fires).toBe(true)
  })

  it('localizes detail', () => {
    expect(timeline('edit', 'en').find((s) => s.event === 'PostToolUse')?.detail).toContain('formatter')
  })
})
