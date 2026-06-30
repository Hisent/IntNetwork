export interface Layer {
  nr: number; de: string; en: string; task: string; example: string; pdu: string
}

export const LAYERS: Layer[] = [
  { nr: 7, de: 'Anwendung', en: 'Application', task: 'Dienste für Anwendungen', example: 'HTTP, DNS', pdu: 'Daten' },
  { nr: 6, de: 'Darstellung', en: 'Presentation', task: 'Codierung, Verschlüsselung', example: 'TLS, UTF-8', pdu: 'Daten' },
  { nr: 5, de: 'Sitzung', en: 'Session', task: 'Sitzungen auf-/abbauen', example: 'Sessions', pdu: 'Daten' },
  { nr: 4, de: 'Transport', en: 'Transport', task: 'Ende-zu-Ende, Ports', example: 'TCP, UDP', pdu: 'Segment' },
  { nr: 3, de: 'Vermittlung', en: 'Network', task: 'Adressierung, Routing', example: 'IP', pdu: 'Paket' },
  { nr: 2, de: 'Sicherung', en: 'Data Link', task: 'Rahmen, MAC-Adressen', example: 'Ethernet, 802.1Q', pdu: 'Frame' },
  { nr: 1, de: 'Bitübertragung', en: 'Physical', task: 'Bits über das Medium', example: 'Kabel, Funk', pdu: 'Bits' },
]

export interface Step { side: 'tx' | 'rx'; layer: number; pieces: string[]; caption: string }

function txPieces(layer: number): string[] {
  if (layer >= 5) return ['Daten']
  if (layer === 4) return ['TCP', 'Daten']
  if (layer === 3) return ['IP', 'TCP', 'Daten']
  return ['ETH', 'IP', 'TCP', 'Daten', 'FCS'] // L2, L1
}

function rxPieces(layer: number): string[] {
  if (layer === 1) return ['ETH', 'IP', 'TCP', 'Daten', 'FCS']
  if (layer === 2) return ['IP', 'TCP', 'Daten']
  if (layer === 3) return ['TCP', 'Daten']
  return ['Daten'] // L4..L7
}

const TX_CAP: Record<number, string> = {
  7: 'Schicht 7: Anwendung erzeugt die Daten (z.B. HTTP-Anfrage).',
  6: 'Schicht 6: Darstellung — Codierung/Verschlüsselung.',
  5: 'Schicht 5: Sitzung verwaltet die Verbindung.',
  4: 'Schicht 4: Transport hängt den TCP-Header an → Segment.',
  3: 'Schicht 3: Vermittlung hängt den IP-Header an → Paket.',
  2: 'Schicht 2: Sicherung hängt Ethernet-Header + FCS an → Frame.',
  1: 'Schicht 1: Bitübertragung sendet die Bits über das Medium.',
}
const RX_CAP: Record<number, string> = {
  1: 'Empfänger Schicht 1: Bits kommen an.',
  2: 'Empfänger Schicht 2: Ethernet-Header/FCS entfernt → Paket.',
  3: 'Empfänger Schicht 3: IP-Header entfernt → Segment.',
  4: 'Empfänger Schicht 4: TCP-Header entfernt → Daten.',
  5: 'Empfänger Schicht 5: Sitzung übergibt nach oben.',
  6: 'Empfänger Schicht 6: Darstellung dekodiert.',
  7: 'Empfänger Schicht 7: Anwendung erhält die Daten.',
}

export function buildSteps(): Step[] {
  const steps: Step[] = []
  for (let nr = 7; nr >= 1; nr--) {
    steps.push({ side: 'tx', layer: nr, pieces: txPieces(nr), caption: TX_CAP[nr] })
  }
  for (let nr = 1; nr <= 7; nr++) {
    steps.push({ side: 'rx', layer: nr, pieces: rxPieces(nr), caption: RX_CAP[nr] })
  }
  return steps
}
