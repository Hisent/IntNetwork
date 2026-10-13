import { describe, it, expect } from 'vitest'
import { learnStep, HOSTS } from './macLearning'

const macA = HOSTS[0].mac
const macB = HOSTS[1].mac

describe('learnStep', () => {
  it('unbekanntes Ziel -> Flooding an alle außer Quelle', () => {
    const r = learnStep({}, 1, macB)
    expect(r.flooded).toBe(true)
    expect(r.delivered).toEqual([2, 3, 4])
    expect(r.table[macA]).toBe(1)
  })

  it('bekanntes Ziel -> Unicast', () => {
    const r = learnStep({ [macA]: 1 }, 2, macA)
    expect(r.flooded).toBe(false)
    expect(r.delivered).toEqual([1])
    expect(r.table[macB]).toBe(2)
  })
})

describe('learnStep — Lernen, Fluten, Unicast', () => {
  const mac = (port: number) => HOSTS.find((h) => h.port === port)!.mac
  it('gelernt wird die QUELL-MAC am Eingangsport, nie das Ziel', () => {
    const r = learnStep({}, 1, mac(2))
    expect(r.table).toEqual({ [mac(1)]: 1 })
    expect(r.flooded).toBe(true)
    expect(r.delivered).toEqual([2, 3, 4]) // alle außer dem Eingangsport
  })
  it('Antwort geht als Unicast zurück, der dritte Port sieht sie nicht', () => {
    const t1 = learnStep({}, 1, mac(2)).table
    const back = learnStep(t1, 2, mac(1))
    expect(back).toMatchObject({ flooded: false, delivered: [1] })
    expect(back.table).toEqual({ [mac(1)]: 1, [mac(2)]: 2 })
    // danach auch die Hinrichtung als Unicast
    expect(learnStep(back.table, 1, mac(2))).toMatchObject({ flooded: false, delivered: [2] })
  })
  it('Broadcast-Ziel ist nie in der Tabelle -> immer Flooding; Eingabetabelle bleibt unverändert', () => {
    const table = { [mac(2)]: 2 }
    const r = learnStep(table, 1, 'FF:FF:FF:FF:FF:FF')
    expect(r.flooded).toBe(true)
    expect(table).toEqual({ [mac(2)]: 2 })
  })
})
