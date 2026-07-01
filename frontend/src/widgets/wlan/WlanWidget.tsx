import { useState } from 'react'
import { overlaps, NON_OVERLAPPING, SECURITY } from '@/widgets/wlan/wlan'
import type { Lang } from '@/lib/i18n'

const CHANNELS = Array.from({ length: 11 }, (_, i) => i + 1)

const STR = {
  de: {
    title: '2,4-GHz-Kanäle — Überlappung', hint: 'Zwei Access Points in Funkreichweite. Überlappende Kanäle stören sich.',
    ap1: 'AP 1', ap2: 'AP 2', channel: 'Kanal', freeChannels: 'Überlappungsfreie Kanäle', encryption: 'WLAN-Verschlüsselung',
    clash: (a: number, b: number) => `Kanäle ${a} und ${b} überlappen → gegenseitige Störung.`,
    free: (a: number, b: number) => `Kanäle ${a} und ${b} sind überlappungsfrei.`,
  },
  en: {
    title: '2.4 GHz Channels — Overlap', hint: 'Two access points in radio range. Overlapping channels interfere with each other.',
    ap1: 'AP 1', ap2: 'AP 2', channel: 'Channel', freeChannels: 'Non-overlapping channels', encryption: 'Wi-Fi Encryption',
    clash: (a: number, b: number) => `Channels ${a} and ${b} overlap → mutual interference.`,
    free: (a: number, b: number) => `Channels ${a} and ${b} are non-overlapping.`,
  },
} as const

export function Wlan({ lang }: { lang: Lang }) {
  const [apA, setApA] = useState(1)
  const [apB, setApB] = useState(3)
  const clash = overlaps(apA, apB)
  const s = STR[lang]

  return (
    <div className="rounded-2xl border bg-white p-5 space-y-5">
      <div>
        <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
        <p className="text-xs text-slate-500 mb-3">
          {s.hint}
        </p>

        <div className="flex flex-wrap items-end gap-3 mb-3">
          {[
            [s.ap1, apA, setApA],
            [s.ap2, apB, setApB],
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
                    {s.channel} {c}
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
          {clash ? s.clash(apA, apB) : s.free(apA, apB)}
        </div>
        <p className="mt-2 text-xs text-slate-500">
          {s.freeChannels}: <span className="font-mono">{NON_OVERLAPPING.join(', ')}</span>
        </p>
      </div>

      <div>
        <p className="text-sm font-semibold text-slate-700 mb-2">{s.encryption}</p>
        <div className="rounded-lg border divide-y text-xs">
          {SECURITY.map((sec) => (
            <div key={sec.name.de} className="flex items-center gap-3 px-3 py-1.5">
              <span className={`w-14 font-semibold ${sec.safe ? 'text-teal-700' : 'text-rose-700'}`}>
                {sec.name[lang]}
              </span>
              <span className={sec.safe ? 'text-slate-600' : 'text-rose-700'}>
                {sec.safe ? '✓' : '✗'}
              </span>
              <span className="text-slate-600">{sec.note[lang]}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
