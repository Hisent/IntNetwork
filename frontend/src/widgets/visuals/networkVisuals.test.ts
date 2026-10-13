import { describe, expect, it } from 'vitest'
import { decidingRule, rules, subnetSlices } from './networkVisualsLogic'

describe('network visualizations', () => {
  it('splits a /24 into correctly aligned /26 networks', () => {
    expect(subnetSlices(26)).toEqual([
      { network: '192.168.10.0/26', hosts: 62 },
      { network: '192.168.10.64/26', hosts: 62 },
      { network: '192.168.10.128/26', hosts: 62 },
      { network: '192.168.10.192/26', hosts: 62 },
    ])
  })

  it('uses first-match semantics for firewall rules', () => {
    expect(decidingRule({ source: 'guest', target: 'erp', port: 443 })).toBe(0)
    expect(decidingRule({ source: 'office', target: 'erp', port: 443 })).toBe(1)
    expect(decidingRule({ source: 'guest', target: 'internet', port: 443 })).toBe(2)
    expect(decidingRule({ source: 'office', target: 'internet', port: 23 })).toBe(3)
  })
})

describe('subnetSlices — whole slider range /24–/28', () => {
  it('yields 2^(p-24) aligned networks whose host count matches 2^(32-p) - 2', () => {
    for (let p = 24; p <= 28; p++) {
      const slices = subnetSlices(p)
      const size = 2 ** (32 - p)
      expect(slices).toHaveLength(2 ** (p - 24))
      slices.forEach((s, i) => expect(s).toEqual({ network: `192.168.10.${i * size}/${p}`, hosts: size - 2 }))
    }
    expect(subnetSlices(28).at(-1)).toEqual({ network: '192.168.10.240/28', hosts: 14 })
  })
  it('default deny catches everything no earlier rule matches', () => {
    expect(decidingRule({ source: 'guest', target: 'internet', port: 80 })).toBe(3)
    expect(decidingRule({ source: 'office', target: 'erp', port: 22 })).toBe(3)
    expect(decidingRule({ source: 'guest', target: 'erp', port: 22 })).toBe(0)
  })
})

describe('firewall rule labels', () => {
  it('are bilingual: the German flow shows no English zone names', () => {
    for (const rule of rules) {
      expect(rule.label.de).not.toBe(rule.label.en)
      expect(rule.label.de).not.toMatch(/Guest|Office/)
    }
    expect(new Set(rules.map(rule => rule.label.en)).size).toBe(rules.length)
  })
})
