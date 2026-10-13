import { describe, it, expect } from 'vitest'
import {
  assessPosture, CRITICAL_VIOLATIONS, GRACE_DAYS, isCritical, PRODUCTION_VLAN, QUARANTINE_VLAN,
  type PostureState,
} from './posture'

const COMPLIANT: PostureState = {
  osPatched: true,
  avActive: true,
  firewallOn: true,
  diskEncrypted: true,
}

describe('assessPosture', () => {
  it('alle Kriterien erfüllt -> compliant, Vollzugriff, keine violations', () => {
    const r = assessPosture(COMPLIANT)
    expect(r.compliant).toBe(true)
    expect(r.level).toBe('compliant')
    expect(r.violations).toEqual([])
    expect(r.vlan).toBe(PRODUCTION_VLAN)
    expect(r.graceDays).toBeNull()
  })

  it.each([
    ['firewallOn', 'firewall-off'],
    ['osPatched', 'os-outdated'],
    ['diskEncrypted', 'disk-not-encrypted'],
  ] as const)('nicht-kritisches Kriterium %s verletzt -> Frist statt Quarantäne', (key, violation) => {
    const r = assessPosture({ ...COMPLIANT, [key]: false })
    expect(r.compliant).toBe(false)
    expect(r.level).toBe('grace')
    expect(r.violations).toEqual([violation])
    expect(r.vlan).toBe(PRODUCTION_VLAN)
    expect(r.graceDays).toBe(GRACE_DAYS)
  })

  it('kritisches Kriterium (AV/EDR) verletzt -> sofort Quarantäne, auch wenn alles andere ok ist', () => {
    const r = assessPosture({ ...COMPLIANT, avActive: false })
    expect(r.compliant).toBe(false)
    expect(r.level).toBe('quarantine')
    expect(r.violations).toEqual(['av-inactive'])
    expect(r.vlan).toBe(QUARANTINE_VLAN)
    expect(r.graceDays).toBeNull()
  })

  it('die Abstufung ist echt: kritisch und nicht-kritisch führen zu verschiedenen Ergebnissen', () => {
    const critical = assessPosture({ ...COMPLIANT, avActive: false })
    const soft = assessPosture({ ...COMPLIANT, firewallOn: false })
    expect(critical.level).not.toBe(soft.level)
    expect(critical.vlan).not.toBe(soft.vlan)
  })

  it('mehrere nicht-kritische Verstöße bleiben bei der Frist', () => {
    const r = assessPosture({ osPatched: false, avActive: true, firewallOn: false, diskEncrypted: false })
    expect(r.level).toBe('grace')
    expect(r.violations).toEqual(['os-outdated', 'firewall-off', 'disk-not-encrypted'])
  })

  it('ein kritischer Verstoß schlägt alle anderen: Quarantäne, alle Verstöße gelistet', () => {
    const r = assessPosture({ osPatched: false, avActive: false, firewallOn: false, diskEncrypted: true })
    expect(r.level).toBe('quarantine')
    expect(r.violations).toEqual(['os-outdated', 'av-inactive', 'firewall-off'])
  })

  it('isCritical kennt genau die kritischen Verstöße', () => {
    expect(CRITICAL_VIOLATIONS).toEqual(['av-inactive'])
    expect(isCritical('av-inactive')).toBe(true)
    expect(isCritical('os-outdated')).toBe(false)
  })

  it('jedes Ergebnis liefert Erklärung und VLAN zweisprachig', () => {
    for (const state of [COMPLIANT, { ...COMPLIANT, avActive: false }, { ...COMPLIANT, osPatched: false }]) {
      const r = assessPosture(state)
      expect(r.note.de.length).toBeGreaterThan(0)
      expect(r.note.en.length).toBeGreaterThan(0)
      expect(r.vlan.en).not.toMatch(/Quarantäne|Mitarbeiter/)
    }
  })
})
