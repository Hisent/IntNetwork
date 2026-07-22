import { describe, it, expect } from 'vitest'
import { DOT1X_STEPS, finalVlan, isAccessAccepted, isPortAuthorized, type Dot1xStep } from './dot1x'

describe('Reihenfolge', () => {
  it('beginnt mit EAPOL-Start', () => {
    expect(DOT1X_STEPS[0].name).toBe('EAPOL-Start')
    expect(DOT1X_STEPS[0].from).toBe('supplicant')
    expect(DOT1X_STEPS[0].to).toBe('authenticator')
  })

  it('Access-Accept kommt vor EAP-Success', () => {
    const acceptIdx = DOT1X_STEPS.findIndex((s) => s.name === 'RADIUS Access-Accept')
    const successIdx = DOT1X_STEPS.findIndex((s) => s.name === 'EAP-Success')
    expect(acceptIdx).toBeGreaterThanOrEqual(0)
    expect(successIdx).toBeGreaterThanOrEqual(0)
    expect(acceptIdx).toBeLessThan(successIdx)
  })

  it('Port authorized ist der letzte Schritt', () => {
    expect(DOT1X_STEPS[DOT1X_STEPS.length - 1].name).toBe('Port authorized')
  })
})

describe('Rollen pro Layer', () => {
  it('EAPOL-Schritte laufen ausschließlich zwischen supplicant und authenticator', () => {
    const eapol = DOT1X_STEPS.filter((s) => s.layer === 'eapol')
    expect(eapol.length).toBeGreaterThan(0)
    for (const step of eapol) {
      expect(['supplicant', 'authenticator']).toContain(step.from)
      expect(['supplicant', 'authenticator']).toContain(step.to)
      expect(step.from).not.toBe(step.to)
    }
  })

  it('RADIUS-Schritte laufen ausschließlich zwischen authenticator und server', () => {
    const radius = DOT1X_STEPS.filter((s) => s.layer === 'radius')
    expect(radius.length).toBeGreaterThan(0)
    for (const step of radius) {
      expect(['authenticator', 'server']).toContain(step.from)
      expect(['authenticator', 'server']).toContain(step.to)
      expect(step.from).not.toBe(step.to)
    }
  })
})

describe('Schritt-Daten Konsistenz', () => {
  it('jeder Schritt hat de- und en-Texte', () => {
    for (const step of DOT1X_STEPS as Dot1xStep[]) {
      expect(step.detail.de.length).toBeGreaterThan(0)
      expect(step.detail.en.length).toBeGreaterThan(0)
    }
  })
})

describe('Port-Status', () => {
  const acceptIdx = DOT1X_STEPS.findIndex((s) => s.name === 'RADIUS Access-Accept')
  const authorizedIdx = DOT1X_STEPS.findIndex((s) => s.name === 'Port authorized')

  it('Port ist vor Access-Accept nicht autorisiert', () => {
    expect(isPortAuthorized(0)).toBe(false)
    expect(isPortAuthorized(acceptIdx)).toBe(false)
  })

  it('Access-Accept ist erst ab dem entsprechenden Schritt erreicht', () => {
    expect(isAccessAccepted(acceptIdx - 1)).toBe(false)
    expect(isAccessAccepted(acceptIdx)).toBe(true)
  })

  it('Port ist erst ab "Port authorized" autorisiert', () => {
    expect(isPortAuthorized(authorizedIdx - 1)).toBe(false)
    expect(isPortAuthorized(authorizedIdx)).toBe(true)
  })

  it('liefert das zugewiesene VLAN', () => {
    expect(finalVlan().length).toBeGreaterThan(0)
  })
})
