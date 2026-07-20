import { describe, it, expect } from 'vitest'
import { wallClock, TASKS } from './orchestrator'

describe('agent orchestration wall-clock', () => {
  it('sequential sums the costs', () => {
    expect(wallClock(TASKS, 'sequential')).toBe(13)
  })

  it('parallel takes the slowest single task', () => {
    expect(wallClock(TASKS, 'parallel')).toBe(6)
  })

  it('parallel is never slower than sequential', () => {
    expect(wallClock(TASKS, 'parallel')).toBeLessThanOrEqual(wallClock(TASKS, 'sequential'))
  })

  it('empty task list is zero', () => {
    expect(wallClock([], 'parallel')).toBe(0)
  })
})
