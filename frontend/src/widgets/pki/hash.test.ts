import { describe, it, expect } from 'vitest'
import { toHex, hexDiffPositions, bitDifference } from './hash'

describe('toHex', () => {
  it('wandelt eine bekannte Bytefolge in Hex um', () => {
    const bytes = Uint8Array.from([0x00, 0xff, 0x10, 0xab])
    expect(toHex(bytes.buffer)).toBe('00ff10ab')
  })

  it('leerer Buffer ergibt leeren String', () => {
    expect(toHex(new ArrayBuffer(0))).toBe('')
  })
})

describe('hexDiffPositions', () => {
  it('identische Strings -> keine Abweichung', () => {
    expect(hexDiffPositions('abcd1234', 'abcd1234')).toEqual([])
  })

  it('markiert genau die abweichenden Positionen', () => {
    expect(hexDiffPositions('abcd1234', 'abcd9234')).toEqual([4])
    expect(hexDiffPositions('00000000', 'f0000f00')).toEqual([0, 5])
  })
})

describe('bitDifference', () => {
  it('identische Strings -> 0 Bit Unterschied', () => {
    const r = bitDifference('deadbeef', 'deadbeef')
    expect(r.bits).toBe(0)
    expect(r.total).toBe(32)
    expect(r.percent).toBe(0)
  })

  it('"00" vs "ff" -> 8 Bit Unterschied (alle Bits des Bytes)', () => {
    const r = bitDifference('00', 'ff')
    expect(r.bits).toBe(8)
    expect(r.total).toBe(8)
    expect(r.percent).toBe(100)
  })

  it('berechnet den Prozentsatz korrekt bei Teilabweichung', () => {
    // '0' = 0000, 'f' = 1111 -> beide Nibbles komplett unterschiedlich = 4 Bit von 8
    const r = bitDifference('00', '0f')
    expect(r.bits).toBe(4)
    expect(r.total).toBe(8)
    expect(r.percent).toBe(50)
  })
})
