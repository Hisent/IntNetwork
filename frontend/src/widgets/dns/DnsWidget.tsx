import { useState } from 'react'
import { resolve, type DnsResult } from '@/widgets/dns/dns'

const PRESETS = ['www.nordwind-logistik.de', 'mail.nordwind-logistik.de', 'gibtsnicht.nordwind-logistik.de']

export function Dns() {
  const [name, setName] = useState('www.nordwind-logistik.de')
  const [res, setRes] = useState<DnsResult | null>(null)

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">DNS-Auflösung</p>

      <div className="flex flex-wrap items-end gap-2 mb-2">
        <label className="text-xs text-slate-600">
          Domain
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            spellCheck={false}
            className="ml-1 w-64 border rounded px-2 py-1 text-sm font-mono"
          />
        </label>
        <button
          onClick={() => setRes(resolve(name))}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium"
        >
          Auflösen
        </button>
      </div>

      <div className="flex flex-wrap gap-2 mb-3">
        {PRESETS.map((p) => (
          <button
            key={p}
            onClick={() => { setName(p); setRes(resolve(p)) }}
            className="rounded-lg border px-2 py-1 text-xs font-mono hover:bg-slate-50"
          >
            {p}
          </button>
        ))}
      </div>

      {res && (
        <>
          <ol className="space-y-2 mb-3">
            {res.steps.map((s, i) => (
              <li key={i} className="flex gap-3 text-xs">
                <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-teal-100 text-teal-700 font-semibold">
                  {i + 1}
                </span>
                <span className="text-slate-700">
                  <span className="font-semibold">{s.server}</span>
                  <span className="text-slate-400"> — </span>
                  <span className="font-mono">{s.answer}</span>
                </span>
              </li>
            ))}
          </ol>
          <p className="text-xs text-slate-600">
            {res.ip ? (
              <>
                Ergebnis: <span className="font-mono text-slate-800">{name}</span> →{' '}
                <span className="font-mono text-teal-700">{res.ip}</span>
              </>
            ) : (
              'Ergebnis: keine IP — Name nicht auflösbar.'
            )}
          </p>
        </>
      )}
    </div>
  )
}
