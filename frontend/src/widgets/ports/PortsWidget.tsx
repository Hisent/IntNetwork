import { useState } from 'react'
import { serviceFor, HANDSHAKE, WELL_KNOWN } from '@/widgets/ports/ports'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const PRESETS = [80, 443, 22, 53]

const STR = {
  de: {
    portToService: 'Port → Dienst', port: 'Port', handshake: 'TCP 3-Wege-Handshake', tcpVsUdp: 'TCP vs. UDP',
    tcp: ['verbindungsorientiert (Handshake)', 'zuverlässig, Reihenfolge garantiert', 'Web, E-Mail, SSH'],
    udp: ['verbindungslos, kein Handshake', 'schnell, keine Garantie', 'DNS, Video, VoIP, Spiele'],
    challenge: 'Finde den Port, auf dem verschlüsselte Fernwartung (SSH) läuft.',
  },
  en: {
    portToService: 'Port → Service', port: 'Port', handshake: 'TCP 3-Way Handshake', tcpVsUdp: 'TCP vs. UDP',
    tcp: ['connection-oriented (handshake)', 'reliable, order guaranteed', 'Web, email, SSH'],
    udp: ['connectionless, no handshake', 'fast, no guarantees', 'DNS, video, VoIP, games'],
    challenge: 'Find the port where encrypted remote administration (SSH) runs.',
  },
} as const

export function Ports({ lang }: { lang: Lang }) {
  const [port, setPort] = useState(443)
  const s = STR[lang]

  return (
    <div className="rounded-2xl border bg-white p-5 space-y-5">
      <div>
        <p className="text-sm font-semibold text-slate-700 mb-3">{s.portToService}</p>
        <div className="flex flex-wrap items-end gap-2 mb-2">
          <label className="text-xs text-slate-600">
            {s.port}
            <input
              type="number"
              value={port}
              onChange={(e) => setPort(Number(e.target.value) || 0)}
              className="ml-1 w-24 border rounded px-2 py-1 text-sm font-mono"
            />
          </label>
          {PRESETS.map((p) => (
            <button
              key={p}
              onClick={() => setPort(p)}
              className="rounded-lg border px-2 py-1 text-xs font-mono hover:bg-slate-50"
            >
              {p} · {WELL_KNOWN[p]}
            </button>
          ))}
        </div>
        <p className="text-xs text-slate-600">
          {s.port} <span className="font-mono">{port}</span> →{' '}
          <span className="font-mono text-teal-700">{serviceFor(port, lang)}</span>
        </p>
        <ChallengeBox lang={lang} task={s.challenge} done={port === 22} />
      </div>

      <div>
        <p className="text-sm font-semibold text-slate-700 mb-3">{s.handshake}</p>
        <ol className="space-y-2">
          {HANDSHAKE.map((step, i) => (
            <li key={i} className="flex items-center gap-3 text-xs">
              <span className="w-14 shrink-0 text-slate-500">{step.from}</span>
              <span className="text-slate-300">{step.from === 'Client' ? '───▶' : '◀───'}</span>
              <span className="rounded bg-teal-100 px-2 py-0.5 font-mono font-semibold text-teal-700">
                {step.flag}
              </span>
              <span className="text-slate-600">{step.text[lang]}</span>
            </li>
          ))}
        </ol>
      </div>

      <div>
        <p className="text-sm font-semibold text-slate-700 mb-2">{s.tcpVsUdp}</p>
        <div className="grid grid-cols-2 gap-3 text-xs">
          <div className="rounded-xl border p-3">
            <p className="font-semibold text-slate-700 mb-1">TCP</p>
            <ul className="list-disc list-inside text-slate-600 space-y-0.5">
              {s.tcp.map((line) => <li key={line}>{line}</li>)}
            </ul>
          </div>
          <div className="rounded-xl border p-3">
            <p className="font-semibold text-slate-700 mb-1">UDP</p>
            <ul className="list-disc list-inside text-slate-600 space-y-0.5">
              {s.udp.map((line) => <li key={line}>{line}</li>)}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
