export interface Layer {
  nr: number; de: string; en: string; task: { de: string; en: string }
  example: string; pdu: { de: string; en: string }
}

export const LAYERS: Layer[] = [
  { nr: 7, de: 'Anwendung', en: 'Application',
    task: { de: 'Dienste für Anwendungen', en: 'Services for applications' },
    example: 'HTTP, DNS', pdu: { de: 'Daten', en: 'Data' } },
  { nr: 6, de: 'Darstellung', en: 'Presentation',
    task: { de: 'Codierung, Verschlüsselung', en: 'Encoding, encryption' },
    example: 'TLS, UTF-8', pdu: { de: 'Daten', en: 'Data' } },
  { nr: 5, de: 'Sitzung', en: 'Session',
    task: { de: 'Sitzungen auf-/abbauen', en: 'Set up/tear down sessions' },
    example: 'Sessions', pdu: { de: 'Daten', en: 'Data' } },
  { nr: 4, de: 'Transport', en: 'Transport',
    task: { de: 'Ende-zu-Ende, Ports', en: 'End-to-end, ports' },
    example: 'TCP, UDP', pdu: { de: 'Segment', en: 'Segment' } },
  { nr: 3, de: 'Vermittlung', en: 'Network',
    task: { de: 'Adressierung, Routing', en: 'Addressing, routing' },
    example: 'IP', pdu: { de: 'Paket', en: 'Packet' } },
  { nr: 2, de: 'Sicherung', en: 'Data Link',
    task: { de: 'Rahmen, MAC-Adressen', en: 'Frames, MAC addresses' },
    example: 'Ethernet, 802.1Q', pdu: { de: 'Frame', en: 'Frame' } },
  { nr: 1, de: 'Bitübertragung', en: 'Physical',
    task: { de: 'Bits über das Medium', en: 'Bits over the medium' },
    example: 'Kabel, Funk', pdu: { de: 'Bits', en: 'Bits' } },
]

export interface Step { side: 'tx' | 'rx'; layer: number; pieces: string[]; caption: { de: string; en: string } }

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

const TX_CAP: Record<number, { de: string; en: string }> = {
  7: { de: 'Schicht 7: Anwendung erzeugt die Daten (z.B. HTTP-Anfrage).',
       en: 'Layer 7: application generates the data (e.g. an HTTP request).' },
  6: { de: 'Schicht 6: Darstellung — Codierung/Verschlüsselung.',
       en: 'Layer 6: presentation — encoding/encryption.' },
  5: { de: 'Schicht 5: Sitzung verwaltet die Verbindung.',
       en: 'Layer 5: session manages the connection.' },
  4: { de: 'Schicht 4: Transport hängt den TCP-Header an → Segment.',
       en: 'Layer 4: transport attaches the TCP header → segment.' },
  3: { de: 'Schicht 3: Vermittlung hängt den IP-Header an → Paket.',
       en: 'Layer 3: network attaches the IP header → packet.' },
  2: { de: 'Schicht 2: Sicherung hängt Ethernet-Header + FCS an → Frame.',
       en: 'Layer 2: data link attaches Ethernet header + FCS → frame.' },
  1: { de: 'Schicht 1: Bitübertragung sendet die Bits über das Medium.',
       en: 'Layer 1: physical sends the bits over the medium.' },
}
const RX_CAP: Record<number, { de: string; en: string }> = {
  1: { de: 'Empfänger Schicht 1: Bits kommen an.', en: 'Receiver layer 1: bits arrive.' },
  2: { de: 'Empfänger Schicht 2: Ethernet-Header/FCS entfernt → Paket.',
       en: 'Receiver layer 2: Ethernet header/FCS removed → packet.' },
  3: { de: 'Empfänger Schicht 3: IP-Header entfernt → Segment.',
       en: 'Receiver layer 3: IP header removed → segment.' },
  4: { de: 'Empfänger Schicht 4: TCP-Header entfernt → Daten.',
       en: 'Receiver layer 4: TCP header removed → data.' },
  5: { de: 'Empfänger Schicht 5: Sitzung übergibt nach oben.',
       en: 'Receiver layer 5: session hands it upward.' },
  6: { de: 'Empfänger Schicht 6: Darstellung dekodiert.', en: 'Receiver layer 6: presentation decodes.' },
  7: { de: 'Empfänger Schicht 7: Anwendung erhält die Daten.',
       en: 'Receiver layer 7: application receives the data.' },
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
