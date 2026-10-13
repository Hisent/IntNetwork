import { describe, it, expect } from 'vitest'
import { resolve } from './dns'

describe('resolve', () => {
  it('bekannter Name -> IP über 3 Stufen', () => {
    const r = resolve('www.nordwind-logistik.de')
    expect(r.ip).toBe('203.0.113.11')
    expect(r.steps).toHaveLength(3)
    expect(r.steps[2].answer.de).toContain('203.0.113.11')
    expect(r.steps[2].answer.en).toContain('203.0.113.11')
  })

  it('Alias (CNAME) -> Zielname und dessen IP', () => {
    const r = resolve('shop.nordwind-logistik.de')
    expect(r.ip).toBe('203.0.113.11')
    expect(r.steps[2].answer.de).toContain('CNAME → www.nordwind-logistik.de')
    expect(r.steps[2].answer.en).toContain('A record: 203.0.113.11')
  })

  it('unbekannter .de-Name -> NXDOMAIN', () => {
    const r = resolve('gibtsnicht.nordwind-logistik.de')
    expect(r.ip).toBeNull()
    expect(r.steps[2].answer.de).toContain('NXDOMAIN')
    expect(r.steps[2].answer.en).toContain('NXDOMAIN')
  })

  it('unbekannte TLD -> keine Auflösung', () => {
    const r = resolve('example.com')
    expect(r.ip).toBeNull()
    expect(r.steps).toHaveLength(1) // kein falscher ".de"-Verweis vom Root
  })

  it('fremde .de-Domain scheitert am TLD-Server, nicht an ns1.nordwind', () => {
    const r = resolve('example.de')
    expect(r.ip).toBeNull()
    expect(r.steps).toHaveLength(2)
  })
})

describe('resolve — Randfälle', () => {
  it('merkt sich den aufgelösten Namen (Ergebniszeile hängt nicht am Eingabefeld)', () => {
    expect(resolve('  WWW.Nordwind-Logistik.de. ').name).toBe('www.nordwind-logistik.de')
    expect(resolve('  WWW.Nordwind-Logistik.de. ').ip).toBe('203.0.113.11')
  })
  it('leere Eingabe: keine Anfrage, keine erfundene TLD „.“', () => {
    for (const blank of ['', '   ', '.']) {
      expect(resolve(blank)).toEqual({ steps: [], ip: null, name: '' })
    }
  })
  it('Zonen-Apex, Mail und ähnlich klingende fremde Domain', () => {
    expect(resolve('nordwind-logistik.de').ip).toBe('203.0.113.10')
    expect(resolve('mail.nordwind-logistik.de').ip).toBe('203.0.113.12')
    // kein Suffix-Treffer ohne Punkt: fremde Domain scheitert am TLD-Server
    expect(resolve('evilnordwind-logistik.de').steps).toHaveLength(2)
    expect(resolve('de').ip).toBeNull()
  })
})
