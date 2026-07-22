import { useEffect, useState } from 'react'
import { toHex, hexDiffPositions, bitDifference } from '@/widgets/pki/hash'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

type Algo = 'SHA-1' | 'SHA-256' | 'SHA-384' | 'SHA-512'
const ALGOS: Algo[] = ['SHA-1', 'SHA-256', 'SHA-384', 'SHA-512']

const DEFAULT_TEXT = 'Nordwind Logistik GmbH'

const STR = {
  de: {
    title: 'Hashfunktionen — Fingerabdruck für Daten',
    subtitle: 'Ein Hash ist eine Einwegfunktion: aus beliebig langen Daten wird ein Digest fester Länge. '
      + 'Gleiche Eingabe → immer gleicher Digest. Schon ein Zeichen Unterschied → komplett anderer Digest.',
    textLabel: 'Text',
    algoLabel: 'Hash-Algorithmus',
    digestLabel: 'Digest (Hex)',
    computing: 'Berechne…',
    sha1Warning: 'SHA-1 gilt für Signaturen und Zertifikate als gebrochen — es gibt praktisch durchführbare '
      + 'Kollisionsangriffe. Es steht hier nur zu Demonstrationszwecken; für neue Systeme SHA-256 oder stärker verwenden.',
    avalancheTitle: 'Lawineneffekt',
    avalancheHint: 'Ändere den zweiten Text um ein einziges Zeichen und beobachte, wie stark sich der Digest ändert.',
    variantLabel: 'Variante des Texts',
    digest1Label: 'Digest 1',
    digest2Label: 'Digest 2',
    bitsDiffLabel: 'Unterschiedliche Bits',
    ofTotal: 'von',
    challenge: 'Mach die beiden Texte unterschiedlich (z.B. ein Zeichen ändern) und beobachte den Lawineneffekt im Digest.',
  },
  en: {
    title: 'Hash functions — a fingerprint for data',
    subtitle: 'A hash is a one-way function: arbitrary-length data becomes a fixed-length digest. '
      + 'Same input → always the same digest. A single character of difference → a completely different digest.',
    textLabel: 'Text',
    algoLabel: 'Hash algorithm',
    digestLabel: 'Digest (hex)',
    computing: 'Computing…',
    sha1Warning: 'SHA-1 is considered broken for signatures and certificates — practical collision attacks exist. '
      + "It's included here for demonstration only; use SHA-256 or stronger for new systems.",
    avalancheTitle: 'Avalanche effect',
    avalancheHint: 'Change the second text by a single character and watch how much the digest changes.',
    variantLabel: 'Variant of the text',
    digest1Label: 'Digest 1',
    digest2Label: 'Digest 2',
    bitsDiffLabel: 'Differing bits',
    ofTotal: 'of',
    challenge: 'Make the two texts different (e.g. change one character) and observe the avalanche effect in the digest.',
  },
} as const

function useDigest(text: string, algo: Algo): string {
  const [digest, setDigest] = useState('')
  useEffect(() => {
    let cancelled = false
    async function run() {
      const bytes = new TextEncoder().encode(text)
      const buffer = await crypto.subtle.digest(algo, bytes)
      if (!cancelled) setDigest(toHex(buffer))
    }
    run()
    return () => { cancelled = true }
  }, [text, algo])
  return digest
}

function DigestView({ digest, diffPositions }: { digest: string; diffPositions: Set<number> }) {
  if (!digest) return null
  return (
    <p className="break-all font-mono text-xs">
      {digest.split('').map((ch, i) => (
        <span key={i} className={diffPositions.has(i) ? 'bg-rose-200 text-rose-900' : 'text-slate-800'}>
          {ch}
        </span>
      ))}
    </p>
  )
}

export function HashLab({ lang }: { lang: Lang }) {
  const [text, setText] = useState(DEFAULT_TEXT)
  const [variant, setVariant] = useState(DEFAULT_TEXT)
  const [algo, setAlgo] = useState<Algo>('SHA-256')
  const s = STR[lang]

  const digest = useDigest(text, algo)
  const digestVariant = useDigest(variant, algo)

  const diffPositions = new Set(digest && digestVariant ? hexDiffPositions(digest, digestVariant) : [])
  const bitDiff = digest && digestVariant ? bitDifference(digest, digestVariant) : null

  const done = text !== variant && digest !== '' && digestVariant !== '' && digest !== digestVariant

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <label htmlFor="hash-text" className="mb-1 block text-xs font-semibold text-slate-500">{s.textLabel}</label>
      <input
        id="hash-text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="mb-3 w-full rounded-lg border border-slate-300 px-3 py-1.5 text-sm outline-none focus:border-teal-500"
      />

      <label htmlFor="hash-algo" className="mb-1 block text-xs font-semibold text-slate-500">{s.algoLabel}</label>
      <select
        id="hash-algo"
        value={algo}
        onChange={(e) => setAlgo(e.target.value as Algo)}
        className="mb-3 rounded-lg border border-slate-300 px-3 py-1.5 text-sm outline-none focus:border-teal-500"
      >
        {ALGOS.map((a) => <option key={a} value={a}>{a}</option>)}
      </select>

      <p className="mb-1 text-xs font-semibold text-slate-500">{s.digestLabel}</p>
      <div className="mb-1 rounded-lg border border-slate-200 bg-slate-50 p-3" aria-live="polite">
        {digest ? <p className="break-all font-mono text-xs text-slate-800">{digest}</p> : <p className="text-xs text-slate-400">{s.computing}</p>}
      </div>

      {algo === 'SHA-1' && (
        <p className="mb-3 rounded-lg border border-amber-200 bg-amber-50 p-3 text-xs text-amber-900">{s.sha1Warning}</p>
      )}

      <hr className="my-4 border-slate-200" />

      <p className="mb-1 text-sm font-semibold text-slate-700">{s.avalancheTitle}</p>
      <p className="mb-3 text-xs text-slate-500">{s.avalancheHint}</p>

      <label htmlFor="hash-variant" className="mb-1 block text-xs font-semibold text-slate-500">{s.variantLabel}</label>
      <input
        id="hash-variant"
        value={variant}
        onChange={(e) => setVariant(e.target.value)}
        className="mb-3 w-full rounded-lg border border-slate-300 px-3 py-1.5 text-sm outline-none focus:border-teal-500"
      />

      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3" aria-live="polite">
        <p className="mb-1 text-xs font-semibold text-slate-500">{s.digest1Label}</p>
        <DigestView digest={digest} diffPositions={diffPositions} />
        <p className="mt-2 mb-1 text-xs font-semibold text-slate-500">{s.digest2Label}</p>
        <DigestView digest={digestVariant} diffPositions={diffPositions} />
        {bitDiff && (
          <p className="mt-2 text-xs text-slate-600">
            {s.bitsDiffLabel}: <span className="font-semibold text-teal-700">{bitDiff.bits}</span> {s.ofTotal} {bitDiff.total}
            {' '}({bitDiff.percent.toFixed(1)}%)
          </p>
        )}
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={done} />
    </div>
  )
}
