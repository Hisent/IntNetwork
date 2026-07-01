import { useState } from 'react'
import { translate, type NatEntry } from '@/widgets/nat/nat'

const PUBLIC_IP = '203.0.113.10'
const HOSTS = [
  { ip: '192.168.10.5', name: 'PC-Lager' },
  { ip: '192.168.20.8', name: 'PC-Büro' },
  { ip: '192.168.20.9', name: 'Laptop' },
]

export function Nat() {
  const [table, setTable] = useState<NatEntry[]>([])
  const [host, setHost] = useState(HOSTS[0].ip)
  const [port, setPort] = useState(5000)
  const [last, setLast] = useState<string | null>(null)

  function send() {
    const r = translate(table, host, port, PUBLIC_IP)
    setTable(r.table)
    setLast(
      r.reused
        ? `${r.entry.insideLocal} bereits übersetzt → ${r.entry.insideGlobal} (wiederverwendet).`
        : `${r.entry.insideLocal} → ${r.entry.insideGlobal} (neuer Eintrag).`,
    )
    setPort((p) => p + 1)
  }

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">NAT (PAT) — Router Nordwind-R1</p>
      <p className="text-xs text-slate-500 mb-3">
        Öffentliche IP: <span className="font-mono">{PUBLIC_IP}</span>
      </p>

      <div className="flex flex-wrap items-end gap-2 mb-3">
        <label className="text-xs text-slate-600">
          Host
          <select
            value={host}
            onChange={(e) => setHost(e.target.value)}
            className="ml-1 border rounded px-1 py-0.5"
          >
            {HOSTS.map((h) => (
              <option key={h.ip} value={h.ip}>
                {h.name} ({h.ip})
              </option>
            ))}
          </select>
        </label>
        <label className="text-xs text-slate-600">
          Quell-Port
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
          Ins Internet senden
        </button>
        <button onClick={() => { setTable([]); setLast(null) }} className="rounded-lg border px-3 py-1.5 text-sm">
          Tabelle leeren
        </button>
      </div>

      {last && <p className="text-xs text-slate-600 mb-3">{last}</p>}

      <p className="text-xs font-semibold text-slate-500 mb-1">NAT-Übersetzungstabelle</p>
      <div className="rounded-lg border divide-y text-xs font-mono">
        <div className="flex justify-between px-3 py-1.5 text-slate-400">
          <span>Inside Local</span>
          <span>Inside Global</span>
        </div>
        {table.length === 0 ? (
          <div className="px-3 py-2 text-slate-400">leer</div>
        ) : (
          table.map((e) => (
            <div key={e.insideLocal} className="flex justify-between px-3 py-1.5">
              <span className="text-slate-700">{e.insideLocal}</span>
              <span className="text-slate-500">{e.insideGlobal}</span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
