import { describe, expect, it } from 'vitest'
import { markLockedVisibility } from './lockedModules'

describe('markLockedVisibility', () => {
  it('keeps done/unlocked modules always visible', () => {
    const result = markLockedVisibility([
      { key: 'a', locked: false },
      { key: 'b', locked: false },
    ])
    expect(result.every((r) => r.visible)).toBe(true)
  })

  it('shows only the next N locked modules and hides the rest', () => {
    const modules = [
      { key: 'a', locked: false },
      { key: 'b', locked: true },
      { key: 'c', locked: true },
      { key: 'd', locked: true },
      { key: 'e', locked: true },
    ]
    const result = markLockedVisibility(modules, 2)
    expect(result.map((r) => r.visible)).toEqual([true, true, true, false, false])
  })

  it('defaults to keeping 3 upcoming locked modules visible', () => {
    const modules = Array.from({ length: 6 }, (_, i) => ({ key: String(i), locked: true }))
    const result = markLockedVisibility(modules)
    expect(result.filter((r) => r.visible).length).toBe(3)
  })

  it('counts the locked budget across the whole list, not per group', () => {
    const modules = [
      { key: 'a', locked: true },
      { key: 'b', locked: true },
      { key: 'c', locked: false },
      { key: 'd', locked: true },
      { key: 'e', locked: true },
    ]
    const result = markLockedVisibility(modules, 2)
    // Die ersten beiden gesperrten (a, b) verbrauchen das Budget; das freie
    // Modul c zählt nicht mit, d/e bleiben verborgen.
    expect(result.map((r) => r.visible)).toEqual([true, true, true, false, false])
  })
})
