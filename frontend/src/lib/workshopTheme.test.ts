import { describe, expect, it } from 'vitest'
import { workshopTheme } from './workshopTheme'

describe('workshopTheme', () => {
  it('maps persisted workshop keys to visual themes', () => {
    expect(workshopTheme('network')).toBe('network')
    expect(workshopTheme('claude-code')).toBe('claude')
  })
})
