import { describe, it, expect } from 'vitest'
import { evaluate, RULES } from './firewall'

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
