import { useState } from 'react'
import { translate, type NatEntry } from '@/widgets/nat/nat'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const PUBLIC_IP = '203.0.113.10'
const HOSTS = [
  { ip: '192.168.10.5', name: { de: 'PC-Lager', en: 'PC-Warehouse' } },
  { ip: '192.168.20.8', name: { de: 'PC-Büro', en: 'PC-Office' } },
  { ip: '192.168.20.9', name: { de: 'Laptop', en: 'Laptop' } },
]

const STR = {
  de: {
    title: 'NAT (PAT) — Router Nordwind-R1', publicIp: 'Öffentliche IP', host: 'Host', srcPort: 'Quell-Port',
    send: 'Ins Internet senden', clear: 'Tabelle leeren', table: 'NAT-Übersetzungstabelle', empty: 'leer',
    reused: (local: string, global: string) => `${local} bereits übersetzt → ${global} (wiederverwendet).`,
    fresh: (local: string, global: string) => `${local} → ${global} (neuer Eintrag).`,
    challenge: 'Schick mindestens zwei verschiedene Hosts ins Internet — beide teilen sich dieselbe öffentliche IP (PAT).',
  },
  en: {
    title: 'NAT (PAT) — Router Nordwind-R1', publicIp: 'Public IP', host: 'Host', srcPort: 'Source port',
    send: 'Send to the Internet', clear: 'Clear table', table: 'NAT translation table', empty: 'empty',
    reused: (local: string, global: string) => `${local} already translated → ${global} (reused).`,
    fresh: (local: string, global: string) => `${local} → ${global} (new entry).`,
    challenge: 'Send at least two different hosts to the Internet — both share the same public IP (PAT).',
  },
} as const

export function Nat({ lang }: { lang: Lang }) {
  const [table, setTable] = useState<NatEntry[]>([])
  const [host, setHost] = useState(HOSTS[0].ip)
  const [port, setPort] = useState(5000)
  const [last, setLast] = useState<string | null>(null)
  const s = STR[lang]

  function send() {
    const r = translate(table, host, port, PUBLIC_IP)
    setTable(r.table)
    setLast(r.reused ? s.reused(r.entry.insideLocal, r.entry.insideGlobal) : s.fresh(r.entry.insideLocal, r.entry.insideGlobal))
    setPort((p) => p + 1)
  }

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-3">
        {s.publicIp}: <span className="font-mono">{PUBLIC_IP}</span>
      </p>

      <div className="flex flex-wrap items-end gap-2 mb-3">
        <label className="text-xs text-slate-600">
          {s.host}
          <select
            value={host}
            onChange={(e) => setHost(e.target.value)}
            className="ml-1 border rounded px-1 py-0.5"
          >
            {HOSTS.map((h) => (
              <option key={h.ip} value={h.ip}>
                {h.name[lang]} ({h.ip})
              </option>
            ))}
          </select>
        </label>
        <label className="text-xs text-slate-600">
          {s.srcPort}
          <input
            type="number"
            value={port}
            onChange={(e) => setPort(Number(e.target.value) || 0)}
            className="ml-1 w-20 border rounded px-1 py-0.5 font-mono"
          />
        </label>
        <button
          onClick={send}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium"
        >
          {s.send}
        </button>
        <button onClick={() => { setTable([]); setLast(null) }} className="rounded-lg border px-3 py-1.5 text-sm">
          {s.clear}
        </button>
      </div>

      {last && <p className="text-xs text-slate-600 mb-3">{last}</p>}

      <p className="text-xs font-semibold text-slate-500 mb-1">{s.table}</p>
      <div className="rounded-lg border divide-y text-xs font-mono">
        <div className="flex justify-between px-3 py-1.5 text-slate-400">
          <span>Inside Local</span>
          <span>Inside Global</span>
        </div>
        {table.length === 0 ? (
          <div className="px-3 py-2 text-slate-400">{s.empty}</div>
        ) : (
          table.map((e) => (
            <div key={e.insideLocal} className="flex justify-between px-3 py-1.5">
              <span className="text-slate-700">{e.insideLocal}</span>
              <span className="text-slate-500">{e.insideGlobal}</span>
            </div>
          ))
        )}
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={table.length >= 2} />
    </div>
  )
}
