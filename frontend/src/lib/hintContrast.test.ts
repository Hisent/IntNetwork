// Kontrast-Guard für Hinweis-/Zusatztexte der Blöcke (axe „serious“: text-slate-400
// erreichte im Hellmodus nur ~2,4–2,6:1). Ergänzt lightContrast/darkContrast.test.ts:
// die sehen nur bg-/text-Paare auf DEMSELBEN Element — Hinweiszeilen erben ihre Fläche
// aber von der Karte (bg-white) bzw. von der Seite (--wb-canvas).

/// <reference types="node" />
import { describe, expect, it } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { contrastRatioForColors } from './colorContrast'
import { parseColorVars, stripComments } from './contrastScan'

const SRC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const read = (rel: string) => fs.readFileSync(path.resolve(SRC, rel), 'utf8')

const light = parseColorVars(read('../node_modules/tailwindcss/theme.css'))
const dark = parseColorVars(read('index.css'))
const workbench = stripComments(read('components/workbench/workbench.css'))
const canvas = [...workbench.matchAll(/--wb-canvas:\s*([^;]+);/g)].map((m) => m[1].trim())  // [hell, dunkel]
const DARK_CARD = '#16211f'  // [data-theme="dark"] .bg-white in index.css

describe('Hinweistexte der Blöcke (WCAG AA >= 4.5:1)', () => {
  it('Farbquellen wurden gefunden', () => {
    expect(canvas).toHaveLength(2)
    expect(read('index.css')).toContain(`[data-theme="dark"] .bg-white { background-color: ${DARK_CARD}; }`)
  })

  it.each([
    ['Hinweiszeile in einer Karte, hell (text-slate-500 auf bg-white)', light.get('slate-500')!, '#ffffff'],
    ['Hinweiszeile in einer Karte, dunkel', dark.get('slate-500')!, DARK_CARD],
    ['Übungsstand-Zeile auf der Seitenfläche, hell (text-slate-600 auf --wb-canvas)', light.get('slate-600')!, canvas[0]],
    ['Übungsstand-Zeile auf der Seitenfläche, dunkel', dark.get('slate-600')!, canvas[1]],
  ])('%s', (_name, fg, bg) => {
    expect(contrastRatioForColors(fg, bg)).toBeGreaterThanOrEqual(4.5)
  })

  it('text-slate-400 hätte hell nicht gereicht (Anlass dieses Guards)', () => {
    expect(contrastRatioForColors(light.get('slate-400')!, '#ffffff')).toBeLessThan(3)
  })

  // Erlaubt bleibt text-slate-400/-300 nur, wo es keinen lesbaren Text färbt:
  // inaktive (disabled) Optionen, Linien/Rahmen in SVG, der leere Aufgaben-Kreis.
  const ALLOWED = [
    "'border-slate-100 text-slate-400'",            // Blocks.tsx: nicht gewählte Option nach der Antwort (disabled)
    '<g className="text-slate-400">',               // DiagramBlock: Trennlinie (stroke=currentColor)
    "'text-slate-400 opacity-45'",                  // DiagramBlock: abgeblendete Elemente außerhalb des Schritts
    "'border-slate-300 text-slate-400'",            // TerminalBlock: leerer Kreis einer offenen Aufgabe (kein Text)
  ]
  const files = ['components/Blocks.tsx', 'components/TrainerBlocks.tsx', 'components/Quiz.tsx', 'components/PayloadJsonField.tsx',
    ...fs.readdirSync(path.resolve(SRC, 'components/blocks')).filter((f) => f.endsWith('.tsx') && !f.includes('.test.')).map((f) => `components/blocks/${f}`),
    // Widgets, die bereits bereinigt sind; weitere Widgets folgen, sobald ihre text-slate-400-Reste geklärt sind.
    'widgets/capstone/CapstoneWidget.tsx',
    ...fs.readdirSync(path.resolve(SRC, 'widgets/tokenizer')).filter((f) => f.endsWith('.tsx')).map((f) => `widgets/tokenizer/${f}`)]

  it.each(files)('%s: kein text-slate-400/-300 für lesbaren Text', (file) => {
    const hits = read(file).split('\n')
      .filter((line) => /text-slate-[34]00/.test(line) && !ALLOWED.some((ok) => line.includes(ok)))
      .map((line) => line.trim().slice(0, 120))
    expect(hits).toEqual([])
  })
})

