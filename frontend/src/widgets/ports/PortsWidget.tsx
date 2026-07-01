import { useState } from 'react'
import { serviceFor, HANDSHAKE, WELL_KNOWN } from '@/widgets/ports/ports'

const PRESETS = [80, 443, 22, 53]

export function Ports() {
  const [port, setPort] = useState(443)

  return (
    <div className="rounded-2xl border bg-white p-5 space-y-5">
      <div>
        <p className="text-sm font-semibold text-slate-700 mb-3">Port → Dienst</p>
        <div className="flex flex-wrap items-end gap-2 mb-2">
          <label className="text-xs text-slate-600">
            Port
            <input
              type="number"
              value={port}
              onChange={(e) => setPort(Number(e.target.value) || 0)}
              className="ml-1 w-24 border rounded px-2 py-1 text-sm font-mono"
            />
          </label>
          {PRESETS.map((p) => (
            <button
              key={p}
              onClick={() => setPort(p)}
              className="rounded-lg border px-2 py-1 text-xs font-mono hover:bg-slate-50"
            >
              {p} · {WELL_KNOWN[p]}
            </button>
          ))}
        </div>
        <p className="text-xs text-slate-600">
          Port <span className="font-mono">{port}</span> →{' '}
          <span className="font-mono text-teal-700">{serviceFor(port)}</span>
        </p>
      </div>

      <div>
        <p className="text-sm font-semibold text-slate-700 mb-3">TCP 3-Wege-Handshake</p>
        <ol className="space-y-2">
          {HANDSHAKE.map((s, i) => (
            <li key={i} className="flex items-center gap-3 text-xs">
              <span className="w-14 shrink-0 text-slate-500">{s.from}</span>
              <span className="text-slate-300">{s.from === 'Client' ? '───▶' : '◀───'}</span>
              <span className="rounded bg-teal-100 px-2 py-0.5 font-mono font-semibold text-teal-700">
                {s.flag}
              </span>
              <span className="text-slate-600">{s.text}</span>
            </li>
          ))}
        </ol>
      </div>

      <div>
        <p className="text-sm font-semibold text-slate-700 mb-2">TCP vs. UDP</p>
        <div className="grid grid-cols-2 gap-3 text-xs">
          <div className="rounded-xl border p-3">
            <p className="font-semibold text-slate-700 mb-1">TCP</p>
            <ul className="list-disc list-inside text-slate-600 space-y-0.5">
              <li>verbindungsorientiert (Handshake)</li>
              <li>zuverlässig, Reihenfolge garantiert</li>
              <li>Web, E-Mail, SSH</li>
            </ul>
          </div>
          <div className="rounded-xl border p-3">
            <p className="font-semibold text-slate-700 mb-1">UDP</p>
            <ul className="list-disc list-inside text-slate-600 space-y-0.5">
              <li>verbindungslos, kein Handshake</li>
              <li>schnell, keine Garantie</li>
              <li>DNS, Video, VoIP, Spiele</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
