import { describe, it, expect } from 'vitest'
import { attackerView, encapsulate, decapsulate, scenarioFor, SCENARIO, TUNNEL_OVERHEAD_BYTES, type Packet } from './vpn'

const inner: Packet = { src: '192.168.10.5', dst: '10.20.0.9', payload: 'Gehaltsliste' }

describe('encapsulate', () => {
  it('äußerer Header trägt die Gateway-Adressen', () => {
    const t = encapsulate(inner, '203.0.113.1', '198.51.100.1')
    expect(t.outerSrc).toBe('203.0.113.1')
    expect(t.outerDst).toBe('198.51.100.1')
  })

  it('Nutzlast ist im Tunnel nicht lesbar', () => {
    const t = encapsulate(inner, '203.0.113.1', '198.51.100.1')
    expect(t.cipher).not.toContain('Gehaltsliste')
    expect(t.cipher).not.toContain('192.168.10.5')
  })

  it('am Ziel wird das Originalpaket wiederhergestellt', () => {
    const t = encapsulate(inner, '203.0.113.1', '198.51.100.1')
    expect(decapsulate(t)).toEqual(inner)
  })
})

describe('attackerView', () => {
  const t = encapsulate(inner, '203.0.113.1', '198.51.100.1')

  it('zeigt ohne VPN Klartext-Adressen und lesbaren Inhalt', () => {
    const view = attackerView(inner, t, false)
    expect(view.contentVisible).toBe(true)
    expect(view.contentLine).toBe('Gehaltsliste')
    expect(view.addressLine).toBe('192.168.10.5 → 10.20.0.9')
  })

  it('zeigt mit VPN nur Gateway-zu-Gateway und einen verschlüsselten Block', () => {
    const view = attackerView(inner, t, true)
    expect(view.contentVisible).toBe(false)
    expect(view.addressLine).toBe('203.0.113.1 → 198.51.100.1')
    expect(view.contentLine).not.toContain('Gehaltsliste')
    expect(view.contentLine).not.toContain('192.168.10.5')
  })

  it('behält Metadaten (Größe, Zeitpunkt) auch mit VPN sichtbar', () => {
    const view = attackerView(inner, t, true, 812, '14:32:07')
    expect(view.metadataVisible.join(' · ')).toContain('Bytes')
    expect(view.metadataVisible).toContain('14:32:07')
  })

  it('mit VPN ist das Paket um den Tunnel-Overhead größer, als Größenordnung gekennzeichnet (de/en)', () => {
    expect(TUNNEL_OVERHEAD_BYTES).toBeGreaterThanOrEqual(60)
    expect(TUNNEL_OVERHEAD_BYTES).toBeLessThanOrEqual(80)
    expect(attackerView(inner, t, false, 812).metadataVisible).toContain('812 Bytes')
    expect(attackerView(inner, t, false, 812, '14:32:07', 'en').metadataVisible).toContain('812 bytes')
    const de = attackerView(inner, t, true, 812).metadataVisible[1]
    const en = attackerView(inner, t, true, 812, '14:32:07', 'en').metadataVisible[1]
    expect(de).toBe(`ca. ${812 + TUNNEL_OVERHEAD_BYTES} Bytes (812 + ca. ${TUNNEL_OVERHEAD_BYTES} Tunnel-Overhead, Größenordnung)`)
    expect(en).toBe(`approx. ${812 + TUNNEL_OVERHEAD_BYTES} bytes (812 + approx. ${TUNNEL_OVERHEAD_BYTES} tunnel overhead, order of magnitude)`)
  })
})

describe('SCENARIO (Remote-Access)', () => {
  // RFC 5737: 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24 · RFC 1918: 10/8, 172.16/12, 192.168/16
  const doc = (ip: string) => /^(192\.0\.2|198\.51\.100|203\.0\.113)\.\d+$/.test(ip)
  const priv = (ip: string) => /^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)/.test(ip)

  it('zeigt außen nur öffentliche Dokumentationsadressen, private nur im Tunnel', () => {
    const t = encapsulate(SCENARIO.inner, SCENARIO.clientOuter, SCENARIO.gateway)
    for (const vpnOn of [false, true]) {
      const view = attackerView(SCENARIO.direct, t, vpnOn)
      const [src, dst] = view.addressLine.split(' → ')
      expect(doc(src)).toBe(true)
      expect(doc(dst)).toBe(true)
    }
    expect(priv(SCENARIO.inner.src)).toBe(true)
    expect(priv(SCENARIO.inner.dst)).toBe(true)
  })

  it('der Laptop bleibt mit und ohne VPN derselbe äußere Absender', () => {
    expect(SCENARIO.direct.src).toBe(SCENARIO.clientOuter)
    expect(SCENARIO.direct.dst).not.toBe(SCENARIO.gateway)
  })
})

describe('scenarioFor (Zweisprachigkeit)', () => {
  it('EN zeigt keinen deutschen Dateinamen, Adressen bleiben gleich', () => {
    const en = scenarioFor('en')
    const de = scenarioFor('de')
    expect(de.inner.payload).toBe('Gehaltsliste.xlsx')
    expect(en.inner.payload).toBe('payroll.xlsx')
    expect(en.direct.payload).toBe('payroll.xlsx')
    expect([en.inner.src, en.inner.dst, en.clientOuter, en.gateway]).toEqual([de.inner.src, de.inner.dst, de.clientOuter, de.gateway])
    const view = attackerView(en.direct, encapsulate(en.inner, en.clientOuter, en.gateway), false)
    expect(view.contentLine).toBe('payroll.xlsx')
  })
  it('mit VPN: außen nur Laptop -> Gateway, innere Adressen und Nutzlast nicht im Chiffrat', () => {
    for (const lang of ['de', 'en'] as const) {
      const sc = scenarioFor(lang)
      const t = encapsulate(sc.inner, sc.clientOuter, sc.gateway)
      const view = attackerView(sc.direct, t, true)
      expect(view.addressLine).toBe('198.51.100.23 → 203.0.113.10')
      expect(view.contentLine).not.toContain(sc.inner.payload)
      expect(view.contentLine).not.toContain('10.20')
      expect(view.contentLine).not.toMatch(/[0-9a-z]/i)
    }
  })
})
