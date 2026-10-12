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

// Bereiche nach IANA/RFC 6335: 0–1023 System (well-known), 1024–49151 registriert, 49152–65535 dynamisch.
function noService(port: number): { de: string; en: string } {
  if (!Number.isInteger(port) || port < 0 || port > 65535)
    return { de: 'ungültig (Ports: 0–65535)', en: 'invalid (ports: 0–65535)' }
  if (port < 1024)
    return { de: 'hier kein Dienst hinterlegt (Well-known-/System-Port)', en: 'no service listed here (well-known/system port)' }
  if (port < 49152)
    return { de: 'hier kein Dienst hinterlegt (registrierter Port)', en: 'no service listed here (registered port)' }
  return { de: 'kein Standard-Dienst (dynamischer Port)', en: 'no standard service (dynamic port)' }
}

export function serviceFor(port: number, lang: 'de' | 'en' = 'de'): string {
  return WELL_KNOWN[port] ?? noService(port)[lang]
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
