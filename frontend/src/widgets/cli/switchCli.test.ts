import { describe, it, expect } from 'vitest'
import { runSwitchCommand, type Port } from './switchCli'

const PORTS: Port[] = [
  { vlan: 10, mode: 'access' },
  { vlan: 10, mode: 'access' },
  { vlan: 20, mode: 'access' },
  { vlan: 10, mode: 'trunk' },
]

describe('runSwitchCommand', () => {
  it('show vlan listet Access-Ports je VLAN', () => {
    const out = runSwitchCommand(PORTS, 'show vlan')
    expect(out).toContain('10')
    expect(out).toContain('Gi0/1, Gi0/2')
    expect(out).toContain('Gi0/3')
  })

  it('show running-config zeigt access + trunk', () => {
    const out = runSwitchCommand(PORTS, 'show running-config')
    expect(out).toContain('interface Gi0/1')
    expect(out).toContain('switchport access vlan 10')
    expect(out).toContain('switchport mode trunk')
  })

  it('unbekannter Befehl', () => {
    expect(runSwitchCommand(PORTS, 'foobar')).toContain('% Invalid input')
  })
})
