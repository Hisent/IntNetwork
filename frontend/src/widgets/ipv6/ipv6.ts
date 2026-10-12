/** Volle 8er-Gruppen-Form, je 4 Hex, kleingeschrieben. */
export function expand(addr: string): string {
  const a = addr.trim().toLowerCase()
  const parts = a.split('::')
  const head = parts[0] ? parts[0].split(':') : []
  const hasGap = parts.length > 1
  const tail = hasGap && parts[1] ? parts[1].split(':') : []
  let groups: string[]
  if (hasGap) {
    const missing = 8 - head.length - tail.length
    groups = [...head, ...Array(Math.max(0, missing)).fill('0'), ...tail]
  } else {
    groups = head
  }
  return groups.map((g) => g.padStart(4, '0')).join(':')
}

/** Kanonische Kurzform: führende Nullen weg, längster Nuller-Lauf → „::". */
export function compress(addr: string): string {
  const groups = expand(addr).split(':').map((g) => g.replace(/^0+/, '') || '0')
  let bestStart = -1
  let bestLen = 0
  let curStart = -1
  let curLen = 0
  groups.forEach((g, i) => {
    if (g === '0') {
      if (curStart < 0) curStart = i
      curLen++
      if (curLen > bestLen) {
        bestLen = curLen
        bestStart = curStart
      }
    } else {
      curStart = -1
      curLen = 0
    }
  })
  if (bestLen < 2) return groups.join(':')
  const before = groups.slice(0, bestStart).join(':')
  const after = groups.slice(bestStart + bestLen).join(':')
  return `${before}::${after}`
}

/** Syntaxprüfung: nur Hex-Gruppen mit 1–4 Ziffern, höchstens ein „::", genau 8 Gruppen. */
export function isValid(addr: string): boolean {
  const a = addr.trim().toLowerCase()
  const parts = a.split('::')
  if (parts.length > 2) return false
  const groups = parts.flatMap((p) => (p ? p.split(':') : []))
  if (!groups.every((g) => /^[0-9a-f]{1,4}$/.test(g))) return false
  return parts.length === 2 ? groups.length <= 7 : groups.length === 8
}

export function classify(addr: string): string {
  const full = expand(addr)
  const first = parseInt(full.slice(0, 4), 16)
  if (full === '0000:0000:0000:0000:0000:0000:0000:0000') return 'Unspecified (::)'
  if (full === '0000:0000:0000:0000:0000:0000:0000:0001') return 'Loopback (::1)'
  if ((first & 0xffc0) === 0xfe80) return 'Link-Local (fe80::/10)'
  if ((first & 0xfe00) === 0xfc00) return 'Unique Local (fc00::/7)'
  if ((first & 0xff00) === 0xff00) return 'Multicast (ff00::/8)'
  if ((first & 0xe000) === 0x2000) return 'Global Unicast (2000::/3)'
  return 'Reserved / other'
}
