export interface NatEntry {
  insideLocal: string // private ip:port
  insideGlobal: string // öffentliche ip:port (nach Übersetzung)
}

export interface NatResult {
  table: NatEntry[]
  entry: NatEntry
  reused: boolean
}

const BASE_PORT = 40000

/** PAT/Overload: alle inneren Hosts teilen sich eine öffentliche IP,
 *  unterschieden per Quell-Port. */
export function translate(
  table: NatEntry[],
  insideIp: string,
  insidePort: number,
  publicIp: string,
): NatResult {
  const insideLocal = `${insideIp}:${insidePort}`
  const existing = table.find((e) => e.insideLocal === insideLocal)
  if (existing) return { table, entry: existing, reused: true }
  const entry: NatEntry = { insideLocal, insideGlobal: `${publicIp}:${BASE_PORT + table.length}` }
  return { table: [...table, entry], entry, reused: false }
}
