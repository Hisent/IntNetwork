import { useState } from 'react'
import { TLS12_STEPS, TLS13_STEPS, roundtripCount } from '@/widgets/pki/handshake'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'TLS-Handshake — 1.2 vs. 1.3',
    subtitle: 'Klicke Schritt für Schritt durch beide Versionen. Der zentrale Unterschied: '
      + 'TLS 1.2 braucht zwei Roundtrips bis zu den ersten Anwendungsdaten, TLS 1.3 nur einen.',
    tls12: 'TLS 1.2', tls13: 'TLS 1.3',
    step: 'Schritt', of: 'von',
    prev: 'Zurück', next: 'Nächster Schritt',
    client: 'Client', server: 'Server',
    encrypted: 'verschlüsselt', plaintext: 'im Klartext',
    roundtrip: 'Roundtrip',
    summaryTitle: 'Zusammenfassung',
    summary12: 'TLS 1.2 überträgt das Server-Zertifikat im Klartext und braucht zwei Roundtrips, '
      + 'bevor Anwendungsdaten fließen können.',
    summary13: 'TLS 1.3 entfernt die statische RSA-Schlüsselübertragung ohne Forward Secrecy, '
      + 'unsichere Cipher Suites, Kompression und Renegotiation. Ab ServerHello läuft alles '
      + 'Weitere verschlüsselt — inklusive des Zertifikats, das in TLS 1.2 noch im Klartext geht. '
      + 'Ergebnis: nur noch ein Roundtrip bis zu den ersten Anwendungsdaten.',
    challenge: 'Klicke dich einmal komplett durch TLS 1.2 und einmal durch TLS 1.3.',
  },
  en: {
    title: 'TLS handshake — 1.2 vs. 1.3',
    subtitle: 'Step through both versions one message at a time. The key difference: TLS 1.2 '
      + 'needs two roundtrips before the first application data, TLS 1.3 needs only one.',
    tls12: 'TLS 1.2', tls13: 'TLS 1.3',
    step: 'Step', of: 'of',
    prev: 'Back', next: 'Next step',
    client: 'Client', server: 'Server',
    encrypted: 'encrypted', plaintext: 'in cleartext',
    roundtrip: 'Roundtrip',
    summaryTitle: 'Summary',
    summary12: 'TLS 1.2 sends the server certificate in cleartext and needs two roundtrips '
      + 'before application data can flow.',
    summary13: 'TLS 1.3 removes static RSA key transport without forward secrecy, insecure '
      + 'cipher suites, compression, and renegotiation. From ServerHello onward, everything '
      + 'else is encrypted — including the certificate, which TLS 1.2 still sends in cleartext. '
      + 'Result: only one roundtrip before the first application data.',
    challenge: 'Click all the way through TLS 1.2 once and through TLS 1.3 once.',
  },
} as const

type Version = 'tls12' | 'tls13'

export function TlsHandshake({ lang }: { lang: Lang }) {
  const [version, setVersion] = useState<Version>('tls12')
  const [idx12, setIdx12] = useState(0)
  const [idx13, setIdx13] = useState(0)
  const [visited12, setVisited12] = useState<Set<number>>(() => new Set([0]))
  const [visited13, setVisited13] = useState<Set<number>>(() => new Set([0]))
  const s = STR[lang]

  const steps = version === 'tls12' ? TLS12_STEPS : TLS13_STEPS
  const idx = version === 'tls12' ? idx12 : idx13
  const setIdx = version === 'tls12' ? setIdx12 : setIdx13
  const setVisited = version === 'tls12' ? setVisited12 : setVisited13
  const step = steps[idx]
  const totalRoundtrips = roundtripCount(steps)

  const done12 = visited12.size >= TLS12_STEPS.length
  const done13 = visited13.size >= TLS13_STEPS.length

  const goNext = () => {
    const ni = Math.min(idx + 1, steps.length - 1)
    setIdx(ni)
    setVisited((prev) => new Set(prev).add(ni))
  }
  const goPrev = () => setIdx(Math.max(idx - 1, 0))

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <div className="flex gap-2 mb-4" role="radiogroup" aria-label={`${s.tls12} / ${s.tls13}`}>
        <button
          role="radio"
          aria-checked={version === 'tls12'}
          onClick={() => setVersion('tls12')}
          className={`rounded-lg px-3 py-1.5 text-sm font-medium border transition-colors ${
            version === 'tls12'
              ? 'bg-teal-600 border-teal-600 text-white'
              : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
          }`}
        >
          {s.tls12} {done12 && '✓'}
        </button>
        <button
          role="radio"
          aria-checked={version === 'tls13'}
          onClick={() => setVersion('tls13')}
          className={`rounded-lg px-3 py-1.5 text-sm font-medium border transition-colors ${
            version === 'tls13'
              ? 'bg-teal-600 border-teal-600 text-white'
              : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
          }`}
        >
          {s.tls13} {done13 && '✓'}
        </button>
      </div>

      <p className="text-xs text-slate-500 mb-2">
        {s.step} {idx + 1} {s.of} {steps.length}
        <span className="ml-3 rounded bg-slate-100 px-2 py-0.5 font-medium text-slate-600">
          {s.roundtrip} {step.roundtrip} {s.of} {totalRoundtrips}
        </span>
      </p>

      <div
        className={`rounded-lg border-2 p-3 mb-3 ${
          step.encrypted ? 'border-teal-300 bg-teal-50/60' : 'border-amber-300 bg-amber-50'
        }`}
        aria-live="polite"
      >
        <p className="text-xs font-semibold text-slate-600 mb-1">
          {step.from === 'client' ? `${s.client} → ${s.server}` : `${s.server} → ${s.client}`}
          <span className={`ml-2 rounded px-1.5 py-0.5 text-[10px] ${
            step.encrypted ? 'bg-teal-200 text-teal-800' : 'bg-amber-200 text-amber-800'
          }`}>
            {step.encrypted ? `🔒 ${s.encrypted}` : `🔓 ${s.plaintext}`}
          </span>
        </p>
        <p className="font-mono text-sm text-slate-800 mb-1">{step.name}</p>
        <p className="text-xs text-slate-600">{step.detail[lang]}</p>
      </div>

      <div className="flex gap-2 mb-4">
        <button
          onClick={goPrev}
          disabled={idx === 0}
          className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-default"
        >
          {s.prev}
        </button>
        <button
          onClick={goNext}
          disabled={idx === steps.length - 1}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium disabled:opacity-40 disabled:cursor-default"
        >
          {s.next}
        </button>
      </div>

      {idx === steps.length - 1 && (
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-xs text-slate-700 mb-1">
          <p className="font-semibold text-slate-600 mb-1">{s.summaryTitle} — {version === 'tls12' ? s.tls12 : s.tls13}</p>
          <p>{version === 'tls12' ? s.summary12 : s.summary13}</p>
        </div>
      )}

      <ChallengeBox lang={lang} task={s.challenge} done={done12 && done13} />
    </div>
  )
}
