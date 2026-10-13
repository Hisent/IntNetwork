import { describe, expect, it } from 'vitest'
import { formatApiTime, parseApiTime } from './apiTime'

describe('parseApiTime', () => {
  it('liest Zeitstempel ohne Zonenangabe als UTC', () => {
    expect(parseApiTime('2026-10-13T11:50:00').toISOString()).toBe('2026-10-13T11:50:00.000Z')
    expect(parseApiTime('2026-10-13T11:50:00.123456').toISOString()).toBe('2026-10-13T11:50:00.123Z')
  })
  it('lässt eine vorhandene Zonenangabe unverändert', () => {
    expect(parseApiTime('2026-10-13T11:50:00Z').toISOString()).toBe('2026-10-13T11:50:00.000Z')
    expect(parseApiTime('2026-10-13T13:50:00+02:00').toISOString()).toBe('2026-10-13T11:50:00.000Z')
  })
})

describe('formatApiTime', () => {
  it('zeigt die Ortszeit statt UTC (11:50 UTC = 13:50 in Berlin)', () => {
    expect(formatApiTime('2026-10-13T11:50:00', 'de', 'Europe/Berlin')).toContain('13:50')
    expect(formatApiTime('2026-10-13T11:50:00+00:00', 'en', 'Europe/Berlin')).toContain('13:50')
  })
  it('gibt Unlesbares unverändert zurück', () => {
    expect(formatApiTime('gestern', 'de')).toBe('gestern')
  })
})
