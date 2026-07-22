// Gemeinsame Parser-Helfer für die Kontrast-Scanner (darkContrast.test.ts,
// lightContrast.test.ts). Reine Extraktion ohne Verhaltensänderung: jede
// Funktion hier stammt unverändert aus darkContrast.test.ts, damit der
// bestehende Dark-Test exakt dieselben Ergebnisse liefert wie vorher.
//
// Bewusst KEIN eigenes .test.ts, damit vitest diese Datei nicht als Testdatei
// einsammelt — sie liefert nur Bausteine für die beiden echten Tests.

/// <reference types="node" />
import fs from 'node:fs'
import path from 'node:path'

// ---------------------------------------------------------------------------
// CSS-Parsing (bewusst schlicht: kein vollständiger CSS-Parser, sondern
// gezielte Regexe auf die konkrete, selbst geschriebene Struktur der
// Quelldateien — siehe "Was dieser Test NICHT sieht" in darkContrast.test.ts).
// ---------------------------------------------------------------------------

export function stripComments(css: string): string {
  return css.replace(/\/\*[\s\S]*?\*\//g, '')
}

export function parseColorVars(css: string): Map<string, string> {
  const vars = new Map<string, string>()
  for (const m of stripComments(css).matchAll(/--color-([a-z]+)-(\d{2,3})\s*:\s*([^;]+);/g)) {
    vars.set(`${m[1]}-${m[2]}`, m[3].trim())
  }
  return vars
}

// ---------------------------------------------------------------------------
// className-Literale einsammeln und bg/text-Paare extrahieren.
// ---------------------------------------------------------------------------

export const COLOR_NAMES = 'slate|teal|amber|green|rose|red|blue|sky|purple|violet|fuchsia|emerald'

export function walk(dir: string, out: string[] = []): string[] {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules') continue
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) { walk(full, out); continue }
    if (!/\.(tsx?|jsx?)$/.test(entry.name)) continue
    if (/\.test\.[jt]sx?$/.test(entry.name)) continue
    out.push(full)
  }
  return out
}

/**
 * Statische String-Segmente aus einer Datei: Inhalt von '...', "..." und die
 * statischen Teile von Template-Literalen (Ausdrücke ${...} werden heraus-
 * geschnitten). Bewusst ein einziger zeichenweiser Durchlauf statt dreier
 * unabhängiger Regexe: Englische Texte enthalten Apostrophe ("that's how…")
 * INNERHALB doppelt gequoteter Strings — drei unabhängige Regexe (' getrennt
 * von ") lesen so ein Apostroph fälschlich als Start eines '...'-Strings und
 * hängen dann alles bis zum nächsten ' irgendwo im Rest der Datei an (auch
 * quer durch völlig unabhängige JSX-Elemente). Ein zeichenweiser Scan, der
 * das öffnende Anführungszeichen als einzig gültiges Ende merkt, hat dieses
 * Problem nicht.
 */
const REGEX_PRECEDING_KEYWORDS = new Set([
  'return', 'typeof', 'instanceof', 'in', 'of', 'case', 'do', 'else', 'yield', 'await', 'new',
])

/** Heuristik "steht hier ein Regex-Literal (statt einer Division)?" — reicht
 * für den hier vorkommenden Fall (z.B. `.replace(/[#*\`>\n]+/g, ' ')`, siehe
 * unten), ohne einen echten JS-Parser zu brauchen. */
function looksLikeRegexStart(text: string, slashIndex: number): boolean {
  let j = slashIndex - 1
  while (j >= 0 && /\s/.test(text[j])) j--
  if (j < 0) return true
  const c = text[j]
  if (/[a-zA-Z0-9_$)\]]/.test(c)) {
    let k = j
    while (k >= 0 && /[a-zA-Z_$]/.test(text[k])) k--
    const word = text.slice(k + 1, j + 1)
    return REGEX_PRECEDING_KEYWORDS.has(word)
  }
  return true // Operator/Satzzeichen/Dateianfang davor -> eher Regex als Division
}

export function extractSegments(fileText: string): string[] {
  const segments: string[] = []
  const n = fileText.length
  let i = 0
  while (i < n) {
    const ch = fileText[i]
    if (ch === "'" || ch === '"' || ch === '`') {
      let j = i + 1
      let buf = ''
      while (j < n && fileText[j] !== ch) {
        if (fileText[j] === '\\') { buf += fileText[j] + (fileText[j + 1] ?? ''); j += 2; continue }
        buf += fileText[j]
        j++
      }
      segments.push(ch === '`' ? buf.replace(/\$\{[^}]*\}/g, ' ') : buf)
      i = j + 1
      continue
    }
    if (ch === '/' && fileText[i + 1] === '/') {
      while (i < n && fileText[i] !== '\n') i++
      continue
    }
    if (ch === '/' && fileText[i + 1] === '*') {
      i += 2
      while (i < n && !(fileText[i] === '*' && fileText[i + 1] === '/')) i++
      i += 2
      continue
    }
    // Regex-Literale (z.B. .replace(/[#*`>\n]+/g, ' ')) überspringen: ihr
    // Inhalt darf NICHT als Anführungszeichen-Scan missverstanden werden —
    // ein Backtick/Quote in einer Zeichenklasse ist kein String-Start.
    if (ch === '/' && looksLikeRegexStart(fileText, i)) {
      let j = i + 1
      let inClass = false
      let closed = false
      while (j < n) {
        const c = fileText[j]
        if (c === '\\') { j += 2; continue }
        if (c === '\n') break
        if (c === '[') inClass = true
        else if (c === ']') inClass = false
        else if (c === '/' && !inClass) { j++; closed = true; break }
        j++
      }
      if (closed) {
        while (j < n && /[a-z]/i.test(fileText[j])) j++
        i = j
        continue
      }
      // keine schließende '/' in der Zeile gefunden -> war wohl doch keine
      // Regex (z.B. Division mit Zeilenumbruch danach) -> normal weiterlesen.
    }
    i++
  }
  return segments
}

export interface Pair { bg: string; text: string; files: Set<string> }

/** Sammelt bg/text-Klassenpaare, die in DERSELBEN Zeichenkette vorkommen,
 * aus allen .tsx/.ts-Dateien unter srcDir. `tokenRe` bestimmt, welche
 * Utility-Klassen als bg- und text-Varianten überhaupt erkannt werden
 * (Dark- und Light-Test nutzen dafür leicht unterschiedliche Muster). */
export function collectPairs(srcDir: string, tokenRe: RegExp): Map<string, Pair> {
  const pairs = new Map<string, Pair>()
  for (const file of walk(srcDir)) {
    const rel = path.relative(srcDir, file).replace(/\\/g, '/')
    const text = fs.readFileSync(file, 'utf8')
    for (const segment of extractSegments(text)) {
      const tokens = segment.match(tokenRe)
      if (!tokens) continue
      const bgTokens = [...new Set(tokens.filter((t) => /(?:^|:)bg-/.test(t)))]
      const textTokens = [...new Set(tokens.filter((t) => /(?:^|:)text-/.test(t)))]
      for (const bg of bgTokens) {
        for (const txt of textTokens) {
          const key = `${bg}|||${txt}`
          const existing = pairs.get(key)
          if (existing) existing.files.add(rel)
          else pairs.set(key, { bg, text: txt, files: new Set([rel]) })
        }
      }
    }
  }
  return pairs
}
