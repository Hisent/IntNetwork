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
import { lightPalette, parseColorVars, stripComments } from './contrastScan'

const SRC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const read = (rel: string) => fs.readFileSync(path.resolve(SRC, rel), 'utf8')

const light = lightPalette(read('../node_modules/tailwindcss/theme.css'), read('index.css'))
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

  // Erlaubt bleibt text-slate-400/-300 nur, wo es keinen lesbaren Text auf hellem Grund färbt:
  // echte disabled-Zustände, Linien/Icons/Kreise ohne Text und dunkle Terminal-Flächen
  // (siehe nächster Block, dort mit Zahlen belegt). "Noch nicht erreichte" Schritte sind KEIN
  // disabled-Zustand — sie stehen auf slate-500 plus gestricheltem Rahmen.
  const ALLOWED = [
    "'border-slate-100 text-slate-400'",            // Blocks.tsx: nicht gewählte Option nach der Antwort (disabled)
    '<g className="text-slate-400">',               // DiagramBlock: Trennlinie (stroke=currentColor)
    "'text-slate-400 opacity-45'",                  // DiagramBlock: abgeblendete Elemente außerhalb des Schritts (SVG-Grafik)
    "'border-slate-300 text-slate-400'",            // TerminalBlock: leerer Kreis einer offenen Aufgabe (kein Text)
    "'text-slate-700' : 'text-slate-400'",          // PolicyWidget: Beschriftung der deaktivierten Checkbox (disabled)
    "'cursor-not-allowed text-slate-400'",          // ModulePage: gesperrtes Modul in der Seitenleiste (aria-disabled)
    'pointer-events-none absolute right-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400', // LandingPage: Lupen-Icon im Suchfeld (kein Text)
    'mt-1 text-sm text-slate-300',                  // LandingPage: Katalog-Kachel (bg-slate-950, immer dunkel)
    'space-y-3 border-t border-slate-800 pt-5 text-sm text-slate-300', // LandingPage: dito
    // --- dunkle Terminal-Flächen (bg-slate-800/-900/-950), text-slate-400 ist dort der HELLE Vordergrund ---
    'tracking-[0.14em] text-slate-400">{language',  // Blocks.tsx CodeBlock: Sprachlabel im Kopf (bg-slate-950)
    '<span className="block text-slate-400 font-mono">{recap.skipped}', // AnsibleLab: Recap-Kachel (bg-slate-800)
    '<p className="text-slate-400">C:\\&gt;',         // Troubleshoot: Prompt "C:\>" im Terminal (bg-slate-900)
    '<p className="text-slate-400">{s.terminalHint}',  // Troubleshoot: Platzhalterzeile im Terminal (bg-slate-900)
    '<p className="mt-2 text-[11px] text-slate-400">',  // LabOutputPanel: Statuszeile im Ausgabefeld (bg-slate-900)
    '<p className="font-mono text-xs text-slate-400">{noRunYetLabel}', // LabOutputPanel: "Noch kein Lauf." im Ausgabefeld (bg-slate-900)
  ]
  const tsxFiles = (dir: string): string[] => fs.readdirSync(path.resolve(SRC, dir), { withFileTypes: true })
    .flatMap((e) => e.isDirectory() ? tsxFiles(`${dir}/${e.name}`)
      : e.name.endsWith('.tsx') && !/\.(test|stories)\./.test(e.name) ? [`${dir}/${e.name}`] : [])
  // ALLE Komponenten, Seiten und Widgets: neue text-slate-400-Fließtexte fallen sofort auf
  const files = ['components', 'pages', 'widgets'].flatMap(tsxFiles)

  it('die Dateisuche findet die Verzeichnisse (kein stiller Leerlauf)', () => {
    expect(files.filter((f) => f.startsWith('widgets/')).length).toBeGreaterThan(40)
    expect(files.filter((f) => f.startsWith('pages/')).length).toBeGreaterThan(8)
    expect(files).toContain('widgets/pki/HashWidget.tsx')
    expect(files).toContain('components/workbench/WorkbenchShell.tsx')
  })

  it.each(files)('%s: kein text-slate-400/-300 für lesbaren Text', (file) => {
    const hits = read(file).split('\n')
      .filter((line) => /text-slate-[34]00/.test(line) && !ALLOWED.some((ok) => line.includes(ok)))
      .map((line) => line.trim().slice(0, 120))
    expect(hits).toEqual([])
  })
})

