import { useState } from 'react'
import { overlaps, NON_OVERLAPPING, SECURITY } from '@/widgets/wlan/wlan'

const CHANNELS = Array.from({ length: 11 }, (_, i) => i + 1)

export function Wlan() {
  const [apA, setApA] = useState(1)
  const [apB, setApB] = useState(3)
  const clash = overlaps(apA, apB)

  return (
    <div className="rounded-2xl border bg-white p-5 space-y-5">
      <div>
        <p className="text-sm font-semibold text-slate-700 mb-1">2,4-GHz-Kanäle — Überlappung</p>
        <p className="text-xs text-slate-500 mb-3">
          Zwei Access Points in Funkreichweite. Überlappende Kanäle stören sich.
        </p>

        <div className="flex flex-wrap items-end gap-3 mb-3">
          {[
            ['AP 1', apA, setApA],
            ['AP 2', apB, setApB],
          ].map(([label, val, set]) => (
            <label key={label as string} className="text-xs text-slate-600">
              {label as string}
              <select
                value={val as number}
                onChange={(e) => (set as (n: number) => void)(Number(e.target.value))}
                className="ml-1 border rounded px-1 py-0.5 font-mono"
              >
                {CHANNELS.map((c) => (
                  <option key={c} value={c}>
                    Kanal {c}
                  </option>
                ))}
              </select>
            </label>
          ))}
        </div>

        <div
          className={`rounded-lg px-3 py-2 text-sm ${
            clash ? 'bg-rose-50 text-rose-800' : 'bg-teal-50 text-teal-800'
          }`}
        >
          {clash
            ? `Kanäle ${apA} und ${apB} überlappen → gegenseitige Störung.`
            : `Kanäle ${apA} und ${apB} sind überlappungsfrei.`}
        </div>
        <p className="mt-2 text-xs text-slate-500">
          Überlappungsfreie Kanäle: <span className="font-mono">{NON_OVERLAPPING.join(', ')}</span>
        </p>
      </div>

      <div>
        <p className="text-sm font-semibold text-slate-700 mb-2">WLAN-Verschlüsselung</p>
        <div className="rounded-lg border divide-y text-xs">
          {SECURITY.map((s) => (
            <div key={s.name} className="flex items-center gap-3 px-3 py-1.5">
              <span className={`w-14 font-semibold ${s.safe ? 'text-teal-700' : 'text-rose-700'}`}>
                {s.name}
              </span>
              <span className={s.safe ? 'text-slate-600' : 'text-rose-700'}>
                {s.safe ? '✓' : '✗'}
              </span>
              <span className="text-slate-600">{s.note}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
