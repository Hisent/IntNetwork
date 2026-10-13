import { describe, expect, it } from 'vitest'
import { workshopTheme } from './workshopTheme'

describe('workshopTheme', () => {
  it('maps persisted workshop keys to visual themes', () => {
    expect(workshopTheme('network')).toBe('network')
    expect(workshopTheme('claude-code')).toBe('claude')
    expect(workshopTheme('infoblox')).toBe('infoblox')
    expect(workshopTheme('ansible')).toBe('ansible')
    expect(workshopTheme('pki')).toBe('pki')
    expect(workshopTheme('nac')).toBe('nac')
  })

  it('falls back to network for unknown or missing keys', () => {
    expect(workshopTheme(undefined)).toBe('network')
    expect(workshopTheme(null)).toBe('network')
    expect(workshopTheme('something-unknown')).toBe('network')
  })
})

// Jedes Nicht-Netzwerk-Theme braucht eigene Dunkel-Werte für die Akzentflächen —
// sonst bleiben sie im Dunkelmodus hell (so geschehen beim PKI-Theme).
describe('workshop themes in index.css', () => {
  it('every theme with light accent variables also defines dark ones', async () => {
    const { readFileSync } = await import('node:fs')
    const css = readFileSync(new URL('../index.css', import.meta.url), 'utf8')
    const themes = [...css.matchAll(/^\.workshop-theme--([a-z]+) \{/gm)].map((m) => m[1]).filter((name) => name !== 'network')
    expect(themes).toEqual(expect.arrayContaining(['claude', 'infoblox', 'ansible', 'pki', 'nac']))
    for (const name of themes) {
      const dark = css.match(new RegExp(`\\[data-theme="dark"\\] \\.workshop-theme--${name} \\{([^}]*--workshop-accent-soft[^}]*)\\}`))
      expect(dark, `dark block for ${name}`).not.toBeNull()
      for (const variable of ['--workshop-accent:', '--workshop-accent-soft:', '--workshop-accent-line:', '--workshop-accent-ink:', '--workshop-accent-pale:'])
        expect(dark![1], `${name} ${variable}`).toContain(variable)
    }
  })
})
