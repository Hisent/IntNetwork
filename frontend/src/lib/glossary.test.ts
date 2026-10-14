import { describe, expect, it } from 'vitest'

import { GLOSSARY, termsForCourse, termsForModule } from './glossary'

const NETWORK_MODULES = ['paket', 'switching', 'vlan', 'subnetting', 'arp', 'routing', 'nat', 'dns', 'dhcp', 'ports', 'icmp', 'firewall', 'ipv6', 'wlan', 'vpn', 'troubleshooting', 'wireshark', 'netzwerk-angriffe', 'dynamisches-routing', 'enterprise-wlan', 'redundanz']

const CLAUDE_CODE_MODULES = ['llm-grundlagen', 'agentic-coding', 'installation-setup', 'cli-workflows', 'claude-md', 'skills-commands', 'plugins', 'mcp', 'subagents', 'spec-driven-bmad', 'hooks', 'ci-cd', 'orchestration', 'security-enterprise', 'safe-ai-workflows', 'effective-workflows', 'git-collaboration', 'capstone']

const INFOBLOX_MODULES = ['infoblox-ueberblick', 'grid-architektur', 'ipam-grundlagen', 'dns-zonen-records', 'dns-views-forwarding', 'dns-hochverfuegbarkeit', 'dns-sicherheit-dnssec', 'dns-sicherheit-rpz-threat-defense', 'dhcp-grundlagen', 'dhcp-failover', 'extensible-attributes', 'rollen-berechtigungen', 'wapi-automatisierung', 'reporting-analytics', 'backup-upgrade-betrieb', 'betrieb-troubleshooting-abschluss']

const ANSIBLE_MODULES = ['ansible-grundlagen', 'inventare', 'playbooks-grundlagen', 'module-collections', 'variablen-vorrang', 'fakten-bedingungen', 'schleifen-handler', 'templates-jinja2', 'rollen', 'ansible-vault', 'fehlerbehandlung-idempotenz', 'qualitaet-testen', 'netzwerk-automatisierung', 'automation-platform-ueberblick', 'automation-controller-betrieb']

const PKI_MODULES = ['krypto-grundlagen', 'symmetrische-verschluesselung', 'asymmetrische-verfahren', 'hashfunktionen', 'digitale-signaturen', 'x509-zertifikate', 'pki-architektur', 'zertifikats-lebenszyklus', 'widerruf-und-transparenz', 'tls-handshake', 'tls-konfiguration', 'tls-pruefen', 'zertifikats-fehlersuche', 'interne-pki-automatisierung', 'post-quantum-kryptografie']

const NAC_MODULES = ['nac-grundlagen', 'nac-8021x', 'nac-radius', 'nac-eap', 'nac-mab', 'nac-eap-tls', 'nac-autorisierung', 'nac-coa', 'nac-profiling', 'nac-posture', 'nac-guest', 'nac-deployment', 'nac-resilienz', 'nac-troubleshooting']

const MODULES_BY_COURSE: Record<string, string[]> = {
  network: NETWORK_MODULES,
  'claude-code': CLAUDE_CODE_MODULES,
  infoblox: INFOBLOX_MODULES,
  ansible: ANSIBLE_MODULES,
  pki: PKI_MODULES,
  nac: NAC_MODULES,
}

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

  it.each([
    ['infoblox', INFOBLOX_MODULES],
    ['ansible', ANSIBLE_MODULES],
    ['pki', PKI_MODULES],
    ['nac', NAC_MODULES],
  ])('offers terms for every %s module', (_course, modules) => {
    for (const key of modules) {
      expect(termsForModule(key).length, key).toBeGreaterThan(0)
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
    const validModules = new Set(Object.values(MODULES_BY_COURSE).flat())
    for (const term of GLOSSARY) {
      for (const moduleKey of term.modules) {
        expect(validModules.has(moduleKey), `${term.key} → ${moduleKey}`).toBe(true)
      }
    }
  })

  it('maps every term only to modules of its own course', () => {
    for (const term of GLOSSARY) {
      const own = MODULES_BY_COURSE[term.course]
      expect(own, term.course).toBeDefined()
      for (const moduleKey of term.modules) {
        expect(own.includes(moduleKey), `${term.key} → ${moduleKey}`).toBe(true)
      }
    }
  })

  it('filters the course view by workshop', () => {
    const nac = termsForCourse('nac')
    expect(nac.length).toBeGreaterThan(0)
    expect(nac.every((term) => term.course === 'nac')).toBe(true)
  })

  it('has no duplicate term keys', () => {
    const keys = GLOSSARY.map((term) => term.key)
    expect(new Set(keys).size).toBe(keys.length)
  })
})
