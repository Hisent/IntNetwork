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

describe('Planungsregel: mindestens 5 Kanalnummern Abstand', () => {
  it('Grenze liegt exakt zwischen Abstand 4 und 5', () => {
    expect(overlaps(1, 5)).toBe(true) // 20 MHz Abstand < 22 MHz DSSS-Breite
    expect(overlaps(5, 1)).toBe(true) // symmetrisch
    expect(overlaps(6, 11)).toBe(false)
    expect(overlaps(2, 7)).toBe(false) // wie im Modul-Quiz: 2/7/12 ist ebenfalls überlappungsfrei
    expect(overlaps(7, 12)).toBe(false)
    expect(overlaps(6, 7)).toBe(true) // Störfall aus dem Modultext (Kanal 7 neben 6)
    expect(overlaps(3, 4)).toBe(true) // Debug-Aufgabe des Moduls
  })
})
