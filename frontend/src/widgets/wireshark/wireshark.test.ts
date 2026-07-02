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
})
