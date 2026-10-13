// Mini-Wireshark: vorbereiteter Capture + Anzeigefilter-Engine.
// Paketliste/Detail-Felder bleiben Englisch wie im echten Tool (vgl. Cisco-CLI).

export interface Layer {
  name: string
  fields: { label: string; value: string }[]
}

export interface Packet {
  no: number
  time: string
  src: string
  dst: string
  protocol: string // Anzeige-Spalte (oberstes Protokoll)
  info: string
  protocols: string[] // ganzer Stack für Filter: http matcht auch tcp/ip
  ports?: [number, number] // [src, dst]
  layers: Layer[]
  secret?: boolean // das Klartext-Passwort-Paket (Challenge-Ziel)
}

// Bekannte Protokollnamen: unbekannte Wörter färbt auch das echte Wireshark rot.
const KNOWN_PROTOCOLS = new Set(['frame', 'eth', 'arp', 'ip', 'ipv6', 'icmp', 'icmpv6', 'tcp', 'udp',
  'dns', 'dhcp', 'http', 'tls', 'ssh', 'ftp', 'smtp', 'ntp', 'telnet', 'quic'])

type Pred = (p: Packet) => boolean

const isIpv4 = (s: string) => /^\d{1,3}(\.\d{1,3}){3}$/.test(s) && s.split('.').every((o) => Number(o) <= 255)

/** Ein Protokollname oder ein Feldvergleich → Prädikat; null = ungültig. */
function parseAtom(atom: string): Pred | null {
  if (KNOWN_PROTOCOLS.has(atom)) return (p) => p.protocols.includes(atom)
  const m = atom.match(/^([a-z.]+)\s*(==|!=)\s*(\S+)$/)
  if (!m) return null
  const [, field, op, value] = m
  const ipField = field.match(/^ip\.(addr|src|dst)$/)
  const portField = field.match(/^(tcp|udp)\.(port|srcport|dstport)$/)
  let has: Pred
  let eq: Pred
  if (ipField && isIpv4(value)) {
    const which = ipField[1]
    has = () => true // jedes Paket des Mitschnitts hat einen IPv4-Header
    eq = (p) => (which !== 'dst' && p.src === value) || (which !== 'src' && p.dst === value)
  } else if (portField && /^\d+$/.test(value) && Number(value) <= 65535) {
    const [, proto, which] = portField
    const port = Number(value)
    has = (p) => p.protocols.includes(proto) && p.ports !== undefined
    eq = (p) => has(p) && (which === 'port' ? p.ports!.includes(port) : p.ports![which === 'srcport' ? 0 : 1] === port)
  } else {
    return null
  }
  // wie Wireshark: ein Vergleich ist falsch, wenn das Paket das Feld gar nicht hat
  return op === '==' ? eq : (p) => has(p) && !eq(p)
}

/** Anzeigefilter → Prädikat. Unterstützt: leer, Protokollname (dns/tcp/http/tls/icmp/udp/ip …),
 *  `ip.addr|ip.src|ip.dst`, `tcp|udp.port|srcport|dstport` mit `==`/`eq` und `!=`/`ne`,
 *  verknüpft mit `&&`/`and`, `||`/`or`, `!`/`not` und Klammern (and bindet stärker als or).
 *  Ungültig → null.
 *  ponytail: andere Felder (tcp.flags.syn, http.request.method …) kennt die Mini-Engine nicht
 *  und meldet sie als ungültig — bei Bedarf in parseAtom ergänzen. */
