export interface Packet {
  src: string
  dst: string
  payload: string
}

export interface Tunneled {
  outerSrc: string // äußere Absender-IP: sendender Tunnel-Endpunkt (Gateway oder VPN-Client)
  outerDst: string // äußere Ziel-IP: öffentliche IP des empfangenden VPN-Gateways
  cipher: string // verschlüsselter (unlesbarer) innerer Block
  inner: Packet // was im Tunnel steckt (für die Empfänger-Ansicht)
}

const mask = (s: string) => s.replace(/\S/g, '▓')

/** Kapselt ein internes Paket in einen verschlüsselten Tunnel zwischen zwei Endpunkten. */
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

/** Remote-Access-Szenario des Widgets: Laptop im Hotel-WLAN -> VPN-Gateway der Zentrale.
 *  Außen (im WLAN/Internet sichtbar) stehen nur Dokumentationsadressen nach RFC 5737,
 *  private RFC-1918-Adressen kommen ausschließlich im Tunnel vor.
 *  ponytail: Das Hotel-WLAN vergibt hier direkt eine öffentliche Adresse; real stünde
 *  dort meist eine private Hotspot-Adresse, die der Hotspot per NAT übersetzt. */
export const SCENARIO = {
  clientOuter: '198.51.100.23', // Laptop im Hotel-WLAN (äußere Adresse)
  gateway: '203.0.113.10', // öffentliche IP des Nordwind-VPN-Gateways
  // im Tunnel: Adresse aus dem VPN-Pool -> Dateiserver der Zentrale
  inner: { src: '10.20.99.5', dst: '10.20.0.9', payload: 'Gehaltsliste.xlsx' } as Packet,
  // ohne VPN: derselbe Inhalt unverschlüsselt an einen öffentlich erreichbaren Server
  direct: { src: '198.51.100.23', dst: '203.0.113.25', payload: 'Gehaltsliste.xlsx' } as Packet,
}

/** Sicht eines Angreifers im offenen WLAN. `plain` ist das Paket, das OHNE VPN über das
 * WLAN ginge (Klartext); mit VPN bleiben nur die Tunnel-Endpunkte als Metadaten und ein
 * verschlüsselter Block. */
export function attackerView(plain: Packet, t: Tunneled, vpnActive: boolean, byteSize = 812, timestamp = '14:32:07'): AttackerView {
  if (!vpnActive) {
    return {
      addressLine: `${plain.src} → ${plain.dst}`,
      contentVisible: true,
      contentLine: plain.payload,
      metadataVisible: [`${plain.src} → ${plain.dst}`, `${byteSize} Bytes`, timestamp],
    }
  }
  return {
    addressLine: `${t.outerSrc} → ${t.outerDst}`,
    contentVisible: false,
    contentLine: t.cipher,
    metadataVisible: [`${t.outerSrc} → ${t.outerDst}`, `${byteSize} Bytes`, timestamp],
  }
}
