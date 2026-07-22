import { describe, it, expect } from 'vitest'
import { outcome } from './deployment'

describe('outcome', () => {
  it('Monitor Mode gibt bei erfolgreicher Auth vollen Zugriff ohne Log', () => {
    const r = outcome('monitor', true)
    expect(r.access).toBe('full')
    expect(r.log).toBe(false)
  })

  it('Monitor Mode gibt auch bei Fehlschlag vollen Zugriff, protokolliert aber', () => {
    const r = outcome('monitor', false)
    expect(r.access).toBe('full')
    expect(r.log).toBe(true)
  })

  it('Low-Impact Mode gibt bei Erfolg vollen Zugriff', () => {
    const r = outcome('low-impact', true)
    expect(r.access).toBe('full')
  })

  it('Low-Impact Mode gibt bei Fehlschlag nur begrenzten Zugriff (dACL)', () => {
    const r = outcome('low-impact', false)
    expect(r.access).toBe('limited')
    expect(r.log).toBe(true)
  })

  it('Closed Mode gibt bei Erfolg vollen Zugriff', () => {
    const r = outcome('closed', true)
    expect(r.access).toBe('full')
  })

  it('Closed Mode gibt bei Fehlschlag keinen Zugriff', () => {
    const r = outcome('closed', false)
    expect(r.access).toBe('none')
    expect(r.log).toBe(true)
  })

  it('alle drei Modi liefern bei Erfolg dasselbe Ergebnis (full, kein Log)', () => {
    for (const mode of ['monitor', 'low-impact', 'closed'] as const) {
      const r = outcome(mode, true)
      expect(r.access).toBe('full')
      expect(r.log).toBe(false)
    }
  })

  it('derselbe Fehlschlag hat in jedem Modus eine andere Zugriffsfolge', () => {
    const results = (['monitor', 'low-impact', 'closed'] as const).map((mode) => outcome(mode, false).access)
    expect(results).toEqual(['full', 'limited', 'none'])
  })

  it('jedes Ergebnis liefert eine zweisprachige Erklärung', () => {
    const r = outcome('closed', false)
    expect(r.note.de.length).toBeGreaterThan(0)
    expect(r.note.en.length).toBeGreaterThan(0)
  })
})
