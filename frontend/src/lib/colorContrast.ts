// Reine Farbmathematik für die WCAG-Kontrastprüfung (kein UI-Code).
// Unterstützt genau die Notationen, die in index.css / workbench.css vorkommen:
// hex (#rgb, #rrggbb) und oklch(L% C H). Keine externe Abhängigkeit.

export interface LinearRgb { r: number; g: number; b: number }

function clamp01(x: number): number {
  return Math.min(1, Math.max(0, x))
}

// sRGB-EOTF: gamma-kodierten Kanal (0..1) in linear-Licht umrechnen.
function srgbChannelToLinear(c: number): number {
  return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)
}

export function hexToLinearRgb(hex: string): LinearRgb {
  let h = hex.trim().replace('#', '')
  if (h.length === 3) h = h.split('').map((c) => c + c).join('')
  const num = parseInt(h.slice(0, 6), 16)
  const r = ((num >> 16) & 0xff) / 255
  const g = ((num >> 8) & 0xff) / 255
  const b = (num & 0xff) / 255
  return {
    r: srgbChannelToLinear(r),
    g: srgbChannelToLinear(g),
    b: srgbChannelToLinear(b),
  }
}

// OKLab/OKLCH -> linear sRGB nach Björn Ottosson (https://bottosson.github.io/posts/oklab/).
export function oklchToLinearRgb(lPercent: number, c: number, hDeg: number): LinearRgb {
  const L = lPercent / 100
  const hRad = (hDeg * Math.PI) / 180
  const a = c * Math.cos(hRad)
  const b = c * Math.sin(hRad)

  const l_ = L + 0.3963377774 * a + 0.2158037573 * b
  const m_ = L - 0.1055613458 * a - 0.0638541728 * b
  const s_ = L - 0.0894841775 * a - 1.2914855480 * b

  const l = l_ ** 3
  const m = m_ ** 3
  const s = s_ ** 3

  const r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
  const g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
  const bl = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

  return { r: clamp01(r), g: clamp01(g), b: clamp01(bl) }
}

/** Erkennt hex- und oklch(...)-Notation und liefert lineares RGB (0..1 je Kanal). */
export function parseCssColorToLinearRgb(value: string): LinearRgb | null {
  const v = value.trim()
  const hexMatch = v.match(/^#[0-9a-fA-F]{3,8}$/)
  if (hexMatch) return hexToLinearRgb(v)
  // Alpha (z.B. "oklch(41% .16 10 / 60%)") wird ignoriert — wir werten die
  // Farbe als deckend (siehe Grenzen der Methode in darkContrast.test.ts).
  const oklchMatch = v.match(/^oklch\(\s*([\d.]+)%\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*[\d.]+%?)?\s*\)$/i)
  if (oklchMatch) {
    const [, l, c, h] = oklchMatch
    return oklchToLinearRgb(parseFloat(l), parseFloat(c), parseFloat(h))
  }
  if (v === 'white') return hexToLinearRgb('#ffffff')
  if (v === 'black') return hexToLinearRgb('#000000')
  return null
}

/** WCAG-relative Luminanz aus linearem RGB. */
export function relativeLuminance({ r, g, b }: LinearRgb): number {
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}

/** WCAG-Kontrastverhältnis zweier Farben (beliebige Reihenfolge). */
export function contrastRatio(a: LinearRgb, b: LinearRgb): number {
  const la = relativeLuminance(a)
  const lb = relativeLuminance(b)
  const lighter = Math.max(la, lb)
  const darker = Math.min(la, lb)
  return (lighter + 0.05) / (darker + 0.05)
}

/** Bequemer Einstieg: Kontrast zweier CSS-Farbstrings (hex oder oklch). */
export function contrastRatioForColors(fg: string, bg: string): number | null {
  const a = parseCssColorToLinearRgb(fg)
  const b = parseCssColorToLinearRgb(bg)
  if (!a || !b) return null
  return contrastRatio(a, b)
}
