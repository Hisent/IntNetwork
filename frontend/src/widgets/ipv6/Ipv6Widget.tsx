import { useState } from 'react'
import { expand, compress, classify } from '@/widgets/ipv6/ipv6'

const PRESETS = ['2001:0db8:0000:0000:0000:0000:0000:0001', 'fe80::1', '::1', 'ff02::1']

export function Ipv6() {
  const [addr, setAddr] = useState('2001:db8:0:0:0:0:0:1')

  let ok = true
  let full = ''
  let short = ''
  try {
    full = expand(addr)
    short = compress(addr)
    ok = /^[0-9a-f:]+$/.test(addr.trim().toLowerCase()) && full.split(':').length === 8
  } catch {
    ok = false
  }

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">IPv6-Adresse: kürzen & prüfen</p>

      <div className="flex flex-wrap items-end gap-2 mb-2">
        <label className="text-xs text-slate-600">
          Adresse
          <input
            value={addr}
            onChange={(e) => setAddr(e.target.value)}
            spellCheck={false}
            className="ml-1 w-72 border rounded px-2 py-1 text-sm font-mono"
          />
        </label>
      </div>

      <div className="flex flex-wrap gap-2 mb-3">
        {PRESETS.map((p) => (
          <button
            key={p}
            onClick={() => setAddr(p)}
            className="rounded-lg border px-2 py-1 text-xs font-mono hover:bg-slate-50"
          >
            {p}
          </button>
        ))}
      </div>

      {ok ? (
        <div className="rounded-lg border divide-y text-xs">
          {[
            ['Kurzform', short],
            ['Vollform', full],
            ['Typ', classify(addr)],
          ].map(([k, v]) => (
            <div key={k} className="flex justify-between px-3 py-1.5">
              <span className="text-slate-500">{k}</span>
              <span className="font-mono text-slate-800">{v}</span>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-xs text-rose-700">Keine gültige IPv6-Adresse.</p>
      )}
    </div>
  )
}
