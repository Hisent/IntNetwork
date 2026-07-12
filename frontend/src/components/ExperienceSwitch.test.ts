import { describe, expect, it, vi } from 'vitest'
import { mayChangeExperience } from './experienceSwitchLogic'

describe('experience switch confirmation', () => {
  it('changes immediately when confirmation is disabled', () => {
    const confirm = vi.fn(() => false)
    expect(mayChangeExperience(false, 'Reset?', confirm)).toBe(true)
    expect(confirm).not.toHaveBeenCalled()
  })

  it('keeps the current mode when confirmation is declined', () => {
    expect(mayChangeExperience(true, 'Reset?', () => false)).toBe(false)
    expect(mayChangeExperience(true, 'Reset?', () => true)).toBe(true)
  })
})
