import { useState } from 'react'
import { probe, PATH, type Probe } from '@/widgets/icmp/icmp'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: { title: 'traceroute 198.51.100.10', hint: 'Jeder Probe erhöht die TTL um 1 — so meldet sich der nächste Router auf dem Weg.',
    nextHop: (ttl: number) => `Nächster Hop (TTL ${ttl})`, restart: 'Neu starten', noProbe: 'noch kein Probe gesendet',
    reply: 'Echo Reply', exceeded: 'Time Exceeded', reached: 'Ziel erreicht — der komplette Pfad ist sichtbar.' },
  en: { title: 'traceroute 198.51.100.10', hint: "Each probe increases the TTL by 1 — that's how the next router on the path responds.",
    nextHop: (ttl: number) => `Next hop (TTL ${ttl})`, restart: 'Restart', noProbe: 'no probe sent yet',
    reply: 'Echo Reply', exceeded: 'Time Exceeded', reached: 'Destination reached — the full path is visible.' },
} as const

export function Icmp({ lang }: { lang: Lang }) {
  const [ttl, setTtl] = useState(0)
  const probes: Probe[] = Array.from({ length: ttl }, (_, i) => probe(i + 1))
  const done = probes.some((p) => p.status === 'reply')
  const s = STR[lang]

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-3">
        {s.hint}
      </p>

      <div className="flex gap-2 mb-3">
        <button
          onClick={() => setTtl((t) => Math.min(t + 1, PATH.length))}
          disabled={done}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium disabled:opacity-50"
        >
          {s.nextHop(ttl + 1)}
        </button>
        <button onClick={() => setTtl(0)} className="rounded-lg border px-3 py-1.5 text-sm">
          {s.restart}
        </button>
      </div>

      <div className="rounded-lg border divide-y text-xs font-mono">
        {probes.length === 0 ? (
          <div className="px-3 py-2 text-slate-400">{s.noProbe}</div>
        ) : (
          probes.map((p) => (
            <div
              key={p.ttl}
              className={`flex items-center justify-between px-3 py-1.5 ${p.status === 'reply' ? 'bg-teal-50' : ''}`}
            >
              <span className="text-slate-500">{p.ttl}</span>
              <span className="text-slate-700">{p.node?.name[lang]}</span>
              <span className="text-slate-500">{p.node?.ip}</span>
              <span className="text-slate-400">{p.node?.rttMs} ms</span>
              <span className={p.status === 'reply' ? 'text-teal-700' : 'text-amber-600'}>
                {p.status === 'reply' ? s.reply : s.exceeded}
              </span>
            </div>
          ))
        )}
      </div>

      {done && <p className="mt-3 text-xs text-teal-700">{s.reached}</p>}
    </div>
  )
}
