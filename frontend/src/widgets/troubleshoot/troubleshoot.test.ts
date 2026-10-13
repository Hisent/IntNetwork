import { describe, it, expect } from 'vitest'
import { SCENARIOS, canDiagnose, outputFor, MIN_EVIDENCE } from './troubleshoot'

describe('canDiagnose', () => {
  it('locks the diagnosis until enough evidence is gathered', () => {
    expect(canDiagnose(0)).toBe(false)
    expect(canDiagnose(MIN_EVIDENCE - 1)).toBe(false)
    expect(canDiagnose(MIN_EVIDENCE)).toBe(true)
  })
})

describe('outputFor', () => {
  it('returns the localized output of a known command', () => {
    const s = SCENARIOS[0]
    expect(outputFor(s, 'ipconfig', 'de')).toContain('169.254.83.12')
    expect(outputFor(s, 'ipconfig', 'en')).toContain('169.254.83.12')
  })

  it('returns empty string for unknown commands', () => {
    expect(outputFor(SCENARIOS[0], 'format c:', 'de')).toBe('')
  })
})

describe('SCENARIOS data consistency', () => {
  it('has unique ids', () => {
    const ids = SCENARIOS.map((s) => s.id)
    expect(new Set(ids).size).toBe(ids.length)
  })

  it.each(SCENARIOS.map((s) => [s.id, s] as const))('%s is well-formed', (_id, s) => {
    expect(s.commands.length).toBeGreaterThanOrEqual(MIN_EVIDENCE)
    // Befehle je Szenario eindeutig
    expect(new Set(s.commands.map((c) => c.cmd)).size).toBe(s.commands.length)
    // beide Sprachen überall vorhanden
    for (const c of s.commands) {
      expect(c.output.de.length).toBeGreaterThan(0)
      expect(c.output.en.length).toBeGreaterThan(0)
    }
    expect(s.diagnoses.de.length).toBe(s.diagnoses.en.length)
    expect(s.correct).toBeGreaterThanOrEqual(0)
    expect(s.correct).toBeLessThan(s.diagnoses.de.length)
    expect(s.explanation.de.length).toBeGreaterThan(0)
    expect(s.explanation.en.length).toBeGreaterThan(0)
  })
})

describe('SCENARIOS — Symptom, Ausgaben und Diagnose passen zusammen', () => {
  const byId = (id: string) => SCENARIOS.find((s) => s.id === id)!
  it('Lager: APIPA ohne Gateway -> DHCP; jeder Ping scheitert schon beim Senden', () => {
    const s = byId('lager')
    expect(outputFor(s, 'ipconfig', 'de')).toMatch(/169\.254\.\d+\.\d+[\s\S]*255\.255\.0\.0/)
    expect(s.diagnoses.de[s.correct]).toContain('DHCP')
    expect(s.diagnoses.en[s.correct]).toContain('DHCP')
    for (const c of s.commands.filter((c) => c.cmd.startsWith('ping'))) expect(c.output.en).toContain('General failure')
  })
  it('DNS: IP-Pings klappen, nur nslookup scheitert am konfigurierten Server', () => {
    const s = byId('dns')
    const dnsServer = outputFor(s, 'ipconfig', 'en').match(/DNS server[ .]*: ([\d.]+)/)![1]
    expect(dnsServer).toBe('192.168.10.53')
    expect(outputFor(s, 'nslookup www.nordwind.de', 'en')).toContain(dnsServer)
    for (const c of s.commands.filter((c) => c.cmd.startsWith('ping'))) expect(c.output.en).toContain('0 lost')
    // gepingtes Gateway = Gateway aus ipconfig
    expect(s.commands.some((c) => c.cmd === 'ping 192.168.20.1')).toBe(true)
    expect(s.diagnoses.en[s.correct]).toContain('DNS')
  })
  it('VLAN: Adresse und Gateway im selben /24; Drucker liegt im Büro-Netz wie im Modultext', () => {
    const s = byId('vlan')
    const out = outputFor(s, 'ipconfig', 'de')
    const [ip, gw] = [out.match(/IPv4-Adresse[ .]*: ([\d.]+)/)![1], out.match(/Standardgateway[ .]*: ([\d.]+)/)![1]]
    expect(ip.split('.').slice(0, 3)).toEqual(gw.split('.').slice(0, 3))
    expect(s.commands.some((c) => c.cmd === `ping ${gw}`)).toBe(true)
    expect(s.commands.map((c) => c.cmd)).toContain('ping 192.168.20.60') // Frau Bergs Drucker (troubleshooting.py)
    expect(s.commands.map((c) => c.cmd)).not.toContain('ping 192.168.10.60')
    expect(s.diagnoses.de[s.correct]).toContain('VLAN')
  })
})