// ---------------------------------------------------------------------------
// Schrift auf Akzentflächen ("bg-teal-600 … text-white", "bg-[var(--wb-accent)] text-white").
// light-/darkContrast.test.ts führen diese Paare als Ausnahme, weil sie zusammengesetzte
// Selektoren nicht auflösen — hier werden die tatsächlich wirksamen Regeln nachgerechnet.
// ---------------------------------------------------------------------------
describe('Schrift auf Akzentflächen (WCAG AA >= 4.5:1, alle Lehrgänge, hell und dunkel)', () => {
  const index = stripComments(read('index.css'))
  const rule = (css: string, selector: string) => {
    const at = css.indexOf(selector)
    expect(at, `Regel fehlt: ${selector}`).toBeGreaterThanOrEqual(0)
    return css.slice(css.indexOf('{', at) + 1, css.indexOf('}', at))
  }
  const value = (decls: string, prop: string) => decls.match(new RegExp(`(?:^|[;\\s])${prop}\\s*:\\s*([^;]+)`))![1].trim()
  const themeVars = (theme: string, mode: 'light' | 'dark') => {
    const vars = new Map<string, string>()
    const re = new RegExp(`(\\[data-theme="dark"\\]\\s*)?\\.workshop-theme--${theme}\\s*\\{([^}]*)\\}`, 'g')
    for (const m of index.matchAll(re)) {
      if (mode === 'light' && m[1]) continue  // dunkel erbt die hellen Werte, nicht umgekehrt
      for (const v of m[2].matchAll(/--(workshop-[\w-]+)\s*:\s*([^;]+);/g)) vars.set(v[1], v[2].trim())
    }
    return vars
  }
  const THEMES = ['claude', 'infoblox', 'ansible', 'pki', 'nac']
  const ratio = (fg: string, bg: string) => contrastRatioForColors(fg, bg)!

  it('Netzwerkkurs: weiße Schrift steht auf teal-700 (Hover teal-800) statt auf teal-600 (3,66:1)', () => {
    expect(ratio('#ffffff', light.get('teal-600')!)).toBeLessThan(4.5)  // Anlass
    const fill = value(rule(index, '.bg-teal-600.text-white {'), 'background-color')
    const hover = value(rule(index, '.bg-teal-600.text-white.hover\\:bg-teal-700:hover {'), 'background-color')
    expect(fill).toBe(light.get('teal-700'))
    expect(ratio('#ffffff', fill)).toBeGreaterThanOrEqual(4.5)
    expect(ratio('#ffffff', hover)).toBeGreaterThanOrEqual(4.5)
  })

  it.each(THEMES)('Kursfarbe %s: hell weiße, dunkel dunkle Schrift auf Akzent und Hover', (theme) => {
    const l = themeVars(theme, 'light')
    expect(ratio('#ffffff', l.get('workshop-accent')!)).toBeGreaterThanOrEqual(4.5)
    expect(ratio('#ffffff', l.get('workshop-accent-hover')!)).toBeGreaterThanOrEqual(4.5)
    const d = themeVars(theme, 'dark')
    const ink = value(rule(index, '[data-theme="dark"] .workshop-theme:not(.workshop-theme--network) .bg-teal-600.text-white'), 'color')
    expect(ratio(ink, d.get('workshop-accent')!)).toBeGreaterThanOrEqual(4.5)
    expect(ratio(ink, d.get('workshop-accent-hover')!)).toBeGreaterThanOrEqual(4.5)
  })

  it('Workbench (aktive Modulnummer, Knöpfe): hell weiß auf --wb-accent, dunkel --wb-canvas auf dem hellen Akzent', () => {
    const tokens = (name: string) => [...workbench.matchAll(new RegExp(`--${name}:\\s*([^;]+);`, 'g'))].map((m) => m[1].trim())
    const [accentLight, accentDark] = tokens('wb-accent')
    const [hoverLight, hoverDark] = tokens('wb-accent-hover')
    expect(ratio('#ffffff', accentLight)).toBeGreaterThanOrEqual(4.5)
    expect(ratio('#ffffff', hoverLight)).toBeGreaterThanOrEqual(4.5)
    expect(ratio('#ffffff', accentDark)).toBeLessThan(3)  // Anlass: 2,5:1
    expect(value(rule(workbench, '[data-theme="dark"] .workbench .bg-\\[var\\(--wb-accent\\)\\].text-white'), 'color')).toBe('var(--wb-canvas)')
    expect(ratio(canvas[1], accentDark)).toBeGreaterThanOrEqual(4.5)
    expect(ratio(canvas[1], hoverDark)).toBeGreaterThanOrEqual(4.5)
    // andere Lehrgänge: --wb-accent/-hover = Kursakzent (index.css) — dunkle Fläche gegen die hellen Dark-Akzente
    for (const theme of THEMES) {
      const d = themeVars(theme, 'dark')
      expect(ratio(canvas[1], d.get('workshop-accent')!)).toBeGreaterThanOrEqual(4.5)
      expect(ratio(canvas[1], d.get('workshop-accent-hover')!)).toBeGreaterThanOrEqual(4.5)
    }
  })
})
