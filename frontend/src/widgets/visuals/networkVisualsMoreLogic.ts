export const vlanHops = [
  { from: 'PC', to: 'Switch A', link: 'Access', action: { de: 'Beim Eingang VLAN 20 zuordnen', en: 'Assign VLAN 20 on ingress' }, tagged: false },
  { from: 'Switch A', to: 'Switch B', link: 'Trunk', action: { de: '802.1Q-Tag VLAN 20 hinzufügen', en: 'Add 802.1Q tag for VLAN 20' }, tagged: true },
  { from: 'Switch B', to: 'Server', link: 'Access', action: { de: '802.1Q-Tag entfernen', en: 'Remove the 802.1Q tag' }, tagged: false },
]

export const arpSteps = {
  de: ['ARP-Request: Wer hat 192.168.10.1?', 'Request als Broadcast an ff:ff:ff:ff:ff:ff', 'ARP-Reply als Unicast an die Client-MAC', 'Zuordnung im ARP-Cache gespeichert'],
  en: ['ARP request: Who has 192.168.10.1?', 'Request broadcast to ff:ff:ff:ff:ff:ff', 'ARP reply unicast to the client MAC', 'Mapping stored in the ARP cache'],
} as const

export type Route = { prefix: string; via: string }
export const routeOptions: Route[] = [
  { prefix: '10.20.30.0/24', via: 'LAN 30' },
  { prefix: '10.20.0.0/16', via: 'Core' },
  { prefix: '0.0.0.0/0', via: 'WAN' },
]
function ipv4Number(ip: string) { return ip.split('.').reduce((value, octet) => (value << 8) + Number(octet), 0) >>> 0 }
export function routeMatches(ip: string, prefix: string) {
  const [network, lengthText] = prefix.split('/'); const length = Number(lengthText)
  const mask = length === 0 ? 0 : (0xffffffff << (32 - length)) >>> 0
  return (ipv4Number(ip) & mask) >>> 0 === (ipv4Number(network) & mask) >>> 0
}
export function matchingRoutes(ip: string) { return routeOptions.filter(route => routeMatches(ip, route.prefix)) }
export function matchingRoute(ip: string) { return matchingRoutes(ip).sort((a, b) => Number(b.prefix.split('/')[1]) - Number(a.prefix.split('/')[1]))[0].prefix }

export function translatedPort(sourcePort: number) { return 40000 + sourcePort % 1000 }
export function natJourney(sourcePort: number) {
  const publicPort = translatedPort(sourcePort)
  return [
    `192.168.10.37:${sourcePort} → 203.0.113.11:443`,
    `198.51.100.8:${publicPort} → 203.0.113.11:443`,
    `203.0.113.11:443 → 198.51.100.8:${publicPort}`,
    `203.0.113.11:443 → 192.168.10.37:${sourcePort}`,
  ]
}

export type LeasePhase = 'bound' | 'renew' | 'rebind' | 'expired'
export function leasePhase(percent: number, serverReachable: boolean): LeasePhase {
  if (percent < 50) return 'bound'
  if (percent < 87.5) return serverReachable ? 'bound' : 'renew'
  if (percent < 100) return serverReachable ? 'bound' : 'rebind'
  return serverReachable ? 'bound' : 'expired'
}

export const tcpPackets = [
  { packet: 'SYN', from: 'Client', to: 'Server', client: 'SYN-SENT', server: 'LISTEN' },
  { packet: 'SYN-ACK', from: 'Server', to: 'Client', client: 'SYN-SENT', server: 'SYN-RECEIVED' },
  { packet: 'ACK', from: 'Client', to: 'Server', client: 'ESTABLISHED', server: 'ESTABLISHED' },
  { packet: 'DATA / ACK', from: 'Client', to: 'Server', client: 'ESTABLISHED', server: 'ESTABLISHED' },
  { packet: 'FIN', from: 'Client', to: 'Server', client: 'FIN-WAIT-1', server: 'ESTABLISHED' },
  { packet: 'ACK', from: 'Server', to: 'Client', client: 'FIN-WAIT-2', server: 'CLOSE-WAIT' },
  { packet: 'FIN', from: 'Server', to: 'Client', client: 'FIN-WAIT-2', server: 'LAST-ACK' },
  { packet: 'ACK', from: 'Client', to: 'Server', client: 'TIME-WAIT', server: 'CLOSED' },
] as const

export const ipv6Stages = {
  de: ['Link-Local-Adresse bilden (fe80::/64)', 'Link-Local-Adresse ist tentative', 'DAD: Neighbor Solicitation für die tentative Link-Local-Adresse', 'Router Solicitation von der Link-Local-Adresse', 'Router Advertisement: Präfix 2001:db8:20::/64', 'Globale SLAAC-Adresse bilden – Status tentative', 'DAD: Neighbor Solicitation für die tentative globale Adresse', 'Globale SLAAC-Adresse ist preferred'],
  en: ['Form a link-local address (fe80::/64)', 'Link-local address is tentative', 'DAD: Neighbor Solicitation for the tentative link-local address', 'Router Solicitation from the link-local address', 'Router Advertisement: prefix 2001:db8:20::/64', 'Form global SLAAC address – status tentative', 'DAD: Neighbor Solicitation for the tentative global address', 'Global SLAAC address is preferred'],
} as const
export function slaacAddress(prefix: string, interfaceId: string) { return `${prefix.replace(/::$/, '')}::${interfaceId.replace(/^:/, '')}` }
