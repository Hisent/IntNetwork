import { describe, expect, it } from 'vitest'
import { parseUiMode, readUiMode, resolveUiMode } from './uiMode'

describe('UI mode', () => {
  it('accepts only supported modes', () => {
    expect(parseUiMode('workbench')).toBe('workbench')
    expect(parseUiMode('unknown')).toBeNull()
  })

  it('defaults defensively and lets a preview override storage', () => {
    expect(resolveUiMode('', 'broken')).toBe('classic')
    expect(resolveUiMode('?ui=workbench', 'classic')).toBe('workbench')
    expect(resolveUiMode('?ui=broken', 'workbench')).toBe('workbench')
  })

  it('falls back when browser storage is unavailable', () => {
    expect(readUiMode('', () => { throw new Error('blocked') })).toBe('classic')
    expect(readUiMode('?ui=workbench', () => { throw new Error('blocked') })).toBe('workbench')
  })
})
