// @vitest-environment jsdom
import { describe, expect, it } from 'vitest'
import { base64UrlToBuffer, bufferToBase64Url } from './passkey'

function bytes(...values: number[]): Uint8Array<ArrayBuffer> {
  return new Uint8Array(values)
}

describe('passkey — Base64url ⇄ ArrayBuffer', () => {
  it('kodiert und dekodiert einen Rundlauf verlustfrei (beliebige Bytes)', () => {
    const original = bytes(0, 1, 2, 253, 254, 255, 16, 32, 48, 64, 128, 200)
    const encoded = bufferToBase64Url(original.buffer)
    const decoded = new Uint8Array(base64UrlToBuffer(encoded))
    expect([...decoded]).toEqual([...original])
  })

  it('erzeugt kein "+" oder "/" und kein Padding ("=") — Base64url statt Standard-Base64', () => {
    // Diese drei Byte-Werte ergeben in Standard-Base64 zuverlässig '+' und '/'
    // (0xfb -> '+', 0xff -> '/'), Base64url muss sie stattdessen als '-'/'_' schreiben.
    const original = bytes(0xfb, 0xff, 0xfb, 0xff, 0xfb, 0xff)
    const encoded = bufferToBase64Url(original.buffer)
    expect(encoded).not.toMatch(/[+/=]/)
    expect(encoded).toMatch(/[-_]/)
    expect(new Uint8Array(base64UrlToBuffer(encoded))).toEqual(original)
  })

  it('rundet Längen korrekt, die in Standard-Base64 Auffüllzeichen brauchen würden (1, 2 und 3 Bytes Rest)', () => {
    // Standard-Base64 füllt Reste von 1 bzw. 2 Bytes mit '==' bzw. '=' auf,
    // Base64url lässt das Padding komplett weg — muss beim Dekodieren wieder
    // korrekt ergänzt werden.
    for (const length of [1, 2, 3, 4, 5, 6, 7]) {
      const original = bytes(...Array.from({ length }, (_, i) => (i * 37 + 11) % 256))
      const encoded = bufferToBase64Url(original.buffer)
      expect(encoded).not.toMatch(/=/)
      const decoded = new Uint8Array(base64UrlToBuffer(encoded))
      expect([...decoded]).toEqual([...original])
    }
  })

  it('dekodiert leere Eingaben zu leeren Puffern', () => {
    expect(bufferToBase64Url(new ArrayBuffer(0))).toBe('')
    expect(base64UrlToBuffer('').byteLength).toBe(0)
  })
})
