// Reine, synchron testbare Hash-Hilfsfunktionen. Die eigentlichen Digests
// kommen aus der WebCrypto-API (crypto.subtle.digest) und bleiben in der
// Komponente (useEffect), da subtle.digest asynchron ist und im Test kein
// Browser-Mock zur Verfügung steht.

/** Wandelt einen ArrayBuffer (z.B. das Ergebnis von crypto.subtle.digest) in einen Hex-String um. */
export function toHex(buffer: ArrayBuffer): string {
  return Array.from(new Uint8Array(buffer))
    .map((byte) => byte.toString(16).padStart(2, '0'))
    .join('')
}

/** Liefert die Zeichen-Indizes, an denen sich zwei gleich lange Hex-Strings unterscheiden. */
export function hexDiffPositions(a: string, b: string): number[] {
  const len = Math.min(a.length, b.length)
  const positions: number[] = []
  for (let i = 0; i < len; i++) {
    if (a[i] !== b[i]) positions.push(i)
  }
  return positions
}

/** Vergleicht zwei Hex-Digests bitweise — Grundlage für die Anzeige des Lawineneffekts. */
export function bitDifference(a: string, b: string): { bits: number; total: number; percent: number } {
  const len = Math.min(a.length, b.length)
  let bits = 0
  for (let i = 0; i < len; i++) {
    // XOR der beiden Hex-Nibbles, danach gesetzte Bits zählen (4 Bit pro Hex-Zeichen).
    let x = parseInt(a[i], 16) ^ parseInt(b[i], 16)
    while (x) {
      bits += x & 1
      x >>= 1
    }
  }
  const total = len * 4
  const percent = total === 0 ? 0 : (bits / total) * 100
  return { bits, total, percent }
}
