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

  it('Grenzen des /30-Transfernetzes: .0–.3 connected, .4 schon Default-Route', () => {
    const t: Route[] = [...TABLE, { network: '203.0.113.0', prefix: 30, via: null, iface: 'Gi0/2', ip: '203.0.113.1' }]
    expect(routeLookup(t, '203.0.113.2').reason).toBe('connected')
    expect(routeLookup(t, '203.0.113.3').route?.prefix).toBe(30)
    expect(routeLookup(t, '203.0.113.4').route?.prefix).toBe(0)
    expect(routeLookup(t, '192.168.10.255').route?.iface).toBe('Gi0/0')
    expect(routeLookup(t, '192.168.11.0').route?.prefix).toBe(0)
  })
  it('Host-Route /32 schlägt /24; ohne Default-Route -> none', () => {
    const t: Route[] = [
      { network: '10.1.2.0', prefix: 24, via: '10.0.0.2', iface: 'Gi0/0' },
      { network: '10.1.2.7', prefix: 32, via: '10.0.0.3', iface: 'Gi0/1' },
    ]
    expect(routeLookup(t, '10.1.2.7').route?.via).toBe('10.0.0.3')
    expect(routeLookup(t, '10.1.2.8').route?.via).toBe('10.0.0.2')
    expect(routeLookup(t, '10.1.3.1')).toEqual({ route: null, reason: 'none' })
    expect(routeLookup(t, '129.1.2.7').reason).toBe('none') // Bit 31 gesetzt: kein Vorzeichenfehler
  })
  it('Gleichstand (gleiches Präfix): der erste Eintrag bleibt, kein Absturz', () => {
    const t: Route[] = [
      { network: '10.0.0.0', prefix: 8, via: '1.1.1.1', iface: 'a' },
      { network: '10.0.0.0', prefix: 8, via: '2.2.2.2', iface: 'b' },
    ]
    expect(routeLookup(t, '10.9.9.9').route?.iface).toBe('a')
  })
  it('leere Tabelle -> none', () => {
    expect(routeLookup([], '1.2.3.4').reason).toBe('none')
  })
})
