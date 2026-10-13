import { describe, it, expect } from 'vitest'
import { probe, PATH } from './icmp'

describe('probe (traceroute)', () => {
  it('TTL 1 -> erster Router, Time Exceeded', () => {
    const p = probe(1)
    expect(p.node?.name.de).toBe('Gateway')
    expect(p.status).toBe('exceeded')
  })

  it('TTL = Pfadlänge -> Ziel antwortet mit Reply', () => {
    const p = probe(PATH.length)
    expect(p.status).toBe('reply')
    expect(p.node?.name.de).toBe('Ziel-Server')
  })

  it('öffentliche Hops liegen in den Doku-Bereichen (RFC 5737)', () => {
    const ok = /^(192\.168\.|192\.0\.2\.|198\.51\.100\.|203\.0\.113\.)/
    for (const n of PATH) expect(n.ip).toMatch(ok)
  })

  it('TTL über Pfadlänge -> Timeout', () => {
    expect(probe(PATH.length + 1).status).toBe('timeout')
  })
})

describe('probe — TTL-Grenzen', () => {
  it('TTL n erreicht genau den n-ten Hop; nur der letzte antwortet mit Echo Reply', () => {
    expect(PATH.map((_, i) => probe(i + 1).status)).toEqual(['exceeded', 'exceeded', 'exceeded', 'reply'])
    expect(PATH.map((_, i) => probe(i + 1).node!.ip)).toEqual(['192.168.10.1', '203.0.113.2', '192.0.2.1', '198.51.100.10'])
  })
  it('TTL 0, negative und zu große TTL: kein Knoten, kein Absturz', () => {
    for (const ttl of [0, -1, PATH.length + 1, 255]) expect(probe(ttl)).toEqual({ ttl, node: null, status: 'timeout' })
  })
  it('Laufzeiten steigen entlang des Pfads; öffentliche Hops nur aus RFC-5737-Bereichen', () => {
    const rtt = PATH.map((n) => n.rttMs)
    expect(rtt).toEqual([...rtt].sort((a, b) => a - b))
    for (const n of PATH.slice(1)) expect(n.ip).toMatch(/^(192\.0\.2|198\.51\.100|203\.0\.113)\./)
  })
})
