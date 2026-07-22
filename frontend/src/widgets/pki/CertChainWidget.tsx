import { useState } from 'react'
import { validateChain, CHAIN_POOL, TRUST_STORE, DEMO_NOW, type Cert, type ChainProblem } from '@/widgets/pki/certs'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'Vertrauenskette bauen — vom Serverzertifikat bis zur Root',
    subtitle: 'Klicke Zertifikatskarten an, um eine Kette Leaf → Intermediate → Root zusammenzustellen, und prüfe sie.',
    poolLabel: 'Verfügbare Zertifikate (anklicken zum Hinzufügen/Entfernen)',
    chainLabel: 'Deine Kette (in dieser Reihenfolge geprüft)',
    chainEmpty: 'Noch keine Zertifikate ausgewählt.',
    check: 'Kette prüfen',
    removeHint: 'anklicken zum Entfernen',
    resultOk: {
      title: '✓ Kette vollständig und gültig',
      text: 'Jedes Glied passt zum nächsten (Issuer = Subject), das letzte Glied ist selbstsigniert und liegt im Trust Store, und kein Zertifikat ist zeitlich abgelaufen. Genau so validiert auch ein Browser oder curl eine TLS-Verbindung.',
    },
    results: {
      incomplete: {
        title: '✗ Kette unvollständig',
        text: 'Die Kette bricht ab, ohne einen Vertrauensanker im Trust Store zu erreichen — es fehlt (mindestens) ein Glied. Das ist der klassische „funktioniert im Browser, aber nicht mit curl/Java“-Fall: Browser cachen bereits gesehene Intermediates oder laden sie automatisch nach (Authority Information Access) und bauen die Kette so trotzdem zusammen. curl, openssl s_client und viele Java-Clients tun das nicht — sie verifizieren strikt nur, was tatsächlich vorliegt.',
      },
      'issuer-mismatch': {
        title: '✗ Issuer passt nicht zum Subject des nächsten Zertifikats',
        text: 'Zwei aufeinanderfolgende Kettenglieder passen nicht zueinander: Der Issuer-Eintrag des einen stimmt nicht mit dem Subject des nächsten überein. Damit lässt sich keine durchgängige Signaturprüfung aufbauen — meist, weil ein Zertifikat einer falschen/fremden CA in die Kette geraten ist.',
      },
      'untrusted-root': {
        title: '✗ Wurzel nicht im Trust Store',
        text: 'Die Kette ist strukturell in Ordnung und endet in einem selbstsignierten Zertifikat — aber genau dieses Root-Zertifikat liegt nicht im Trust Store des Clients. Das passiert z. B. bei privaten/internen CAs, deren Root nie importiert wurde, oder bei einem längst durch ein neueres Root abgelösten, alten Root-Zertifikat.',
      },
      'expired-link': {
        title: '✗ Ein Glied der Kette ist abgelaufen',
        text: 'Mindestens ein Zertifikat in der Kette liegt außerhalb seines Gültigkeitszeitraums (notBefore/notAfter). Selbst eine sonst technisch perfekte Kette gilt dann als ungültig.',
      },
    } as Record<ChainProblem, { title: string; text: string }>,
    whyOffline: {
      title: 'Warum liegt die Root-CA offline?',
      text: 'Die Root-CA wird nach der Ausstellung ihrer Intermediates offline genommen und in einem Tresor verwahrt — das tägliche Ausstellungsgeschäft übernimmt das Intermediate. Wird ein Intermediate kompromittiert, lässt es sich einfach widerrufen und durch ein neues ersetzen, ohne dass irgendjemandes Vertrauensanker (die Root) angetastet werden muss. Eine kompromittierte Root dagegen wäre praktisch nicht widerrufbar: Sie steckt in unzähligen Trust Stores weltweit, ein Austausch dort ist langwierig bis unmöglich.',
    },
    challenge: 'Stelle eine vollständige, gültige Kette zusammen und prüfe sie erfolgreich.',
  },
  en: {
    title: 'Build a trust chain — from server certificate to root',
    subtitle: 'Click certificate cards to assemble a chain Leaf → Intermediate → Root, then validate it.',
    poolLabel: 'Available certificates (click to add/remove)',
    chainLabel: 'Your chain (validated in this order)',
    chainEmpty: 'No certificates selected yet.',
    check: 'Validate chain',
    removeHint: 'click to remove',
    resultOk: {
      title: '✓ Chain complete and valid',
      text: 'Every link matches the next one (issuer = subject), the last link is self-signed and present in the trust store, and no certificate has expired. This is exactly how a browser or curl validates a TLS connection.',
    },
    results: {
      incomplete: {
        title: '✗ Chain incomplete',
        text: 'The chain stops without reaching a trust anchor in the trust store — at least one link is missing. This is the classic “works in the browser, but not with curl/Java” case: browsers cache intermediates they’ve already seen or fetch them automatically (Authority Information Access) and still complete the chain. curl, openssl s_client, and many Java clients do not — they strictly verify only what is actually present.',
      },
      'issuer-mismatch': {
        title: '✗ Issuer does not match the next certificate’s subject',
        text: 'Two consecutive links in the chain don’t fit together: one certificate’s issuer entry does not match the next one’s subject. That breaks the signature-verification chain — usually because a certificate from the wrong/a different CA ended up in the chain.',
      },
      'untrusted-root': {
        title: '✗ Root not in the trust store',
        text: 'The chain is structurally fine and ends in a self-signed certificate — but that exact root certificate is not present in the client’s trust store. This happens e.g. with private/internal CAs whose root was never imported, or with an old root certificate long since replaced by a newer one.',
      },
      'expired-link': {
        title: '✗ A link in the chain has expired',
        text: 'At least one certificate in the chain is outside its validity window (notBefore/notAfter). Even an otherwise technically perfect chain then counts as invalid.',
      },
    } as Record<ChainProblem, { title: string; text: string }>,
    whyOffline: {
      title: 'Why is the root CA kept offline?',
      text: 'After issuing its intermediates, the root CA is taken offline and locked away in a vault — day-to-day issuance is handled by the intermediate. If an intermediate is compromised, it can simply be revoked and replaced with a new one, without touching anyone’s trust anchor (the root). A compromised root, by contrast, would be practically unrevocable: it sits in countless trust stores worldwide, and replacing it there is slow to impossible.',
    },
    challenge: 'Assemble a complete, valid chain and validate it successfully.',
  },
} as const

