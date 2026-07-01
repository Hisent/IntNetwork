import { useState } from 'react'
import { subnetInfo } from '@/widgets/subnet/subnet'

export function Subnet() {
  const [octets, setOctets] = useState([192, 168, 10, 37])
  const [prefix, setPrefix] = useState(24)

  const setOctet = (i: number, v: string) => {
    const n = Math.max(0, Math.min(255, Number(v) || 0))
    setOctets((o) => o.map((x, j) => (j === i ? n : x)))
  }

  const info = subnetInfo(octets.join('.'), prefix)

  const rows: [string, string][] = [
    ['Subnetzmaske', info.mask],
    ['Netzadresse', info.network],
    ['Broadcast', info.broadcast],
    ['Erster Host', info.firstHost],
    ['Letzter Host', info.lastHost],
    ['Nutzbare Hosts', String(info.usableHosts)],
  ]

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">Subnetz-Rechner</p>

      <div className="flex flex-wrap items-end gap-3 mb-4">
        <div className="flex items-center gap-1">
          {octets.map((o, i) => (
            <span key={i} className="flex items-center gap-1">
              <input
                type="number" min={0} max={255} value={o}
                onChange={(e) => setOctet(i, e.target.value)}
                className="w-14 border rounded px-1 py-1 text-sm font-mono text-center"
              />
              {i < 3 && <span className="text-slate-400">.</span>}
            </span>
          ))}
        </div>
        <label className="text-xs text-slate-600">
          Präfix /{prefix}
          <input
            type="range" min={8} max={30} value={prefix}
            onChange={(e) => setPrefix(Number(e.target.value))}
            className="ml-2 align-middle accent-teal-600"
          />
        </label>
      </div>

      <div className="rounded-lg border divide-y text-sm">
        {rows.map(([label, value]) => (
          <div key={label} className="flex justify-between px-3 py-1.5">
            <span className="text-slate-500">{label}</span>
            <span className="font-mono text-slate-800 tabular-nums">{value}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
