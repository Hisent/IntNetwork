import { useState } from 'react'
import { lease, type Lease } from '@/widgets/dhcp/dhcp'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: { title: 'DHCP — automatische IP-Vergabe', newClient: 'Neuer Client verbindet sich', reset: 'Zurücksetzen',
    ip: 'IP-Adresse', mask: 'Subnetzmaske', gateway: 'Gateway', dns: 'DNS-Server',
    leases: 'Vergebene Leases', none: 'keine', client: 'Client', nextStep: 'Nächster Schritt',
    challenge: 'Verbinde drei Clients und vergleiche ihre Leases — was ist gleich, was unterscheidet sich?' },
  en: { title: 'DHCP — Automatic IP Assignment', newClient: 'New client connects', reset: 'Reset',
    ip: 'IP address', mask: 'Subnet mask', gateway: 'Gateway', dns: 'DNS server',
    leases: 'Assigned leases', none: 'none', client: 'Client', nextStep: 'Next step',
    challenge: 'Connect three clients and compare their leases — what is identical, what differs?' },
} as const

export function Dhcp({ lang }: { lang: Lang }) {
  const [leases, setLeases] = useState<Lease[]>([])
  // laufender DORA-Handshake: Schritte werden einzeln aufgedeckt,
  // erst nach dem Ack landet die Lease in der Tabelle
  const [pending, setPending] = useState<{ lease: Lease; step: number } | null>(null)
  const s = STR[lang]

  const add = () => setPending({ lease: lease(leases.length), step: 1 })
  const advance = () => {
    if (!pending) return
    const step = pending.step + 1
    setPending({ ...pending, step })
    if (step === pending.lease.steps.length) setLeases((ls) => [...ls, pending.lease])
  }
  const inProgress = pending !== null && pending.step < pending.lease.steps.length

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">{s.title}</p>

      <div className="flex gap-2 mb-3">
        <button
          onClick={add}
          disabled={inProgress}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium disabled:opacity-50"
        >
          {s.newClient}
        </button>
        <button onClick={() => { setLeases([]); setPending(null) }} className="rounded-lg border px-3 py-1.5 text-sm">
          {s.reset}
        </button>
      </div>

      {pending && (
        <>
          <ol className="space-y-1.5 mb-3">
            {pending.lease.steps.slice(0, pending.step).map((step, i) => (
              <li key={i} className="flex gap-3 text-xs animate-fade-up">
                <span className="w-16 shrink-0 font-semibold text-teal-700">{step.phase}</span>
                <span className="text-slate-600">{step.text[lang]}</span>
              </li>
            ))}
          </ol>
          {inProgress ? (
            <button onClick={advance}
              className="rounded-lg border px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 mb-4">
              {s.nextStep} →
            </button>
          ) : (
            <div className="rounded-lg border divide-y text-xs font-mono mb-4 animate-fade-up">
              {[
                [s.ip, pending.lease.ip],
                [s.mask, pending.lease.mask],
                [s.gateway, pending.lease.gateway],
                [s.dns, pending.lease.dns],
              ].map(([k, v]) => (
                <div key={k} className="flex justify-between px-3 py-1.5">
                  <span className="text-slate-500">{k}</span>
                  <span className="text-slate-800">{v}</span>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      <p className="text-xs font-semibold text-slate-500 mb-1">{s.leases}</p>
      <div className="rounded-lg border divide-y text-xs font-mono">
        {leases.length === 0 ? (
          <div className="px-3 py-2 text-slate-400">{s.none}</div>
        ) : (
          leases.map((l, i) => (
            <div key={l.ip} className="flex justify-between px-3 py-1.5">
              <span className="text-slate-700">{s.client} {i + 1}</span>
              <span className="text-slate-500">{l.ip}</span>
            </div>
          ))
        )}
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={leases.length >= 3} />
    </div>
  )
}
