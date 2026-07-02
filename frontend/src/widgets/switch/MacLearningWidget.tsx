import { useState } from 'react'
import { HOSTS, learnStep, type LearnResult } from '@/widgets/switch/macLearning'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'Switch — MAC-Lernen', from: 'Von', to: 'An', send: 'Frame senden', clear: 'Tabelle leeren',
    table: 'MAC-Adresstabelle', empty: 'leer',
    flooded: (ports: string, port: number) => `Ziel unbekannt → Flooding an Ports ${ports}. Quell-MAC am Port ${port} gelernt.`,
    unicast: (port: number) => `Ziel bekannt → Unicast an Port ${port}.`,
    challenge: 'Bring den Switch dazu, einen Frame als Unicast zuzustellen — Tipp: das Ziel muss vorher selbst gesendet haben.',
  },
  en: {
    title: 'Switch — MAC Learning', from: 'From', to: 'To', send: 'Send frame', clear: 'Clear table',
    table: 'MAC address table', empty: 'empty',
    flooded: (ports: string, port: number) => `Unknown destination → flooding to ports ${ports}. Source MAC learned on port ${port}.`,
    unicast: (port: number) => `Known destination → unicast to port ${port}.`,
    challenge: 'Get the switch to deliver a frame as unicast — hint: the destination must have sent something first.',
  },
} as const

export function MacLearning({ lang }: { lang: Lang }) {
  const [table, setTable] = useState<Record<string, number>>({})
  const [src, setSrc] = useState(1)
  const [dst, setDst] = useState(2)
  const [last, setLast] = useState<LearnResult | null>(null)
  const s = STR[lang]

  function send() {
    if (src === dst) return
    const dstMac = HOSTS.find((h) => h.port === dst)!.mac
    const r = learnStep(table, src, dstMac)
    setTable(r.table)
    setLast(r)
  }

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">{s.title}</p>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4">
        {HOSTS.map((h) => {
          const lit = last?.delivered.includes(h.port)
          const isSrc = last && src === h.port
          return (
            <div key={h.port}
              className={`rounded-xl border-2 p-2 text-xs ${isSrc ? 'border-teal-500 bg-teal-50' : lit ? 'border-amber-400 bg-amber-50' : 'border-slate-200 bg-white'}`}>
              <div className="font-semibold text-slate-700">{s.to} {h.port} · {h.name[lang]}</div>
              <div className="font-mono text-[10px] text-slate-500">{h.mac}</div>
            </div>
          )
        })}
      </div>

      <div className="flex flex-wrap items-end gap-2">
        <label className="text-xs text-slate-600">{s.from}
          <select value={src} onChange={(e) => setSrc(Number(e.target.value))} className="ml-1 border rounded px-1 py-0.5">
            {HOSTS.map((h) => <option key={h.port} value={h.port}>{h.name[lang]}</option>)}
          </select>
        </label>
        <label className="text-xs text-slate-600">{s.to}
          <select value={dst} onChange={(e) => setDst(Number(e.target.value))} className="ml-1 border rounded px-1 py-0.5">
            {HOSTS.map((h) => <option key={h.port} value={h.port}>{h.name[lang]}</option>)}
          </select>
        </label>
        <button onClick={send} disabled={src === dst}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium disabled:opacity-50">
          {s.send}
        </button>
        <button onClick={() => { setTable({}); setLast(null) }}
          className="rounded-lg border px-3 py-1.5 text-sm">{s.clear}</button>
      </div>

      {last && (
        <p className="mt-3 text-xs text-slate-600">
          {last.flooded ? s.flooded(last.delivered.join(', '), src) : s.unicast(last.delivered[0])}
        </p>
      )}

      <ChallengeBox lang={lang} task={s.challenge} done={last !== null && !last.flooded} />

      <div className="mt-4">
        <p className="text-xs font-semibold text-slate-500 mb-1">{s.table}</p>
        <div className="rounded-lg border divide-y text-xs font-mono">
          {Object.keys(table).length === 0
            ? <div className="px-3 py-2 text-slate-400">{s.empty}</div>
            : Object.entries(table).map(([mac, port]) => (
              <div key={mac} className="flex justify-between px-3 py-1.5">
                <span className="text-slate-700">{mac}</span><span className="text-slate-500">{s.to} {port}</span>
              </div>
            ))}
        </div>
      </div>
    </div>
  )
}
