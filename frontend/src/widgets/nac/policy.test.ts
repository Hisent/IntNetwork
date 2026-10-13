import { describe, it, expect } from 'vitest'
import { certRelevant, evaluatePolicy, type DeviceType, type PolicyInput } from './policy'
import { VLAN } from './vlans'

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

describe('evaluatePolicy — Schalter "Zertifikat"', () => {
  it('verwaltet + 802.1X + compliant OHNE Zertifikat → nur eingeschränkt, nicht Vollzugriff', () => {
    const result = evaluatePolicy({ deviceType: 'managed', dot1xCapable: true, hasCert: false, compliant: true })
    expect(result.outcome).toBe('restricted')
    expect(result.vlan).toEqual(VLAN.employee)
    expect(result.reason.de).toContain('PEAP')
  })

  it('IoT mit Supplicant, aber ohne Zertifikat → eingeschränkt im IoT-VLAN', () => {
    const result = evaluatePolicy({ deviceType: 'iot', dot1xCapable: true, hasCert: false, compliant: true })
    expect(result.outcome).toBe('restricted')
    expect(result.vlan).toEqual(VLAN.iot)
  })

  it('mit Supplicant ändert der Schalter bei JEDEM Gerätetyp das Ergebnis (compliant)', () => {
    for (const deviceType of ['managed', 'iot', 'byod'] as DeviceType[]) {
      const withCert = evaluatePolicy({ deviceType, dot1xCapable: true, hasCert: true, compliant: true })
      const without = evaluatePolicy({ deviceType, dot1xCapable: true, hasCert: false, compliant: true })
      expect(without.outcome).not.toBe(withCert.outcome)
    }
  })

  it('ohne Supplicant ist der Schalter wirkungslos — und wird als solcher gemeldet', () => {
    expect(certRelevant({ dot1xCapable: false })).toBe(false)
    expect(certRelevant({ dot1xCapable: true })).toBe(true)
    for (const deviceType of ['managed', 'iot', 'byod'] as DeviceType[]) {
      const a = evaluatePolicy({ deviceType, dot1xCapable: false, hasCert: true, compliant: true })
      const b = evaluatePolicy({ deviceType, dot1xCapable: false, hasCert: false, compliant: true })
      expect(a).toEqual(b)
    }
  })

  it('nicht compliant schlägt fehlendes Zertifikat: Quarantäne', () => {
    const result = evaluatePolicy({ deviceType: 'managed', dot1xCapable: true, hasCert: false, compliant: false })
    expect(result.outcome).toBe('quarantine')
    expect(result.vlan).toEqual(VLAN.quarantine)
  })
})

describe('VLAN-Labels', () => {
  it('sind zweisprachig und nutzen in allen Widgets dieselben Nummern (20/30/40/50/90/99)', () => {
    expect(Object.values(VLAN).map((v) => v.de.match(/\d+/)?.[0])).toEqual(['20', '30', '40', '50', '90', '99'])
    for (const v of Object.values(VLAN)) {
      expect(v.en.match(/\d+/)?.[0]).toBe(v.de.match(/\d+/)?.[0])
      expect(v.en).not.toMatch(/Mitarbeiter|Gast|Quarantäne|Notbetrieb/)
    }
  })
})
