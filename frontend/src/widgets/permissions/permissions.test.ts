import { describe, it, expect } from 'vitest'
import { evaluate, explain, matches, type Rule } from './permissions'

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

  it('no match: a state-changing bash command falls back to ask', () => {
    expect(explain(RULES, { tool: 'Bash', arg: 'npm install' })).toEqual({ effect: 'ask', reason: 'default' })
    expect(evaluate(RULES, { tool: 'Edit', arg: 'src/app.ts' })).toBe('ask')
  })

  it('no match: read-only bash and reads in the working directory need no prompt', () => {
    expect(explain(RULES, { tool: 'Bash', arg: 'ls -la' })).toEqual({ effect: 'allow', reason: 'readonly' })
    expect(explain(RULES, { tool: 'Read', arg: 'README.md' })).toEqual({ effect: 'allow', reason: 'readonly' })
  })

  it('no match: redirects, chained commands and reads outside the working directory still ask', () => {
    expect(evaluate(RULES, { tool: 'Bash', arg: 'ls > out.txt' })).toBe('ask')
    expect(evaluate(RULES, { tool: 'Bash', arg: 'cat a && rm a' })).toBe('ask')
    expect(evaluate(RULES, { tool: 'Read', arg: '/etc/passwd' })).toBe('ask')
    expect(evaluate(RULES, { tool: 'Read', arg: '../other/secret.txt' })).toBe('ask')
  })

  it('a rule beats the built-in read-only behaviour', () => {
    expect(explain(RULES, { tool: 'Read', arg: './.env' })).toEqual({ effect: 'deny', reason: 'rule' })
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
