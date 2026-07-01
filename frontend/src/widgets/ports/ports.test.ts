import { describe, it, expect } from 'vitest'
import { serviceFor, HANDSHAKE } from './ports'

describe('serviceFor', () => {
  it('bekannter Port -> Dienst', () => {
    expect(serviceFor(443)).toBe('HTTPS')
    expect(serviceFor(22)).toBe('SSH')
  })

  it('unbekannter Port -> Hinweis', () => {
    expect(serviceFor(49152)).toContain('dynamischer Port')
  })
})

describe('HANDSHAKE', () => {
  it('ist der klassische 3-Wege-Handshake', () => {
    expect(HANDSHAKE.map((s) => s.flag)).toEqual(['SYN', 'SYN-ACK', 'ACK'])
  })
})
