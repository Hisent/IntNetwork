import { describe, it, expect } from 'vitest'
import { assessPosture, CRITICAL_VIOLATION, PRODUCTION_VLAN, QUARANTINE_VLAN, type PostureState } from './posture'

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
    expect(r.violations).toEqual([])
    expect(r.vlan).toBe(PRODUCTION_VLAN)
  })

  it('ein weiches Kriterium verletzt (Firewall aus) -> non-compliant + Quarantäne', () => {
    const r = assessPosture({ ...COMPLIANT, firewallOn: false })
    expect(r.compliant).toBe(false)
    expect(r.violations).toContain('firewall-off')
    expect(r.vlan).toBe(QUARANTINE_VLAN)
  })

  it('veraltete Patches -> non-compliant + violation gelistet', () => {
    const r = assessPosture({ ...COMPLIANT, osPatched: false })
    expect(r.compliant).toBe(false)
    expect(r.violations).toContain('os-outdated')
  })

  it('Festplatte nicht verschlüsselt -> non-compliant + violation gelistet', () => {
    const r = assessPosture({ ...COMPLIANT, diskEncrypted: false })
    expect(r.compliant).toBe(false)
    expect(r.violations).toContain('disk-not-encrypted')
  })

  it('kritisches Kriterium (AV/EDR) verletzt -> non-compliant, auch wenn alles andere ok ist', () => {
    const r = assessPosture({ ...COMPLIANT, avActive: false })
    expect(r.compliant).toBe(false)
    expect(r.violations).toEqual([CRITICAL_VIOLATION])
    expect(r.vlan).toBe(QUARANTINE_VLAN)
  })

  it('mehrere verletzte Kriterien werden alle gelistet', () => {
    const r = assessPosture({ osPatched: false, avActive: false, firewallOn: false, diskEncrypted: true })
    expect(r.compliant).toBe(false)
    expect(r.violations).toEqual(['os-outdated', 'av-inactive', 'firewall-off'])
  })

  it('jedes Ergebnis liefert eine zweisprachige Erklärung', () => {
    const r = assessPosture({ ...COMPLIANT, avActive: false })
    expect(r.note.de.length).toBeGreaterThan(0)
    expect(r.note.en.length).toBeGreaterThan(0)
  })
})
