export interface Node {
  name: { de: string; en: string }
  ip: string
  rttMs: number
}

// Pfad vom Client zum Ziel-Server (letzter Eintrag = Ziel). Öffentliche Adressen nur aus den
// Doku-Bereichen nach RFC 5737 (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24).
export const PATH: Node[] = [
  { name: { de: 'Gateway', en: 'Gateway' }, ip: '192.168.10.1', rttMs: 1 },
  { name: { de: 'ISP-Edge', en: 'ISP Edge' }, ip: '203.0.113.2', rttMs: 9 },
  { name: { de: 'Backbone', en: 'Backbone' }, ip: '192.0.2.1', rttMs: 21 },
  { name: { de: 'Ziel-Server', en: 'Destination Server' }, ip: '198.51.100.10', rttMs: 28 },
]

export type ProbeStatus = 'exceeded' | 'reply' | 'timeout'

export interface Probe {
  ttl: number
  node: Node | null
  status: ProbeStatus
}

/** Ein Traceroute-Probe mit gegebener TTL — Vorbild ist Windows-`tracert` (ICMP Echo Request):
 *  Zwischen-Router antworten mit „Time Exceeded", das Ziel mit „Echo Reply". Unix-`traceroute`
 *  sendet standardmäßig UDP, dort antwortet das Ziel mit „Port Unreachable". */
export function probe(ttl: number): Probe {
  const node = PATH[ttl - 1] ?? null
  if (!node) return { ttl, node: null, status: 'timeout' }
  return { ttl, node, status: ttl === PATH.length ? 'reply' : 'exceeded' }
}
