import { describe, it, expect } from 'vitest'
import { modPow, publicValue, sharedSecret, bruteForceExponent } from './keyexchange'

describe('modPow', () => {
  it('stimmt mit bekannten Werten überein', () => {
    expect(modPow(5, 3, 23)).toBe(10) // 125 mod 23 = 10
    expect(modPow(4, 13, 497)).toBe(445) // Lehrbuchbeispiel
    expect(modPow(2, 10, 1000)).toBe(24) // 1024 mod 1000
    expect(modPow(7, 0, 13)).toBe(1)
  })

  it('bleibt auch bei großen Zwischenwerten korrekt (kein Overflow)', () => {
    // Ohne laufende Modulo-Reduktion würde base^exp hier weit über
    // Number.MAX_SAFE_INTEGER hinauswachsen.
    expect(modPow(123456, 654321, 1000003)).toBe(
      Number(BigInt(123456) ** BigInt(654321) % BigInt(1000003)),
    )
    expect(modPow(65521, 65521, 65537)).toBe(
      Number(BigInt(65521) ** BigInt(65521) % BigInt(65537)),
    )
  })
})

describe('Diffie-Hellman mit p=23, g=5', () => {
  const p = 23
  const g = 5
  const a = 6
  const b = 15

  it('beide Seiten errechnen dasselbe gemeinsame Geheimnis', () => {
    const A = publicValue(g, a, p)
    const B = publicValue(g, b, p)
    const sA = sharedSecret(B, a, p)
    const sB = sharedSecret(A, b, p)
    expect(sA).toBe(sB)
    expect(sA).toBeGreaterThan(0)
  })

  it('bruteForceExponent findet den geheimen Exponenten bei kleinem p', () => {
    const A = publicValue(g, a, p)
    expect(bruteForceExponent(g, A, p)).toBe(a)
    const B = publicValue(g, b, p)
    expect(bruteForceExponent(g, B, p)).toBe(b)
  })

  it('liefert null, wenn kein Exponent passt', () => {
    expect(bruteForceExponent(g, 999, p)).toBeNull()
  })
})
