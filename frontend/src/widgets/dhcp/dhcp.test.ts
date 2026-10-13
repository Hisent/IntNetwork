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
