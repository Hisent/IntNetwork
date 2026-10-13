import { describe, it, expect } from 'vitest'
import { CAPTURE, applyFilter, parseFilter } from './wireshark'

describe('applyFilter', () => {
  it('empty filter returns everything', () => {
    expect(applyFilter(CAPTURE, '')).toHaveLength(CAPTURE.length)
    expect(applyFilter(CAPTURE, '  ')).toHaveLength(CAPTURE.length)
  })

  it('protocol filter matches the whole stack (http implies tcp)', () => {
    const http = applyFilter(CAPTURE, 'http')!
    expect(http.length).toBeGreaterThan(0)
    expect(http.every((p) => p.protocols.includes('http'))).toBe(true)
    // tcp matcht auch HTTP/TLS-Pakete, weil sie über TCP laufen
    const tcpN = applyFilter(CAPTURE, 'tcp')!.length
    expect(tcpN).toBeGreaterThan(http.length)
    expect(applyFilter(CAPTURE, 'HTTP')!.length).toBe(http.length) // case-insensitiv
  })

  it('dns and icmp filters find their packets', () => {
    expect(applyFilter(CAPTURE, 'dns')).toHaveLength(2)
    expect(applyFilter(CAPTURE, 'icmp')).toHaveLength(2)
  })

  it('ip.addr matches source or destination', () => {
    const r = applyFilter(CAPTURE, 'ip.addr == 192.168.10.53')!
    expect(r).toHaveLength(2)
    expect(r.every((p) => p.src === '192.168.10.53' || p.dst === '192.168.10.53')).toBe(true)
  })

  it('tcp.port matches either port', () => {
    const r = applyFilter(CAPTURE, 'tcp.port == 443')!
    expect(r.length).toBeGreaterThan(0)
    expect(r.every((p) => p.ports?.includes(443))).toBe(true)
    // Port 53 ist UDP -> tcp.port findet nichts
    expect(applyFilter(CAPTURE, 'tcp.port == 53')).toHaveLength(0)
  })

  it('invalid filter returns null (red field)', () => {
    expect(applyFilter(CAPTURE, 'kaputt ==')).toBeNull()
    expect(parseFilter('ip.addr = 1.2.3.4')).toBeNull()
    expect(parseFilter('kaputt')).toBeNull() // unbekanntes Protokoll
    expect(applyFilter(CAPTURE, 'arp')).toHaveLength(0) // bekannt, aber nicht im Mitschnitt
  })

  it('udp.port and ip.src/ip.dst work like in Wireshark', () => {
    expect(applyFilter(CAPTURE, 'udp.port == 53')).toHaveLength(2)
    expect(applyFilter(CAPTURE, 'ip.src == 192.168.10.53')).toHaveLength(1)
    expect(applyFilter(CAPTURE, 'ip.dst == 192.168.10.53')).toHaveLength(1)
  })
})

describe('CAPTURE data consistency', () => {
  it('has unique, ascending packet numbers', () => {
    const nos = CAPTURE.map((p) => p.no)
    expect(nos).toEqual([...nos].sort((a, b) => a - b))
    expect(new Set(nos).size).toBe(nos.length)
  })

  it('contains exactly one secret packet with cleartext credentials', () => {
    const secrets = CAPTURE.filter((p) => p.secret)
    expect(secrets).toHaveLength(1)
    const fields = secrets[0].layers.flatMap((l) => l.fields)
    expect(fields.some((f) => f.label === 'password')).toBe(true)
  })

  it('every packet has ethernet + ip layers at least', () => {
    for (const p of CAPTURE) {
      expect(p.layers.length).toBeGreaterThanOrEqual(2)
      expect(p.protocols).toContain('ip')
    }
  })

  it('TLS flow is complete: handshake both ways, server packets, no .local zone', () => {
    const tls = CAPTURE.filter((p) => p.ports?.includes(443))
    const flags = tls.map((p) => p.layers.find((l) => l.name === 'Transmission Control Protocol')!.fields[2].value)
    expect(flags.slice(0, 3)).toEqual(['SYN', 'SYN, ACK', 'ACK'])
    const server = tls.filter((p) => p.ports![0] === 443)
    expect(server.length).toBeGreaterThanOrEqual(3)
    expect(server.some((p) => p.info.startsWith('Server Hello'))).toBe(true)
    expect(server.some((p) => p.info === 'Application Data')).toBe(true)
    // .local ist für mDNS reserviert (RFC 6762) -> nicht als interne DNS-Zone zeigen
    expect(JSON.stringify(CAPTURE)).not.toContain('.local')
  })
})

