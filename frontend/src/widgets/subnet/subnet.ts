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

/** ip = "a.b.c.d", prefix 0..32. Assumes valid input (widget clamps). */
export function subnetInfo(ip: string, prefix: number): SubnetInfo {
  const ipNum = ip.split('.').reduce((acc, o) => (acc << 8) + (Number(o) & 255), 0) >>> 0
  const maskNum = prefix === 0 ? 0 : (0xffffffff << (32 - prefix)) >>> 0
  const network = (ipNum & maskNum) >>> 0
  const broadcast = (network | (~maskNum >>> 0)) >>> 0
  const size = 2 ** (32 - prefix)
  const usableHosts = Math.max(0, size - 2)
  // ponytail: /31 and /32 have no usable range; first/last collapse to net/bcast
  const firstHost = usableHosts > 0 ? network + 1 : network
  const lastHost = usableHosts > 0 ? broadcast - 1 : broadcast
  return {
    network: toStr(network),
    broadcast: toStr(broadcast),
    firstHost: toStr(firstHost),
    lastHost: toStr(lastHost),
    mask: toStr(maskNum),
    usableHosts,
  }
}
