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
