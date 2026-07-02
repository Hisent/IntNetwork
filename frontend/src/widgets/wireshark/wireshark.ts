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

/** Anzeigefilter → Prädikat. Unterstützt: leer, Protokollname (dns/tcp/http/
 *  tls/icmp/udp/ip), `ip.addr == X`, `tcp.port == N`. Ungültig → null. */
export function parseFilter(filter: string): ((p: Packet) => boolean) | null {
  const f = filter.trim().toLowerCase()
  if (f === '') return () => true
  if (/^[a-z0-9.]+$/.test(f) && !f.includes('.')) {
    return (p) => p.protocols.includes(f)
  }
  let m = f.match(/^ip\.addr\s*==\s*([0-9.]+)$/)
  if (m) {
    const ip = m[1]
    return (p) => p.src === ip || p.dst === ip
  }
  m = f.match(/^tcp\.port\s*==\s*(\d+)$/)
  if (m) {
    const port = Number(m[1])
    return (p) => p.protocols.includes('tcp') && (p.ports?.includes(port) ?? false)
  }
  return null
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
    info: 'Standard query A intranet.nordwind.local',
    protocols: ['eth', 'ip', 'udp', 'dns'], ports: [55201, 53],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, DNSRV), udp(55201, 53),
      { name: 'Domain Name System (query)', fields: [{ label: 'Name', value: 'intranet.nordwind.local' }, { label: 'Type', value: 'A' }] }],
  },
  {
    no: 4, time: '1.106', src: DNSRV, dst: PC, protocol: 'DNS',
    info: 'Standard query response A 192.168.10.80',
    protocols: ['eth', 'ip', 'udp', 'dns'], ports: [53, 55201],
    layers: [eth(MAC_GW, MAC_PC), ip(DNSRV, PC), udp(53, 55201),
      { name: 'Domain Name System (response)', fields: [{ label: 'Name', value: 'intranet.nordwind.local' }, { label: 'Address', value: WEB }] }],
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
        { label: 'Host', value: 'intranet.nordwind.local' }] }],
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
        { label: 'Host', value: 'intranet.nordwind.local' },
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
    no: 13, time: '15.230', src: PC, dst: BANK, protocol: 'TLS',
    info: 'Client Hello  (SNI=bank.example.com)',
    protocols: ['eth', 'ip', 'tcp', 'tls'], ports: [52101, 443],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, BANK), tcp(52101, 443, 'PSH, ACK'),
      { name: 'Transport Layer Security', fields: [
        { label: 'Handshake', value: 'Client Hello' },
        { label: 'Server Name (SNI)', value: 'bank.example.com' }] }],
  },
  {
    no: 14, time: '15.290', src: PC, dst: BANK, protocol: 'TLS',
    info: 'Application Data',
    protocols: ['eth', 'ip', 'tcp', 'tls'], ports: [52101, 443],
    layers: [eth(MAC_PC, MAC_GW), ip(PC, BANK), tcp(52101, 443, 'PSH, ACK'),
      { name: 'Transport Layer Security', fields: [
        { label: 'Content Type', value: 'Application Data (23)' },
        { label: 'Encrypted Data', value: '17 03 03 00 8a f2 9c 41 …  (unlesbar)' }] }],
  },
]
