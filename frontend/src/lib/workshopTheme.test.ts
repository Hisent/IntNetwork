import { describe, expect, it } from 'vitest'
import { workshopTheme } from './workshopTheme'

describe('workshopTheme', () => {
  it('maps persisted workshop keys to visual themes', () => {
    expect(workshopTheme('network')).toBe('network')
    expect(workshopTheme('claude-code')).toBe('claude')
    expect(workshopTheme('infoblox')).toBe('infoblox')
    expect(workshopTheme('ansible')).toBe('ansible')
    expect(workshopTheme('pki')).toBe('pki')
    expect(workshopTheme('nac')).toBe('nac')
  })

  it('falls back to network for unknown or missing keys', () => {
    expect(workshopTheme(undefined)).toBe('network')
    expect(workshopTheme(null)).toBe('network')
    expect(workshopTheme('something-unknown')).toBe('network')
  })
})