describe('parseFilter — Operatoren und Kombinationen wie in Wireshark', () => {
  const n = (f: string) => applyFilter(CAPTURE, f)?.length ?? null
  it('and/or/not, auch als &&, ||, !', () => {
    expect(n('http && ip.src == 192.168.20.34')).toBe(2) // GET + POST
    expect(n('http and ip.src == 192.168.20.34')).toBe(2)
    expect(n('dns || icmp')).toBe(4)
    expect(n('dns or icmp')).toBe(4)
    expect(n('!dns')).toBe(CAPTURE.length - 2)
    expect(n('not dns')).toBe(CAPTURE.length - 2)
    expect(n('ip.src == 192.168.20.34 || ip.dst == 192.168.20.34')).toBe(CAPTURE.length) // = ip.addr
  })
  it('and bindet stärker als or; Klammern ändern das', () => {
    expect(n('icmp || dns && ip.src == 192.168.10.53')).toBe(3) // 2 ICMP + 1 DNS-Antwort
    expect(n('(icmp || dns) && ip.src == 192.168.10.53')).toBe(1)
    expect(n('!(tcp || udp)')).toBe(2) // nur die beiden ICMP-Pakete
    expect(n('((http))')).toBe(4)
  })
  it('eq/ne, != und Quell-/Zielport', () => {
    expect(n('tcp.port eq 443')).toBe(n('tcp.port == 443'))
    expect(n('tcp.dstport == 443')).toBe(5)
    expect(n('tcp.srcport == 443')).toBe(3)
    expect(n('udp.dstport == 53')).toBe(1)
    expect(n('ip.addr != 192.168.10.53')).toBe(CAPTURE.length - 2)
    expect(n('ip.addr ne 192.168.10.53')).toBe(CAPTURE.length - 2)
    // != ist falsch, wenn das Feld fehlt: nur TCP-Pakete ohne Port 80
    expect(n('tcp.port != 80')).toBe(8)
  })
  it('unvollständige oder unmögliche Werte sind ungültig (rot), nicht „0 Treffer"', () => {
    for (const bad of ['ip.addr == 192.168.10', 'ip.addr == 999.1.1.1', 'tcp.port == 70000', 'tcp.port == abc',
      'http &&', '&& http', 'http || || dns', '()', '(http', 'http)', '!', 'not', 'http dns', 'ip.addr ==', 'port == 80'])
      expect(parseFilter(bad), bad).toBeNull()
  })
  it('extreme Eingaben stürzen nicht ab', () => {
    expect(parseFilter('('.repeat(2000))).toBeNull()
    expect(parseFilter('! '.repeat(500) + 'dns')).not.toBeNull()
    expect(parseFilter('http && '.repeat(500) + 'http')).not.toBeNull()
  })
})

describe('CAPTURE — Ports, Flags und Sprache konsistent', () => {
  const tcpFlags = (no: number) => CAPTURE[no - 1].layers.find((l) => l.name === 'Transmission Control Protocol')!.fields[2].value
  it('Info-Spalte, ports[] und Layer-Felder nennen dieselben Ports', () => {
    for (const p of CAPTURE.filter((x) => x.ports)) {
      const l4 = p.layers.find((l) => /Transmission|Datagram/.test(l.name))!
      expect([Number(l4.fields[0].value), Number(l4.fields[1].value)]).toEqual(p.ports)
      if (p.protocol === 'TCP') expect(p.info.startsWith(`${p.ports![0]} → ${p.ports![1]}`)).toBe(true)
    }
  })
  it('Anfrage und Antwort tauschen Adressen und Ports', () => {
    for (const [req, res] of [[1, 2], [3, 4], [5, 6], [8, 9], [10, 11], [12, 13]]) {
      const a = CAPTURE[req - 1], b = CAPTURE[res - 1]
      expect([b.src, b.dst]).toEqual([a.dst, a.src])
      if (a.ports) expect(b.ports).toEqual([a.ports[1], a.ports[0]])
    }
  })
  it('beide TCP-Handshakes: SYN(Seq=0) → SYN,ACK(Seq=0 Ack=1) → ACK(Seq=1 Ack=1)', () => {
    for (const start of [5, 12]) {
      expect([0, 1, 2].map((d) => tcpFlags(start + d))).toEqual(['SYN', 'SYN, ACK', 'ACK'])
      expect(CAPTURE[start - 1].info).toContain('[SYN] Seq=0')
      expect(CAPTURE[start].info).toContain('[SYN, ACK] Seq=0 Ack=1')
      expect(CAPTURE[start + 1].info).toContain('[ACK] Seq=1 Ack=1')
    }
  })
  it('Zeitstempel steigen monoton', () => {
    const t = CAPTURE.map((p) => Number(p.time))
    expect(t).toEqual([...t].sort((a, b) => a - b))
  })
  it('Paketdetails bleiben englisch wie im echten Tool (kein „unlesbar")', () => {
    expect(JSON.stringify(CAPTURE)).not.toMatch(/unlesbar|[äöüß]/)
  })
})
