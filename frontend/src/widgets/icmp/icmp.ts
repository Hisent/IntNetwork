export interface Node {
  name: string
  ip: string
  rttMs: number
}

// Pfad vom Client zum Ziel-Server (letzter Eintrag = Ziel).
export const PATH: Node[] = [
  { name: 'Gateway', ip: '192.168.10.1', rttMs: 1 },
  { name: 'ISP-Edge', ip: '203.0.113.1', rttMs: 9 },
  { name: 'Backbone', ip: '62.10.0.1', rttMs: 21 },
  { name: 'Ziel-Server', ip: '198.51.100.10', rttMs: 28 },
]

export type ProbeStatus = 'exceeded' | 'reply' | 'timeout'

export interface Probe {
  ttl: number
  node: Node | null
  status: ProbeStatus
}

/** Ein Traceroute-Probe mit gegebener TTL. Zwischen-Router antworten mit
 *  „Time Exceeded", das Ziel mit „Echo Reply". */
export function probe(ttl: number): Probe {
  const node = PATH[ttl - 1] ?? null
  if (!node) return { ttl, node: null, status: 'timeout' }
  return { ttl, node, status: ttl === PATH.length ? 'reply' : 'exceeded' }
}
