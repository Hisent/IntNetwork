import { describe, it, expect } from 'vitest'
import { arpResolve, HOSTS } from './arp'

describe('arpResolve', () => {
  it('unbekannte IP -> Broadcast, Besitzer antwortet, Cache lernt', () => {
    const r = arpResolve({}, '192.168.10.11')
    expect(r.broadcast).toBe(true)
    expect(r.repliedBy).toBe('AA:00:00:00:10:11')
    expect(r.table['192.168.10.11']).toBe('AA:00:00:00:10:11')
  })

  it('gecachte IP -> kein Broadcast', () => {
    const r = arpResolve({ '192.168.10.11': 'AA:00:00:00:10:11' }, '192.168.10.11')
    expect(r.broadcast).toBe(false)
    expect(r.repliedBy).toBe('AA:00:00:00:10:11')
  })

  it('IP existiert nicht -> Broadcast ohne Antwort', () => {
    const r = arpResolve({}, '192.168.10.99')
    expect(r.broadcast).toBe(true)
    expect(r.repliedBy).toBeNull()
  })
})

describe('arpResolve — Randfälle', () => {
  it('unbekannte IP: Broadcast ohne Antwort, Cache bleibt unverändert', () => {
    const r = arpResolve({ '192.168.10.11': 'AA:00:00:00:10:11' }, '192.168.10.99')
    expect(r).toEqual({ table: { '192.168.10.11': 'AA:00:00:00:10:11' }, repliedBy: null, broadcast: true })
    // auch die zweite Anfrage flutet wieder — ein Fehlschlag wird nicht gecacht
    expect(arpResolve(r.table, '192.168.10.99').broadcast).toBe(true)
  })
  it('zweite Auflösung derselben IP kommt aus dem Cache; Gateway und Drucker wie im Modul', () => {
    const first = arpResolve({}, '192.168.10.1')
    expect(first).toMatchObject({ repliedBy: 'AA:00:00:00:10:01', broadcast: true })
    expect(arpResolve(first.table, '192.168.10.1')).toMatchObject({ repliedBy: 'AA:00:00:00:10:01', broadcast: false })
    expect(HOSTS.find((h) => h.ip === '192.168.10.12')!.mac).toBe('AA:00:00:00:10:12') // dhcp.py: aa00.0000.1012
    expect(arpResolve({}, '').repliedBy).toBeNull()
  })
})
