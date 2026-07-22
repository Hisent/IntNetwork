import { describe, it, expect } from 'vitest'
import {
  checkCert,
  validateChain,
  DEMO_NOW,
  HOSTNAME,
  LEAF_VALID,
  LEAF_EXPIRED,
  LEAF_WRONG_NAME,
  LEAF_SELF_SIGNED,
  LEAF_NOT_YET_VALID,
  LEAF_CN_ONLY_LEGACY,
  INTERMEDIATE_VALID,
  ROOT_VALID,
  FOREIGN_INTERMEDIATE,
  ROOT_UNTRUSTED_EXPIRED,
  TRUST_STORE,
} from './certs'

describe('checkCert', () => {
  it('gültiges Zertifikat besteht ohne Probleme', () => {
    const r = checkCert(LEAF_VALID, HOSTNAME, DEMO_NOW)
    expect(r.valid).toBe(true)
    expect(r.problems).toHaveLength(0)
  })

  it('abgelaufenes Zertifikat wird erkannt', () => {
    const r = checkCert(LEAF_EXPIRED, HOSTNAME, DEMO_NOW)
    expect(r.valid).toBe(false)
    expect(r.problems).toContain('expired')
  })

  it('noch nicht gültiges Zertifikat wird erkannt', () => {
    const r = checkCert(LEAF_NOT_YET_VALID, HOSTNAME, DEMO_NOW)
    expect(r.valid).toBe(false)
    expect(r.problems).toContain('not-yet-valid')
  })

  it('selbstsigniertes Zertifikat wird als solches markiert', () => {
    const r = checkCert(LEAF_SELF_SIGNED, HOSTNAME, DEMO_NOW)
    expect(r.valid).toBe(false)
    expect(r.problems).toContain('self-signed')
  })

  it('Hostname-Prüfung trifft über SAN, nicht über CN', () => {
    // CN passt hier zufällig ("www.nordwind-logistik.de"), aber SAN ist leer
    // -> muss trotzdem als hostname-mismatch gelten.
    const r = checkCert(LEAF_CN_ONLY_LEGACY, HOSTNAME, DEMO_NOW)
    expect(r.valid).toBe(false)
    expect(r.problems).toContain('hostname-mismatch')
  })

  it('falscher Name (Zertifikat für alt.*) liefert hostname-mismatch', () => {
    const r = checkCert(LEAF_WRONG_NAME, HOSTNAME, DEMO_NOW)
    expect(r.valid).toBe(false)
    expect(r.problems).toContain('hostname-mismatch')
  })

  it('Wildcard-SAN passt auf die passende Subdomain', () => {
    const wildcard = { ...LEAF_VALID, san: ['*.nordwind-logistik.de'] }
    const r = checkCert(wildcard, 'www.nordwind-logistik.de', DEMO_NOW)
    expect(r.problems).not.toContain('hostname-mismatch')
  })

  it('Wildcard-SAN passt NICHT auf die nackte Domain oder tiefere Subdomains', () => {
    const wildcard = { ...LEAF_VALID, san: ['*.nordwind-logistik.de'] }
    expect(checkCert(wildcard, 'nordwind-logistik.de', DEMO_NOW).problems).toContain('hostname-mismatch')
    expect(checkCert(wildcard, 'a.b.nordwind-logistik.de', DEMO_NOW).problems).toContain('hostname-mismatch')
  })
})

describe('validateChain', () => {
  it('vollständige, gültige Kette wird akzeptiert', () => {
    const r = validateChain([LEAF_VALID, INTERMEDIATE_VALID, ROOT_VALID], TRUST_STORE, DEMO_NOW)
    expect(r.ok).toBe(true)
    expect(r.problem).toBeUndefined()
  })

  it('fehlendes Intermediate liefert incomplete', () => {
    const r = validateChain([LEAF_VALID], TRUST_STORE, DEMO_NOW)
    expect(r.ok).toBe(false)
    expect(r.problem).toBe('incomplete')
  })

  it('fremdes Intermediate liefert issuer-mismatch', () => {
    const r = validateChain([LEAF_VALID, FOREIGN_INTERMEDIATE, ROOT_VALID], TRUST_STORE, DEMO_NOW)
    expect(r.ok).toBe(false)
    expect(r.problem).toBe('issuer-mismatch')
  })

  it('unbekannte Wurzel liefert untrusted-root', () => {
    const r = validateChain([LEAF_VALID, INTERMEDIATE_VALID, ROOT_UNTRUSTED_EXPIRED], TRUST_STORE, DEMO_NOW)
    expect(r.ok).toBe(false)
    expect(r.problem).toBe('untrusted-root')
  })

  it('Wurzel komplett außerhalb des Trust Stores liefert ebenfalls untrusted-root', () => {
    const r = validateChain([LEAF_VALID, INTERMEDIATE_VALID, ROOT_VALID], [], DEMO_NOW)
    expect(r.ok).toBe(false)
    expect(r.problem).toBe('untrusted-root')
  })

  it('abgelaufenes Glied in ansonsten korrekter, vertrauter Kette liefert expired-link', () => {
    const expiredIntermediate = { ...INTERMEDIATE_VALID, notAfter: '2021-01-01T00:00:00Z' }
    const leafForExpiredIntermediate = { ...LEAF_VALID, issuer: expiredIntermediate.subject }
    const r = validateChain([leafForExpiredIntermediate, expiredIntermediate, ROOT_VALID], TRUST_STORE, DEMO_NOW)
    expect(r.ok).toBe(false)
    expect(r.problem).toBe('expired-link')
  })

  it('leere Kette liefert incomplete', () => {
    const r = validateChain([], TRUST_STORE, DEMO_NOW)
    expect(r.ok).toBe(false)
    expect(r.problem).toBe('incomplete')
  })
})
