export interface Tok {
  text: string
  kind: 'word' | 'space' | 'punct'
}

// Grobe, deterministische Heuristik (KEIN echtes BPE): Wörter in ~4-Zeichen-
// Stücke zerlegen, Whitespace-Läufe und einzelne Satz-/Code-Zeichen als eigene
// Tokens. Reicht, um sichtbar zu machen: Umlaute/lange Bezeichner = mehr Tokens,
// Symbole zählen einzeln.
export function tokenize(text: string): Tok[] {
  const toks: Tok[] = []
  const re = /([A-Za-z0-9ÄÖÜäöüß]+)|([ \t\n]+)|([^A-Za-z0-9ÄÖÜäöüß \t\n])/g
  let m: RegExpExecArray | null
  while ((m = re.exec(text)) !== null) {
    if (m[1]) {
      const word = m[1]
      for (let k = 0; k < word.length; k += 4) {
        toks.push({ text: word.slice(k, k + 4), kind: 'word' })
      }
    } else if (m[2]) {
      toks.push({ text: m[2], kind: 'space' })
    } else if (m[3]) {
      toks.push({ text: m[3], kind: 'punct' })
    }
  }
  return toks
}

export function tokenCount(text: string): number {
  return tokenize(text).length
}
