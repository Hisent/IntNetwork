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

export function classify(addr: string): string {
  const full = expand(addr)
  if (full === '0000:0000:0000:0000:0000:0000:0000:0001') return 'Loopback (::1)'
  if (full.startsWith('fe80')) return 'Link-Local (fe80::/10)'
  if (full.startsWith('ff')) return 'Multicast (ff00::/8)'
  return 'Global Unicast'
}
