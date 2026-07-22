// Guard-Test gegen "lautlos gebrochenes Theming": Es gibt zwei Theming-Wege
// in dieser App — --wb-*/--workshop-*-Tokens UND hartkodierte teal-*-
// Tailwind-Klassen in Widgets/Kursbereich. Die teal-*-Klassen werden für die
// 4 Nicht-Netzwerk-Kurse per Override-Block in index.css
// (".workshop-theme:not(.workshop-theme--network) .bg-teal-600 {…}" usw.)
// auf die jeweilige Kursakzentfarbe umgeschrieben. Nutzt ein Widget eine
// teal-*-Variante, die dort NICHT gelistet ist (wie zuletzt border-teal-300),
// bricht das Theming in den 4 Nicht-Netzwerk-Kursen lautlos — die Fläche/der
// Text bleibt teal statt der Kursfarbe zu folgen, ohne dass irgendetwas
// crasht oder eine Warnung zeigt.
//
// Wichtig: Der Override-Block überschreibt keine CSS-Variable, sondern jede
// einzelne kompilierte Tailwind-Klasse für sich (siehe die Kommentare in
// index.css über dem Block). Varianten-Präfixe (hover:, focus:, dark: usw.)
// erzeugen JEWEILS eine eigene kompilierte Klasse — "text-teal-800" im
// Override deckt "hover:text-teal-800" NICHT automatisch mit ab. Deshalb prüft
// dieser Test auf EXAKTE Übereinstimmung, keine Basis-Klassen-Fallbacks (im
// Gegensatz zu darkContrast.test.ts, wo eine echte CSS-Variablen-Spiegelung
// vorliegt und Fallbacks deshalb korrekt sind).

/// <reference types="node" />
import { describe, expect, it } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { extractSegments, stripComments, walk } from './contrastScan'

const here = path.dirname(fileURLToPath(import.meta.url))
const SRC_DIR = path.resolve(here, '..')
const INDEX_CSS_PATH = path.resolve(SRC_DIR, 'index.css')

// ---------------------------------------------------------------------------
// 1) Alle teal-*-Utility-Klassen aus dem Code einsammeln (inkl. Varianten-
//    Präfixen wie hover:/focus:/dark:/print:/focus-visible: und Opacity-
//    Varianten wie bg-teal-50/60).
// ---------------------------------------------------------------------------

const TEAL_PREFIXES = 'accent|bg|text|border|ring|from|to|outline|divide|decoration|caret|fill|stroke|shadow'
const TEAL_TOKEN_RE = new RegExp(
  `(?:[\\w-]+:)*(?:${TEAL_PREFIXES})-teal-\\d{2,3}(?:/\\d{1,3})?`,
  'g',
)

interface Usage { className: string; files: Set<string> }

function collectTealUsages(): Map<string, Usage> {
  const usages = new Map<string, Usage>()
  for (const file of walk(SRC_DIR)) {
    const rel = path.relative(SRC_DIR, file).replace(/\\/g, '/')
    const text = fs.readFileSync(file, 'utf8')
    for (const segment of extractSegments(text)) {
      const tokens = segment.match(TEAL_TOKEN_RE)
      if (!tokens) continue
      for (const className of new Set(tokens)) {
        const existing = usages.get(className)
        if (existing) existing.files.add(rel)
        else usages.set(className, { className, files: new Set([rel]) })
      }
    }
  }
  return usages
}

// ---------------------------------------------------------------------------
// 2) Die tatsächlich im Workshop-Override-Block umgeschriebenen teal-Klassen
//    aus index.css parsen (nur der
//    ".workshop-theme:not(.workshop-theme--network) .<klasse>"-Block).
// ---------------------------------------------------------------------------

