import { describe, it, expect } from 'vitest'
import { encapsulate, decapsulate, type Packet } from './vpn'

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
