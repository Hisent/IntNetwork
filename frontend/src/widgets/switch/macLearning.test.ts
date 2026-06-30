import { describe, it, expect } from 'vitest'
import { learnStep, HOSTS } from './macLearning'

const macA = HOSTS[0].mac
const macB = HOSTS[1].mac

describe('learnStep', () => {
  it('unbekanntes Ziel -> Flooding an alle außer Quelle', () => {
    const r = learnStep({}, 1, macB)
    expect(r.flooded).toBe(true)
    expect(r.delivered).toEqual([2, 3, 4])
    expect(r.table[macA]).toBe(1)
  })

  it('bekanntes Ziel -> Unicast', () => {
    const r = learnStep({ [macA]: 1 }, 2, macA)
    expect(r.flooded).toBe(false)
    expect(r.delivered).toEqual([1])
    expect(r.table[macB]).toBe(2)
  })
})
