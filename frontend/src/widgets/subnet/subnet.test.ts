import { describe, it, expect } from 'vitest'
import { subnetInfo } from './subnet'

describe('subnetInfo', () => {
  it('/24 network, broadcast, host range, count', () => {
    const r = subnetInfo('192.168.10.37', 24)
    expect(r.network).toBe('192.168.10.0')
    expect(r.broadcast).toBe('192.168.10.255')
    expect(r.firstHost).toBe('192.168.10.1')
    expect(r.lastHost).toBe('192.168.10.254')
    expect(r.mask).toBe('255.255.255.0')
    expect(r.usableHosts).toBe(254)
  })

  it('/26 splits the last octet', () => {
    const r = subnetInfo('10.0.0.130', 26)
    expect(r.network).toBe('10.0.0.128')
    expect(r.broadcast).toBe('10.0.0.191')
    expect(r.usableHosts).toBe(62)
  })

  it('/31 has no usable hosts', () => {
    const r = subnetInfo('192.168.1.0', 31)
    expect(r.usableHosts).toBe(0)
  })
})
