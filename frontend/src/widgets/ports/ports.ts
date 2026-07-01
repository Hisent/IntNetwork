export const WELL_KNOWN: Record<number, string> = {
  20: 'FTP-Data',
  21: 'FTP',
  22: 'SSH',
  23: 'Telnet',
  25: 'SMTP',
  53: 'DNS',
  67: 'DHCP',
  80: 'HTTP',
  110: 'POP3',
  143: 'IMAP',
  443: 'HTTPS',
  3389: 'RDP',
}

export function serviceFor(port: number): string {
  return WELL_KNOWN[port] ?? 'kein Standard-Dienst (dynamischer Port)'
}

export interface HandshakeStep {
  from: 'Client' | 'Server'
  flag: string
  text: string
}

export const HANDSHAKE: HandshakeStep[] = [
  { from: 'Client', flag: 'SYN', text: 'Verbindungswunsch, Startnummer x' },
  { from: 'Server', flag: 'SYN-ACK', text: 'akzeptiert, Startnummer y, bestätigt x+1' },
  { from: 'Client', flag: 'ACK', text: 'bestätigt y+1 — Verbindung steht' },
]
