// Diffie-Hellman-Schlüsseltausch mit Spielzeugzahlen (p, g klein genug zum
// Mitrechnen). Reine Zahlentheorie — keine Krypto-Library nötig, da die
// gewählten Werte (p < 100) weit unter jeder Overflow-Grenze bleiben.

/** Modulare Exponentiation per Square-and-Multiply — bleibt auch bei großen
 * Zwischenwerten korrekt, weil nach jeder Multiplikation sofort `% mod`
 * angewendet wird (kein Zwischenergebnis wächst über `mod^2` hinaus). */
export function modPow(base: number, exp: number, mod: number): number {
  if (mod === 1) return 0
  let result = 1
  let b = ((base % mod) + mod) % mod
  let e = exp
  while (e > 0) {
    if (e % 2 === 1) result = (result * b) % mod
    e = Math.floor(e / 2)
    b = (b * b) % mod
  }
  return result
}

/** Öffentlicher Wert einer Seite: g^secret mod p. */
export function publicValue(g: number, secret: number, p: number): number {
  return modPow(g, secret, p)
}

/** Gemeinsames Geheimnis aus dem öffentlichen Wert der Gegenseite und dem
 * eigenen geheimen Exponenten: otherPublic^ownSecret mod p. */
export function sharedSecret(otherPublic: number, ownSecret: number, p: number): number {
  return modPow(otherPublic, ownSecret, p)
}

/** Was ein Angreifer bei diesen winzigen Spielzeugzahlen tun kann: alle
 * möglichen Exponenten 1..p-2 durchprobieren, bis g^a mod p den beobachteten
 * öffentlichen Wert ergibt. Bei realen Gruppengrößen (2048 Bit oder
 * elliptische Kurven) ist das rechnerisch unmöglich — hier, mit p=23, dauert
 * es Millisekunden. */
export function bruteForceExponent(g: number, publicValue: number, p: number): number | null {
  for (let a = 1; a <= p - 2; a++) {
    if (modPow(g, a, p) === publicValue) return a
  }
  return null
}
