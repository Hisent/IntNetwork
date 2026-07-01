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

const NO_SERVICE = { de: 'kein Standard-Dienst (dynamischer Port)', en: 'no standard service (dynamic port)' }

export function serviceFor(port: number, lang: 'de' | 'en' = 'de'): string {
  return WELL_KNOWN[port] ?? NO_SERVICE[lang]
}

export interface HandshakeStep {
  from: 'Client' | 'Server'
  flag: string
  text: { de: string; en: string }
}

export const HANDSHAKE: HandshakeStep[] = [
  { from: 'Client', flag: 'SYN', text: { de: 'Verbindungswunsch, Startnummer x', en: 'Wants to connect, starting number x' } },
  { from: 'Server', flag: 'SYN-ACK', text: { de: 'akzeptiert, Startnummer y, bestätigt x+1', en: 'accepts, starting number y, confirms x+1' } },
  { from: 'Client', flag: 'ACK', text: { de: 'bestätigt y+1 — Verbindung steht', en: 'confirms y+1 — connection established' } },
]
