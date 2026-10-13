export interface SubnetInfo {
  network: string
  broadcast: string
  firstHost: string
  lastHost: string
  mask: string
  usableHosts: number
}

const toStr = (n: number) =>
  [(n >>> 24) & 255, (n >>> 16) & 255, (n >>> 8) & 255, n & 255].join('.')

/** Oktett-Eingabe auf eine ganze Zahl 0..255 bringen ("1.5" -> 1, "" -> 0, "999" -> 255). */
export function clampOctet(v: string | number): number {
  return Math.max(0, Math.min(255, Math.trunc(Number(v)) || 0))
}

/** ip = "a.b.c.d", prefix 0..32. Assumes valid input (widget clamps). */
export function subnetInfo(ip: string, prefix: number): SubnetInfo {
  const ipNum = ip.split('.').reduce((acc, o) => (acc << 8) + (Number(o) & 255), 0) >>> 0
  const maskNum = prefix === 0 ? 0 : (0xffffffff << (32 - prefix)) >>> 0
  const network = (ipNum & maskNum) >>> 0
  const broadcast = (network | (~maskNum >>> 0)) >>> 0
  const size = 2 ** (32 - prefix)
  // RFC 3021: ein /31 (Punkt-zu-Punkt) hat weder Netz- noch Broadcast-Adresse, beide
  // Adressen sind nutzbar; ein /32 ist eine einzelne Host-Adresse (Host-Route).
  const pointToPoint = prefix >= 31
  const usableHosts = pointToPoint ? size : size - 2
  const firstHost = pointToPoint ? network : network + 1
  const lastHost = pointToPoint ? broadcast : broadcast - 1
  return {
    network: toStr(network),
    broadcast: toStr(broadcast),
    firstHost: toStr(firstHost),
    lastHost: toStr(lastHost),
    mask: toStr(maskNum),
    usableHosts,
  }
}
