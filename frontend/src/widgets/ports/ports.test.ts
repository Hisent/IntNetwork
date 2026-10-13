import { describe, it, expect } from 'vitest'
import { serviceFor, runPortsCommand, HANDSHAKE, INTRANET_IP } from './ports'

describe('serviceFor', () => {
  it('bekannter Port -> Dienst', () => {
    expect(serviceFor(443)).toBe('HTTPS')
    expect(serviceFor(22)).toBe('SSH')
  })

  it('unbekannter Port -> Hinweis', () => {
    expect(serviceFor(49152)).toContain('dynamischer Port')
    expect(serviceFor(8080)).toContain('registrierter Port')
    expect(serviceFor(123)).toContain('System-Port')
    expect(serviceFor(70000)).toContain('ungültig')
  })
})

describe('HANDSHAKE', () => {
  it('ist der klassische 3-Wege-Handshake', () => {
    expect(HANDSHAKE.map((s) => s.flag)).toEqual(['SYN', 'SYN-ACK', 'ACK'])
  })
})

describe('serviceFor — Bereichsgrenzen nach RFC 6335', () => {
  it('0–1023 System, 1024–49151 registriert, 49152–65535 dynamisch, sonst ungültig', () => {
    expect(serviceFor(1023)).toContain('System-Port')
    expect(serviceFor(1024)).toContain('registrierter Port')
    expect(serviceFor(49151)).toContain('registrierter Port')
    expect(serviceFor(65535)).toContain('dynamischer Port')
    for (const bad of [-1, 65536, 22.5, NaN]) expect(serviceFor(bad)).toContain('ungültig')
    expect(serviceFor(65536, 'en')).toContain('invalid')
  })
})

describe('runPortsCommand (Terminal)', () => {
  it('intranet hat dieselbe Adresse wie im Wireshark-Mitschnitt (web01)', () => {
    expect(INTRANET_IP).toBe('192.168.10.80')
    expect(runPortsCommand('de', 'scan intranet')).toContain('Scanning intranet (192.168.10.80)')
    expect(runPortsCommand('de', 'scan intranet')).toMatch(/22\/tcp  open  SSH[\s\S]*80\/tcp  open  HTTP[\s\S]*443\/tcp  open  HTTPS/)
  })
  it('EN-Ausgabe enthält keinen deutschen Text', () => {
    const en = ['?', 'scan intranet', 'telnet intranet 22', 'telnet intranet 443', 'telnet intranet 53', 'telnet intranet 8080', 'foo']
      .map((c) => runPortsCommand('en', c)).join('\n')
    expect(en).not.toMatch(/[äöüß]|verschlüsselt|Befehl|Merke/i)
    expect(runPortsCommand('en', 'telnet intranet 443')).toContain('TLS handshake')
    expect(runPortsCommand('de', 'telnet intranet 443')).toContain('TLS-Handshake')
  })
  it('geschlossener Port, ungültiger Port, leere und unbekannte Eingabe', () => {
    expect(runPortsCommand('de', 'telnet intranet 8080')).toContain('Connection refused')
    expect(runPortsCommand('de', 'telnet  INTRANET   22')).toContain('SSH-2.0')
    expect(runPortsCommand('de', 'telnet intranet 99999')).toContain('Ungültiger Port')
    expect(runPortsCommand('en', 'telnet intranet 0')).toContain('Invalid port')
    expect(runPortsCommand('de', '   ')).toBe('')
    expect(runPortsCommand('de', 'rm -rf /')).toContain('Unbekannter Befehl')
  })
})
