export interface Packet {
  src: string
  dst: string
  payload: string
}

export interface Tunneled {
  outerSrc: string // öffentliche IP des sendenden VPN-Gateways
  outerDst: string // öffentliche IP des empfangenden VPN-Gateways
  cipher: string // verschlüsselter (unlesbarer) innerer Block
  inner: Packet // was im Tunnel steckt (für die Empfänger-Ansicht)
}

const mask = (s: string) => s.replace(/\S/g, '▓')

/** Kapselt ein internes Paket in einen verschlüsselten Tunnel zwischen zwei Gateways. */
export function encapsulate(inner: Packet, gwSrc: string, gwDst: string): Tunneled {
  const plain = `${inner.src} → ${inner.dst} | ${inner.payload}`
  return { outerSrc: gwSrc, outerDst: gwDst, cipher: mask(plain), inner }
}

/** Am Ziel-Gateway: entschlüsseln, inneres Paket wieder herausholen. */
export function decapsulate(t: Tunneled): Packet {
  return t.inner
}
