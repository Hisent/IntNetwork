import { useState } from 'react'
import { HOSTS, arpResolve, type ArpResult } from '@/widgets/arp/arp'
import type { Lang } from '@/lib/i18n'

const SENDER = HOSTS[0]

const STR = {
  de: {
    title: 'ARP — IP zu MAC auflösen', sender: 'Absender', destIp: 'Ziel-IP', notExists: 'existiert nicht',
    send: 'ARP-Request senden', clear: 'Cache leeren', cache: 'ARP-Cache', empty: 'leer',
    hit: (mac: string) => `Treffer im ARP-Cache → ${mac}. Kein Broadcast nötig.`,
    replied: (target: string, mac: string) => `Broadcast „Wer hat ${target}?“ → Antwort ${mac}, im Cache gespeichert.`,
    unanswered: (target: string) => `Broadcast „Wer hat ${target}?“ → niemand antwortet (IP existiert nicht).`,
  },
  en: {
    title: 'ARP — Resolving IP to MAC', sender: 'Sender', destIp: 'Destination IP', notExists: "doesn't exist",
    send: 'Send ARP request', clear: 'Clear cache', cache: 'ARP cache', empty: 'empty',
    hit: (mac: string) => `ARP cache hit → ${mac}. No broadcast needed.`,
    replied: (target: string, mac: string) => `Broadcast “Who has ${target}?” → reply ${mac}, stored in cache.`,
    unanswered: (target: string) => `Broadcast “Who has ${target}?” → nobody replies (IP doesn't exist).`,
  },
} as const

export function Arp({ lang }: { lang: Lang }) {
  const [table, setTable] = useState<Record<string, string>>({})
  const [target, setTarget] = useState(HOSTS[1].ip)
  const [last, setLast] = useState<ArpResult | null>(null)
  const s = STR[lang]

  function send() {
    const r = arpResolve(table, target)
    setTable(r.table)
    setLast(r)
  }

  const msg = !last
    ? null
    : !last.broadcast
      ? s.hit(last.repliedBy!)
      : last.repliedBy
        ? s.replied(target, last.repliedBy)
        : s.unanswered(target)

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-3">
        {s.sender}: <span className="font-mono">{SENDER.name[lang]} ({SENDER.ip})</span>
      </p>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4">
        {HOSTS.map((h) => {
          const isTarget = last?.broadcast && h.ip === target
          const replied = last?.repliedBy === h.mac
          return (
            <div
              key={h.ip}
              className={`rounded-xl border-2 p-2 text-xs ${
                replied ? 'border-teal-500 bg-teal-50' : isTarget ? 'border-amber-400 bg-amber-50' : 'border-slate-200 bg-white'
              }`}
            >
              <div className="font-semibold text-slate-700">{h.name[lang]}</div>
              <div className="font-mono text-[10px] text-slate-500">{h.ip}</div>
              <div className="font-mono text-[10px] text-slate-400">{h.mac}</div>
            </div>
          )
        })}
      </div>

      <div className="flex flex-wrap items-end gap-2 mb-3">
        <label className="text-xs text-slate-600">
          {s.destIp}
          <select
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            className="ml-1 border rounded px-1 py-0.5 font-mono"
          >
            {HOSTS.slice(1).map((h) => (
              <option key={h.ip} value={h.ip}>{h.ip}</option>
            ))}
            <option value="192.168.10.99">192.168.10.99 ({s.notExists})</option>
          </select>
        </label>
        <button
          onClick={send}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium"
        >
          {s.send}
        </button>
        <button onClick={() => { setTable({}); setLast(null) }} className="rounded-lg border px-3 py-1.5 text-sm">
          {s.clear}
        </button>
      </div>

      {msg && <p className="text-xs text-slate-600 mb-3">{msg}</p>}

      <p className="text-xs font-semibold text-slate-500 mb-1">{s.cache} ({SENDER.name[lang]})</p>
      <div className="rounded-lg border divide-y text-xs font-mono">
        {Object.keys(table).length === 0 ? (
          <div className="px-3 py-2 text-slate-400">{s.empty}</div>
        ) : (
          Object.entries(table).map(([ip, mac]) => (
            <div key={ip} className="flex justify-between px-3 py-1.5">
              <span className="text-slate-700">{ip}</span>
              <span className="text-slate-500">{mac}</span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