export function CertChain({ lang }: { lang: Lang }) {
  const [chain, setChain] = useState<Cert[]>([])
  const [checked, setChecked] = useState(false)
  const [solvedOnce, setSolvedOnce] = useState(false)
  const s = STR[lang]

  const toggle = (c: Cert) => {
    setChecked(false)
    setChain((prev) => (prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]))
  }

  const result = validateChain(chain, TRUST_STORE, DEMO_NOW)
  const showResult = checked
  const check = () => {
    setChecked(true)
    if (result.ok) setSolvedOnce(true)
  }

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <p className="mb-1 text-xs font-semibold text-slate-500" id="chain-pool-label">{s.poolLabel}</p>
      <div className="flex flex-wrap gap-2 mb-4" role="group" aria-labelledby="chain-pool-label">
        {CHAIN_POOL.map((c) => {
          const inChain = chain.includes(c)
          return (
            <button
              key={c.id}
              onClick={() => toggle(c)}
              title={inChain ? s.removeHint : undefined}
              className={`rounded-lg border px-3 py-1.5 text-xs font-medium transition-colors ${
                inChain
                  ? 'bg-teal-600 border-teal-600 text-white'
                  : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
              }`}
            >
              {c.label[lang]}
            </button>
          )
        })}
      </div>

      <p className="mb-1 text-xs font-semibold text-slate-500">{s.chainLabel}</p>
      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 mb-3 min-h-[3rem] flex flex-wrap items-center gap-2">
        {chain.length === 0 ? (
          <p className="text-xs italic text-slate-400">{s.chainEmpty}</p>
        ) : (
          chain.map((c, i) => (
            <span key={c.id} className="flex items-center gap-2">
              <button
                onClick={() => toggle(c)}
                className="rounded border border-teal-300 bg-white px-2 py-1 text-xs font-mono text-teal-800 hover:bg-teal-50"
              >
                {c.label[lang]}
              </button>
              {i < chain.length - 1 && <span className="text-slate-400" aria-hidden="true">→</span>}
            </span>
          ))
        )}
      </div>

      <button
        onClick={check}
        disabled={chain.length === 0}
        className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium disabled:opacity-40 mb-3"
      >
        {s.check}
      </button>

      {showResult && (
        <div
          className={`rounded-lg border p-3 text-sm mb-4 ${
            result.ok ? 'border-green-200 bg-green-50 text-green-900' : 'border-rose-200 bg-rose-50 text-rose-900'
          }`}
          aria-live="polite"
        >
          <p className="font-semibold mb-1">{result.ok ? s.resultOk.title : s.results[result.problem!].title}</p>
          <p>{result.ok ? s.resultOk.text : s.results[result.problem!].text}</p>
        </div>
      )}

      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700">
        <p className="font-semibold text-slate-800 mb-1">{s.whyOffline.title}</p>
        <p>{s.whyOffline.text}</p>
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={solvedOnce} />
    </div>
  )
}
