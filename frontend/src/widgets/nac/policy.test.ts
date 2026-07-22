import { describe, it, expect } from 'vitest'
import { evaluatePolicy, type PolicyInput } from './policy'

describe('evaluatePolicy — Kernpfade', () => {
  it('verwaltet + 802.1X + Zertifikat + konform → Vollzugriff', () => {
    const input: PolicyInput = { deviceType: 'managed', dot1xCapable: true, hasCert: true, compliant: true }
    const result = evaluatePolicy(input)
    expect(result.outcome).toBe('full')
    expect(result.vlan).not.toBeNull()
  })

  it('verwaltet aber nicht compliant → Quarantäne', () => {
    const input: PolicyInput = { deviceType: 'managed', dot1xCapable: true, hasCert: true, compliant: false }
    const result = evaluatePolicy(input)
    expect(result.outcome).toBe('quarantine')
  })

  it('Drucker/IoT ohne 802.1X-Supplicant → MAB', () => {
    const input: PolicyInput = { deviceType: 'iot', dot1xCapable: false, hasCert: false, compliant: true }
    const result = evaluatePolicy(input)
    expect(result.outcome).toBe('iot-mab')
    expect(result.reason.de.toLowerCase()).toContain('spoof')
  })

  it('unbekannt/BYOD ohne Zertifikat → Gast', () => {
    const input: PolicyInput = { deviceType: 'byod', dot1xCapable: true, hasCert: false, compliant: true }
    const result = evaluatePolicy(input)
    expect(result.outcome).toBe('guest')
  })

  it('kein 802.1X + kein MAB erlaubt (verwaltetes Gerät) → Deny', () => {
    const input: PolicyInput = { deviceType: 'managed', dot1xCapable: false, hasCert: false, compliant: true }
    const result = evaluatePolicy(input)
    expect(result.outcome).toBe('deny')
    expect(result.vlan).toBeNull()
  })
})

describe('evaluatePolicy — Zusatzpfade', () => {
  it('BYOD ohne 802.1X → Gast (kein Deny, keine Prüfung ohne Supplicant möglich)', () => {
    const input: PolicyInput = { deviceType: 'byod', dot1xCapable: false, hasCert: false, compliant: true }
    expect(evaluatePolicy(input).outcome).toBe('guest')
  })

  it('IoT mit echtem 802.1X-Supplicant und compliant → Vollzugriff im IoT-VLAN', () => {
    const input: PolicyInput = { deviceType: 'iot', dot1xCapable: true, hasCert: true, compliant: true }
    expect(evaluatePolicy(input).outcome).toBe('full')
  })

  it('BYOD mit Zertifikat, 802.1X und compliant → Vollzugriff im BYOD-VLAN', () => {
    const input: PolicyInput = { deviceType: 'byod', dot1xCapable: true, hasCert: true, compliant: true }
    expect(evaluatePolicy(input).outcome).toBe('full')
  })

  it('jedes Ergebnis liefert eine de- und en-Begründung', () => {
    const combos: PolicyInput[] = [
      { deviceType: 'managed', dot1xCapable: true, hasCert: true, compliant: true },
      { deviceType: 'managed', dot1xCapable: true, hasCert: true, compliant: false },
      { deviceType: 'iot', dot1xCapable: false, hasCert: false, compliant: true },
      { deviceType: 'byod', dot1xCapable: true, hasCert: false, compliant: true },
      { deviceType: 'managed', dot1xCapable: false, hasCert: false, compliant: true },
    ]
    for (const input of combos) {
      const result = evaluatePolicy(input)
      expect(result.reason.de.length).toBeGreaterThan(0)
      expect(result.reason.en.length).toBeGreaterThan(0)
    }
  })
})
