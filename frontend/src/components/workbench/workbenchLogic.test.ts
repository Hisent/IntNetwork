import { describe, expect, it } from 'vitest'
import { prerequisitesMet, readPercent } from './workbenchLogic'

describe('workbench progress', () => {
  it('counts only text blocks that belong to the module', () => {
    expect(readPercent([0, 2, 5], [0, 1, 5])).toBe(67)
    expect(readPercent([], [0])).toBe(0)
  })

  it('unlocks modules only after every prerequisite is complete', () => {
    expect(prerequisitesMet(['osi', 'switch'], ['osi', 'switch', 'dns'])).toBe(true)
    expect(prerequisitesMet(['osi', 'switch'], ['osi'])).toBe(false)
  })
})
