export interface Tok {
  text: string
  kind: 'word' | 'space' | 'punct'
}

// Grobe, deterministische Heuristik (KEIN echtes BPE): ASCII-Läufe in ~4-Zeichen-
// Stücke zerlegen, Whitespace-Läufe und einzelne Satz-/Code-Zeichen als eigene
// Tokens. Umlaute und ß stehen je als eigenes Token und zerteilen das Wort –
// so wird sichtbar: Umlaute/lange Bezeichner = mehr Tokens, Symbole zählen einzeln.
// ponytail: überzeichnet (echte Tokenizer fassen häufige deutsche Wörter zusammen);
// für exakte Zahlen einen echten Tokenizer/die Token-Counting-API nehmen.
export function tokenize(text: string): Tok[] {
  const toks: Tok[] = []
  const re = /([A-Za-z0-9ÄÖÜäöüß]+)|([ \t\n]+)|([^A-Za-z0-9ÄÖÜäöüß \t\n])/g
  let m: RegExpExecArray | null
  while ((m = re.exec(text)) !== null) {
    if (m[1]) {
      const word = m[1]
      for (const piece of word.match(/[A-Za-z0-9]{1,4}|[^A-Za-z0-9]/g) ?? []) {
        toks.push({ text: piece, kind: 'word' })
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