export function parseFilter(filter: string): Pred | null {
  const f = filter.trim().toLowerCase()
  if (f === '') return () => true
  const tokens = f.replace(/\s+eq\s+/g, ' == ').replace(/\s+ne\s+/g, ' != ')
    .split(/\s*(\(|\)|&&|\|\||!(?!=)|\band\b|\bor\b|\bnot\b)\s*/).filter(Boolean)
  let i = 0
  const unary = (): Pred | null => {
    const t = tokens[i++]
    if (t === undefined) return null
    if (t === '!' || t === 'not') { const x = unary(); return x && ((p) => !x(p)) }
    if (t === '(') { const x = or(); return tokens[i++] === ')' ? x : null }
    return parseAtom(t)
  }
  const and = (): Pred | null => {
    let left = unary()
    while (left && (tokens[i] === '&&' || tokens[i] === 'and')) {
      i++
      const l = left, r = unary()
      left = r && ((p) => l(p) && r(p))
    }
    return left
  }
  function or(): Pred | null {
    let left = and()
    while (left && (tokens[i] === '||' || tokens[i] === 'or')) {
      i++
      const l = left, r = and()
      left = r && ((p) => l(p) || r(p))
    }
    return left
  }
  const pred = or()
  return pred && i === tokens.length ? pred : null
}

export function applyFilter(packets: Packet[], filter: string): Packet[] | null {
  const pred = parseFilter(filter)
  return pred ? packets.filter(pred) : null
}

const eth = (src: string, dst: string): Layer => ({
  name: 'Ethernet II',
  fields: [{ label: 'Source MAC', value: src }, { label: 'Destination MAC', value: dst }],
})
const ip = (src: string, dst: string): Layer => ({
  name: 'Internet Protocol Version 4',
  fields: [{ label: 'Source Address', value: src }, { label: 'Destination Address', value: dst }],
})
const tcp = (sport: number, dport: number, flags: string): Layer => ({
  name: 'Transmission Control Protocol',
  fields: [
    { label: 'Source Port', value: String(sport) },
    { label: 'Destination Port', value: String(dport) },
    { label: 'Flags', value: flags },
  ],
})
const udp = (sport: number, dport: number): Layer => ({
  name: 'User Datagram Protocol',
  fields: [{ label: 'Source Port', value: String(sport) }, { label: 'Destination Port', value: String(dport) }],
})

const PC = '192.168.20.34'
const DNSRV = '192.168.10.53'
const WEB = '192.168.10.80'
const BANK = '203.0.113.80'
const MAC_PC = '00:1b:44:11:3a:b7'
const MAC_GW = '00:09:0f:aa:00:01'

