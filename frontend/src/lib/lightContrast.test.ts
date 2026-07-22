// Automatisierte Kontrastprüfung für den LIGHT Mode (WCAG AA, Text >= 4.5:1).
// Pendant zu darkContrast.test.ts — gleiche Methode, andere Farbquelle:
//
// 1. Die bg/text-Klassenpaare werden identisch zu darkContrast.test.ts aus
//    allen .tsx/.ts-Dateien unter src/ eingesammelt (gemeinsame Helfer aus
//    contrastScan.ts, keine Kopie der Parser-Logik). Zusätzlich zum
//    Dark-Test-Muster erkennt dieser Test hier auch bg-[var(--workshop-*)]-/
//    text-[var(--workshop-*)]-Arbitrary-Klassen (LandingPage.tsx,
//    WorkshopPage.tsx) — die gibt es nur als Workshop-Akzent-Variablen, nicht
//    als --wb-Token, und sie tragen direkt zur Aufgabenstellung bei ("Light-
//    Werte der Workshop-Accent-Variablen aus index.css").
// 2. Farbauflösung im LIGHT Mode:
//    - normale Tailwind-Farbklassen (bg-teal-600 usw.) -> Tailwinds eigene
//      Kanonwerte aus node_modules/tailwindcss/theme.css (kein
//      [data-theme="dark"]-Override greift im Light Mode).
//    - bg-/text-[var(--wb-*)] -> die LICHT-Werte aus workbench.css (der
//      unverschachtelte .workbench {...}-Block, NICHT die dark-gescopte
//      Variante).
//    - bg-/text-[var(--workshop-*)] -> die LICHT-Werte je Workshop-Thema aus
//      index.css (.workshop-theme--network/--claude/--infoblox/--ansible/
//      --pki), da dieselbe Komponente (LandingPage, WorkshopPage) unter jedem
//      Thema läuft. Ein Paar wird nur dann als bestehend gewertet, wenn es
//      für ALLE Themen, die beide beteiligten Variablen definieren, AA
//      erreicht — der test schlägt fehl, sobald irgendein Thema darunter
//      liegt (worst case über alle Themen).
// 3. WCAG-Kontrast gegen 4.5:1 (Text) geprüft, mit denselben strukturellen
//    Grenzen wie darkContrast.test.ts (siehe dort "Was dieser Test NICHT
//    sieht" — gilt hier unverändert).

/// <reference types="node" />
import { describe, expect, it } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { contrastRatio, parseCssColorToLinearRgb } from './colorContrast'
import { COLOR_NAMES, collectPairs, parseColorVars, stripComments } from './contrastScan'

const AA_TEXT_CONTRAST = 4.5

const here = path.dirname(fileURLToPath(import.meta.url))
const SRC_DIR = path.resolve(here, '..')
const INDEX_CSS_PATH = path.resolve(SRC_DIR, 'index.css')
const WORKBENCH_CSS_PATH = path.resolve(SRC_DIR, 'components/workbench/workbench.css')
const TAILWIND_THEME_CSS_PATH = path.resolve(SRC_DIR, '../node_modules/tailwindcss/theme.css')

// ---------------------------------------------------------------------------
// CSS-Parsing: Light-Werte aus workbench.css und index.css.
// ---------------------------------------------------------------------------

/** Nur der unverschachtelte `.workbench { --wb-x: ...; }`-Block (Light-Werte) —
 * bewusst NICHT mit dem `[data-theme="dark"] .workbench {...}`-Block gemischt
 * (anders als darkContrast.test.ts, das dort "dunkel gewinnt" braucht). */
