import { useState } from 'react'
import { publicValue, sharedSecret, bruteForceExponent } from '@/widgets/pki/keyexchange'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

// Lehrbuch-Spielzeuggröße — echte Diffie-Hellman-Gruppen nutzen 2048-Bit-Primzahlen
// oder elliptische Kurven wie X25519. Hier klein genug, um mitzurechnen und um
// Eve per Brute-Force in Millisekunden gewinnen zu lassen.
const P = 23
const G = 5

const STR = {
  de: {
    title: 'Diffie-Hellman — ein Geheimnis, nie übertragen',
    subtitle: `Alice und Bob einigen sich über eine offene, abgehörte Leitung auf ein gemeinsames `
      + `Geheimnis. Spielzeuggröße zum Mitrechnen: p = ${P}, g = ${G}. Echte Verfahren nutzen `
      + '2048-Bit-Gruppen oder elliptische Kurven wie X25519.',
    aliceSecret: 'Alices geheimes a', bobSecret: 'Bobs geheimes b',
    publicValues: 'Öffentlich ausgetauschte Werte',
    sharedSecrets: 'Berechnete gemeinsame Geheimnisse',
    sA: 'Alice berechnet s_A = B^a mod p', sB: 'Bob berechnet s_B = A^b mod p',
    match: 'Beide Seiten haben dasselbe Geheimnis erreicht — ohne es je zu übertragen.',
    noMatch: 'Stimmt noch nicht überein (sollte mathematisch nie vorkommen).',
    eveToggle: 'Angreifersicht öffnen: „Was Eve auf der Leitung sieht“',
    eveTitle: 'Was Eve auf der Leitung sieht',
    eveHint: 'Eve kennt nur die öffentlich übertragenen Werte — nicht a, b oder das Geheimnis.',
    eveButton: 'Eve rechnet durch (Brute-Force über alle 22 Möglichkeiten)',
    eveFound: (a: number) => `Eve hat a = ${a} gefunden — bei p = ${P} sind das nur ${P - 2} Versuche.`,
    eveReality: 'Bei einer echten 2048-Bit-Gruppe oder X25519 ist dieses Durchprobieren '
      + 'rechnerisch unmöglich — die Anzahl der Möglichkeiten übersteigt jede verfügbare Rechenleistung.',
    pfsTitle: 'Perfect Forward Secrecy',
    pfsText: 'Wird für jede Sitzung ein neuer, flüchtiger (ephemeraler) Schlüsseltausch wie dieser '
      + 'durchgeführt, macht ein später kompromittierter Server-Langzeitschlüssel alte, '
      + 'aufgezeichnete Sitzungen nicht nachträglich lesbar — dafür steht das „E“ in ECDHE.',
    challenge: 'Bring beide Seiten auf dasselbe Geheimnis und öffne die Angreifersicht.',
  },
  en: {
    title: 'Diffie-Hellman — a secret that never travels',
    subtitle: `Alice and Bob agree on a shared secret over an open, wiretapped line. Toy size to `
      + `follow along: p = ${P}, g = ${G}. Real schemes use 2048-bit groups or elliptic curves `
      + 'such as X25519.',
    aliceSecret: "Alice's secret a", bobSecret: "Bob's secret b",
    publicValues: 'Publicly exchanged values',
    sharedSecrets: 'Computed shared secrets',
    sA: 'Alice computes s_A = B^a mod p', sB: 'Bob computes s_B = A^b mod p',
    match: 'Both sides reached the same secret — without ever transmitting it.',
    noMatch: 'Not matching yet (mathematically this should never happen).',
    eveToggle: 'Open attacker view: "What Eve sees on the wire"',
    eveTitle: 'What Eve sees on the wire',
    eveHint: 'Eve only knows the publicly transmitted values — not a, b, or the secret.',
    eveButton: 'Have Eve brute-force it (tries all 22 possibilities)',
    eveFound: (a: number) => `Eve found a = ${a} — with p = ${P} that is only ${P - 2} attempts.`,
    eveReality: 'With a real 2048-bit group or X25519, this brute-force search is computationally '
      + 'impossible — the number of possibilities exceeds any available computing power.',
    pfsTitle: 'Perfect Forward Secrecy',
    pfsText: 'If every session performs a fresh, ephemeral key exchange like this one, a later '
      + 'compromise of the server’s long-term key does not make old, recorded sessions '
      + 'readable in hindsight — that is the "E" in ECDHE.',
    challenge: 'Bring both sides to the same secret and open the attacker view.',
  },
} as const

