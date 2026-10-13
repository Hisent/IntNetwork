// 2,4-GHz-Kanäle 1..13, Mittenfrequenzen im 5-MHz-Raster (Kanal 1 = 2412 MHz).
// Planungsregel wie im Modultext: Abstand von mindestens 5 Kanalnummern (25 MHz) → 1/6/11.
// Sie stammt von der 22 MHz breiten DSSS-Maske (802.11b): 1/5 lägen nur 20 MHz auseinander
// und überlappen dort um 2 MHz. Reine OFDM-Netze (802.11g/n, 20 MHz) kämen in Europa auch
// mit 1/5/9/13 aus — das Widget bleibt bewusst bei der konservativen, gelehrten Regel.
export const CHANNELS = Array.from({ length: 13 }, (_, i) => i + 1) // EU/ETSI: 1–13 (USA nur 1–11)
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
