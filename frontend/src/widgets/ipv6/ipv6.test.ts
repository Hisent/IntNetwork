import { describe, it, expect } from 'vitest'
import { expand, compress, classify } from './ipv6'

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
  })
})
