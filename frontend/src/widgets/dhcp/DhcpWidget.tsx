import { useState } from 'react'
import { lease, type Lease } from '@/widgets/dhcp/dhcp'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: { title: 'DHCP — automatische IP-Vergabe', newClient: 'Neuer Client verbindet sich', reset: 'Zurücksetzen',
    ip: 'IP-Adresse', mask: 'Subnetzmaske', gateway: 'Gateway', dns: 'DNS-Server',
    leases: 'Vergebene Leases', none: 'keine', client: 'Client',
    challenge: 'Verbinde drei Clients und vergleiche ihre Leases — was ist gleich, was unterscheidet sich?' },
  en: { title: 'DHCP — Automatic IP Assignment', newClient: 'New client connects', reset: 'Reset',
    ip: 'IP address', mask: 'Subnet mask', gateway: 'Gateway', dns: 'DNS server',
    leases: 'Assigned leases', none: 'none', client: 'Client',
    challenge: 'Connect three clients and compare their leases — what is identical, what differs?' },
} as const

export function Dhcp({ lang }: { lang: Lang }) {
  const [leases, setLeases] = useState<Lease[]>([])
  const s = STR[lang]

  const add = () => setLeases((ls) => [...ls, lease(ls.length)])
  const last = leases[leases.length - 1]

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">{s.title}</p>

      <div className="flex gap-2 mb-3">
        <button
          onClick={add}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium"
        >
          {s.newClient}
        </button>
        <button onClick={() => setLeases([])} className="rounded-lg border px-3 py-1.5 text-sm">
          {s.reset}
        </button>
      </div>

      {last && (
        <>
          <ol className="space-y-1.5 mb-3">
            {last.steps.map((step, i) => (
              <li key={i} className="flex gap-3 text-xs">
                <span className="w-16 shrink-0 font-semibold text-teal-700">{step.phase}</span>
                <span className="text-slate-600">{step.text[lang]}</span>
              </li>
            ))}
          </ol>
          <div className="rounded-lg border divide-y text-xs font-mono mb-4">
            {[
              [s.ip, last.ip],
              [s.mask, last.mask],
              [s.gateway, last.gateway],
              [s.dns, last.dns],
            ].map(([k, v]) => (
              <div key={k} className="flex justify-between px-3 py-1.5">
                <span className="text-slate-500">{k}</span>
                <span className="text-slate-800">{v}</span>
              </div>
            ))}
          </div>
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
