import { describe, it, expect } from 'vitest'
import { overlaps, CHANNELS, NON_OVERLAPPING } from './wlan'

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

describe('CHANNELS', () => {
  it('bietet die in Europa erlaubten Kanäle 1–13 an', () => {
    expect(CHANNELS).toHaveLength(13)
    expect(CHANNELS[0]).toBe(1)
    expect(CHANNELS[12]).toBe(13)
    for (const c of NON_OVERLAPPING) expect(CHANNELS).toContain(c)
  })
})
