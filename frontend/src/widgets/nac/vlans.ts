// Einheitliches VLAN-Schema des NAC-Lehrgangs (Nordwind Logistik), zweisprachig.
// Dieselben Nummern stehen in den Modultexten (backend/app/content/nac_*.py,
// u. a. match-geraeteklassen in nac_autorisierung) — hier ändern heißt dort ändern.

export interface Bilingual { de: string; en: string }

export const VLAN = {
  employee: { de: 'VLAN 20 (Mitarbeiter)', en: 'VLAN 20 (employees)' },
  byod: { de: 'VLAN 30 (BYOD)', en: 'VLAN 30 (BYOD)' },
  iot: { de: 'VLAN 40 (IoT)', en: 'VLAN 40 (IoT)' },
  guest: { de: 'VLAN 50 (Gast)', en: 'VLAN 50 (guest)' },
  critical: { de: 'VLAN 90 (Critical/Notbetrieb)', en: 'VLAN 90 (critical/emergency)' },
  quarantine: { de: 'VLAN 99 (Quarantäne)', en: 'VLAN 99 (quarantine)' },
} as const satisfies Record<string, Bilingual>