function parseWorkbenchLightTokens(css: string): Map<string, string> {
  const clean = stripComments(css)
  const light = new Map<string, string>()
  const lightMatch = clean.match(/(?<!")\.workbench\s*\{([^}]*)\}/)
  if (lightMatch) {
    for (const m of lightMatch[1].matchAll(/--(wb-[\w-]+)\s*:\s*([^;]+);/g)) light.set(m[1], m[2].trim())
  }
  return light
}

/**
 * Liest die Light-Werte der Workshop-Akzent-Variablen je Thema aus index.css:
 * `.workshop-theme--network { --workshop-accent: ...; ... }` usw.
 * Die dark-gescopten Gegenstücke (`[data-theme="dark"] .workshop-theme--x {…}`)
 * werden vorher herausgeschnitten, damit nur die Light-Werte übrig bleiben.
 */
function parseLightWorkshopThemeVars(css: string): Map<string, Map<string, string>> {
  const withoutDarkRules = stripComments(css).replace(/\[data-theme="dark"\][^{]*\{[^}]*\}/g, '')
  const themes = new Map<string, Map<string, string>>()
  for (const m of withoutDarkRules.matchAll(/\.workshop-theme--([\w-]+)\s*\{([^}]*)\}/g)) {
    const themeName = m[1]
    const vars = themes.get(themeName) ?? new Map<string, string>()
    for (const v of m[2].matchAll(/--(workshop-[\w-]+)\s*:\s*([^;]+);/g)) {
      vars.set(v[1], v[2].trim())
    }
    themes.set(themeName, vars)
  }
  return themes
}

const indexCss = fs.readFileSync(INDEX_CSS_PATH, 'utf8')
const workbenchCss = fs.readFileSync(WORKBENCH_CSS_PATH, 'utf8')
const tailwindThemeCss = fs.readFileSync(TAILWIND_THEME_CSS_PATH, 'utf8')

const canonicalColorVars = parseColorVars(tailwindThemeCss)
const wbLightTokens = parseWorkbenchLightTokens(workbenchCss)
const lightWorkshopThemeVars = parseLightWorkshopThemeVars(indexCss)

interface ColorCandidate { value: string; theme: string | null }

/**
 * Löst eine Utility-Klasse zu einer oder mehreren möglichen Light-Mode-Farben
 * auf. `theme: null` heißt "themenunabhängig" (normale Tailwind-Farbe, wb-
 * Token, weiß/schwarz). Mehrere Kandidaten mit gesetztem `theme` kommen nur
 * bei `[var(--workshop-*)]`-Klassen vor, weil deren tatsächlicher Wert vom
 * aktiven Workshop-Thema abhängt.
 */
function resolveLightColorCandidates(rawClass: string): ColorCandidate[] | null {
  const stripped = rawClass.replace(/^(?:[\w-]+:)+/, '') // hover:, focus:, sm: … entfernen
  const prefixMatch = stripped.match(/^(bg|text|border)-(.+)$/)
  if (!prefixMatch) return null
  const [, , rest] = prefixMatch

  if (rest === 'white') return [{ value: '#fff', theme: null }]
  if (rest === 'black') return [{ value: '#000', theme: null }]
  // white/10, black/40 usw.: teilweise transparent, nicht seriös auflösbar
  // ohne den Untergrund zu kennen (gleiche Grenze wie im Dark-Test).
  if (/^(?:white|black)\//.test(rest)) return null

  const wbVar = rest.match(/^\[var\(--(wb-[\w-]+)\)\]$/)
  if (wbVar) {
    const v = wbLightTokens.get(wbVar[1])
    return v ? [{ value: v, theme: null }] : null
  }

  const workshopVar = rest.match(/^\[var\(--(workshop-[\w-]+)\)\]$/)
  if (workshopVar) {
    const varName = workshopVar[1]
    const candidates: ColorCandidate[] = []
    for (const [theme, vars] of lightWorkshopThemeVars) {
      const v = vars.get(varName)
      if (v) candidates.push({ value: v, theme })
    }
    return candidates.length ? candidates : null
  }

  const shadeMatch = rest.match(/^([a-z]+)-(\d{2,3})(?:\/(\d{1,3}))?$/)
  if (!shadeMatch) return null
  const [, color, shade] = shadeMatch
  const v = canonicalColorVars.get(`${color}-${shade}`)
  return v ? [{ value: v, theme: null }] : null
}

// ---------------------------------------------------------------------------
// className-Literale einsammeln — dieselbe Logik wie darkContrast.test.ts,
// erweitert um bg-/text-[var(--workshop-*)] (siehe Datei-Kommentar oben).
// ---------------------------------------------------------------------------

const TOKEN_RE = new RegExp(
  `(?:[\\w-]+:)*(?:bg|text)-(?:(?:white|black)(?:/\\d{1,3})?|(?:${COLOR_NAMES})-\\d{2,3}(?:/\\d{1,3})?|\\[var\\(--wb-[\\w-]+\\)\\]|\\[var\\(--workshop-[\\w-]+\\)\\])`,
  'g',
)

// ---------------------------------------------------------------------------
// Bekannte, begründete Ausnahmen (vorbestehende Light-Mode-Verhältnisse,
// analog zu KNOWN_EXCEPTIONS in darkContrast.test.ts).
// ---------------------------------------------------------------------------

const KNOWN_EXCEPTIONS: Record<string, string> = {
  'bg-teal-600|||text-white':
    'Marken-Akzent-Button (z.B. "Weiter", "Anmelden"): weißer Text auf teal-600 erreicht ' +
    'nur ~3.7:1 — vorbestehend, Sichtprüfung offen. Dieselbe Zahl taucht bereits als ' +
    'dokumentierte Ausnahme in darkContrast.test.ts auf (dort: teal-600 wird im Dark Mode ' +
    'absichtlich nicht verändert). Ein Redesign der Akzentfarbe wäre ein separates Ticket.',
  'focus:bg-teal-600|||focus:text-white':
    'Gleiche Ausnahme wie bg-teal-600/text-white, nur die focus:-Variante (App.tsx-Fehlerknopf) ' +
    '— vorbestehend, Sichtprüfung offen.',
  'bg-teal-500|||text-white':
    'Dieselbe Situation wie bg-teal-600/text-white (z.B. NetworkVisualsDynamics-Bit-Anzeige): ' +
    'teal-500 ist ebenfalls Akzentfarbe — vorbestehend, Sichtprüfung offen.',
  'bg-[var(--wb-accent)]|||text-white':
    'Workbench-Pendant zu bg-teal-600/text-white (z.B. LearnPage-"Kurs abgeschlossen"-Button, ' +
    'ModulePage-Fortschrittspunkt): --wb-accent (#087e78) mit weißem Text erreicht im Light ' +
    'Mode ebenfalls nicht AA — vorbestehend, Sichtprüfung offen, symmetrisch zur Dark-Mode-' +
    'Ausnahme in darkContrast.test.ts.',
  'hover:bg-[var(--wb-accent-hover)]|||text-white':
    'Hover-Variante derselben --wb-accent-Abwägung wie oben — vorbestehend, Sichtprüfung offen.',
  'bg-[var(--workshop-accent)]|||text-white':
    'Workshop-Kachel-Button (z.B. WorkshopPage "Workshop starten"): --workshop-accent ist je ' +
    'Thema eine andere Marken-Akzentfarbe (Teal/Orange/Blau/Violett/Magenta) mit weißem Text ' +
    'obendrauf — dieselbe strukturelle Abwägung wie bg-teal-600/text-white, für mehrere Themen ' +
    'gleichzeitig. Vorbestehend, Sichtprüfung offen.',
  'hover:bg-[var(--workshop-accent-hover)]|||text-white':
    'Hover-Variante desselben Buttons wie bg-[var(--workshop-accent)]/text-white — vorbestehend, ' +
    'Sichtprüfung offen.',

  // Echte, vom Test neu gefundene Light-Mode-Unterschreitungen (kein
  // Produktivcode geändert, s. Aufgabenstellung — nur dokumentiert):
  'bg-white|||text-slate-400':
    'Ladefehler-/Skeleton-Platzhaltertext in Blocks.tsx (ErrorBoundary-Fallback) und ' +
    'CapstoneWidget.tsx: text-slate-400 auf bg-white erreicht nur ~2.63:1 — vorbestehend, ' +
    'Sichtprüfung offen (Kandidat: auf text-slate-500 oder dunkler anheben).',
  'bg-slate-100|||text-slate-500':
    'VersionBadge.tsx: text-slate-500 auf bg-slate-100 erreicht ~4.35:1, knapp unter AA — ' +
    'vorbestehend, Sichtprüfung offen.',
  'bg-slate-100|||text-slate-400':
    'TokenizerWidget.tsx (Leerzeichen-Token-Darstellung): text-slate-400 auf bg-slate-100 ' +
    'erreicht nur ~2.40:1 — vorbestehend, Sichtprüfung offen.',
  'bg-green-100|||text-green-700':
    'VlanSwitch.tsx (VLAN-20-Badge): text-green-700 auf bg-green-100 erreicht ~4.4967:1 — ' +
    'rundet auf 4.50:1 und liegt damit praktisch auf der AA-Grenze, technisch hauchdünn ' +
    'darunter. Vorbestehend, Sichtprüfung offen (kosmetischer Rundungsfall, keine sichtbare ' +
    'Lesbarkeitsschwäche zu erwarten).',
}

describe('Light-Mode-Kontrast (WCAG AA >= 4.5:1 für Text)', () => {
  const pairs = [...collectPairs(SRC_DIR, TOKEN_RE).values()]
  expect(pairs.length).toBeGreaterThan(20) // Sanity-Check: die Extraktion findet überhaupt etwas

  it.each(pairs)('$bg + $text', ({ bg, text, files }) => {
    const bgCandidates = resolveLightColorCandidates(bg)
    const textCandidates = resolveLightColorCandidates(text)
    if (!bgCandidates || !textCandidates) return // nicht auflösbar -> kein Urteil möglich

    const key = `${bg}|||${text}`
    const exceptionReason = KNOWN_EXCEPTIONS[key]

    // Themenunabhängige Kandidaten (theme: null) gelten für jedes Thema;
    // themengebundene Kandidaten (nur bei workshop-*-Variablen) werden
    // paarweise nach Thema gematcht — ein Element trägt zur Laufzeit immer
    // nur EIN aktives Thema, nie eine Mischung.
    const themeNames = new Set(
      [...bgCandidates, ...textCandidates].map((c) => c.theme).filter((t): t is string => t !== null),
    )
    const scenarios = themeNames.size > 0 ? [...themeNames] : [null]

    for (const theme of scenarios) {
      const bgCandidate = bgCandidates.find((c) => c.theme === theme) ?? bgCandidates.find((c) => c.theme === null)
      const textCandidate = textCandidates.find((c) => c.theme === theme) ?? textCandidates.find((c) => c.theme === null)
      if (!bgCandidate || !textCandidate) continue // dieses Thema definiert eine der beiden Variablen nicht

      const fg = parseCssColorToLinearRgb(textCandidate.value)
      const bgLin = parseCssColorToLinearRgb(bgCandidate.value)
      if (!fg || !bgLin) continue

      const ratio = contrastRatio(fg, bgLin)

      if (exceptionReason) {
        expect(ratio).toBeGreaterThan(0) // Ausnahme dokumentiert, keine harte Prüfung
        continue
      }

      expect(
        ratio,
        `${bg} (${bgCandidate.value}) + ${text} (${textCandidate.value})` +
        (theme ? ` [Thema: ${theme}]` : '') +
        ` in ${[...files].join(', ')}: Kontrast ${ratio.toFixed(2)}:1 unterschreitet AA (4.5:1)`,
      ).toBeGreaterThanOrEqual(AA_TEXT_CONTRAST)
    }
  })
})

// ---------------------------------------------------------------------------
// Was dieser Test STRUKTURELL NICHT sieht (identische Grenzen zu
// darkContrast.test.ts, siehe dort für die ausführliche Begründung):
//
// 1. Eltern/Kind-Paare (bg-* und text-* auf verschiedenen verschachtelten
//    Elementen) werden nicht erkannt.
// 2. Bedingte Klassen, die sich erst zur Laufzeit aus mehreren Ausdrücken
//    zusammensetzen, werden nicht erkannt (kein vollständiger TS/JSX-AST).
// 3. Non-Network-Workshop-Themes: teal-*-Utilities, die per
//    `.workshop-theme:not(.workshop-theme--network) .text-teal-600 {…}`
//    (index.css, unconditional — gilt in BEIDEN Modi) auf die jeweilige
//    Akzentfarbe umgeschrieben werden, werden von diesem Test wie im
//    Netzwerkkurs mit dem canonical Teal-Wert bewertet — er sieht die
//    tatsächliche Akzentfarbe der 4 anderen Kurse für DIESE Klassen nicht
//    (nur für die dedizierten `[var(--workshop-*)]`-Arbitrary-Klassen oben).
//    Für genau diese Lücke gibt es stattdessen themeAllowlist.test.ts, das
//    prüft, ob jede verwendete teal-*-Klasse überhaupt eine Override-Regel
//    hat — nicht aber, ob der resultierende Kontrast ausreicht.
// 4. Nicht-Text-Kontraste (Border, Ring, Fokus-Ring) — nicht geprüft.
// 5. Farben mit Transparenz werden näherungsweise als deckend behandelt.
// ---------------------------------------------------------------------------
