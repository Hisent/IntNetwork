import { describe, it, expect } from 'vitest'
import { overlaps, NON_OVERLAPPING } from './wlan'

describe('overlaps', () => {
  it('1 und 6 überlappen nicht', () => {
    expect(overlaps(1, 6)).toBe(false)
  })
  it('1 und 3 überlappen', () => {
    expect(overlaps(1, 3)).toBe(true)
  })
  it('gleicher Kanal gilt als Überlappung', () => {
    expect(overlaps(6, 6)).toBe(true)
  })
})

describe('NON_OVERLAPPING', () => {
  it('sind paarweise überlappungsfrei', () => {
    for (const a of NON_OVERLAPPING)
      for (const b of NON_OVERLAPPING) if (a !== b) expect(overlaps(a, b)).toBe(false)
  })
})
