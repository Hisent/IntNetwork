import { describe, it, expect } from 'vitest'
import { evaluate, matches, type Rule } from './permissions'

const RULES: Rule[] = [
  { effect: 'deny', tool: 'Bash', glob: 'rm -rf *' },
  { effect: 'deny', tool: 'Read', glob: './.env' },
  { effect: 'ask', tool: 'Bash', glob: 'git push *' },
  { effect: 'allow', tool: 'Read', glob: 'src/*' },
]

describe('permissions', () => {
  it('deny matches a dangerous bash command', () => {
    expect(evaluate(RULES, { tool: 'Bash', arg: 'rm -rf build' })).toBe('deny')
  })

  it('allow matches a whitelisted read', () => {
    expect(evaluate(RULES, { tool: 'Read', arg: 'src/app.ts' })).toBe('allow')
  })

  it('ask matches git push', () => {
    expect(evaluate(RULES, { tool: 'Bash', arg: 'git push origin main' })).toBe('ask')
  })

  it('no match falls back to ask', () => {
    expect(evaluate(RULES, { tool: 'Bash', arg: 'ls -la' })).toBe('ask')
  })

  it('deny overrides allow', () => {
    const rules: Rule[] = [
      { effect: 'allow', tool: 'Bash', glob: '*' },
      { effect: 'deny', tool: 'Bash', glob: 'rm *' },
    ]
    expect(evaluate(rules, { tool: 'Bash', arg: 'rm x' })).toBe('deny')
  })

  it('tool name must match', () => {
    expect(matches({ effect: 'deny', tool: 'Bash', glob: '*' }, { tool: 'Read', arg: 'x' })).toBe(false)
  })
})
