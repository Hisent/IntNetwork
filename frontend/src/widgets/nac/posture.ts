// Reine Logik für das Posture-Assessment-Widget: bewertet den Zustand eines
// Endpunkts (Patches, AV/EDR, Host-Firewall, Festplattenverschlüsselung) und
// leitet daraus eine ABGESTUFTE Reaktion ab:
//
//   - alles erfüllt                 -> compliant, Vollzugriff
//   - nur nicht-kritische Verstöße  -> Remediation-Frist (Grace Period): Zugriff
//                                      bleibt, nach Ablauf der Frist Quarantäne
//   - kritischer Verstoß            -> sofort Quarantäne
//
// Welche Kriterien "kritisch" sind, ist eine Richtlinienentscheidung; hier
// (wie im Modul nac-posture) ist es AV/EDR.

import { VLAN, type Bilingual } from './vlans'

export interface PostureState {
  osPatched: boolean
  avActive: boolean
  firewallOn: boolean
  diskEncrypted: boolean
}

export type PostureViolation = 'os-outdated' | 'av-inactive' | 'firewall-off' | 'disk-not-encrypted'
export type PostureLevel = 'compliant' | 'grace' | 'quarantine'

export interface PostureResult {
  compliant: boolean
  level: PostureLevel
  violations: PostureViolation[]
  vlan: Bilingual
  /** Tage bis zur Quarantäne, nur bei level === 'grace'. */
  graceDays: number | null
  note: Bilingual
}

export const PRODUCTION_VLAN = VLAN.employee
export const QUARANTINE_VLAN = VLAN.quarantine

/** Verstöße, die allein schon zur sofortigen Quarantäne führen. */
export const CRITICAL_VIOLATIONS: readonly PostureViolation[] = ['av-inactive']
/** Frist für nicht-kritische Verstöße, bevor ebenfalls Quarantäne folgt. */
export const GRACE_DAYS = 7

export function isCritical(v: PostureViolation): boolean {
  return CRITICAL_VIOLATIONS.includes(v)
}

export function assessPosture(state: PostureState): PostureResult {
  const violations: PostureViolation[] = []
  if (!state.osPatched) violations.push('os-outdated')
  if (!state.avActive) violations.push('av-inactive')
  if (!state.firewallOn) violations.push('firewall-off')
  if (!state.diskEncrypted) violations.push('disk-not-encrypted')

  if (violations.length === 0) {
    return {
      compliant: true, level: 'compliant', violations, vlan: PRODUCTION_VLAN, graceDays: null,
      note: {
        de: 'Alle Pflichtkriterien erfüllt — der Endpunkt gilt als compliant und erhält vollen Zugriff auf das Produktivnetz.',
        en: 'All mandatory criteria are met — the endpoint is compliant and gets full access to the production network.',
      },
    }
  }

  if (violations.some(isCritical)) {
    return {
      compliant: false, level: 'quarantine', violations, vlan: QUARANTINE_VLAN, graceDays: null,
      note: {
        de: 'Kritischer Verstoß (AV/EDR inaktiv): sofort Quarantäne — per CoA, ohne Neuanmeldung. Erreichbar bleiben nur die Remediation-Server.',
        en: 'Critical violation (AV/EDR inactive): immediate quarantine — via CoA, without a new login. Only the remediation servers remain reachable.',
      },
    }
  }

  return {
    compliant: false, level: 'grace', violations, vlan: PRODUCTION_VLAN, graceDays: GRACE_DAYS,
    note: {
      de: `Nicht konform, aber kein kritischer Verstoß: Der Zugriff bleibt für eine Remediation-Frist von ${GRACE_DAYS} Tagen bestehen. Ist der Mangel danach nicht behoben, folgt die Quarantäne.`,
      en: `Non-compliant, but no critical violation: access remains for a remediation deadline of ${GRACE_DAYS} days. If the issue is not fixed by then, quarantine follows.`,
    },
  }
}
