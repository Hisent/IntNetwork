import { describe, it, expect } from 'vitest'
import { evaluate, isValidPort, labSolved, RULES, type Rule } from './firewall'

describe('evaluate (Firewall)', () => {
  it('erlaubter Dienst -> allow durch passende Regel', () => {
    const d = evaluate(RULES, { proto: 'TCP', port: 443 })
    expect(d.action).toBe('allow')
    expect(d.ruleIndex).toBe(0)
  })

  it('explizit verbotener Port -> deny durch Regel', () => {
    const d = evaluate(RULES, { proto: 'TCP', port: 23 })
    expect(d.action).toBe('deny')
    expect(d.ruleIndex).toBe(2)
  })

  it('nichts trifft zu -> Default-Deny', () => {
    const d = evaluate(RULES, { proto: 'TCP', port: 3389 })
    expect(d.action).toBe('deny')
    expect(d.ruleIndex).toBeNull()
  })
})

describe('isValidPort', () => {
  it('akzeptiert nur ganze Zahlen von 1 bis 65535', () => {
    expect(isValidPort(443)).toBe(true)
    expect(isValidPort(65535)).toBe(true)
    expect(isValidPort(0)).toBe(false)
    expect(isValidPort(70000)).toBe(false)
    expect(isValidPort(-1)).toBe(false)
    expect(isValidPort(22.5)).toBe(false)
  })
})

describe('evaluate — Reihenfolge, Protokoll, Wildcards', () => {
  it('First-Match: eine frühe breite allow-Regel macht die spätere deny-Regel wirkungslos', () => {
    const broadFirst: Rule[] = [{ action: 'allow', proto: 'TCP', port: 'any' }, { action: 'deny', proto: 'TCP', port: 23 }]
    expect(evaluate(broadFirst, { proto: 'TCP', port: 23 })).toEqual({ action: 'allow', ruleIndex: 0 })
    expect(evaluate([...broadFirst].reverse(), { proto: 'TCP', port: 23 })).toEqual({ action: 'deny', ruleIndex: 0 })
  })
  it('Protokoll wird mitgeprüft: UDP 443 und TCP 53 treffen keine Regel -> Default-Deny', () => {
    expect(evaluate(RULES, { proto: 'UDP', port: 443 })).toEqual({ action: 'deny', ruleIndex: null })
    expect(evaluate(RULES, { proto: 'TCP', port: 53 })).toEqual({ action: 'deny', ruleIndex: null })
    expect(evaluate(RULES, { proto: 'UDP', port: 53 }).action).toBe('allow')
  })
  it('leeres Regelwerk: alles Default-Deny', () => {
    expect(evaluate([], { proto: 'TCP', port: 443 })).toEqual({ action: 'deny', ruleIndex: null })
  })
})

describe('labSolved (Regel-Baukasten)', () => {
  const https: Rule = { action: 'allow', proto: 'TCP', port: 443 }
  it('die gewollte Lösung gilt — in beliebiger Reihenfolge', () => {
    const dns: Rule = { action: 'allow', proto: 'UDP', port: 53 }
    expect(labSolved([https, dns])).toBe(true)
    expect(labSolved([dns, https])).toBe(true)
  })
  it('zu breite Regeln sind keine Lösung für „genau HTTPS und DNS"', () => {
    expect(labSolved([https, { action: 'allow', proto: 'UDP', port: 'any' }])).toBe(false) // ließ früher alles UDP durch
    expect(labSolved([{ action: 'allow', proto: 'any', port: 'any' }])).toBe(false)
    expect(labSolved([{ action: 'allow', proto: 'TCP', port: 'any' }, { action: 'allow', proto: 'UDP', port: 53 }])).toBe(false)
  })
  it('kein Regelwerk, unvollständig oder mehr als 2 Regeln: nicht gelöst', () => {
    expect(labSolved([])).toBe(false)
    expect(labSolved([https])).toBe(false)
    expect(labSolved([https, { action: 'allow', proto: 'UDP', port: 53 }, { action: 'deny', proto: 'TCP', port: 23 }])).toBe(false)
  })
})
