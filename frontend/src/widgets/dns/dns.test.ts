import { describe, it, expect } from 'vitest'
import { resolve } from './dns'

describe('resolve', () => {
  it('bekannter Name -> IP über 3 Stufen', () => {
    const r = resolve('www.nordwind-logistik.de')
    expect(r.ip).toBe('203.0.113.11')
    expect(r.steps).toHaveLength(3)
    expect(r.steps[2].answer.de).toContain('203.0.113.11')
    expect(r.steps[2].answer.en).toContain('203.0.113.11')
  })

  it('unbekannter .de-Name -> NXDOMAIN', () => {
    const r = resolve('gibtsnicht.nordwind-logistik.de')
    expect(r.ip).toBeNull()
    expect(r.steps[2].answer.de).toContain('NXDOMAIN')
    expect(r.steps[2].answer.en).toContain('NXDOMAIN')
  })

  it('unbekannte TLD -> keine Auflösung', () => {
    const r = resolve('example.com')
    expect(r.ip).toBeNull()
  })
})
