import { describe, expect, it } from 'vitest'

import { GLOSSARY, termsForModule } from './glossary'

const NETWORK_MODULES = ['paket', 'switching', 'vlan', 'subnetting', 'arp', 'routing', 'nat', 'dns', 'dhcp', 'ports', 'icmp', 'firewall', 'ipv6', 'wlan', 'vpn', 'troubleshooting', 'wireshark']

const CLAUDE_CODE_MODULES = ['llm-grundlagen', 'agentic-coding', 'installation-setup', 'cli-workflows', 'claude-md', 'skills-commands', 'plugins', 'mcp', 'subagents', 'spec-driven-bmad', 'hooks', 'ci-cd', 'orchestration', 'security-enterprise', 'safe-ai-workflows', 'effective-workflows', 'git-collaboration', 'capstone']

describe('contextual glossary', () => {
  it('offers terms for every shipped module', () => {
    for (const key of NETWORK_MODULES) {
      expect(termsForModule(key).length).toBeGreaterThan(0)
    }
  })

  it('offers terms for every Claude-Code-Workshop module', () => {
    for (const key of CLAUDE_CODE_MODULES) {
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

  it('only maps terms to modules that actually exist', () => {
    const validModules = new Set([...NETWORK_MODULES, ...CLAUDE_CODE_MODULES])
    for (const term of GLOSSARY) {
      for (const moduleKey of term.modules) {
        expect(validModules.has(moduleKey)).toBe(true)
      }
    }
  })

  it('has no duplicate term keys', () => {
    const keys = GLOSSARY.map((term) => term.key)
    expect(new Set(keys).size).toBe(keys.length)
  })
})
