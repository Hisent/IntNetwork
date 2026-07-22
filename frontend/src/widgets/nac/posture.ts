// Reine Logik für das Posture-Assessment-Widget: bewertet den Zustand eines
// Endpunkts (Patches, AV/EDR, Host-Firewall, Festplattenverschlüsselung) und
// entscheidet, ob er vollen Zugriff bekommt oder in ein Quarantäne-VLAN muss.
//
// Alle vier Kriterien sind Pflicht (compliant = alle erfüllt). AV/EDR gilt
// zusätzlich als "kritisch": Es ist inhaltlich kein weicheres Kriterium als
// die anderen drei — die Unterscheidung ist rein didaktisch, um zu zeigen,
// dass ein Prüfpunkt allein (ohne dass irgendein anderer auch nur betroffen
// wäre) bereits für sich genommen zur Quarantäne führt.

export interface PostureState {
  osPatched: boolean
  avActive: boolean
  firewallOn: boolean
  diskEncrypted: boolean
}

export type PostureViolation = 'os-outdated' | 'av-inactive' | 'firewall-off' | 'disk-not-encrypted'

export interface PostureResult {
  compliant: boolean
  violations: PostureViolation[]
  vlan: string
  note: { de: string; en: string }
}

export const PRODUCTION_VLAN = 'VLAN 10 – Produktionsnetz / production network'
export const QUARANTINE_VLAN = 'VLAN 999 – Quarantäne / quarantine'

/** Kriterium, das allein schon zur Quarantäne führt ("kritisch"). */
export const CRITICAL_VIOLATION: PostureViolation = 'av-inactive'

export function assessPosture(state: PostureState): PostureResult {
  const violations: PostureViolation[] = []
  if (!state.osPatched) violations.push('os-outdated')
  if (!state.avActive) violations.push('av-inactive')
  if (!state.firewallOn) violations.push('firewall-off')
  if (!state.diskEncrypted) violations.push('disk-not-encrypted')

  const compliant = violations.length === 0

  if (compliant) {
    return {
      compliant: true,
      violations: [],
      vlan: PRODUCTION_VLAN,
      note: {
        de: 'Alle Pflichtkriterien erfüllt — der Endpunkt gilt als compliant und erhält vollen Zugriff auf das Produktivnetz.',
        en: 'All mandatory criteria are met — the endpoint is compliant and gets full access to the production network.',
      },
    }
  }

  const hasCritical = violations.includes(CRITICAL_VIOLATION)
  return {
    compliant: false,
    violations,
    vlan: QUARANTINE_VLAN,
    note: {
      de: hasCritical
        ? 'AV/EDR ist ein kritisches Kriterium: Fehlt es, landet der Endpunkt allein deswegen in Quarantäne, selbst wenn alle anderen Kriterien erfüllt sind.'
        : 'Ein oder mehrere Pflichtkriterien sind verletzt — der Endpunkt ist non-compliant und wird ins Quarantäne-VLAN verschoben, bis die Mängel behoben sind.',
      en: hasCritical
        ? 'AV/EDR is a critical criterion: if it is missing, the endpoint is quarantined for that reason alone, even if every other criterion is met.'
        : 'One or more mandatory criteria are violated — the endpoint is non-compliant and is moved to the quarantine VLAN until the issues are remediated.',
    },
  }
}
