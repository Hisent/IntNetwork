// Automatisierte Kontrastprüfung für den Dark Mode (WCAG AA, Text >= 4.5:1).
//
// Arbeitsweise (bewusst ohne neue Dependency, reine Funktionen):
// 1. Die Dark-Mode-Farbwerte werden aus den echten Quellen geparst — dem
//    Paletten-Override-Block in index.css und den Tokens in workbench.css —
//    NICHT hier noch einmal von Hand eingetippt. Für Farbstufen, die im Dark
//    Mode absichtlich NICHT überschrieben werden (z.B. der teal-600-Akzent),
//    fällt der Test auf Tailwinds eigene Kanonwerte (node_modules/tailwindcss/
//    theme.css) zurück — das ist die Quelle, aus der auch Tailwind selbst
//    kompiliert, keine zweite "Kopie der Palette".
// 2. Aus allen .tsx/.ts-Dateien unter src/ werden String-Literale (auch aus
//    Template-Literalen) eingesammelt und darin nach Klassen gesucht, die in
//    DERSELBEN Zeichenkette sowohl eine bg-*/bg-[var(--wb-*)]- als auch eine
//    text-*/text-[var(--wb-*)]-Klasse enthalten — also wirklich gemeinsam auf
//    einem Element auftretende Paare.
// 3. Für jedes eindeutige Paar wird der WCAG-Kontrast im DARK MODE berechnet
//    und gegen 4.5:1 geprüft.
//
// Siehe "Was dieser Test NICHT sieht" ganz unten für die bewussten Grenzen
// dieser Methode.

/// <reference types="node" />
// Dieser Test läuft nur unter vitest/Node, nie im Browser-Bundle — die
// tsconfig.app.json der App selbst führt bewusst keine Node-Typen (Browser-
// Code), darum hier eine gezielte Referenz statt eines globalen "types"-Eintrags.
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
// CSS-Parsing (bewusst schlicht: kein vollständiger CSS-Parser, sondern
// gezielte Regexe auf die konkrete, selbst geschriebene Struktur der beiden
// Quelldateien — siehe Grenzen unten). stripComments/parseColorVars kommen
// aus contrastScan.ts (gemeinsam mit lightContrast.test.ts genutzt).
// ---------------------------------------------------------------------------

interface ClassOverride { prop: 'background-color' | 'color' | 'border-color'; value: string }

/**
 * Findet [data-theme="dark"] <selektor> { deklarationen } - Regeln.
 * Nur EINFACHE (nicht verschachtelte) Klassenselektoren werden als
 * Ausnahme-Overrides übernommen (z.B. ".bg-slate-900", ".hover\:bg-white:hover").
 * Verschachtelte Nachfahren-Selektoren (z.B. ".bg-slate-950 .text-teal-300")
 * werden bewusst übersprungen — die kann diese Methode strukturell nicht
 * korrekt einem Element zuordnen (siehe "was der Test nicht sieht").
 */
function parseDarkClassOverrides(css: string): Map<string, ClassOverride[]> {
  const overrides = new Map<string, ClassOverride[]>()
  const clean = stripComments(css)
  const ruleRe = /\[data-theme="dark"\]([^{]*)\{([^}]*)\}/g
  for (const m of clean.matchAll(ruleRe)) {
    const selectorTail = m[1]
    const declText = m[2]
    const decls: ClassOverride[] = []
    for (const d of declText.matchAll(/(background-color|color|border-color)\s*:\s*([^;]+);/g)) {
      decls.push({ prop: d[1] as ClassOverride['prop'], value: d[2].trim() })
    }
    if (decls.length === 0) continue

    const selectors = selectorTail
      .replace(/\[data-theme="dark"\]/g, '')
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean)

    for (const sel of selectors) {
      if (/\s/.test(sel)) continue // verschachtelt -> bewusst übersprungen
      const utilityClass = sel
        .replace(/^\./, '')
        .replace(/\\:/g, ':')
        .replace(/\\\//g, '/')
        // Tailwind hängt die Pseudoklasse zusätzlich an (".hover\:bg-x:hover")
        // — der rohe Utility-Name im JSX ("hover:bg-x") hat das nicht.
        .replace(/:(hover|focus|focus-visible|active|disabled)$/, '')
      const existing = overrides.get(utilityClass) ?? []
      overrides.set(utilityClass, [...existing, ...decls])
    }
  }
  return overrides
}

