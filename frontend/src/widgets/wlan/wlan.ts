// 2,4-GHz-Kanäle 1..13. Ein Kanal belegt ~20 MHz (5 Kanal-Nummern breit),
// daher überlappen sich Kanäle, die weniger als 5 auseinanderliegen.
export const NON_OVERLAPPING = [1, 6, 11]

export function overlaps(a: number, b: number): boolean {
  return Math.abs(a - b) < 5
}

export interface WifiSecurity {
  name: { de: string; en: string }
  safe: boolean
  note: { de: string; en: string }
}

export const SECURITY: WifiSecurity[] = [
  { name: { de: 'Offen', en: 'Open' }, safe: false,
    note: { de: 'keine Verschlüsselung — nie im Firmennetz', en: 'no encryption — never on the company network' } },
  { name: { de: 'WEP', en: 'WEP' }, safe: false,
    note: { de: 'gebrochen, in Minuten knackbar', en: 'broken, crackable in minutes' } },
  { name: { de: 'WPA2', en: 'WPA2' }, safe: true,
    note: { de: 'solider Standard (AES)', en: 'solid standard (AES)' } },
  { name: { de: 'WPA3', en: 'WPA3' }, safe: true,
    note: { de: 'aktuell, stärkster Schutz', en: 'current, strongest protection' } },
]
