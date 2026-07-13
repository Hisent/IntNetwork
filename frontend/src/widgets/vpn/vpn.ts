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

export interface AttackerView {
  addressLine: string // was der Angreifer als Quelle/Ziel sieht
  contentVisible: boolean // ob die Nutzlast im Klartext lesbar ist
  contentLine: string // Klartext-Inhalt oder ein anonymisierter Metadaten-Hinweis
  metadataVisible: string[] // Metadaten, die auch mit VPN sichtbar bleiben (Ehrlichkeit)
}

/** Sicht eines Angreifers im offenen WLAN: ohne VPN Klartext, mit VPN nur
 * Gateway-zu-Gateway-Metadaten und ein verschlüsselter Block. */
export function attackerView(inner: Packet, t: Tunneled, vpnActive: boolean, byteSize = 812, timestamp = '14:32:07'): AttackerView {
  if (!vpnActive) {
    return {
      addressLine: `${inner.src} → ${inner.dst}`,
      contentVisible: true,
      contentLine: inner.payload,
      metadataVisible: [`${inner.src} → ${inner.dst}`, `${byteSize} Bytes`, timestamp],
    }
  }
  return {
    addressLine: `${t.outerSrc} → ${t.outerDst}`,
    contentVisible: false,
    contentLine: t.cipher,
    metadataVisible: [`${t.outerSrc} → ${t.outerDst}`, `${byteSize} Bytes`, timestamp],
  }
}
