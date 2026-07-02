import { useState } from 'react'
import { evaluate, RULES, type Action, type Packet, type Proto, type Rule } from '@/widgets/firewall/firewall'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

// Ziel-Traffic für den Regel-Baukasten: was soll durch, was nicht
const SAMPLES: { label: string; pkt: Packet; expected: Action }[] = [
  { label: 'HTTPS (TCP 443)', pkt: { proto: 'TCP', port: 443 }, expected: 'allow' },
  { label: 'DNS (UDP 53)', pkt: { proto: 'UDP', port: 53 }, expected: 'allow' },
  { label: 'Telnet (TCP 23)', pkt: { proto: 'TCP', port: 23 }, expected: 'deny' },
  { label: 'RDP (TCP 3389)', pkt: { proto: 'TCP', port: 3389 }, expected: 'deny' },
  { label: 'HTTP (TCP 80)', pkt: { proto: 'TCP', port: 80 }, expected: 'deny' },
]

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
    challenge: 'Finde ein Paket, das von keiner Regel getroffen wird — also am Default-Deny hängen bleibt.',
    testTab: 'Regeln testen', buildTab: 'Regeln bauen',
    yourRules: 'Dein Regelwerk', noRules: 'noch keine Regeln — alles läuft ins Default-Deny',
    addRule: 'Regel hinzufügen', anyPort: 'leer = beliebiger Port', traffic: 'Live-Traffic',
    expected: 'Soll', actual: 'Ist',
    buildChallenge: 'Baue ein Regelwerk, das genau HTTPS und DNS erlaubt — alles andere blockt das Default-Deny. Schaffst du es mit höchstens 2 Regeln?',
  },
  en: {
    title: 'Firewall — Rule Evaluation', protocol: 'Protocol', port: 'Port',
    allowed: 'ALLOWED', blocked: 'BLOCKED', rules: 'Ruleset (first match wins)',
    defaultDeny: 'default deny — everything else is blocked', defaultDenyReason: 'No rule matches → default deny',
    challenge: 'Find a packet no rule matches — one that gets stuck at the default deny.',
    testTab: 'Test rules', buildTab: 'Build rules',
    yourRules: 'Your ruleset', noRules: 'no rules yet — everything hits the default deny',
    addRule: 'Add rule', anyPort: 'empty = any port', traffic: 'Live traffic',
    expected: 'Goal', actual: 'Now',
    buildChallenge: 'Build a ruleset that allows exactly HTTPS and DNS — the default deny blocks the rest. Can you do it with at most 2 rules?',
  },
} as const

