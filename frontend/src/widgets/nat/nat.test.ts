import { describe, it, expect } from 'vitest'
import { translate, type NatEntry } from './nat'

const PUB = '203.0.113.10'

describe('translate (PAT)', () => {
  it('verschiedene innere Hosts -> eine öffentliche IP, verschiedene Ports', () => {
    let t: NatEntry[] = []
    const a = translate(t, '192.168.10.5', 5000, PUB)
    t = a.table
    const b = translate(t, '192.168.10.6', 5000, PUB)
    expect(a.entry.insideGlobal).toBe('203.0.113.10:40000')
    expect(b.entry.insideGlobal).toBe('203.0.113.10:40001')
    expect(b.reused).toBe(false)
  })

  it('gleicher Host:Port -> Eintrag wiederverwendet', () => {
    const t = translate([], '192.168.10.5', 5000, PUB).table
    const again = translate(t, '192.168.10.5', 5000, PUB)
    expect(again.reused).toBe(true)
    expect(again.table.length).toBe(1)
  })
})
