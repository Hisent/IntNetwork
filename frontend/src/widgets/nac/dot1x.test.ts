import { describe, it, expect } from 'vitest'
import {
  DOT1X_PATHS, DOT1X_PATH_IDS, DOT1X_STEPS, finalVlan, isAccessAccepted, isDecided, isPortAuthorized,
  type Dot1xStep,
} from './dot1x'
import { VLAN } from './vlans'

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

  it('liefert das zugewiesene VLAN zweisprachig', () => {
    expect(finalVlan()).toEqual(VLAN.employee)
    expect(finalVlan()?.en).not.toMatch(/Mitarbeiter/)
  })
})

describe('Pfade', () => {
  it('jeder Pfad ist in sich konsistent (Texte, Layer-Rollen, Entscheidung vor dem Ende)', () => {
    for (const id of DOT1X_PATH_IDS) {
      const path = DOT1X_PATHS[id]
      expect(path.label.de.length).toBeGreaterThan(0)
      expect(path.label.en.length).toBeGreaterThan(0)
      expect(path.result.note.de.length).toBeGreaterThan(0)
      expect(path.result.note.en.length).toBeGreaterThan(0)
      expect(path.decisionIndex).toBeGreaterThanOrEqual(0)
      expect(path.decisionIndex).toBeLessThan(path.steps.length)
      for (const step of path.steps) {
        expect(step.detail.de.length).toBeGreaterThan(0)
        expect(step.detail.en.length).toBeGreaterThan(0)
        if (step.layer === 'radius') expect([step.from, step.to].sort()).toEqual(['authenticator', 'server'])
        if (step.layer === 'eapol' || step.layer === 'data') {
          expect([step.from, step.to]).not.toContain('server')
        }
        if (step.layer === 'local') expect(step.from).toBe('authenticator')
      }
    }
  })

  it('EAP-TLS und PEAP enden beide im Mitarbeiter-VLAN, unterscheiden sich aber in der Challenge', () => {
    expect(finalVlan('peap')).toEqual(finalVlan('eap-tls'))
    const challenge = (id: 'eap-tls' | 'peap') =>
      DOT1X_PATHS[id].steps.find((s) => s.name === 'RADIUS Access-Challenge')!.detail.de
    expect(challenge('eap-tls')).not.toBe(challenge('peap'))
  })

  it('Reject: kein Access-Accept, Port bleibt zu, kein VLAN', () => {
    const { steps } = DOT1X_PATHS.reject
    expect(steps.some((s) => s.name === 'RADIUS Access-Accept')).toBe(false)
    expect(steps.some((s) => s.name === 'EAP-Failure')).toBe(true)
    expect(isPortAuthorized(steps.length - 1, 'reject')).toBe(false)
    expect(finalVlan('reject')).toBeNull()
  })

  it('kein Supplicant: MAB erst nach dem Timeout, ohne EAP-Success, im IoT-VLAN', () => {
    const { steps } = DOT1X_PATHS.mab
    const timeout = steps.findIndex((s) => s.layer === 'local')
    const mabRequest = steps.findIndex((s) => s.name === 'RADIUS Access-Request (MAB)')
    expect(timeout).toBeGreaterThanOrEqual(0)
    expect(timeout).toBeLessThan(mabRequest)
    expect(steps.some((s) => s.name === 'EAP-Success')).toBe(false)
    expect(steps.some((s) => s.from === 'supplicant' && s.layer === 'eapol')).toBe(false)
    expect(finalVlan('mab')).toEqual(VLAN.iot)
  })

  it('MAB unbekannt: Reject führt ins Gast-VLAN, Identität gilt als nicht geprüft', () => {
    const path = DOT1X_PATHS['mab-unknown']
    expect(path.steps[path.decisionIndex].name).toBe('RADIUS Access-Reject')
    expect(path.result.vlan).toEqual(VLAN.guest)
    expect(path.result.authenticated).toBe(false)
  })

  it('RADIUS nicht erreichbar: keine Server-Antwort, Critical VLAN ohne Authentifizierung', () => {
    const path = DOT1X_PATHS['radius-down']
    expect(path.steps.some((s) => s.from === 'server')).toBe(false)
    expect(path.result.vlan).toEqual(VLAN.critical)
    expect(path.result.authorized).toBe(true)
    expect(path.result.authenticated).toBe(false)
    expect(isPortAuthorized(path.steps.length - 2, 'radius-down')).toBe(false)
    expect(isPortAuthorized(path.steps.length - 1, 'radius-down')).toBe(true)
  })

  it('isDecided folgt dem decisionIndex des jeweiligen Pfads', () => {
    for (const id of DOT1X_PATH_IDS) {
      const { decisionIndex } = DOT1X_PATHS[id]
      expect(isDecided(decisionIndex - 1, id)).toBe(false)
      expect(isDecided(decisionIndex, id)).toBe(true)
    }
  })
})
