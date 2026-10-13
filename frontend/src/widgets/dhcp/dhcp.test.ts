import { describe, it, expect } from 'vitest'
import { lease, POOL_SIZE } from './dhcp'

describe('lease (DORA)', () => {
  it('erster Client bekommt .100 über 4 Phasen', () => {
    const l = lease(0)!
    expect(l.ip).toBe('192.168.10.100')
    expect(l.steps.map((s) => s.phase)).toEqual(['Discover', 'Offer', 'Request', 'Ack'])
  })

  it('nächster Client bekommt die nächste Adresse', () => {
    expect(lease(3)!.ip).toBe('192.168.10.103')
  })

  it('Pool endet bei .199 — danach ist er erschöpft', () => {
    expect(POOL_SIZE).toBe(100)
    expect(lease(POOL_SIZE - 1)!.ip).toBe('192.168.10.199')
    expect(lease(POOL_SIZE)).toBeNull()
  })
})

describe('lease — Pool und Optionen wie im Modultext (dhcp.py)', () => {
  it('alle 100 Adressen .100–.199 sind eindeutig, Maske/Gateway/DNS gleich', () => {
    const all = Array.from({ length: POOL_SIZE }, (_, i) => lease(i)!)
    expect(new Set(all.map((l) => l.ip)).size).toBe(100)
    expect([all[0].ip, all[99].ip]).toEqual(['192.168.10.100', '192.168.10.199'])
    for (const l of all) expect([l.mask, l.gateway, l.dns]).toEqual(['255.255.255.0', '192.168.10.1', '192.168.10.1'])
  })
  it('DORA: Discover und Request sind Broadcasts, die angebotene Adresse zieht sich durch', () => {
    const l = lease(7)!
    expect(l.steps.map((s) => s.phase)).toEqual(['Discover', 'Offer', 'Request', 'Ack'])
    expect(l.steps[0].text.en).toContain('broadcast')
    expect(l.steps[2].text.en).toContain('broadcast')
    for (const s of l.steps.slice(1)) { expect(s.text.de).toContain(l.ip); expect(s.text.en).toContain(l.ip) }
  })
  it('außerhalb des Pools: null statt erfundener Adresse', () => {
    expect(lease(-1)).toBeNull()
    expect(lease(100)).toBeNull()
    expect(lease(1e9)).toBeNull()
  })
})
