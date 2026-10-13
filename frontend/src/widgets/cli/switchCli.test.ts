import { describe, it, expect } from 'vitest'
import { clampVlan, runSwitchCommand, trunkTag, type Port } from './switchCli'

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

  it('clampVlan begrenzt auf 1–4094', () => {
    expect(clampVlan(0)).toBe(1)
    expect(clampVlan(-5)).toBe(1)
    expect(clampVlan(20)).toBe(20)
    expect(clampVlan(4095)).toBe(4094)
    expect(clampVlan(99999)).toBe(4094)
    expect(clampVlan(NaN)).toBe(1)
  })

  it('Trunk: Native VLAN ungetaggt, alle anderen VLANs getaggt', () => {
    const trunk: Port = { vlan: 10, mode: 'trunk' }
    expect(trunkTag(trunk, 10)).toBeNull()
    expect(trunkTag(trunk, 20)).toBe(20)
  })

  it('running-config nennt ein Native VLAN ungleich 1', () => {
    expect(runSwitchCommand(PORTS, 'show run')).toContain('switchport trunk native vlan 10')
    const std: Port[] = [{ vlan: 1, mode: 'trunk' }]
    expect(runSwitchCommand(std, 'show run')).not.toContain('native vlan')
  })

  it('MAC-Tabelle: gültige MACs, unabhängig vom VLAN des Ports', () => {
    const mac = (ports: Port[]) => runSwitchCommand(ports, 'show mac address-table').split('\n')[2].split(/\s+/)[1]
    for (const vlan of [1, 10, 100, 4094]) {
      expect(mac([{ vlan, mode: 'access' }])).toMatch(/^[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}$/)
    }
    expect(mac([{ vlan: 10, mode: 'access' }])).toBe(mac([{ vlan: 20, mode: 'access' }]))
  })
  it('IOS-Kurzformen sh/sho und Groß-/Kleinschreibung', () => {
    expect(runSwitchCommand(PORTS, 'sh vlan')).toBe(runSwitchCommand(PORTS, 'show vlan'))
    expect(runSwitchCommand(PORTS, 'SHO  RUN')).toBe(runSwitchCommand(PORTS, 'show running-config'))
    expect(runSwitchCommand(PORTS, 'sh int status')).toContain('Gi0/4     connected     trunk')
    expect(runSwitchCommand(PORTS, 'shvlan')).toContain('% Invalid input')
    expect(runSwitchCommand(PORTS, '   ')).toBe('')
  })
  it('unbekannter Befehl', () => {
    expect(runSwitchCommand(PORTS, 'foobar')).toContain('% Invalid input')
  })
})
