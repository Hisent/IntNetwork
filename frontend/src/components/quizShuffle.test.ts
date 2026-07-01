import { describe, it, expect } from 'vitest'
import { shuffledIndices } from '@/components/Quiz'

describe('shuffledIndices', () => {
  it('gibt eine Permutation von 0..n-1 zurueck (keine verlorenen/doppelten Optionen)', () => {
    for (const n of [0, 1, 2, 4, 10]) {
      const res = shuffledIndices(n)
      expect(res).toHaveLength(n)
      expect([...res].sort((a, b) => a - b)).toEqual(Array.from({ length: n }, (_, i) => i))
    }
  })

  it('mischt tatsaechlich (nicht immer Identitaet) -> bricht die Positions-Verzerrung', () => {
    // 100 Laeufe mit n=6: die Wahrscheinlichkeit, dass NIE gemischt wird, ist
    // (1/720)^100 -> praktisch null. Ein einziger Nicht-Identitaets-Lauf reicht.
    const identity = [0, 1, 2, 3, 4, 5]
    const anyShuffled = Array.from({ length: 100 }, () => shuffledIndices(6))
      .some((r) => r.some((v, i) => v !== identity[i]))
    expect(anyShuffled).toBe(true)
  })
})