function RuleLab({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const [rules, setRules] = useState<Rule[]>([])
  const [action, setAction] = useState<Action>('allow')
  const [proto, setProto] = useState<Proto | 'any'>('TCP')
  const [port, setPort] = useState('')

  const results = SAMPLES.map((smp) => ({ ...smp, got: evaluate(rules, smp.pkt).action }))
  const done = results.every((r) => r.got === r.expected) && rules.length <= 2 && rules.length > 0

  const add = () => {
    setRules((rs) => [...rs, { action, proto, port: port.trim() === '' ? 'any' : Number(port) || 0 }])
    setPort('')
  }

  return (
    <div>
      <p className="text-xs font-semibold text-slate-500 mb-1">{s.yourRules}</p>
      <div className="rounded-lg border divide-y text-xs font-mono mb-3">
        {rules.length === 0 && <div className="px-3 py-1.5 text-slate-400">{s.noRules}</div>}
        {rules.map((r, i) => (
          <div key={i} className="flex items-center gap-3 px-3 py-1.5">
            <span className={r.action === 'allow' ? 'text-teal-700' : 'text-rose-700'}>{r.action.padEnd(5)}</span>
            <span className="text-slate-600">{r.proto}/{r.port}</span>
            <button onClick={() => setRules((rs) => rs.filter((_, idx) => idx !== i))}
              className="ml-auto text-rose-500 hover:text-rose-700">✕</button>
          </div>
        ))}
        <div className="px-3 py-1.5 text-slate-500">{s.defaultDeny}</div>
      </div>

      <div className="flex flex-wrap items-end gap-2 mb-4 text-xs text-slate-600">
        <select value={action} onChange={(e) => setAction(e.target.value as Action)}
          className="border rounded px-1 py-0.5 font-mono">
          <option value="allow">allow</option>
          <option value="deny">deny</option>
        </select>
        <select value={proto} onChange={(e) => setProto(e.target.value as Proto | 'any')}
          className="border rounded px-1 py-0.5 font-mono">
          <option>TCP</option>
          <option>UDP</option>
          <option value="any">any</option>
        </select>
        <input type="number" value={port} onChange={(e) => setPort(e.target.value)} placeholder={s.port}
          title={s.anyPort} className="w-20 border rounded px-1 py-0.5 font-mono" />
        <button onClick={add} className="rounded-lg border px-2 py-1 hover:bg-slate-50">{s.addRule}</button>
        <span className="text-slate-400">{s.anyPort}</span>
      </div>

      <p className="text-xs font-semibold text-slate-500 mb-1">{s.traffic}</p>
      <div className="rounded-lg border divide-y text-xs font-mono mb-1">
        {results.map((r) => (
          <div key={r.label} className="flex items-center gap-3 px-3 py-1.5">
            <span className="text-slate-700 w-32">{r.label}</span>
            <span className={r.got === 'allow' ? 'text-teal-700' : 'text-rose-700'}>
              {r.got === 'allow' ? s.allowed : s.blocked}
            </span>
            <span className={`ml-auto ${r.got === r.expected ? 'text-green-600' : 'text-amber-600'}`}>
              {r.got === r.expected ? '✓' : `✗ ${s.expected}: ${r.expected === 'allow' ? s.allowed : s.blocked}`}
            </span>
          </div>
        ))}
      </div>

      <ChallengeBox lang={lang} task={s.buildChallenge} done={done} />
    </div>
  )
}

export function Firewall({ lang }: { lang: Lang }) {
  const [pkt, setPkt] = useState<Packet>({ proto: 'TCP', port: 443 })
  const [mode, setMode] = useState<'test' | 'build'>('test')
  const decision = evaluate(RULES, pkt)
  const s = STR[lang]
  const reason = decision.ruleIndex !== null ? RULE_DESC[decision.ruleIndex][lang] : s.defaultDenyReason

  if (mode === 'build') {
    return (
      <div className="rounded-2xl border bg-white p-5">
        <div className="flex items-center justify-between mb-3">
          <p className="text-sm font-semibold text-slate-700">{s.title}</p>
          <div className="flex gap-1 text-xs font-medium">
            <button onClick={() => setMode('test')}
              className="rounded px-2 py-1 border text-slate-500 border-slate-200 hover:bg-slate-50">{s.testTab}</button>
            <button className="rounded px-2 py-1 border bg-teal-600 text-white border-teal-600">{s.buildTab}</button>
          </div>
        </div>
        <RuleLab lang={lang} />
      </div>
    )
  }

  return (
    <div className="rounded-2xl border bg-white p-5">
      <div className="flex items-center justify-between mb-3">
        <p className="text-sm font-semibold text-slate-700">{s.title}</p>
        <div className="flex gap-1 text-xs font-medium">
          <button className="rounded px-2 py-1 border bg-teal-600 text-white border-teal-600">{s.testTab}</button>
          <button onClick={() => setMode('build')}
            className="rounded px-2 py-1 border text-slate-500 border-slate-200 hover:bg-slate-50">{s.buildTab}</button>
        </div>
      </div>

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

      <ChallengeBox lang={lang} task={s.challenge} done={decision.ruleIndex === null} />
    </div>
  )
}
