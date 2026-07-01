import { useState } from 'react'
import { lease, type Lease } from '@/widgets/dhcp/dhcp'

export function Dhcp() {
  const [leases, setLeases] = useState<Lease[]>([])

  const add = () => setLeases((ls) => [...ls, lease(ls.length)])
  const last = leases[leases.length - 1]

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">DHCP — automatische IP-Vergabe</p>

      <div className="flex gap-2 mb-3">
        <button
          onClick={add}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium"
        >
          Neuer Client verbindet sich
        </button>
        <button onClick={() => setLeases([])} className="rounded-lg border px-3 py-1.5 text-sm">
          Zurücksetzen
        </button>
      </div>

      {last && (
        <>
          <ol className="space-y-1.5 mb-3">
            {last.steps.map((s, i) => (
              <li key={i} className="flex gap-3 text-xs">
                <span className="w-16 shrink-0 font-semibold text-teal-700">{s.phase}</span>
                <span className="text-slate-600">{s.text}</span>
              </li>
            ))}
          </ol>
          <div className="rounded-lg border divide-y text-xs font-mono mb-4">
            {[
              ['IP-Adresse', last.ip],
              ['Subnetzmaske', last.mask],
              ['Gateway', last.gateway],
              ['DNS-Server', last.dns],
            ].map(([k, v]) => (
              <div key={k} className="flex justify-between px-3 py-1.5">
                <span className="text-slate-500">{k}</span>
                <span className="text-slate-800">{v}</span>
              </div>
            ))}
          </div>
        </>
      )}

      <p className="text-xs font-semibold text-slate-500 mb-1">Vergebene Leases</p>
      <div className="rounded-lg border divide-y text-xs font-mono">
        {leases.length === 0 ? (
          <div className="px-3 py-2 text-slate-400">keine</div>
        ) : (
          leases.map((l, i) => (
            <div key={l.ip} className="flex justify-between px-3 py-1.5">
              <span className="text-slate-700">Client {i + 1}</span>
              <span className="text-slate-500">{l.ip}</span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
