import { describe, it, expect } from 'vitest'
import { buildSteps, LAYERS } from './osiModel'

describe('osiModel', () => {
  it('hat 7 Schichten', () => {
    expect(LAYERS.map((l) => l.nr)).toEqual([7, 6, 5, 4, 3, 2, 1])
  })

  it('buildSteps: 14 Schritte (7 tx + 7 rx)', () => {
    const s = buildSteps()
    expect(s).toHaveLength(14)
    expect(s.filter((x) => x.side === 'tx')).toHaveLength(7)
  })

  it('Start = Sender Schicht 7 mit nur Daten', () => {
    const s = buildSteps()[0]
    expect(s.side).toBe('tx')
    expect(s.layer).toBe(7)
    expect(s.pieces).toEqual(['Daten'])
  })

  it('Sender Schicht 2 ist ein vollständiger Frame', () => {
    const s = buildSteps().find((x) => x.side === 'tx' && x.layer === 2)!
    expect(s.pieces).toEqual(['ETH', 'IP', 'TCP', 'Daten', 'FCS'])
  })

  it('Empfänger Schicht 7 hat wieder nur Daten', () => {
    const s = buildSteps().at(-1)!
    expect(s.side).toBe('rx')
    expect(s.layer).toBe(7)
    expect(s.pieces).toEqual(['Daten'])
  })
})
