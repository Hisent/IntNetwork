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
    expect(out).toContain('S    0.0.0.0/0 [1/0] via 203.0.113.2')
  })

  it('unbekannter Befehl -> Fehlermeldung', () => {
    expect(runRouterCommand(ROUTES, 'foo')).toContain('% Invalid input')
  })
})
