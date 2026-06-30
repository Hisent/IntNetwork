export interface Host { port: number; name: string; mac: string }

export const HOSTS: Host[] = [
  { port: 1, name: 'PC-A', mac: 'AA:00:00:00:00:01' },
  { port: 2, name: 'PC-B', mac: 'AA:00:00:00:00:02' },
  { port: 3, name: 'Drucker', mac: 'AA:00:00:00:00:03' },
  { port: 4, name: 'Kamera', mac: 'AA:00:00:00:00:04' },
]

export interface LearnResult {
  table: Record<string, number>
  delivered: number[]
  flooded: boolean
  learnedMac: string
}

export function learnStep(table: Record<string, number>, srcPort: number, dstMac: string): LearnResult {
  const src = HOSTS.find((h) => h.port === srcPort)!
  const next = { ...table, [src.mac]: srcPort }
  const known = next[dstMac]
  if (known !== undefined && known !== srcPort) {
    return { table: next, delivered: [known], flooded: false, learnedMac: src.mac }
  }
  const delivered = HOSTS.map((h) => h.port).filter((p) => p !== srcPort)
  return { table: next, delivered, flooded: true, learnedMac: src.mac }
}
