import { useState } from 'react'
import { evaluate, RULES, type Packet, type Proto } from '@/widgets/firewall/firewall'

const PRESETS: { label: string; pkt: Packet }[] = [
  { label: 'HTTPS (TCP 443)', pkt: { proto: 'TCP', port: 443 } },
  { label: 'Telnet (TCP 23)', pkt: { proto: 'TCP', port: 23 } },
  { label: 'RDP (TCP 3389)', pkt: { proto: 'TCP', port: 3389 } },
  { label: 'DNS (UDP 53)', pkt: { proto: 'UDP', port: 53 } },
]

export function Firewall() {
  const [pkt, setPkt] = useState<Packet>({ proto: 'TCP', port: 443 })
  const decision = evaluate(RULES, pkt)

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">Firewall — Regelauswertung</p>

      <div className="flex flex-wrap items-end gap-2 mb-2">
        <label className="text-xs text-slate-600">
          Protokoll
          <select
            value={pkt.proto}
            onChange={(e) => setPkt((p) => ({ ...p, proto: e.target.value as Proto }))}
            className="ml-1 border rounded px-1 py-0.5 font-mono"
          >
            <option>TCP</option>
            <option>UDP</option>
          </select>
        </label>
        <label className="text-xs text-slate-600">
          Port
          <input
            type="number"
            value={pkt.port}
            onChange={(e) => setPkt((p) => ({ ...p, port: Number(e.target.value) || 0 }))}
            className="ml-1 w-20 border rounded px-1 py-0.5 font-mono"
          />
        </label>
      </div>

      <div className="flex flex-wrap gap-2 mb-3">
        {PRESETS.map((pr) => (
          <button
            key={pr.label}
            onClick={() => setPkt(pr.pkt)}
            className="rounded-lg border px-2 py-1 text-xs hover:bg-slate-50"
          >
            {pr.label}
          </button>
        ))}
      </div>

      <div
        className={`rounded-lg px-3 py-2 text-sm mb-4 ${
          decision.action === 'allow' ? 'bg-teal-50 text-teal-800' : 'bg-rose-50 text-rose-800'
        }`}
      >
        <span className="font-semibold">{decision.action === 'allow' ? 'ERLAUBT' : 'BLOCKIERT'}</span>
        {' — '}
        {decision.reason}
      </div>

      <p className="text-xs font-semibold text-slate-500 mb-1">Regelwerk (erste Übereinstimmung gewinnt)</p>
      <div className="rounded-lg border divide-y text-xs font-mono">
        {RULES.map((r, i) => (
          <div
            key={i}
            className={`flex items-center gap-3 px-3 py-1.5 ${i === decision.ruleIndex ? 'bg-amber-50' : ''}`}
          >
            <span className={r.action === 'allow' ? 'text-teal-700' : 'text-rose-700'}>
              {r.action.padEnd(5)}
            </span>
            <span className="text-slate-600">
              {r.proto}/{r.port}
            </span>
            <span className="text-slate-600">{r.desc}</span>
          </div>
        ))}
        <div className={`px-3 py-1.5 ${decision.ruleIndex === null ? 'bg-amber-50 text-amber-800' : 'text-slate-500'}`}>
          default deny — alles andere blockiert
        </div>
      </div>
    </div>
  )
}
