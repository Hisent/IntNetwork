// Reine, synchron testbare Hilfsfunktionen rund um AEAD-Verschlüsselung.
// Die eigentliche PBKDF2-Schlüsselableitung sowie AES-GCM-Ver-/Entschlüsselung
// laufen über die WebCrypto-API (crypto.subtle) und bleiben in der Komponente,
// da sie asynchron sind und im Unit-Test kein Browser-Mock zur Verfügung steht.

/** Kippt genau ein Bit an der gegebenen Bit-Position (0 = niedrigstwertiges Bit des ersten Bytes).
 *  Gibt immer eine Kopie zurück — das übergebene Array bleibt unverändert. */
export function flipBit(bytes: Uint8Array, index: number): Uint8Array {
  const copy = new Uint8Array(bytes)
  const byteIndex = Math.floor(index / 8)
  const bitIndex = index % 8
  if (byteIndex < 0 || byteIndex >= copy.length) return copy
  copy[byteIndex] = copy[byteIndex] ^ (1 << bitIndex)
  return copy
}

/** Bytes -> Base64 über das native btoa (kein Bibliotheks-Fallback nötig). */
export function toBase64(bytes: Uint8Array): string {
  let binary = ''
  for (const byte of bytes) binary += String.fromCharCode(byte)
  return btoa(binary)
}

/** Base64 -> Bytes über das native atob. */
export function fromBase64(s: string): Uint8Array {
  const binary = atob(s)
  const bytes = new Uint8Array(binary.length)
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i)
  return bytes
}

/** Bytes -> Hex-String (Kleinbuchstaben, zweistellig pro Byte). */
export function bytesToHex(bytes: Uint8Array): string {
  return Array.from(bytes)
    .map((byte) => byte.toString(16).padStart(2, '0'))
    .join('')
}
