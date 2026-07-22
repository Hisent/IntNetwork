import { describe, it, expect } from 'vitest'
import { flipBit, toBase64, fromBase64, bytesToHex } from './aead'

function popcount(bytes: Uint8Array): number {
  let count = 0
  for (const byte of bytes) {
    let x = byte
    while (x) {
      count += x & 1
      x >>= 1
    }
  }
  return count
}

describe('flipBit', () => {
  it('ändert genau ein Bit', () => {
    const original = Uint8Array.from([0x00, 0xff, 0x10])
    const flipped = flipBit(original, 3)
    const diff = flipped.map((byte, i) => byte ^ original[i])
    expect(popcount(diff)).toBe(1)
  })

  it('lässt das Original unangetastet (gibt eine Kopie zurück)', () => {
    const original = Uint8Array.from([0x00, 0xff, 0x10])
    const snapshot = Uint8Array.from(original)
    flipBit(original, 3)
    expect(original).toEqual(snapshot)
  })

  it('rechnet die Bit-Position korrekt in Byte- und Bit-Index um', () => {
    const original = Uint8Array.from([0x00, 0x00])
    // Bit 8 ist das niedrigstwertige Bit des zweiten Bytes.
    const flipped = flipBit(original, 8)
    expect(flipped).toEqual(Uint8Array.from([0x00, 0x01]))
  })
})

describe('Base64-Roundtrip', () => {
  it('encodes and decodes beliebige Bytes verlustfrei', () => {
    const bytes = Uint8Array.from([0, 1, 2, 3, 127, 128, 250, 251, 252, 253, 254, 255])
    expect(fromBase64(toBase64(bytes))).toEqual(bytes)
  })

  it('leere Bytefolge bleibt leer', () => {
    const bytes = new Uint8Array(0)
    expect(fromBase64(toBase64(bytes))).toEqual(bytes)
  })
})

describe('bytesToHex', () => {
  it('formatiert Bytes als zweistelliges Hex', () => {
    expect(bytesToHex(Uint8Array.from([0x00, 0xff, 0x10, 0x0a]))).toBe('00ff100a')
  })
})
