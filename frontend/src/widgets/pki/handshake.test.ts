import { describe, it, expect } from 'vitest'
import { TLS12_STEPS, TLS13_STEPS, roundtripCount, type HandshakeStep } from './handshake'

describe('roundtripCount', () => {
  it('TLS 1.3 braucht weniger Roundtrips als TLS 1.2', () => {
    expect(roundtripCount(TLS13_STEPS)).toBeLessThan(roundtripCount(TLS12_STEPS))
    expect(roundtripCount(TLS12_STEPS)).toBe(2)
    expect(roundtripCount(TLS13_STEPS)).toBe(1)
  })
})

describe('Zertifikat-Verschlüsselung', () => {
  it('ist in TLS 1.3 verschlüsselt, in TLS 1.2 nicht', () => {
    const cert12 = TLS12_STEPS.find((s) => s.name.includes('Certificate'))
    const cert13 = TLS13_STEPS.find((s) => s.name.includes('Certificate'))
    expect(cert12?.encrypted).toBe(false)
    expect(cert13?.encrypted).toBe(true)
  })
})

describe('Schritt-Daten Konsistenz', () => {
  const allSteps: HandshakeStep[] = [...TLS12_STEPS, ...TLS13_STEPS]

  it('jeder Schritt hat de- und en-Texte', () => {
    for (const step of allSteps) {
      expect(step.detail.de.length).toBeGreaterThan(0)
      expect(step.detail.en.length).toBeGreaterThan(0)
    }
  })

  it('jeder Schritt hat eine gültige Richtung und Roundtrip-Nummer', () => {
    for (const step of allSteps) {
      expect(['client', 'server']).toContain(step.from)
      expect(step.roundtrip).toBeGreaterThanOrEqual(1)
    }
  })
})
