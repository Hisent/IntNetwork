import { describe, it, expect } from 'vitest'
import { isValidPort, patChallengeDone, translate, type NatEntry } from './nat'

const PUB = '203.0.113.10'

describe('translate (PAT)', () => {
  it('verschiedene innere Hosts -> eine öffentliche IP, verschiedene Ports', () => {
    let t: NatEntry[] = []
    const a = translate(t, '192.168.10.5', 5000, PUB)
    t = a.table
    const b = translate(t, '192.168.10.6', 5000, PUB)
    expect(a.entry.insideGlobal).toBe('203.0.113.10:40000')
    expect(b.entry.insideGlobal).toBe('203.0.113.10:40001')
    expect(b.reused).toBe(false)
  })

  it('gleicher Host:Port -> Eintrag wiederverwendet', () => {
    const t = translate([], '192.168.10.5', 5000, PUB).table
    const again = translate(t, '192.168.10.5', 5000, PUB)
    expect(again.reused).toBe(true)
    expect(again.table.length).toBe(1)
  })
})

describe('isValidPort', () => {
  it('akzeptiert nur ganze Zahlen von 1 bis 65535', () => {
    expect(isValidPort(1)).toBe(true)
    expect(isValidPort(65535)).toBe(true)
    expect(isValidPort(0)).toBe(false)
    expect(isValidPort(65536)).toBe(false)
    expect(isValidPort(-80)).toBe(false)
    expect(isValidPort(80.5)).toBe(false)
    expect(isValidPort(NaN)).toBe(false)
  })
})

describe('PAT-Tabelle: Eindeutigkeit und Rückweg', () => {
  it('jede Verbindung bekommt einen eigenen öffentlichen Port — der Rückweg ist eindeutig', () => {
    let t: NatEntry[] = []
    for (const [ip, port] of [['192.168.10.5', 5000], ['192.168.20.8', 5000], ['192.168.20.8', 5001], ['192.168.10.5', 5000]] as const) {
      t = translate(t, ip, port, PUB).table
    }
    expect(t).toHaveLength(3)
    const globals = t.map((e) => e.insideGlobal)
    expect(new Set(globals).size).toBe(3) // keine Port-Kollision
    // Rückweg: öffentlicher Port -> genau ein innerer Host:Port
    expect(t.find((e) => e.insideGlobal === '203.0.113.10:40001')!.insideLocal).toBe('192.168.20.8:5000')
  })
})

describe('patChallengeDone', () => {
  const two = translate(translate([], '192.168.10.5', 5000, PUB).table, '192.168.20.8', 5000, PUB).table
  it('zwei Ports desselben Hosts erfüllen die Aufgabe nicht', () => {
    const sameHost = translate(translate([], '192.168.10.5', 5000, PUB).table, '192.168.10.5', 5001, PUB).table
    expect(sameHost).toHaveLength(2)
    expect(patChallengeDone(sameHost, true)).toBe(false)
  })
  it('zwei Hosts ohne Wiederverwendung reichen nicht, mit Wiederverwendung schon', () => {
    expect(patChallengeDone(two, false)).toBe(false)
    expect(patChallengeDone(two, true)).toBe(true)
    expect(patChallengeDone([], true)).toBe(false)
  })
})
