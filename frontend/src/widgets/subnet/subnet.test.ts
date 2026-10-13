import { describe, it, expect } from 'vitest'
import { clampOctet, subnetInfo } from './subnet'

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

  it('/31 (RFC 3021, point-to-point): both addresses are usable', () => {
    const r = subnetInfo('192.168.1.1', 31)
    expect(r.usableHosts).toBe(2)
    expect(r.firstHost).toBe('192.168.1.0')
    expect(r.lastHost).toBe('192.168.1.1')
    expect(r.mask).toBe('255.255.255.254')
  })
  it('/32 is a single host address', () => {
    const r = subnetInfo('172.16.5.77', 32)
    expect(r.usableHosts).toBe(1)
    expect(r.network).toBe('172.16.5.77')
    expect(r.firstHost).toBe('172.16.5.77')
    expect(r.lastHost).toBe('172.16.5.77')
  })
  it('matches an independent BigInt reference for every prefix /0–/32', () => {
    const str = (x: bigint) => [x >> 24n, (x >> 16n) & 255n, (x >> 8n) & 255n, x & 255n].join('.')
    for (const ip of ['0.0.0.0', '255.255.255.255', '172.16.5.77', '128.0.0.1', '223.255.255.254']) {
      const n = ip.split('.').reduce((a, o) => a * 256n + BigInt(o), 0n)
      for (let p = 0; p <= 32; p++) {
        const size = 1n << BigInt(32 - p)
        const net = n - (n % size)
        const r = subnetInfo(ip, p)
        expect([r.network, r.broadcast, r.mask]).toEqual([str(net), str(net + size - 1n), str((1n << 32n) - size)])
        if (p <= 30) {
          expect(r.usableHosts).toBe(Number(size) - 2)
          expect([r.firstHost, r.lastHost]).toEqual([str(net + 1n), str(net + size - 2n)])
        }
      }
    }
  })
  it('challenge value: 172.16.5.77/26 -> broadcast 172.16.5.127', () => {
    expect(subnetInfo('172.16.5.77', 26).broadcast).toBe('172.16.5.127')
  })
})

describe('clampOctet', () => {
  it('yields an integer 0..255 for empty, fractional and extreme input', () => {
    expect(clampOctet('')).toBe(0)
    expect(clampOctet('abc')).toBe(0)
    expect(clampOctet('1.5')).toBe(1) // früher 1.5 -> "192.168.1.5.37" (fünf Oktette)
    expect(clampOctet('-3')).toBe(0)
    expect(clampOctet('999')).toBe(255)
    expect(clampOctet('1e2')).toBe(100)
    expect(clampOctet(77)).toBe(77)
  })
})
