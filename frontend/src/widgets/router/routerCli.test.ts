import { describe, it, expect } from 'vitest'
import { runRouterCommand } from './routerCli'
import type { Route } from './routing'

const ROUTES: Route[] = [
  { network: '192.168.10.0', prefix: 24, via: null, iface: 'Gi0/0', ip: '192.168.10.1' },
  { network: '0.0.0.0', prefix: 0, via: '203.0.113.2', iface: 'Gi0/2' },
]

describe('runRouterCommand', () => {
  it('show ip route listet connected + static', () => {
    const out = runRouterCommand(ROUTES, 'show ip route')
    expect(out).toContain('C    192.168.10.0/24 is directly connected, Gi0/0')
    expect(out).toContain('S*   0.0.0.0/0 [1/0] via 203.0.113.2')
    expect(out).toContain('Gateway of last resort is 203.0.113.2 to network 0.0.0.0')
  })

  it('statische Route ohne Default bleibt S, Gateway of last resort nicht gesetzt', () => {
    const out = runRouterCommand(
      [{ network: '10.0.0.0', prefix: 8, via: '203.0.113.2', iface: 'Gi0/2' }], 'show ip route')
    expect(out).toContain('S    10.0.0.0/8 [1/0] via 203.0.113.2')
    expect(out).toContain('Gateway of last resort is not set')
  })

  it('IOS-Kurzformen: sh ip route / sh ip int brief / sh run', () => {
    expect(runRouterCommand(ROUTES, 'sh ip route')).toBe(runRouterCommand(ROUTES, 'show ip route'))
    expect(runRouterCommand(ROUTES, 'sh ip int brief')).toContain('Gi0/0      192.168.10.1')
    expect(runRouterCommand(ROUTES, 'sho run')).toContain('ip route 0.0.0.0 0.0.0.0 203.0.113.2')
    expect(runRouterCommand(ROUTES, 'sh run')).toContain(' ip address 192.168.10.1 255.255.255.0')
  })
  it('unbekannter Befehl -> Fehlermeldung', () => {
    expect(runRouterCommand(ROUTES, 'foo')).toContain('% Invalid input')
  })
})
