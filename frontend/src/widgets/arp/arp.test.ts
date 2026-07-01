import { describe, it, expect } from 'vitest'
import { arpResolve } from './arp'

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
