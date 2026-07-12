import { describe, expect, it } from 'vitest'
import { decidingRule, subnetSlices } from './NetworkVisuals'

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