export function KeyExchange({ lang }: { lang: Lang }) {
  const [a, setA] = useState(6)
  const [b, setB] = useState(15)
  const [eveOpen, setEveOpen] = useState(false)
  const [eveFoundA, setEveFoundA] = useState<number | null>(null)
  const s = STR[lang]

  const A = publicValue(G, a, P)
  const B = publicValue(G, b, P)
  const sA = sharedSecret(B, a, P)
  const sB = sharedSecret(A, b, P)
  const match = sA === sB

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
        <label htmlFor="pki-a-slider" className="block text-xs text-slate-600">
          {s.aliceSecret}: <span className="font-mono font-semibold text-teal-700">{a}</span>
          <input
            id="pki-a-slider"
            type="range" min={1} max={22} value={a}
            onChange={(e) => setA(Number(e.target.value))}
            className="mt-1 w-full accent-teal-600"
          />
        </label>
        <label htmlFor="pki-b-slider" className="block text-xs text-slate-600">
          {s.bobSecret}: <span className="font-mono font-semibold text-teal-700">{b}</span>
          <input
            id="pki-b-slider"
            type="range" min={1} max={22} value={b}
            onChange={(e) => setB(Number(e.target.value))}
            className="mt-1 w-full accent-teal-600"
          />
        </label>
      </div>

      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-xs font-mono mb-3" aria-live="polite">
        <p className="text-slate-500 font-sans font-semibold mb-1 not-italic">{s.publicValues}</p>
        <p className="text-slate-700">p = {P}, g = {G}</p>
        <p className="text-slate-700">A = g^a mod p = {A}</p>
        <p className="text-slate-700">B = g^b mod p = {B}</p>
      </div>

      <div
        className={`rounded-lg border p-3 text-xs font-mono mb-1 ${
          match ? 'border-green-300 bg-green-50' : 'border-rose-300 bg-rose-50'
        }`}
        aria-live="polite"
      >
        <p className="text-slate-500 font-sans font-semibold mb-1 not-italic">{s.sharedSecrets}</p>
        <p className="text-slate-700">{s.sA} = {sA}</p>
        <p className="text-slate-700">{s.sB} = {sB}</p>
        <p className={`mt-1 font-sans font-semibold not-italic ${match ? 'text-green-700' : 'text-rose-700'}`}>
          {match ? `✓ ${s.match}` : `✗ ${s.noMatch}`}
        </p>
      </div>

      <div className="mt-4 rounded-lg border border-slate-200 bg-slate-50 p-3">
        <label className="flex items-center gap-2 text-sm font-medium text-slate-700">
          <input type="checkbox" checked={eveOpen} onChange={(e) => setEveOpen(e.target.checked)} />
          {s.eveToggle}
        </label>
        {eveOpen && (
          <div className="mt-2">
            <p className="text-xs font-semibold text-slate-500 mb-1">{s.eveTitle}</p>
            <div className="rounded-lg border border-rose-200 bg-rose-50 p-3 text-xs font-mono mb-2">
              <p className="text-slate-700">p = {P}, g = {G}, A = {A}, B = {B}</p>
            </div>
            <p className="text-xs text-slate-500 mb-2 font-sans">{s.eveHint}</p>
            <button
              onClick={() => setEveFoundA(bruteForceExponent(G, A, P))}
              className="rounded-lg border border-rose-300 px-3 py-1.5 text-sm font-medium text-rose-700 hover:bg-rose-50"
            >
              {s.eveButton}
            </button>
            {eveFoundA !== null && (
              <div className="mt-2 text-xs" aria-live="polite">
                <p className="text-rose-700 font-semibold">{s.eveFound(eveFoundA)}</p>
                <p className="mt-1 text-slate-500">{s.eveReality}</p>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="mt-4 rounded-lg border border-teal-200 bg-teal-50/60 p-3 text-xs text-teal-900">
        <span className="font-semibold">{s.pfsTitle}:</span> {s.pfsText}
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={match && eveOpen} />
    </div>
  )
}
