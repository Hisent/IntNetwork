import { useState } from 'react'
import { evaluate, RULES, type Packet, type Proto } from '@/widgets/firewall/firewall'
import type { Lang } from '@/lib/i18n'

const PRESETS: { de: string; en: string; pkt: Packet }[] = [
  { de: 'HTTPS (TCP 443)', en: 'HTTPS (TCP 443)', pkt: { proto: 'TCP', port: 443 } },
  { de: 'Telnet (TCP 23)', en: 'Telnet (TCP 23)', pkt: { proto: 'TCP', port: 23 } },
  { de: 'RDP (TCP 3389)', en: 'RDP (TCP 3389)', pkt: { proto: 'TCP', port: 3389 } },
  { de: 'DNS (UDP 53)', en: 'DNS (UDP 53)', pkt: { proto: 'UDP', port: 53 } },
]

const RULE_DESC: Record<number, { de: string; en: string }> = {
  0: { de: 'HTTPS zum Webserver', en: 'HTTPS to the web server' },
  1: { de: 'SSH nur für Admins', en: 'SSH for admins only' },
  2: { de: 'Telnet verboten (unverschlüsselt)', en: 'Telnet forbidden (unencrypted)' },
  3: { de: 'DNS-Anfragen', en: 'DNS queries' },
}

const STR = {
  de: {
    title: 'Firewall — Regelauswertung', protocol: 'Protokoll', port: 'Port',
    allowed: 'ERLAUBT', blocked: 'BLOCKIERT', rules: 'Regelwerk (erste Übereinstimmung gewinnt)',
    defaultDeny: 'default deny — alles andere blockiert', defaultDenyReason: 'Keine Regel trifft zu → Default-Deny',
  },
  en: {
    title: 'Firewall — Rule Evaluation', protocol: 'Protocol', port: 'Port',
    allowed: 'ALLOWED', blocked: 'BLOCKED', rules: 'Ruleset (first match wins)',
    defaultDeny: 'default deny — everything else is blocked', defaultDenyReason: 'No rule matches → default deny',
  },
} as const

export function Firewall({ lang }: { lang: Lang }) {
  const [pkt, setPkt] = useState<Packet>({ proto: 'TCP', port: 443 })
  const decision = evaluate(RULES, pkt)
  const s = STR[lang]
  const reason = decision.ruleIndex !== null ? RULE_DESC[decision.ruleIndex][lang] : s.defaultDenyReason

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">{s.title}</p>

      <div className="flex flex-wrap items-end gap-2 mb-2">
        <label className="text-xs text-slate-600">
          {s.protocol}
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
          {s.port}
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
            key={pr.de}
            onClick={() => setPkt(pr.pkt)}
            className="rounded-lg border px-2 py-1 text-xs hover:bg-slate-50"
          >
            {pr[lang]}
          </button>
        ))}
      </div>

      <div
        className={`rounded-lg px-3 py-2 text-sm mb-4 ${
          decision.action === 'allow' ? 'bg-teal-50 text-teal-800' : 'bg-rose-50 text-rose-800'
        }`}
      >
        <span className="font-semibold">{decision.action === 'allow' ? s.allowed : s.blocked}</span>
        {' — '}
        {reason}
      </div>

      <p className="text-xs font-semibold text-slate-500 mb-1">{s.rules}</p>
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
            <span className="text-slate-600">{RULE_DESC[i][lang]}</span>
          </div>
        ))}
        <div className={`px-3 py-1.5 ${decision.ruleIndex === null ? 'bg-amber-50 text-amber-800' : 'text-slate-500'}`}>
          {s.defaultDeny}
        </div>
      </div>
    </div>
  )
}
