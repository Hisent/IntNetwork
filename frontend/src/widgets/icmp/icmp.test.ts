import { describe, it, expect } from 'vitest'
import { probe, PATH } from './icmp'

describe('probe (traceroute)', () => {
  it('TTL 1 -> erster Router, Time Exceeded', () => {
    const p = probe(1)
    expect(p.node?.name).toBe('Gateway')
    expect(p.status).toBe('exceeded')
  })

  it('TTL = Pfadlänge -> Ziel antwortet mit Reply', () => {
    const p = probe(PATH.length)
    expect(p.status).toBe('reply')
    expect(p.node?.name).toBe('Ziel-Server')
  })

  it('TTL über Pfadlänge -> Timeout', () => {
    expect(probe(PATH.length + 1).status).toBe('timeout')
  })
})
