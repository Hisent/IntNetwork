// Bitmask (Subnetting) --------------------------------------------------
export function maskFromPrefix(prefix: number): { binaryOctets: string[]; dotted: string; hosts: number } {
  const maskBits = Array.from({ length: 32 }, (_, i) => (i < prefix ? '1' : '0'))
  const binaryOctets = Array.from({ length: 4 }, (_, i) => maskBits.slice(i * 8, i * 8 + 8).join(''))
  const dotted = binaryOctets.map(octet => parseInt(octet, 2)).join('.')
  const hostBits = 32 - prefix
  const hosts = hostBits <= 1 ? 0 : Math.max(0, 2 ** hostBits - 2)
  return { binaryOctets, dotted, hosts }
}

// Broadcast storm (Switching) --------------------------------------------
export function stormFrames(tick: number): number { return tick <= 0 ? 1 : 2 ** tick }
export function stormDisplay(tick: number): string {
  const frames = stormFrames(tick)
  return frames > 1000 ? '>1000' : String(frames)
}
export const STORM_OVERLOAD_TICK = 10

// DHCP relay ---------------------------------------------------------------
export function relaySteps(relayOn: boolean, lang: 'de' | 'en'): string[] {
  if (relayOn) {
    return lang === 'de'
      ? [
          'Client (VLAN 20): DHCPDISCOVER als Broadcast',
          'Router-Interface VLAN 20: Discover kommt an, ip helper-address ist konfiguriert',
          'Router wandelt in Unicast an DHCP-Server (VLAN 10) um, setzt giaddr = VLAN-20-Interface',
          'DHCP-Server erkennt VLAN 20 anhand giaddr, sendet Offer an den Router zurück',
          'Router leitet Offer an den Client in VLAN 20 weiter',
          'Client erhält eine gültige Lease aus dem VLAN-20-Pool',
        ]
      : [
          'Client (VLAN 20): DHCPDISCOVER as broadcast',
          'Router interface VLAN 20: Discover arrives, ip helper-address configured',
          'Router converts to unicast to the DHCP server (VLAN 10), sets giaddr = VLAN 20 interface',
          'DHCP server recognizes VLAN 20 via giaddr, sends the offer back to the router',
          'Router forwards the offer to the client in VLAN 20',
          'Client receives a valid lease from the VLAN 20 pool',
        ]
  }
  return lang === 'de'
    ? [
        'Client (VLAN 20): DHCPDISCOVER als Broadcast',
        'Router-Interface VLAN 20: kein ip helper-address konfiguriert',
        'Broadcast endet an der VLAN-Grenze, der DHCP-Server in VLAN 10 erhält nichts',
        'Client erhält keine Antwort und vergibt sich selbst eine APIPA-Adresse (169.254.x.x)',
      ]
    : [
        'Client (VLAN 20): DHCPDISCOVER as broadcast',
        'Router interface VLAN 20: no ip helper-address configured',
        'Broadcast stops at the VLAN boundary, the DHCP server in VLAN 10 gets nothing',
        'Client gets no reply and self-assigns an APIPA address (169.254.x.x)',
      ]
}

// Ephemeral ports -----------------------------------------------------------
export const EPHEMERAL_PORTS = [49152, 51512, 60333] as const
export function matchResponse(port: number, flows: readonly number[]): number { return flows.indexOf(port) }

// Stateful firewall -----------------------------------------------------
export type StatefulScenario = 'allow-out' | 'deny-in'
export function statefulSteps(scenario: StatefulScenario, lang: 'de' | 'en'): string[] {
  if (scenario === 'allow-out') {
    return lang === 'de'
      ? [
          'Interner Client sendet SYN nach außen: 192.168.10.37:51512 → 203.0.113.11:443',
          'Regel "allow out" greift, das Paket wird durchgelassen',
          'State-Eintrag wird angelegt: 192.168.10.37:51512 ↔ 203.0.113.11:443',
          'Antwort SYN-ACK kommt zurück: 203.0.113.11:443 → 192.168.10.37:51512',
          'State-Eintrag passt bereits, das Paket passiert ohne eigene Regel',
        ]
      : [
          'Internal client sends SYN outbound: 192.168.10.37:51512 → 203.0.113.11:443',
          'Rule "allow out" matches, the packet is let through',
          'A state entry is created: 192.168.10.37:51512 ↔ 203.0.113.11:443',
          'Reply SYN-ACK comes back: 203.0.113.11:443 → 192.168.10.37:51512',
          'The state entry already matches, the packet passes without its own rule',
        ]
  }
  return lang === 'de'
    ? [
        'Externes SYN trifft ein: 203.0.113.55:51512 → 192.168.10.37:3389',
        'Kein passender State-Eintrag vorhanden',
        'Keine "allow in"-Regel für dieses Ziel definiert',
        'Default Deny greift: Paket wird verworfen',
      ]
    : [
        'External SYN arrives: 203.0.113.55:51512 → 192.168.10.37:3389',
        'No matching state entry exists',
        'No "allow in" rule defined for this destination',
        'Default deny applies: the packet is dropped',
      ]
}

export type StateEntry = { flow: string; highlighted: boolean }
export function stateTableAfter(scenario: StatefulScenario, step: number): StateEntry[] {
  if (scenario === 'allow-out' && step >= 2) {
    return [{ flow: '192.168.10.37:51512 ↔ 203.0.113.11:443', highlighted: step >= 3 }]
  }
  return []
}