export const CAPTURE: Packet[] = [
  {
    no: 1, time: '0.000', src: PC, dst: WEB, protocol: 'ICMP',
    info: 'Echo (ping) request  id=0x0001, seq=1',
    protocols: ['eth', 'ip', 'icmp'],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, WEB),
      { name: 'Internet Control Message Protocol', fields: [{ label: 'Type', value: '8 (Echo request)' }] }],
  },
  {
    no: 2, time: '0.002', src: WEB, dst: PC, protocol: 'ICMP',
    info: 'Echo (ping) reply    id=0x0001, seq=1',
    protocols: ['eth', 'ip', 'icmp'],
    layers: [eth(MAC_GW, MAC_PC), ip(WEB, PC),
      { name: 'Internet Control Message Protocol', fields: [{ label: 'Type', value: '0 (Echo reply)' }] }],
  },
  {
    no: 3, time: '1.104', src: PC, dst: DNSRV, protocol: 'DNS',
    info: 'Standard query A intranet.nordwind-intern.de',
    protocols: ['eth', 'ip', 'udp', 'dns'], ports: [55201, 53],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, DNSRV), udp(55201, 53),
      { name: 'Domain Name System (query)', fields: [{ label: 'Name', value: 'intranet.nordwind-intern.de' }, { label: 'Type', value: 'A' }] }],
  },
  {
    no: 4, time: '1.106', src: DNSRV, dst: PC, protocol: 'DNS',
    info: 'Standard query response A 192.168.10.80',
    protocols: ['eth', 'ip', 'udp', 'dns'], ports: [53, 55201],
    layers: [eth(MAC_GW, MAC_PC), ip(DNSRV, PC), udp(53, 55201),
      { name: 'Domain Name System (response)', fields: [{ label: 'Name', value: 'intranet.nordwind-intern.de' }, { label: 'Address', value: WEB }] }],
  },
  {
    no: 5, time: '1.110', src: PC, dst: WEB, protocol: 'TCP',
    info: '52100 → 80 [SYN] Seq=0',
    protocols: ['eth', 'ip', 'tcp'], ports: [52100, 80],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, WEB), tcp(52100, 80, 'SYN')],
  },
  {
    no: 6, time: '1.112', src: WEB, dst: PC, protocol: 'TCP',
    info: '80 → 52100 [SYN, ACK] Seq=0 Ack=1',
    protocols: ['eth', 'ip', 'tcp'], ports: [80, 52100],
    layers: [eth(MAC_GW, MAC_PC), ip(WEB, PC), tcp(80, 52100, 'SYN, ACK')],
  },
  {
    no: 7, time: '1.113', src: PC, dst: WEB, protocol: 'TCP',
    info: '52100 → 80 [ACK] Seq=1 Ack=1',
    protocols: ['eth', 'ip', 'tcp'], ports: [52100, 80],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, WEB), tcp(52100, 80, 'ACK')],
  },
  {
    no: 8, time: '1.120', src: PC, dst: WEB, protocol: 'HTTP',
    info: 'GET /login HTTP/1.1',
    protocols: ['eth', 'ip', 'tcp', 'http'], ports: [52100, 80],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, WEB), tcp(52100, 80, 'PSH, ACK'),
      { name: 'Hypertext Transfer Protocol', fields: [
        { label: 'Request', value: 'GET /login HTTP/1.1' },
        { label: 'Host', value: 'intranet.nordwind-intern.de' }] }],
  },
  {
    no: 9, time: '1.135', src: WEB, dst: PC, protocol: 'HTTP',
    info: 'HTTP/1.1 200 OK  (text/html)',
    protocols: ['eth', 'ip', 'tcp', 'http'], ports: [80, 52100],
    layers: [eth(MAC_GW, MAC_PC), ip(WEB, PC), tcp(80, 52100, 'PSH, ACK'),
      { name: 'Hypertext Transfer Protocol', fields: [
        { label: 'Response', value: 'HTTP/1.1 200 OK' },
        { label: 'Content-Type', value: 'text/html' }] }],
  },
  {
    no: 10, time: '9.480', src: PC, dst: WEB, protocol: 'HTTP',
    info: 'POST /login HTTP/1.1  (application/x-www-form-urlencoded)',
    protocols: ['eth', 'ip', 'tcp', 'http'], ports: [52100, 80],
    secret: true,
    layers: [eth(MAC_PC, MAC_GW), ip(PC, WEB), tcp(52100, 80, 'PSH, ACK'),
      { name: 'Hypertext Transfer Protocol', fields: [
        { label: 'Request', value: 'POST /login HTTP/1.1' },
        { label: 'Host', value: 'intranet.nordwind-intern.de' },
        { label: 'Content-Type', value: 'application/x-www-form-urlencoded' }] },
      { name: 'HTML Form URL Encoded', fields: [
        { label: 'username', value: 'b.berg' },
        { label: 'password', value: 'Sommer2026!' }] }],
  },
  {
    no: 11, time: '9.512', src: WEB, dst: PC, protocol: 'HTTP',
    info: 'HTTP/1.1 302 Found  (Location: /start)',
    protocols: ['eth', 'ip', 'tcp', 'http'], ports: [80, 52100],
    layers: [eth(MAC_GW, MAC_PC), ip(WEB, PC), tcp(80, 52100, 'PSH, ACK'),
      { name: 'Hypertext Transfer Protocol', fields: [
        { label: 'Response', value: 'HTTP/1.1 302 Found' },
        { label: 'Location', value: '/start' }] }],
  },
  {
    no: 12, time: '15.201', src: PC, dst: BANK, protocol: 'TCP',
    info: '52101 → 443 [SYN] Seq=0',
    protocols: ['eth', 'ip', 'tcp'], ports: [52101, 443],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, BANK), tcp(52101, 443, 'SYN')],
  },
  {
    no: 13, time: '15.228', src: BANK, dst: PC, protocol: 'TCP',
    info: '443 → 52101 [SYN, ACK] Seq=0 Ack=1',
    protocols: ['eth', 'ip', 'tcp'], ports: [443, 52101],
    layers: [eth(MAC_GW, MAC_PC), ip(BANK, PC), tcp(443, 52101, 'SYN, ACK')],
  },
  {
    no: 14, time: '15.229', src: PC, dst: BANK, protocol: 'TCP',
    info: '52101 → 443 [ACK] Seq=1 Ack=1',
    protocols: ['eth', 'ip', 'tcp'], ports: [52101, 443],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, BANK), tcp(52101, 443, 'ACK')],
  },
  {
    no: 15, time: '15.230', src: PC, dst: BANK, protocol: 'TLS',
    info: 'Client Hello  (SNI=bank.example.com)',
    protocols: ['eth', 'ip', 'tcp', 'tls'], ports: [52101, 443],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, BANK), tcp(52101, 443, 'PSH, ACK'),
      { name: 'Transport Layer Security', fields: [
        { label: 'Handshake', value: 'Client Hello' },
        { label: 'Server Name (SNI)', value: 'bank.example.com' }] }],
  },
  {
    // TLS 1.3: ab dem Server Hello ist der Rest des Handshakes (Zertifikat, Finished)
    // bereits verschlüsselt und erscheint in Wireshark als "Application Data".
    no: 16, time: '15.258', src: BANK, dst: PC, protocol: 'TLS',
    info: 'Server Hello, Change Cipher Spec, Application Data',
    protocols: ['eth', 'ip', 'tcp', 'tls'], ports: [443, 52101],
    layers: [eth(MAC_GW, MAC_PC), ip(BANK, PC), tcp(443, 52101, 'PSH, ACK'),
      { name: 'Transport Layer Security', fields: [
        { label: 'Handshake', value: 'Server Hello' },
        { label: 'Supported Version', value: 'TLS 1.3 (0x0304)' },
        { label: 'Encrypted Data', value: '17 03 03 09 c4 5b e0 1d …  (encrypted)' }] }],
  },
  {
    no: 17, time: '15.262', src: PC, dst: BANK, protocol: 'TLS',
    info: 'Change Cipher Spec, Application Data',
    protocols: ['eth', 'ip', 'tcp', 'tls'], ports: [52101, 443],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, BANK), tcp(52101, 443, 'PSH, ACK'),
      { name: 'Transport Layer Security', fields: [
        { label: 'Content Type', value: 'Change Cipher Spec (20)' },
        { label: 'Encrypted Data', value: '17 03 03 00 45 7a 0c 93 …  (encrypted)' }] }],
  },
  {
    no: 18, time: '15.290', src: PC, dst: BANK, protocol: 'TLS',
    info: 'Application Data',
    protocols: ['eth', 'ip', 'tcp', 'tls'], ports: [52101, 443],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, BANK), tcp(52101, 443, 'PSH, ACK'),
      { name: 'Transport Layer Security', fields: [
        { label: 'Content Type', value: 'Application Data (23)' },
        { label: 'Encrypted Data', value: '17 03 03 00 8a f2 9c 41 …  (encrypted)' }] }],
  },
  {
    no: 19, time: '15.331', src: BANK, dst: PC, protocol: 'TLS',
    info: 'Application Data',
    protocols: ['eth', 'ip', 'tcp', 'tls'], ports: [443, 52101],
    layers: [eth(MAC_GW, MAC_PC), ip(BANK, PC), tcp(443, 52101, 'PSH, ACK'),
      { name: 'Transport Layer Security', fields: [
        { label: 'Content Type', value: 'Application Data (23)' },
        { label: 'Encrypted Data', value: '17 03 03 04 1e 6d b8 27 …  (encrypted)' }] }],
  },
]
