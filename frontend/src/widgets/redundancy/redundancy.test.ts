import { describe, it, expect } from 'vitest'
import { electRoot, aggregateBandwidth, singleFlowBandwidth } from './redundancy'

describe('electRoot', () => {
  it('niedrigste Priorität gewinnt', () => {
    const r = electRoot([
      { name: 'SW1', priority: 32768, mac: '00:11:22:33:44:55' },
      { name: 'SW2', priority: 4096, mac: 'AA:BB:CC:DD:EE:FF' },
      { name: 'SW3', priority: 16384, mac: '11:11:11:11:11:11' },
    ])
    expect(r).toEqual({ root: 'SW2', reason: 'priority' })
  })

  it('bei Prioritätsgleichstand entscheidet die niedrigste MAC-Adresse', () => {
    const r = electRoot([
      { name: 'SW1', priority: 4096, mac: 'AA:11:22:33:44:55' },
      { name: 'SW2', priority: 4096, mac: '00:11:22:33:44:55' },
      { name: 'SW3', priority: 8192, mac: '11:11:11:11:11:11' },
    ])
    expect(r).toEqual({ root: 'SW2', reason: 'mac' })
  })

  it('vergleicht MAC-Adressen numerisch pro Oktett, nicht nur lexikografisch', () => {
    // '2:...' vs '10:...': lexikografischer String-Vergleich würde "10" fälschlich
    // vor "2" einordnen; die korrekte numerische Auflösung ist 2 < 10.
    const r = electRoot([
      { name: 'SW1', priority: 4096, mac: '10:00:00:00:00:00' },
      { name: 'SW2', priority: 4096, mac: '02:00:00:00:00:00' },
    ])
    expect(r).toEqual({ root: 'SW2', reason: 'mac' })
  })
})

describe('Link-Aggregation', () => {
  it('Summenbandbreite skaliert linear mit der Anzahl Leitungen', () => {
    expect(aggregateBandwidth(1, 1000)).toBe(1000)
    expect(aggregateBandwidth(2, 1000)).toBe(2000)
    expect(aggregateBandwidth(4, 1000)).toBe(4000)
  })

  it('Einzelfluss bleibt unabhängig von der Leitungsanzahl auf einer Leitung begrenzt', () => {
    expect(singleFlowBandwidth(1000)).toBe(1000)
  })

  it('Ausfall einer Leitung reduziert die Summenbandbreite korrekt', () => {
    const total = aggregateBandwidth(4, 1000)
    const afterFailure = aggregateBandwidth(3, 1000)
    expect(total).toBe(4000)
    expect(afterFailure).toBe(3000)
    expect(afterFailure).toBeLessThan(total)
    // Einzelfluss bleibt von dem Ausfall unberührt (immer noch 1 Gbit/s).
    expect(singleFlowBandwidth(1000)).toBe(1000)
  })
})
