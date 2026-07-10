import type { Lang } from '@/lib/i18n'

export interface GlossaryTerm {
  key: string
  label: Record<Lang, string>
  description: Record<Lang, string>
  modules: string[]
}

export const GLOSSARY: GlossaryTerm[] = [
  { key: 'osi', label: { de: 'OSI-Schichten', en: 'OSI layers' }, description: { de: 'Ein Modell, das Netzwerkkommunikation in sieben Aufgabenbereiche gliedert.', en: 'A model that separates network communication into seven areas of responsibility.' }, modules: ['paket'] },
  { key: 'frame', label: { de: 'Ethernet-Frame', en: 'Ethernet frame' }, description: { de: 'Die Datenform auf Schicht 2 mit Ziel-/Quell-MAC, Typ, Nutzdaten und Fehlerprüfung.', en: 'The Layer-2 data unit with destination/source MAC, type, payload and error check.' }, modules: ['paket', 'switching'] },
  { key: 'mac', label: { de: 'MAC-Adresse', en: 'MAC address' }, description: { de: 'Eine Layer-2-Adresse, mit der Switches Frames innerhalb eines lokalen Netzes weiterleiten.', en: 'A Layer-2 address switches use to forward frames within a local network.' }, modules: ['paket', 'switching', 'arp'] },
  { key: 'vlan', label: { de: 'VLAN', en: 'VLAN' }, description: { de: 'Eine logische Trennung eines Switch-Netzes in eigene Broadcast-Domänen.', en: 'A logical separation of a switched network into distinct broadcast domains.' }, modules: ['vlan', 'wlan', 'troubleshooting'] },
  { key: 'trunk', label: { de: 'Trunk', en: 'Trunk' }, description: { de: 'Eine Verbindung, die mehrere VLANs transportiert, normalerweise mit 802.1Q-Tags.', en: 'A link that carries multiple VLANs, normally using 802.1Q tags.' }, modules: ['vlan', 'paket'] },
  { key: 'cidr', label: { de: 'CIDR-Präfix', en: 'CIDR prefix' }, description: { de: 'Die Schreibweise /24 oder /26: Sie bestimmt, wie viele Bits zum Netz gehören.', en: 'The /24 or /26 notation: it determines how many bits belong to the network.' }, modules: ['subnetting', 'routing', 'troubleshooting'] },
  { key: 'gateway', label: { de: 'Standard-Gateway', en: 'Default gateway' }, description: { de: 'Der Router im eigenen Netz, an den Pakete für fremde Netze gesendet werden.', en: 'The local router that receives packets destined for other networks.' }, modules: ['subnetting', 'arp', 'routing', 'troubleshooting'] },
  { key: 'arp', label: { de: 'ARP', en: 'ARP' }, description: { de: 'IPv4 löst damit im lokalen Netz eine IP-Adresse in eine MAC-Adresse auf.', en: 'IPv4 uses it to resolve a local IP address to a MAC address.' }, modules: ['arp', 'routing', 'troubleshooting'] },
  { key: 'route', label: { de: 'Route', en: 'Route' }, description: { de: 'Ein Eintrag, der festlegt, über welchen Next Hop ein Zielnetz erreichbar ist.', en: 'An entry that determines through which next hop a destination network is reachable.' }, modules: ['routing', 'icmp', 'troubleshooting'] },
  { key: 'nat', label: { de: 'NAT/PAT', en: 'NAT/PAT' }, description: { de: 'Übersetzt private Adressen und bei PAT zusätzlich Ports für Internetverbindungen.', en: 'Translates private addresses and, with PAT, ports for internet connections.' }, modules: ['nat', 'routing', 'troubleshooting'] },
  { key: 'dns', label: { de: 'DNS', en: 'DNS' }, description: { de: 'Löst Namen wie www.example.com in IP-Adressen auf.', en: 'Resolves names such as www.example.com to IP addresses.' }, modules: ['dns', 'ports', 'troubleshooting', 'wireshark'] },
  { key: 'dhcp', label: { de: 'DHCP', en: 'DHCP' }, description: { de: 'Vergibt IP-Konfiguration automatisch und zeitlich begrenzt als Lease.', en: 'Automatically assigns IP configuration for a limited time as a lease.' }, modules: ['dhcp', 'troubleshooting'] },
  { key: 'tcp', label: { de: 'TCP', en: 'TCP' }, description: { de: 'Ein verbindungsorientiertes Transportprotokoll mit zuverlässiger, geordneter Übertragung.', en: 'A connection-oriented transport protocol with reliable, ordered delivery.' }, modules: ['ports', 'wireshark'] },
  { key: 'udp', label: { de: 'UDP', en: 'UDP' }, description: { de: 'Ein verbindungsloses Transportprotokoll ohne Zustell- oder Reihenfolgegarantie.', en: 'A connectionless transport protocol without delivery or ordering guarantees.' }, modules: ['ports', 'dns', 'wireshark'] },
  { key: 'port', label: { de: 'Port', en: 'Port' }, description: { de: 'Eine Nummer, die einen Dienst auf einem Host identifiziert.', en: 'A number that identifies a service on a host.' }, modules: ['ports', 'firewall', 'nat', 'wireshark'] },
  { key: 'icmp', label: { de: 'ICMP', en: 'ICMP' }, description: { de: 'IP-Meldungen für Fehler und Diagnose, etwa Echo Request/Reply bei ping.', en: 'IP messages for errors and diagnostics, such as ping echo requests/replies.' }, modules: ['icmp', 'troubleshooting', 'wireshark'] },
  { key: 'ttl', label: { de: 'TTL', en: 'TTL' }, description: { de: 'Ein Hop-Zähler im IP-Header; bei null wird ein Paket verworfen.', en: 'A hop counter in the IP header; when it reaches zero, a packet is discarded.' }, modules: ['icmp', 'routing'] },
  { key: 'firewall', label: { de: 'Firewall', en: 'Firewall' }, description: { de: 'Prüft Verkehr gegen Regeln, zum Beispiel nach IP, Protokoll und Port.', en: 'Checks traffic against rules, for example by IP, protocol and port.' }, modules: ['firewall', 'vlan', 'vpn', 'troubleshooting'] },
  { key: 'ipv6', label: { de: 'IPv6', en: 'IPv6' }, description: { de: 'Die IP-Version mit 128-Bit-Adressen, Neighbor Discovery und Multicast statt Broadcast.', en: 'The IP version with 128-bit addresses, Neighbor Discovery and multicast instead of broadcast.' }, modules: ['ipv6'] },
  { key: 'wlan', label: { de: 'SSID', en: 'SSID' }, description: { de: 'Der sichtbare Name eines WLANs, mit dem sich Geräte assoziieren.', en: 'The visible Wi-Fi network name that devices associate with.' }, modules: ['wlan'] },
  { key: 'vpn', label: { de: 'VPN', en: 'VPN' }, description: { de: 'Ein verschlüsselter Tunnel durch ein nicht vertrauenswürdiges Netz.', en: 'An encrypted tunnel through an untrusted network.' }, modules: ['vpn', 'troubleshooting'] },
  { key: 'capture', label: { de: 'Paketmitschnitt', en: 'Packet capture' }, description: { de: 'Aufzeichnung von Netzwerkverkehr zur Analyse, nur mit Auftrag oder Erlaubnis.', en: 'A recording of network traffic for analysis, only with authorisation or permission.' }, modules: ['wireshark'] },
]

export function termsForModule(moduleKey: string): GlossaryTerm[] {
  return GLOSSARY.filter((term) => term.modules.includes(moduleKey))
}
