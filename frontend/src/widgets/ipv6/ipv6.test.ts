import { describe, it, expect } from 'vitest'
import { expand, compress, classify, isValid } from './ipv6'

describe('expand', () => {
  it('füllt :: zu 8 Gruppen auf', () => {
    expect(expand('fe80::1')).toBe('fe80:0000:0000:0000:0000:0000:0000:0001')
  })
})

describe('compress', () => {
  it('kürzt führende Nullen und längsten Nuller-Lauf', () => {
    expect(compress('2001:0db8:0000:0000:0000:0000:0000:0001')).toBe('2001:db8::1')
  })
  it('ist idempotent auf Kurzform', () => {
    expect(compress('fe80::1')).toBe('fe80::1')
  })
})

describe('classify', () => {
  it('erkennt Adresstypen', () => {
    expect(classify('::1')).toContain('Loopback')
    expect(classify('fe80::abcd')).toContain('Link-Local')
    expect(classify('2001:db8::1')).toContain('Global')
    expect(classify('fd00::1')).toContain('Unique Local')
    expect(classify('febf::1')).toContain('Link-Local')
    expect(classify('ff02::1')).toContain('Multicast')
    expect(classify('::')).toContain('Unspecified')
  })
})

describe('isValid', () => {
  it('akzeptiert gültige und verwirft kaputte Adressen', () => {
    for (const ok of ['::', '::1', 'fe80::1', '2001:db8:0:0:0:0:0:1', '1:2:3:4:5:6:7::']) expect(isValid(ok)).toBe(true)
    for (const bad of ['', '2001::db8::1', '12345::1', '1:2:3', '1:2:3:4:5:6:7:8:9', '1:::2', 'g::1', '1:2:3:4:5:6:7:8::']) expect(isValid(bad)).toBe(false)
  })
})

describe('RFC 5952 — kanonische Kurzform', () => {
  it('kürzt nur den längsten Nuller-Lauf, bei Gleichstand den ersten', () => {
    expect(compress('2001:db8:0:0:1:0:0:1')).toBe('2001:db8::1:0:0:1')
    expect(compress('2001:0:0:1:0:0:0:1')).toBe('2001:0:0:1::1')
    expect(compress('1:0:0:0:2:0:0:3')).toBe('1::2:0:0:3')
  })
  it('ein einzelner Null-Block wird nicht zu „::" (§4.2.2)', () => {
    expect(compress('2001:db8:0:1:1:1:1:1')).toBe('2001:db8:0:1:1:1:1:1')
    expect(compress('1:2:3:4:5:6:7::')).toBe('1:2:3:4:5:6:7:0')
  })
  it('Kleinbuchstaben, führende Nullen weg, Ränder', () => {
    expect(compress('2001:0DB8:00A0::0001')).toBe('2001:db8:a0::1')
    expect(compress('0:0:0:0:0:0:0:0')).toBe('::')
    expect(compress('1:0:0:0:0:0:0:0')).toBe('1::')
    expect(compress('0:0:0:0:0:0:0:1')).toBe('::1')
  })
  it('expand(compress(x)) ist verlustfrei', () => {
    for (const a of ['2001:0db8:0000:0000:00a0:0000:0000:0001', 'fe80:0000:0000:0000:a8bb:ccff:fedd:ee01', '0000:0000:0000:0000:0000:0000:0000:0000'])
      expect(expand(compress(a))).toBe(a)
  })
})

describe('classify — Präfixgrenzen', () => {
  it('fe80::/10, fc00::/7, ff00::/8, 2000::/3 exakt an den Rändern', () => {
    expect(classify('febf:ffff::1')).toContain('Link-Local')
    expect(classify('fec0::1')).toContain('Reserved') // Site-Local, abgekündigt (RFC 3879)
    expect(classify('fc00::1')).toContain('Unique Local')
    expect(classify('fdff::1')).toContain('Unique Local')
    expect(classify('fe00::1')).toContain('Reserved')
    expect(classify('ff00::')).toContain('Multicast')
    expect(classify('2000::')).toContain('Global')
    expect(classify('3fff:ffff::')).toContain('Global')
    expect(classify('4000::1')).toContain('Reserved')
    expect(classify('1::')).toContain('Reserved')
  })
  it('Rest-Kategorie ist zweisprachig', () => {
    expect(classify('4000::1', 'de')).toBe('Reserviert / sonstige')
    expect(classify('4000::1', 'en')).toBe('Reserved / other')
  })
})

describe('IPv4-Schreibweise am Ende (RFC 4291 §2.2)', () => {
  it('::ffff:192.0.2.1 ist gültig und IPv4-mapped', () => {
    expect(isValid('::ffff:192.0.2.1')).toBe(true) // früher: „Keine gültige IPv6-Adresse"
    expect(expand('::ffff:192.0.2.1')).toBe('0000:0000:0000:0000:0000:ffff:c000:0201')
    expect(compress('::FFFF:192.0.2.1')).toBe('::ffff:c000:201')
    expect(classify('::ffff:192.0.2.1')).toContain('IPv4-mapped')
    expect(classify('::ffff:c000:201')).toContain('IPv4-mapped')
  })
  it('ungültige Varianten bleiben ungültig', () => {
    for (const bad of ['::ffff:192.0.2.256', '::ffff:192.0.2', '192.0.2.1', '1:2:3:4:5:6:7:192.0.2.1', '::1.2.3.4.5'])
      expect(isValid(bad)).toBe(false)
  })
})

describe('isValid — weitere Randfälle ohne Absturz', () => {
  it('Leerraum, Großschreibung, Präfix- und Zonen-Schreibweise', () => {
    expect(isValid('  ::1  ')).toBe(true)
    expect(isValid('FE80::1')).toBe(true)
    for (const bad of [':::', ':', '::1:', ':1::', '2001:db8::/32', 'fe80::1%eth0', '::1:2:3:4:5:6:7:8', 'x'.repeat(5000)])
      expect(isValid(bad)).toBe(false)
  })
})
