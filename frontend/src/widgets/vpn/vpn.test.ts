import { describe, it, expect } from 'vitest'
import { attackerView, encapsulate, decapsulate, type Packet } from './vpn'

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
    expect(view.metadataVisible).toContain('812 Bytes')
    expect(view.metadataVisible).toContain('14:32:07')
  })
})
