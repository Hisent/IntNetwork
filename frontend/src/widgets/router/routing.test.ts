import { describe, it, expect } from 'vitest'
import { routeLookup, type Route } from './routing'

const TABLE: Route[] = [
  { network: '192.168.10.0', prefix: 24, via: null, iface: 'Gi0/0', ip: '192.168.10.1' },
  { network: '192.168.20.0', prefix: 24, via: null, iface: 'Gi0/1', ip: '192.168.20.1' },
  { network: '0.0.0.0', prefix: 0, via: '203.0.113.2', iface: 'Gi0/2' },
]

describe('routeLookup', () => {
  it('Ziel im direkt verbundenen Netz -> connected', () => {
    const r = routeLookup(TABLE, '192.168.10.50')
    expect(r.reason).toBe('connected')
    expect(r.route?.iface).toBe('Gi0/0')
  })

  it('unbekanntes Ziel -> Default-Route via Next-Hop', () => {
    const r = routeLookup(TABLE, '8.8.8.8')
    expect(r.reason).toBe('via')
    expect(r.route?.via).toBe('203.0.113.2')
  })

  it('Longest-Prefix schlägt Default-Route', () => {
    const r = routeLookup(TABLE, '192.168.20.5')
    expect(r.route?.prefix).toBe(24)
    expect(r.route?.iface).toBe('Gi0/1')
  })

  it('leere Tabelle -> none', () => {
    expect(routeLookup([], '1.2.3.4').reason).toBe('none')
  })
})
