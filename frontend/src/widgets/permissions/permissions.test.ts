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

// Beispiele aus code.claude.com/docs/en/permissions (Stand 2026-10-13).
describe('rule syntax like the docs', () => {
  const bash = (effect: Rule['effect'], glob: string): Rule => ({ effect, tool: 'Bash', glob })
  const call = (arg: string) => ({ tool: 'Bash', arg })

  it('a trailing " *" also matches the bare command, but respects the word boundary', () => {
    const rule = bash('allow', 'npm run *')
    for (const arg of ['npm run build', 'npm run test --watch', 'npm run']) expect(matches(rule, call(arg))).toBe(true)
    expect(matches(rule, call('npm install'))).toBe(false)
    expect(matches(bash('allow', 'ls *'), call('lsof'))).toBe(false)
    expect(matches(bash('allow', 'ls*'), call('lsof'))).toBe(true)
    expect(matches(bash('allow', 'ls:*'), call('ls -la'))).toBe(true)
    expect(matches(bash('allow', 'npm run build'), call('npm run build --watch'))).toBe(false)
  })

  it('an allow rule must match every subcommand, deny and ask match any subcommand', () => {
    expect(evaluate([bash('allow', 'npm run *')], call('npm run test && rm -rf build'))).toBe('ask')
    expect(evaluate([bash('allow', 'npm run *')], call('npm run lint && npm run test'))).toBe('allow')
    expect(evaluate([bash('deny', 'rm -rf *')], call('cd build && rm -rf dist'))).toBe('deny')
    expect(evaluate([bash('ask', 'git clean *')], call('cd /tmp && git clean -f'))).toBe('ask')
  })

  it('Read rules use gitignore syntax: * stays in one segment, ** crosses directories', () => {
    const read = (glob: string, arg: string) => matches({ effect: 'deny', tool: 'Read', glob }, { tool: 'Read', arg })
    expect(read('./secrets/**', 'secrets/prod/key.pem')).toBe(true)
    expect(read('./secrets/**', './secrets/key.pem')).toBe(true)
    expect(read('./secrets/**', 'src/secrets.ts')).toBe(false)
    expect(read('src/*', 'src/app.ts')).toBe(true)
    expect(read('src/*', 'src/lib/util.ts')).toBe(false)
    expect(read('.env', 'config/.env')).toBe(true)
    expect(read('./.env', '.env')).toBe(true)
    expect(read('*.env', 'prod.env')).toBe(true)
    expect(read('src/**/*.ts', 'src/app.ts')).toBe(true)
  })

  it('does not crash on empty or extreme input', () => {
    expect(evaluate(RULES, call(''))).toBe('ask')
    expect(evaluate(RULES, call('&& ;; ||'))).toBe('ask')
    expect(evaluate(RULES, call('x'.repeat(100_000)))).toBe('ask')
    expect(evaluate([bash('allow', '(((*')], call('((('))).toBe('allow') // Regex-Sonderzeichen werden maskiert
  })
})