// Dunkle Terminal-Flächen der Widgets (bg-slate-800/-900): im Hellmodus die Tailwind-Werte, im
// Dunkelmodus die festen Ausnahmen aus index.css (Terminals bleiben dunkel). Der Vordergrund
// text-slate-400 folgt dort der jeweiligen Palette — beide Paare müssen AA halten.
describe('text-slate-400 auf dunklen Terminal-Flächen der Widgets (WCAG AA >= 4.5:1)', () => {
  const index = stripComments(read('index.css'))
  const darkTerminal = (cls: string) => index.match(new RegExp(`\\[data-theme="dark"\\] \\.${cls},?\\s*(?:\\[[^{]*)?\\{\\s*background-color:\\s*([^;]+);`))?.[1].trim()
  it.each([['slate-800', '800'], ['slate-900', '900']])('bg-%s', (_n, shade) => {
    const darkBg = darkTerminal(`bg-slate-${shade}`)
    expect(darkBg, `Dark-Ausnahme für bg-slate-${shade} fehlt`).toBeTruthy()
    expect(contrastRatioForColors(light.get('slate-400')!, light.get(`slate-${shade}`)!)).toBeGreaterThanOrEqual(4.5)
    expect(contrastRatioForColors(dark.get('slate-400')!, darkBg!)).toBeGreaterThanOrEqual(4.5)
  })
  it('text-slate-100 (Terminal-Standardschrift) ist im Dunkelmodus fest hell gepinnt', () => {
    expect(index).toMatch(/\[data-theme="dark"\] \.text-slate-100 \{ color: oklch\(96\.8%/)
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

  // --- Kursakzent als SCHRIFT auf den hellen/dunklen Flächen, auf denen er steht --------------------
  const subtle = [...workbench.matchAll(/--wb-subtle:\s*([^;]+);/g)].map((m) => m[1].trim())  // [hell, dunkel]
  const wbTok = (name: string) => [...workbench.matchAll(new RegExp(`--${name}:\\s*([^;]+);`, 'g'))].map((m) => m[1].trim())

  it('Netzwerkkurs hell: --wb-accent als Schrift auf accent-soft, subtle, Seitenfläche und Karte', () => {
    const [accent] = wbTok('wb-accent'); const [soft] = wbTok('wb-accent-soft')
    for (const bg of [soft, subtle[0], canvas[0], '#ffffff']) expect(ratio(accent, bg)).toBeGreaterThanOrEqual(4.5)
  })

  it.each(['network', ...THEMES.filter((t) => t !== 'network')])('Kursfarbe %s: Akzent als Schrift auf accent-soft/Seite/Karte, hell und dunkel', (theme) => {
    const l = themeVars(theme, 'light'); const d = themeVars(theme, 'dark')
    const accentL = l.get('workshop-accent')!; const softL = l.get('workshop-accent-soft')!
    for (const bg of [softL, canvas[0], '#ffffff']) expect(ratio(accentL, bg), `hell ${theme} auf ${bg}`).toBeGreaterThanOrEqual(4.5)
    // Dunkel: Netzwerkkurs bekommt den Workbench-Akzent aus dem allgemeinen [data-theme="dark"]-Block
    const rootDark = rule(index, '[data-theme="dark"],\n  [data-theme="dark"] .workshop-theme--network {')
    const accentD = d.get('workshop-accent') ?? value(rootDark, '--workshop-accent')
    const softD = theme === 'network' ? value(rule(index, '[data-theme="dark"] .workshop-theme--network {'), '--workshop-accent-soft') : d.get('workshop-accent-soft')!
    for (const bg of [softD, canvas[1], DARK_CARD]) expect(ratio(accentD, bg), `dunkel ${theme} auf ${bg}`).toBeGreaterThanOrEqual(4.5)
  })

  it('Netzwerkkurs dunkel: der Akzent-Fallback von "IntLab" (Wortmarke außerhalb eines Kursrahmens) ist hell genug', () => {
    expect(ratio('#0f766e', canvas[1])).toBeLessThan(4.5)  // Anlass: 3,4:1
    expect(index).toMatch(/\[data-theme="dark"\],\s*\[data-theme="dark"\] \.workshop-theme--network \{\s*--workshop-accent: #14b8a6;/)
    expect(ratio('#14b8a6', canvas[1])).toBeGreaterThanOrEqual(4.5)
    expect(ratio('#14b8a6', DARK_CARD)).toBeGreaterThanOrEqual(4.5)
    // darauf stehende Schrift (bg-[var(--workshop-accent)] text-white) ist dunkel gepinnt, für ALLE Kurse
    expect(index).toMatch(/\[data-theme="dark"\] \.bg-\\\[var\\\(--workshop-accent\\\)\\\]\.text-white \{ color: #0d1417; \}/)
    expect(ratio('#0d1417', '#14b8a6')).toBeGreaterThanOrEqual(4.5)
  })

  it.each(THEMES.filter((t) => t !== 'network'))('Code-Kopf (Kopieren-Knopf auf bg-slate-950), Kursfarbe %s dunkel: heller Akzent statt accent-pale', (theme) => {
    const d = themeVars(theme, 'dark')
    expect(index).toContain('.workshop-theme:not(.workshop-theme--network) .bg-slate-950 .text-teal-300 { color: var(--workshop-accent-strong); }')
    expect(ratio(d.get('workshop-accent-pale')!, 'oklch(12.9% 0.042 264.695)')).toBeLessThan(4.5)  // Anlass: 1,7–2,3:1
    expect(ratio(d.get('workshop-accent-strong')!, 'oklch(12.9% 0.042 264.695)')).toBeGreaterThanOrEqual(4.5)
    expect(ratio(d.get('workshop-accent-hover')!, 'oklch(12.9% 0.042 264.695)')).toBeGreaterThanOrEqual(4.5)
  })

  it('slate-500 (Hinweisstufe) hält AA auf allen hellen und dunklen Flächen, auf denen sie steht', () => {
    for (const bg of [canvas[0], subtle[0], light.get('slate-50')!, light.get('slate-100')!, '#ffffff', light.get('teal-50')!, light.get('amber-50')!])
      expect(ratio(light.get('slate-500')!, bg), `hell auf ${bg}`).toBeGreaterThanOrEqual(4.5)
    for (const bg of [canvas[1], subtle[1], dark.get('slate-50')!, dark.get('slate-100')!, DARK_CARD])
      expect(ratio(dark.get('slate-500')!, bg), `dunkel auf ${bg}`).toBeGreaterThanOrEqual(4.5)
  })

  it('Sprachumschalter, Version und Hinweise: kein text-slate-400 mehr in der Kopfleiste', () => {
    expect(read('components/workbench/WorkbenchShell.tsx')).not.toMatch(/text-slate-400/)
  })
})

// Text wird nicht über opacity abgeschwächt (das mischt die Farbe mit dem Grund und unterschreitet 4,5:1
// unvorhersehbar) — dafür gibt es die Slate-Stufen. Erlaubt: disabled:/hover:-Varianten und die Fälle unten.
describe('keine opacity-Abschwächung von Text', () => {
  const OPACITY_OK = [
    'opacity-70 transition-opacity hover:opacity-100',  // ThemeToggle: Icon, kein Text
    'opacity-25 transition-[width]',                    // LivePoll: Balkenfläche, kein Text
    'cursor-not-allowed opacity-65',                    // LearnPage: aria-disabled Modulzeile (gesperrt)
    'uppercase tracking-[0.14em] opacity-80',           // LearnPage: Weiterlernen-Karte, immer dunkel, Text ~ 9:1
    'mt-1 block text-sm opacity-80',                    // LearnPage: dito
    "'text-slate-400 opacity-45'",                      // DiagramBlock: SVG-Grafik außerhalb des Schritts
  ]
  const tsx = (dir: string): string[] => fs.readdirSync(path.resolve(SRC, dir), { withFileTypes: true })
    .flatMap((e) => e.isDirectory() ? tsx(`${dir}/${e.name}`) : e.name.endsWith('.tsx') && !e.name.includes('.test.') ? [`${dir}/${e.name}`] : [])
  it.each(['components', 'pages', 'widgets'].flatMap(tsx))('%s', (file) => {
    const hits = read(file).split('\n')
      .filter((line) => /(?:^|[\s'"`])opacity-\d+/.test(line) && !OPACITY_OK.some((ok) => line.includes(ok)))
      .map((line) => line.trim().slice(0, 120))
    expect(hits).toEqual([])
  })
})