function parseWorkshopTealAllowlist(css: string): Set<string> {
  const clean = stripComments(css)
  const allowlist = new Set<string>()
  const selectorRe = /\.workshop-theme:not\(\.workshop-theme--network\)\s+\.([^\s,{]+)/g
  for (const m of clean.matchAll(selectorRe)) {
    const utilityClass = m[1]
      .replace(/\\:/g, ':')
      .replace(/\\\//g, '/')
      // Tailwind hängt die Pseudoklasse zusätzlich an (".hover\:bg-x:hover")
      // — der rohe Utility-Name im JSX ("hover:bg-x") hat das nicht.
      .replace(/:(hover|focus|focus-visible|active|disabled)$/, '')
    if (/-teal-/.test(utilityClass)) allowlist.add(utilityClass)
  }
  return allowlist
}

// ---------------------------------------------------------------------------
// 3) "Netzwerk-Kurs-exklusiv" wird mechanisch über den Datei-Pfad erkannt:
//    Diese Widget-Dateien/-Ordner werden AUSSCHLIESSLICH über Netzwerk-Kurs-
//    Module gerendert (siehe widgets/registry.tsx: vlan-switch, frame-
//    builder, osi-model, mac-learning, subnet-calc, arp-demo, routing-demo,
//    nat-demo, dns-demo, dhcp-demo, ports-demo, icmp-demo, firewall-demo,
//    ipv6-demo, wlan-demo, vpn-demo, troubleshoot-demo, capstone-demo,
//    wireshark-demo, ospf-demo, redundancy-demo, learning-*, visual-*) — sie
//    laufen nie unter .workshop-theme--claude/--infoblox/--ansible/--pki,
//    darum bricht dort nichts, wenn eine teal-Klasse nicht in der Allowlist
//    steht. ACHTUNG: reine Pfad-Heuristik, keine Laufzeit-Analyse — wenn ein
//    Widget aus dieser Liste künftig auch in einem anderen Kurs eingebunden
//    wird, muss diese Liste mitgepflegt werden.
// ---------------------------------------------------------------------------

const NETWORK_EXCLUSIVE_RE = new RegExp(
  '^widgets/(?:' +
  [
    'VlanSwitch\\.tsx',
    'FrameBuilder\\.tsx',
    'osi/',
    'switch/',
    'subnet/',
    'arp/',
    'router/',
    'nat/',
    'dns/',
    'dhcp/',
    'ports/',
    'icmp/',
    'firewall/',
    'ipv6/',
    'wlan/',
    'vpn/',
    'troubleshoot/',
    'capstone/',
    'wireshark/',
    'ospf/',
    'redundancy/',
    'learning/',
    'visuals/',
  ].join('|') +
  ')',
)

function isNetworkExclusive(files: Set<string>): boolean {
  return [...files].every((f) => NETWORK_EXCLUSIVE_RE.test(f))
}

describe('Workshop-Theme-Allowlist (teal-* muss in index.css überschrieben werden)', () => {
  const usages = [...collectTealUsages().values()]
  expect(usages.length).toBeGreaterThan(10) // Sanity-Check: Extraktion findet überhaupt etwas

  const allowlist = parseWorkshopTealAllowlist(fs.readFileSync(INDEX_CSS_PATH, 'utf8'))
  expect(allowlist.size).toBeGreaterThan(5) // Sanity-Check: Override-Block wird gefunden

  // Bewusste Ausnahmen: teal-Klassen, die NIE unter einem
  // .workshop-theme-Wrapper gerendert werden — dort kann der Override gar nicht
  // greifen, also ist das Fehlen einer Regel kein Bruch.
  const KNOWN_EXCEPTIONS = new Set([
    // Skip-Link in App.tsx: steht vor dem Router-Outlet, ausserhalb jeder Seite
    // und damit ausserhalb jedes .workshop-theme-Wrappers.
    'focus:bg-teal-600',
  ])

  it('jede verwendete teal-Klasse (außerhalb des Netzwerkkurses) hat eine Override-Regel', () => {
    const gaps: string[] = []
    for (const { className, files } of usages) {
      if (allowlist.has(className)) continue
      if (KNOWN_EXCEPTIONS.has(className)) continue
      if (isNetworkExclusive(files)) continue // nur im Netzwerkkurs -> teal ist dort die Originalfarbe
      gaps.push(
        `teal-Klasse "${className}" wird verwendet (${[...files].join(', ')}), fehlt aber im ` +
        `Workshop-Override in index.css → bricht Theming in Nicht-Netzwerk-Kursen lautlos.`,
      )
    }
    expect(gaps, gaps.join('\n')).toEqual([])
  })
})
