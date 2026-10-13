// Reine Logik der Grafiken aus NetworkVisuals.tsx — eigene Datei, damit die
// Komponentendatei nur Komponenten exportiert (Fast Refresh).
export function subnetSlices(prefix: number): { network: string; hosts: number }[] {
  const count = 2 ** (prefix - 24)
  const size = 256 / count
  return Array.from({ length: count }, (_, index) => ({ network: `192.168.10.${index * size}/${prefix}`, hosts: size - 2 }))
}

export type Packet = { source: string; target: string; port: number }
export const rules = [
  { label: { de: 'Gäste → ERP', en: 'Guest → ERP' }, matches: (packet: Packet) => packet.source === 'guest' && packet.target === 'erp', action: 'DENY' },
  { label: { de: 'Büro → ERP HTTPS', en: 'Office → ERP HTTPS' }, matches: (packet: Packet) => packet.source === 'office' && packet.target === 'erp' && packet.port === 443, action: 'ALLOW' },
  { label: { de: 'Gäste → Internet HTTPS', en: 'Guest → Internet HTTPS' }, matches: (packet: Packet) => packet.source === 'guest' && packet.target === 'internet' && packet.port === 443, action: 'ALLOW' },
  { label: { de: 'Alles andere verweigern (Default Deny)', en: 'Default deny' }, matches: () => true, action: 'DENY' },
] as const

export function decidingRule(packet: Packet): number { return rules.findIndex(rule => rule.matches(packet)) }
