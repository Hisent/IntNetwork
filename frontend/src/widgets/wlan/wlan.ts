// 2,4-GHz-Kanäle 1..13. Ein Kanal belegt ~20 MHz (5 Kanal-Nummern breit),
// daher überlappen sich Kanäle, die weniger als 5 auseinanderliegen.
export const NON_OVERLAPPING = [1, 6, 11]

export function overlaps(a: number, b: number): boolean {
  return Math.abs(a - b) < 5
}

export interface WifiSecurity {
  name: string
  safe: boolean
  note: string
}

export const SECURITY: WifiSecurity[] = [
  { name: 'Offen', safe: false, note: 'keine Verschlüsselung — nie im Firmennetz' },
  { name: 'WEP', safe: false, note: 'gebrochen, in Minuten knackbar' },
  { name: 'WPA2', safe: true, note: 'solider Standard (AES)' },
  { name: 'WPA3', safe: true, note: 'aktuell, stärkster Schutz' },
]
