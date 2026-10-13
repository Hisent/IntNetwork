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

/** Gültiger TCP/UDP-Port: ganze Zahl 1–65535 (Port 0 ist reserviert). */
export function isValidPort(n: number): boolean {
  return Number.isInteger(n) && n >= 1 && n <= 65535
}

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

/** Challenge des Widgets: mindestens zwei VERSCHIEDENE innere Hosts sind übersetzt (zwei Ports
 *  desselben Hosts zählen nicht) und ein bestehender Eintrag wurde danach wiederverwendet. */
export function patChallengeDone(table: NatEntry[], reusedSeen: boolean): boolean {
  const hosts = new Set(table.map((e) => e.insideLocal.split(':')[0]))
  return hosts.size >= 2 && reusedSeen
}
