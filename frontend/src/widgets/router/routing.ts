export interface Route {
  network: string
  prefix: number
  via: string | null // null = direkt verbunden (connected)
  iface: string
  ip?: string // gesetzt bei connected: IP des Router-Interfaces
}

export function ipToInt(ip: string): number {
  return ip.split('.').reduce((a, o) => (a << 8) + (Number(o) & 255), 0) >>> 0
}

const maskOf = (prefix: number) =>
  prefix === 0 ? 0 : (0xffffffff << (32 - prefix)) >>> 0

export interface RouteResult {
  route: Route | null
  reason: 'connected' | 'via' | 'none'
}

/** Longest-Prefix-Match über die Routing-Tabelle. */
export function routeLookup(table: Route[], dstIp: string): RouteResult {
  const dst = ipToInt(dstIp)
  let best: Route | null = null
  for (const r of table) {
    const mask = maskOf(r.prefix)
    if (((dst & mask) >>> 0) === ((ipToInt(r.network) & mask) >>> 0)) {
      if (!best || r.prefix > best.prefix) best = r
    }
  }
  if (!best) return { route: null, reason: 'none' }
  return { route: best, reason: best.via === null ? 'connected' : 'via' }
}
