export interface ArpHost {
  ip: string
  mac: string
  name: string
}

export const HOSTS: ArpHost[] = [
  { ip: '192.168.10.10', mac: 'AA:00:00:00:10:10', name: 'PC-A' },
  { ip: '192.168.10.11', mac: 'AA:00:00:00:10:11', name: 'PC-B' },
  { ip: '192.168.10.12', mac: 'AA:00:00:00:10:12', name: 'Drucker' },
  { ip: '192.168.10.1', mac: 'AA:00:00:00:10:01', name: 'Gateway' },
]

export interface ArpResult {
  table: Record<string, string> // ip -> mac
  repliedBy: string | null // MAC oder null (niemand)
  broadcast: boolean // wurde ein ARP-Request geflutet?
}

/** ARP: gesuchte MAC im Cache? sonst Broadcast „Wer hat IP?", Besitzer antwortet. */
export function arpResolve(table: Record<string, string>, targetIp: string): ArpResult {
  const cached = table[targetIp]
  if (cached) return { table, repliedBy: cached, broadcast: false }
  const owner = HOSTS.find((h) => h.ip === targetIp)
  if (!owner) return { table, repliedBy: null, broadcast: true }
  return { table: { ...table, [targetIp]: owner.mac }, repliedBy: owner.mac, broadcast: true }
}
