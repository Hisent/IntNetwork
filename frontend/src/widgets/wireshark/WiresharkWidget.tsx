import { useState } from 'react'
import { CAPTURE, applyFilter, type Packet } from './wireshark'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'Mini-Wireshark — ein Mitschnitt aus dem Nordwind-Netz',
    subtitle: 'Ein PC pingt, löst einen Namen auf, loggt sich per HTTP ein und ruft danach eine Bank-Seite per HTTPS auf. Klicke Pakete an, um die Schichten zu sehen.',
    filterLabel: 'Anzeigefilter',
    filterHint: 'Probiere: http · dns · icmp · tls · ip.addr == 192.168.10.53 · tcp.port == 443',
    invalid: 'Ungültiger Filter',
    noMatch: 'Kein Paket passt auf diesen Filter.',
    detailHint: 'Klicke ein Paket in der Liste an, um seine Schichten zu sehen.',
    secretFound: 'Genau das ist das Problem: Bei HTTP wandern Zugangsdaten im Klartext durchs Netz — jeder auf dem Weg kann sie mitlesen. Vergleiche mit Paket 14: Bei TLS/HTTPS ist nur noch verschlüsselter Datensalat zu sehen.',
    challenge: 'Jemand hat sich per HTTP eingeloggt. Finde die abgefangenen Zugangsdaten im Mitschnitt (Tipp: Filter „http“, dann der POST).',
  },
  en: {
    title: 'Mini-Wireshark — a capture from the Nordwind network',
    subtitle: 'A PC pings, resolves a name, logs in via HTTP and then opens a banking site via HTTPS. Click packets to inspect their layers.',
    filterLabel: 'Display filter',
    filterHint: 'Try: http · dns · icmp · tls · ip.addr == 192.168.10.53 · tcp.port == 443',
    invalid: 'Invalid filter',
    noMatch: 'No packet matches this filter.',
    detailHint: 'Click a packet in the list to inspect its layers.',
    secretFound: 'This is exactly the problem: with HTTP, credentials travel through the network in cleartext — anyone on the path can read them. Compare with packet 14: with TLS/HTTPS all you see is encrypted gibberish.',
    challenge: 'Someone logged in via HTTP. Find the intercepted credentials in the capture (hint: filter “http”, then the POST).',
  },
} as const

// Zeilenfarben wie im echten Wireshark grob nach Protokoll
const PROTO_STYLE: Record<string, string> = {
  ICMP: 'bg-fuchsia-50 text-fuchsia-900',
  DNS: 'bg-sky-50 text-sky-900',
  TCP: 'bg-slate-50 text-slate-700',
  HTTP: 'bg-green-50 text-green-900',
  TLS: 'bg-violet-50 text-violet-900',
}

export function Wireshark({ lang }: { lang: Lang }) {
  const [filter, setFilter] = useState('')
  const [selected, setSelected] = useState<Packet | null>(null)
  const [found, setFound] = useState(false)
  const s = STR[lang]

  const filtered = applyFilter(CAPTURE, filter)
  const invalid = filtered === null

  const select = (p: Packet) => {
    setSelected(p)
    if (p.secret) setFound(true)
  }

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <label className="block mb-1 text-xs font-semibold text-slate-500">{s.filterLabel}</label>
      <input
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        spellCheck={false}
        placeholder="http"
        className={`w-full rounded-lg border px-3 py-1.5 font-mono text-sm mb-1 outline-none ${
          invalid
            ? 'border-rose-400 bg-rose-50 text-rose-900'
            : filter.trim()
              ? 'border-green-400 bg-green-50 text-green-900'
              : 'border-slate-300'
        }`}
      />
      <p className="text-xs text-slate-400 mb-3">{invalid ? `✗ ${s.invalid}` : s.filterHint}</p>

      <div className="rounded-lg border border-slate-200 overflow-x-auto mb-3">
        <table className="w-full text-xs font-mono">
          <thead>
            <tr className="bg-slate-800 text-slate-100 text-left">
              <th className="px-2 py-1 font-medium">No.</th>
              <th className="px-2 py-1 font-medium">Time</th>
              <th className="px-2 py-1 font-medium">Source</th>
              <th className="px-2 py-1 font-medium">Destination</th>
              <th className="px-2 py-1 font-medium">Protocol</th>
              <th className="px-2 py-1 font-medium">Info</th>
            </tr>
          </thead>
          <tbody>
            {(filtered ?? []).map((p) => (
              <tr
                key={p.no}
                onClick={() => select(p)}
                className={`cursor-pointer border-t border-slate-100 ${PROTO_STYLE[p.protocol] ?? ''} ${
                  selected?.no === p.no ? 'outline outline-2 -outline-offset-2 outline-teal-500' : 'hover:brightness-95'
                }`}
              >
                <td className="px-2 py-1">{p.no}</td>
                <td className="px-2 py-1">{p.time}</td>
                <td className="px-2 py-1">{p.src}</td>
                <td className="px-2 py-1">{p.dst}</td>
                <td className="px-2 py-1">{p.protocol}</td>
                <td className="px-2 py-1 whitespace-nowrap">{p.info}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered !== null && filtered.length === 0 && (
          <p className="px-3 py-2 text-xs text-slate-500">{s.noMatch}</p>
        )}
      </div>

      {selected ? (
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 mb-1 font-mono text-xs">
          <p className="text-slate-600 mb-2">
            Frame {selected.no}: {selected.protocol} — {selected.info}
          </p>
          {selected.layers.map((l) => (
            <details key={l.name} open={l.name.includes('Form') || selected.layers.length <= 3}>
              <summary className="cursor-pointer select-none text-slate-800 font-semibold py-0.5">
                ▸ {l.name}
              </summary>
              <div className="pl-5 pb-1">
                {l.fields.map((f) => (
                  <p key={f.label}>
                    <span className="text-slate-600">{f.label}:</span>{' '}
                    <span className={f.label === 'password' ? 'bg-amber-200 text-amber-900 px-1 rounded' : 'text-slate-800'}>
                      {f.value}
                    </span>
                  </p>
                ))}
              </div>
            </details>
          ))}
        </div>
      ) : (
        <p className="text-xs text-slate-500 italic mb-1">{s.detailHint}</p>
      )}

      {found && (
        <div className="mt-2 rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm text-amber-900">
          ⚠️ {s.secretFound}
        </div>
      )}

      <ChallengeBox lang={lang} task={s.challenge} done={found} />
    </div>
  )
}
