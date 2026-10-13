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

  it('Header werden vorangestellt, nur die FCS wird angehängt', () => {
    const tx = (nr: number) => buildSteps().find((x) => x.side === 'tx' && x.layer === nr)!.caption
    for (const nr of [4, 3]) {
      expect(tx(nr).de).toContain('voran')
      expect(tx(nr).de).not.toContain('hängt')
      expect(tx(nr).en).toContain('prepends')
    }
    expect(tx(2).de).toMatch(/voran.*hängt die FCS an/)
    expect(tx(2).en).toMatch(/prepends.*appends the FCS/)
  })

  it('Schicht 5 nennt konkrete Beispiele', () => {
    expect(LAYERS.find((l) => l.nr === 5)!.example).toBe('RPC, NetBIOS')
  })

  it('EN: kein deutsches Beispiel (Schicht 1), Captions in beiden Sprachen vollständig', () => {
    for (const l of LAYERS) expect(l.exampleEn ?? l.example).not.toMatch(/Kabel|Funk|[äöüß]/)
    expect(LAYERS.find((l) => l.nr === 1)!.exampleEn).toBe('Cable, radio')
    for (const s of buildSteps()) {
      expect(s.caption.de.length).toBeGreaterThan(0)
      expect(s.caption.en).not.toMatch(/[äöüß]|Schicht|Empfänger/)
    }
  })
  it('Encapsulation und Decapsulation sind spiegelbildlich', () => {
    const steps = buildSteps()
    const at = (side: 'tx' | 'rx', nr: number) => steps.find((x) => x.side === side && x.layer === nr)!.pieces
    expect(at('rx', 1)).toEqual(at('tx', 1)) // auf dem Medium: vollständiger Frame
    expect(at('rx', 2)).toEqual(at('tx', 3)) // nach L2: IP-Paket
    expect(at('rx', 3)).toEqual(at('tx', 4)) // nach L3: TCP-Segment
    expect(at('rx', 4)).toEqual(at('tx', 5)) // nach L4: Daten
    expect(LAYERS.find((l) => l.nr === 3)!.pdu).toEqual({ de: 'Paket', en: 'Packet' }) // Challenge-Antwort
  })
  it('Empfänger Schicht 7 hat wieder nur Daten', () => {
    const s = buildSteps().at(-1)!
    expect(s.side).toBe('rx')
    expect(s.layer).toBe(7)
    expect(s.pieces).toEqual(['Daten'])
  })
})
