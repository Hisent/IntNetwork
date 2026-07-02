import { useState } from 'react'
import { serviceFor, HANDSHAKE, WELL_KNOWN } from '@/widgets/ports/ports'
import { ChallengeBox } from '@/components/ChallengeBox'
import { DeviceCli } from '@/widgets/cli/DeviceCli'
import type { Lang } from '@/lib/i18n'

const PRESETS = [80, 443, 22, 53]

// offene TCP-Ports auf dem fiktiven Host "intranet" + Banner wie im echten Leben
const OPEN_PORTS: Record<number, string> = {
  22: 'SSH-2.0-OpenSSH_9.6',
  80: 'HTTP/1.1 200 OK\nServer: nginx',
  443: '(TLS-Handshake — verschlüsselt, kein Klartext-Banner)',
}

function runPortsCommand(lang: Lang, cmd: string): string {
  const c = cmd.trim().toLowerCase()
  if (c === '?' || c === 'help') {
    return lang === 'de'
      ? 'Befehle:\n  telnet intranet <port>   TCP-Verbindung testen\n  scan intranet            offene Ports suchen'
      : 'Commands:\n  telnet intranet <port>   test a TCP connection\n  scan intranet            look for open ports'
  }
  if (c === 'scan intranet') {
    const list = Object.keys(OPEN_PORTS).map((p) => `  ${p}/tcp  open  ${WELL_KNOWN[Number(p)]}`).join('\n')
    return `Scanning intranet (192.168.10.20)…\n${list}`
  }
  const m = c.match(/^telnet\s+intranet\s+(\d+)$/)
  if (m) {
    const port = Number(m[1])
    if (OPEN_PORTS[port]) return `Trying 192.168.10.20:${port}…\nConnected to intranet.\n${OPEN_PORTS[port]}`
    if (port === 53) {
      return lang === 'de'
        ? 'Trying 192.168.10.20:53…\nConnection refused.\n(DNS läuft über UDP — telnet spricht nur TCP.)'
        : 'Trying 192.168.10.20:53…\nConnection refused.\n(DNS runs over UDP — telnet only speaks TCP.)'
    }
    return `Trying 192.168.10.20:${port}…\nConnection refused.`
  }
  return lang === 'de' ? `Unbekannter Befehl: ${cmd} — tippe ?` : `Unknown command: ${cmd} — type ?`
}

const STR = {
  de: {
    portToService: 'Port → Dienst', port: 'Port', handshake: 'TCP 3-Wege-Handshake', tcpVsUdp: 'TCP vs. UDP',
    tcp: ['verbindungsorientiert (Handshake)', 'zuverlässig, Reihenfolge garantiert', 'Web, E-Mail, SSH'],
    udp: ['verbindungslos, kein Handshake', 'schnell, keine Garantie', 'DNS, Video, VoIP, Spiele'],
    challenge: 'Finde den Port, auf dem verschlüsselte Fernwartung (SSH) läuft.',
    terminal: 'Ausprobieren: Terminal',
  },
  en: {
    portToService: 'Port → Service', port: 'Port', handshake: 'TCP 3-Way Handshake', tcpVsUdp: 'TCP vs. UDP',
    tcp: ['connection-oriented (handshake)', 'reliable, order guaranteed', 'Web, email, SSH'],
    udp: ['connectionless, no handshake', 'fast, no guarantees', 'DNS, video, VoIP, games'],
    challenge: 'Find the port where encrypted remote administration (SSH) runs.',
    terminal: 'Try it: terminal',
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

      <div>
        <p className="text-sm font-semibold text-slate-700">{s.terminal}</p>
        <DeviceCli prompt="pc-lager-01$" run={(c) => runPortsCommand(lang, c)} />
      </div>
    </div>
  )
}
