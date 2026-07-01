import { useState } from 'react'
import { DeviceCli } from '@/widgets/cli/DeviceCli'
import { routeLookup, type Route } from '@/widgets/router/routing'
import { runRouterCommand } from '@/widgets/router/routerCli'

const ROUTES: Route[] = [
  { network: '192.168.10.0', prefix: 24, via: null, iface: 'Gi0/0', ip: '192.168.10.1' },
  { network: '192.168.20.0', prefix: 24, via: null, iface: 'Gi0/1', ip: '192.168.20.1' },
  { network: '0.0.0.0', prefix: 0, via: '203.0.113.2', iface: 'Gi0/2' },
]

const PRESETS = ['192.168.10.50', '192.168.20.5', '8.8.8.8']

export function Routing() {
  const [dst, setDst] = useState('192.168.20.5')
  const res = routeLookup(ROUTES, dst)

  const verdict =
    res.reason === 'connected'
      ? `Ziel liegt im direkt verbundenen Netz ${res.route!.network}/${res.route!.prefix} → über ${res.route!.iface} direkt zustellbar.`
      : res.reason === 'via'
        ? `Kein direktes Netz → Longest-Prefix-Match ${res.route!.network}/${res.route!.prefix}, weiter an Next-Hop ${res.route!.via} (${res.route!.iface}).`
        : 'Keine passende Route → Ziel nicht erreichbar.'

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">Router Nordwind-R1 — Routing-Tabelle</p>

      <div className="rounded-lg border divide-y text-sm font-mono mb-4">
        {ROUTES.map((r) => (
          <div key={r.network + r.prefix} className="flex justify-between px-3 py-1.5">
            <span className="text-slate-700">
              {r.network}/{r.prefix}
            </span>
            <span className="text-slate-500">
              {r.via === null ? `connected · ${r.iface}` : `via ${r.via} · ${r.iface}`}
            </span>
          </div>
        ))}
      </div>

      <div className="flex flex-wrap items-end gap-2 mb-2">
        <label className="text-xs text-slate-600">
          Ziel-IP
          <input
            value={dst}
            onChange={(e) => setDst(e.target.value)}
            spellCheck={false}
            className="ml-1 w-36 border rounded px-2 py-1 text-sm font-mono"
          />
        </label>
        {PRESETS.map((p) => (
          <button
            key={p}
            onClick={() => setDst(p)}
            className="rounded-lg border px-2 py-1 text-xs font-mono hover:bg-slate-50"
          >
            {p}
          </button>
        ))}
      </div>

      <p className="text-xs text-slate-600">{verdict}</p>

      <DeviceCli prompt="Nordwind-R1#" run={(c) => runRouterCommand(ROUTES, c)} />
    </div>
  )
}
