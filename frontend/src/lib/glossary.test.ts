import { describe, expect, it } from 'vitest'

import { GLOSSARY, termsForModule } from './glossary'

describe('contextual glossary', () => {
  it('offers terms for every shipped module', () => {
    for (const key of ['paket', 'switching', 'vlan', 'subnetting', 'arp', 'routing', 'nat', 'dns', 'dhcp', 'ports', 'icmp', 'firewall', 'ipv6', 'wlan', 'vpn', 'troubleshooting', 'wireshark']) {
      expect(termsForModule(key).length).toBeGreaterThan(0)
    }
  })

  it('keeps every term bilingual', () => {
    for (const term of GLOSSARY) {
      expect(term.label.de).not.toBe('')
      expect(term.label.en).not.toBe('')
      expect(term.description.de).not.toBe('')
      expect(term.description.en).not.toBe('')
    }
  })
})
