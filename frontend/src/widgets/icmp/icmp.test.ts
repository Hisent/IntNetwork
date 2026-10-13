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
