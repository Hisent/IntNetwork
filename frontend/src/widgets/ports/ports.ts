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

// --- Terminal des Widgets: fiktiver Host "intranet" ---------------------------------
// Adresse wie im Wireshark-Mitschnitt und im Troubleshooting-Modul: intranet = web01 = 192.168.10.80.
export const INTRANET_IP = '192.168.10.80'

// offene TCP-Ports + Banner wie im echten Leben
const OPEN_PORTS: Record<number, string | { de: string; en: string }> = {
  22: 'SSH-2.0-OpenSSH_9.6',
  80: 'HTTP/1.1 200 OK\nServer: nginx',
  443: {
    de: '(TLS-Handshake — verschlüsselt, kein Klartext-Banner)',
    en: '(TLS handshake — encrypted, no cleartext banner)',
  },
}

export function runPortsCommand(lang: 'de' | 'en', cmd: string): string {
  const c = cmd.trim().toLowerCase().replace(/\s+/g, ' ')
  if (!c) return ''
  if (c === '?' || c === 'help') {
    return lang === 'de'
      ? 'Befehle:\n  telnet intranet <port>   TCP-Verbindung testen\n  scan intranet            offene Ports suchen'
      : 'Commands:\n  telnet intranet <port>   test a TCP connection\n  scan intranet            look for open ports'
  }
  if (c === 'scan intranet') {
    const list = Object.keys(OPEN_PORTS).map((p) => `  ${p}/tcp  open  ${WELL_KNOWN[Number(p)]}`).join('\n')
    return `Scanning intranet (${INTRANET_IP})…\n${list}`
  }
  const m = c.match(/^telnet intranet (\d+)$/)
  if (m) {
    const port = Number(m[1])
    if (port < 1 || port > 65535) {
      return lang === 'de' ? `Ungültiger Port ${m[1]} — gültig sind 1–65535.` : `Invalid port ${m[1]} — valid ports are 1–65535.`
    }
    const banner = OPEN_PORTS[port]
    if (banner) return `Trying ${INTRANET_IP}:${port}…\nConnected to intranet.\n${typeof banner === 'string' ? banner : banner[lang]}`
    if (port === 53) {
      return lang === 'de'
        ? `Trying ${INTRANET_IP}:53…\nConnection refused.\n(Auf diesem Host läuft kein DNS-Server. Merke: DNS nutzt meist UDP 53, telnet testet nur TCP.)`
        : `Trying ${INTRANET_IP}:53…\nConnection refused.\n(No DNS server runs on this host. Note: DNS mostly uses UDP 53, telnet only tests TCP.)`
    }
    return `Trying ${INTRANET_IP}:${port}…\nConnection refused.`
  }
  return lang === 'de' ? `Unbekannter Befehl: ${cmd} — tippe ?` : `Unknown command: ${cmd} — type ?`
}
