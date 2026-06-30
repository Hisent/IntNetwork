import { useState } from 'react'
import { HOSTS, learnStep, type LearnResult } from '@/widgets/switch/macLearning'

export function MacLearning() {
  const [table, setTable] = useState<Record<string, number>>({})
  const [src, setSrc] = useState(1)
  const [dst, setDst] = useState(2)
  const [last, setLast] = useState<LearnResult | null>(null)

  function send() {
    if (src === dst) return
    const dstMac = HOSTS.find((h) => h.port === dst)!.mac
    const r = learnStep(table, src, dstMac)
    setTable(r.table)
    setLast(r)
  }

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">Switch — MAC-Lernen</p>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4">
        {HOSTS.map((h) => {
          const lit = last?.delivered.includes(h.port)
          const isSrc = last && src === h.port
          return (
            <div key={h.port}
              className={`rounded-xl border-2 p-2 text-xs ${isSrc ? 'border-teal-500 bg-teal-50' : lit ? 'border-amber-400 bg-amber-50' : 'border-slate-200 bg-white'}`}>
              <div className="font-semibold text-slate-700">Port {h.port} · {h.name}</div>
              <div className="font-mono text-[10px] text-slate-500">{h.mac}</div>
            </div>
          )
        })}
      </div>

      <div className="flex flex-wrap items-end gap-2">
        <label className="text-xs text-slate-600">Von
          <select value={src} onChange={(e) => setSrc(Number(e.target.value))} className="ml-1 border rounded px-1 py-0.5">
            {HOSTS.map((h) => <option key={h.port} value={h.port}>{h.name}</option>)}
          </select>
        </label>
        <label className="text-xs text-slate-600">An
          <select value={dst} onChange={(e) => setDst(Number(e.target.value))} className="ml-1 border rounded px-1 py-0.5">
            {HOSTS.map((h) => <option key={h.port} value={h.port}>{h.name}</option>)}
          </select>
        </label>
        <button onClick={send} disabled={src === dst}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium disabled:opacity-50">
          Frame senden
        </button>
        <button onClick={() => { setTable({}); setLast(null) }}
          className="rounded-lg border px-3 py-1.5 text-sm">Tabelle leeren</button>
      </div>

      {last && (
        <p className="mt-3 text-xs text-slate-600">
          {last.flooded
            ? `Ziel unbekannt → Flooding an Ports ${last.delivered.join(', ')}. Quell-MAC am Port ${src} gelernt.`
            : `Ziel bekannt → Unicast an Port ${last.delivered[0]}.`}
        </p>
      )}

      <div className="mt-4">
        <p className="text-xs font-semibold text-slate-500 mb-1">MAC-Adresstabelle</p>
        <div className="rounded-lg border divide-y text-xs font-mono">
          {Object.keys(table).length === 0
            ? <div className="px-3 py-2 text-slate-400">leer</div>
            : Object.entries(table).map(([mac, port]) => (
              <div key={mac} className="flex justify-between px-3 py-1.5">
                <span className="text-slate-700">{mac}</span><span className="text-slate-500">Port {port}</span>
              </div>
            ))}
        </div>
      </div>
    </div>
  )
}