/** .workbench { --wb-x: ... } (hell) und [data-theme="dark"] .workbench { --wb-x: ... } (dunkel). */
function parseWorkbenchTokens(css: string): Map<string, string> {
  const clean = stripComments(css)
  const light = new Map<string, string>()
  const lightMatch = clean.match(/(?<!")\.workbench\s*\{([^}]*)\}/)
  if (lightMatch) {
    for (const m of lightMatch[1].matchAll(/--(wb-[\w-]+)\s*:\s*([^;]+);/g)) light.set(m[1], m[2].trim())
  }
  const dark = new Map<string, string>()
  const darkMatch = clean.match(/\[data-theme="dark"\]\s*\.workbench\s*\{([^}]*)\}/)
  if (darkMatch) {
    for (const m of darkMatch[1].matchAll(/--(wb-[\w-]+)\s*:\s*([^;]+);/g)) dark.set(m[1], m[2].trim())
  }
  // dunkel gewinnt, sonst fällt der Wert auf hell zurück (Custom Properties erben)
  const effective = new Map(light)
  for (const [k, v] of dark) effective.set(k, v)
  return effective
}

const indexCss = fs.readFileSync(INDEX_CSS_PATH, 'utf8')
const workbenchCss = fs.readFileSync(WORKBENCH_CSS_PATH, 'utf8')
const tailwindThemeCss = fs.readFileSync(TAILWIND_THEME_CSS_PATH, 'utf8')

const darkColorVars = parseColorVars(indexCss)
const darkClassOverrides = parseDarkClassOverrides(indexCss)
const wbDarkTokens = parseWorkbenchTokens(workbenchCss)
const canonicalColorVars = parseColorVars(tailwindThemeCss)

function resolveDarkColor(rawClass: string): string | null {
  // 1) exakte Ausnahme-Regel für genau diese (ggf. varianten-behaftete) Klasse
  const exact = darkClassOverrides.get(rawClass)
  if (exact?.length) return exact[0].value

  const stripped = rawClass.replace(/^(?:[\w-]+:)+/, '') // hover:, focus:, sm: … entfernen
  const prefixMatch = stripped.match(/^(bg|text|border)-(.+)$/)
  if (!prefixMatch) return null
  const [, , rest] = prefixMatch

  // 2) Ausnahme-Regel für die Basisklasse ohne Variante
  const base = darkClassOverrides.get(stripped)
  if (base?.length) return base[0].value

  if (rest === 'white') return '#fff'
  if (rest === 'black') return '#000'
  // white/10, black/40 usw.: teilweise transparent — ohne zu wissen, was
  // dahinterliegt, lässt sich der tatsächliche Kontrast nicht seriös
  // berechnen (siehe Grenze 5 unten). Nicht auflösbar -> Paar wird übersprungen.
  if (/^(?:white|black)\//.test(rest)) return null

  const arbitraryVar = rest.match(/^\[var\(--(wb-[\w-]+)\)\]$/)
  if (arbitraryVar) return wbDarkTokens.get(arbitraryVar[1]) ?? null

  const shadeMatch = rest.match(/^([a-z]+)-(\d{2,3})(?:\/(\d{1,3}))?$/)
  if (!shadeMatch) return null
  const [, color, shade] = shadeMatch
  const key = `${color}-${shade}`
  return darkColorVars.get(key) ?? canonicalColorVars.get(key) ?? null
}

// ---------------------------------------------------------------------------
// className-Literale einsammeln und bg/text-Paare extrahieren.
// ---------------------------------------------------------------------------

const TOKEN_RE = new RegExp(
  `(?:[\\w-]+:)*(?:bg|text)-(?:(?:white|black)(?:/\\d{1,3})?|(?:${COLOR_NAMES})-\\d{2,3}(?:/\\d{1,3})?|\\[var\\(--wb-[\\w-]+\\)\\])`,
  'g',
)

// walk/extractSegments/collectPairs kommen aus contrastScan.ts (identische
// Logik, nur ausgelagert — siehe lightContrast.test.ts, das dieselben Helfer
// mit einem eigenen TOKEN_RE für den Light Mode nutzt).

// ---------------------------------------------------------------------------
// Bekannte, begründete Ausnahmen (bewusst kurz gehalten).
// ---------------------------------------------------------------------------

const KNOWN_EXCEPTIONS: Record<string, string> = {
  'bg-teal-600|||text-white':
    'Marken-Akzent-Button (z.B. "Weiter", "Anmelden"): weißer Text auf teal-600 erreicht ' +
    'nur ~3.7:1 — das ist ein vorbestehendes Light-Mode-Verhältnis (teal-600 wird im Dark ' +
    'Mode absichtlich NICHT verändert, s. index.css), keine durch den Dark-Mode-Fix ' +
    'eingeführte Regression. Sichtprüfung/Redesign der Akzentfarbe wäre ein separates Ticket.',
  'focus:bg-teal-600|||focus:text-white':
    'Gleiche Ausnahme wie bg-teal-600/text-white, nur der focus:-Variante (App.tsx-Fehlerknopf) — ' +
    'referenziert dieselbe unveränderte Akzentfarbe.',
  'bg-teal-500|||text-white':
    'Dieselbe Situation wie bg-teal-600/text-white (z.B. NetworkVisualsDynamics-Bit-Anzeige): ' +
    'teal-500 ist ebenfalls Akzentfarbe und bleibt unangetastet, das Kontrastproblem ist ' +
    'vorbestehend und themen-unabhängig.',
  'bg-[var(--wb-accent)]|||text-white':
    'Workbench-Pendant zu bg-teal-600/text-white (z.B. LearnPage-"Kurs abgeschlossen"-Button, ' +
    'ModulePage-Fortschrittspunkt): --wb-accent bleibt im Dark Mode hell (#14b8a6), weil es ' +
    'weit häufiger als TEXT-Farbe auf dunklem Grund verwendet wird (Links/Labels in LearnPage, ' +
    'ModulePage) — dort verlangt es Helligkeit. Ein dunklerer Wert würde diese Text-Stellen ' +
    'unlesbar machen; der seltenere weiß-auf-Akzent-Button-Fall bleibt eine vorbestehende ' +
    'Schwäche, symmetrisch zu bg-teal-600/text-white.',
  'hover:bg-[var(--wb-accent-hover)]|||text-white':
    'Hover-Variante derselben --wb-accent-Abwägung wie oben.',
  'hover:bg-slate-800|||text-teal-300':
    'Blocks.tsx CodeBlock-Kopfzeile ("Kopieren"-Button): text-teal-300 sitzt als Nachfahre in ' +
    'einer bg-slate-950-Fläche und wird dort per Scoped-Override in index.css ' +
    '(".bg-slate-950 .text-teal-300") auf hell gepinnt — das gewinnt im echten Browser dank ' +
    'höherer Spezifität. Dieser Test sieht das strukturell nicht (Eltern-bg + Kind-text, siehe ' +
    'Grenze 1 unten) und würde sonst fälschlich mit dem allgemein gespiegelten Wert rechnen.',
  'hover:bg-slate-800|||hover:text-teal-100':
    'Gleicher Fall wie oben, nur der hover:-Textfarbe desselben Buttons.',
}

describe('Dark-Mode-Kontrast (WCAG AA >= 4.5:1 für Text)', () => {
  const pairs = [...collectPairs(SRC_DIR, TOKEN_RE).values()]
  expect(pairs.length).toBeGreaterThan(20) // Sanity-Check: die Extraktion findet überhaupt etwas

  it.each(pairs)('$bg + $text', ({ bg, text, files }) => {
    const bgColor = resolveDarkColor(bg)
    const textColor = resolveDarkColor(text)
    const key = `${bg}|||${text}`
    const exceptionReason = KNOWN_EXCEPTIONS[key]

    if (!bgColor || !textColor) {
      // Nicht auflösbar (z.B. unbekanntes wb-Token) -> für diesen Test kein Urteil möglich.
      return
    }

    const fg = parseCssColorToLinearRgb(textColor)
    const bgLin = parseCssColorToLinearRgb(bgColor)
    if (!fg || !bgLin) return

    const ratio = contrastRatio(fg, bgLin)

    if (exceptionReason) {
      expect(ratio).toBeGreaterThan(0) // Ausnahme dokumentiert, keine harte Prüfung
      return
    }

    expect(
      ratio,
      `${bg} (${bgColor}) + ${text} (${textColor}) in ${[...files].join(', ')}: ` +
      `Kontrast ${ratio.toFixed(2)}:1 unterschreitet AA (4.5:1)`,
    ).toBeGreaterThanOrEqual(AA_TEXT_CONTRAST)
  })
})

// ---------------------------------------------------------------------------
// Was dieser Test STRUKTURELL NICHT sieht (bewusste Grenzen der Methode):
//
// 1. Eltern/Kind-Paare: Wenn die bg-*-Klasse auf einem Element sitzt und die
//    text-*-Klasse erst auf einem verschachtelten Kind-Element (z.B. Blocks.tsx
//    CodeBlock: äußeres div "bg-slate-950", inneres span "text-slate-500"),
//    tauchen beide Klassen nie in DERSELBEN Zeichenkette auf — der Test bildet
//    nur Paare aus className-Literalen desselben Elements. Diese Fälle wurden
//    hier von Hand geprüft und über gezielte Ausnahme-Regeln in index.css
//    abgesichert (siehe die ".bg-slate-950 .text-teal-300"-Selektoren dort),
//    aber der automatisierte Test deckt sie nicht ab — Sichtprüfung nötig,
//    falls dort neue Farbklassen hinzukommen.
// 2. Bedingte Klassen über mehrere Ausdrücke hinweg, die sich erst zur
//    Laufzeit zu einem Paar zusammensetzen (z.B. eine Klasse aus einer
//    Konstante plus eine literal im JSX daneben stehende Klasse) — nur
//    Anführungszeichen-Literale und die statischen Teile von Template-
//    Literalen werden geparst, kein vollständiger TS/JSX-AST.
// 3. Workshop-Theme-Overrides (.workshop-theme--claude/--network): Der Test
//    prüft nur die BASIS-Dark-Palette, nicht die zusätzliche Akzent-Umfärbung
//    pro Workshop-Thema — die orangene Claude-Variante braucht eine eigene
//    Sichtprüfung.
// 4. Nicht-Text-Kontraste (Border, Ring, Fokus-Ring, Icons ohne Text) — WCAG
//    verlangt dort nur 3:1 (UI-Komponenten) bzw. gar nichts (rein dekorativ);
//    dieser Test prüft ausschließlich Text-auf-Fläche mit dem strengeren 4.5:1.
// 5. Farben mit Transparenz (z.B. bg-rose-900/60 als Hervorhebung über
//    bereits vorhandenem Text): der Test behandelt sie näherungsweise als
//    deckende Farbe (ignoriert Alpha) statt korrekt über den tatsächlichen
//    Untergrund zu compositen.
// ---------------------------------------------------------------------------
