import { useState } from 'react'
import { DeviceCli } from '@/widgets/cli/DeviceCli'
import { routeLookup, type Route } from '@/widgets/router/routing'
import { runRouterCommand } from '@/widgets/router/routerCli'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const ROUTES: Route[] = [
  { network: '192.168.10.0', prefix: 24, via: null, iface: 'Gi0/0', ip: '192.168.10.1' },
  { network: '192.168.20.0', prefix: 24, via: null, iface: 'Gi0/1', ip: '192.168.20.1' },
  { network: '0.0.0.0', prefix: 0, via: '203.0.113.2', iface: 'Gi0/2' },
]

const PRESETS = ['192.168.10.50', '192.168.20.5', '8.8.8.8']

interface Hop { label: string; text: { de: string; en: string }; nat?: boolean }

// Hop-für-Hop-Pfade für den Traceroute-Simulator; beim externen Ziel
// übersetzt R1 die private Quell-IP (NAT) bevor es Richtung ISP geht
const TRACES: Record<string, Hop[]> = {
  '192.168.20.5': [
    { label: 'PC (192.168.10.50)', text: {
      de: 'Ziel liegt in fremdem Netz → Paket geht ans Gateway. TTL 64.',
      en: 'Destination is in another network → packet goes to the gateway. TTL 64.' } },
    { label: 'R1 (192.168.10.1)', text: {
      de: 'Routing-Tabelle: 192.168.20.0/24 ist direkt verbunden (Gi0/1). TTL 63.',
      en: 'Routing table: 192.168.20.0/24 is directly connected (Gi0/1). TTL 63.' } },
    { label: 'Ziel 192.168.20.5', text: {
      de: 'Angekommen — zwei Hops, kein NAT nötig (beide Netze privat & intern).',
      en: 'Arrived — two hops, no NAT needed (both networks private & internal).' } },
  ],
  '8.8.8.8': [
    { label: 'PC (192.168.10.50)', text: {
      de: 'Ziel liegt in fremdem Netz → Paket geht ans Gateway. TTL 64.',
      en: 'Destination is in another network → packet goes to the gateway. TTL 64.' } },
    { label: 'R1 (192.168.10.1)', nat: true, text: {
      de: 'Kein direktes Netz → Default-Route. NAT: Quell-IP 192.168.10.50 → 203.0.113.1. TTL 63.',
      en: 'No direct network → default route. NAT: source IP 192.168.10.50 → 203.0.113.1. TTL 63.' } },
    { label: 'ISP (203.0.113.2)', text: {
      de: 'Der Provider routet weiter Richtung Internet. TTL 62.',
      en: 'The provider routes onward toward the internet. TTL 62.' } },
    { label: 'Ziel 8.8.8.8', text: {
      de: 'Angekommen — die Antwort läuft denselben Weg zurück, R1 übersetzt die NAT wieder zurück.',
      en: 'Arrived — the reply takes the same path back, R1 reverses the NAT translation.' } },
  ],
}

const STR = {
  de: {
    title: 'Router Nordwind-R1 — Routing-Tabelle', destIp: 'Ziel-IP', connected: 'connected', via: 'via',
    connectedVerdict: (net: string, prefix: number, iface: string) =>
      `Ziel liegt im direkt verbundenen Netz ${net}/${prefix} → über ${iface} direkt zustellbar.`,
    viaVerdict: (net: string, prefix: number, nextHop: string, iface: string) =>
      `Kein direktes Netz → Longest-Prefix-Match ${net}/${prefix}, weiter an Next-Hop ${nextHop} (${iface}).`,
    noneVerdict: 'Keine passende Route → Ziel nicht erreichbar.',
    challenge: 'Finde eine Ziel-IP, die über die Default-Route (0.0.0.0/0) hinausgeleitet wird.',
    traceTitle: 'Traceroute — Hop für Hop', traceTarget: 'Ziel', nextHop: 'Nächster Hop',
    restart: 'Neu starten', natBadge: 'NAT',
  },
  en: {
    title: 'Router Nordwind-R1 — Routing Table', destIp: 'Destination IP', connected: 'connected', via: 'via',
    connectedVerdict: (net: string, prefix: number, iface: string) =>
      `Destination is in the directly connected network ${net}/${prefix} → deliverable directly via ${iface}.`,
    viaVerdict: (net: string, prefix: number, nextHop: string, iface: string) =>
      `No direct network → longest-prefix match ${net}/${prefix}, forwarded to next hop ${nextHop} (${iface}).`,
    noneVerdict: 'No matching route → destination unreachable.',
    challenge: 'Find a destination IP that gets forwarded via the default route (0.0.0.0/0).',
    traceTitle: 'Traceroute — hop by hop', traceTarget: 'Target', nextHop: 'Next hop',
    restart: 'Restart', natBadge: 'NAT',
  },
} as const

function Traceroute({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const [target, setTarget] = useState<keyof typeof TRACES>('8.8.8.8')
  const [step, setStep] = useState(1)
  const hops = TRACES[target]
  const finished = step >= hops.length

  return (
    <div className="mt-5">
      <p className="text-sm font-semibold text-slate-700 mb-2">{s.traceTitle}</p>
      <div className="flex flex-wrap items-center gap-2 mb-3 text-xs text-slate-600">
        {s.traceTarget}:
        {(Object.keys(TRACES) as (keyof typeof TRACES)[]).map((ip) => (
          <button key={ip} onClick={() => { setTarget(ip); setStep(1) }}
            className={`rounded-lg border px-2 py-1 font-mono ${
              target === ip ? 'border-teal-500 bg-teal-50 text-teal-700 font-medium' : 'hover:bg-slate-50'}`}>
            {ip}
          </button>
        ))}
      </div>
      <ol className="flex flex-col gap-1.5 mb-3">
        {hops.slice(0, step).map((h, i) => (
          <li key={h.label} className="flex items-start gap-3 text-xs animate-fade-up">
            <span className="w-5 shrink-0 font-mono text-slate-400">{i + 1}.</span>
            <span className="w-40 shrink-0 font-mono text-slate-700">
              {h.label}
              {h.nat && <span className="ml-1 rounded bg-amber-100 px-1 py-0.5 text-[10px] font-semibold text-amber-800">{s.natBadge}</span>}
            </span>
            <span className="text-slate-600">{h.text[lang]}</span>
          </li>
        ))}
      </ol>
      <button onClick={() => (finished ? setStep(1) : setStep((x) => x + 1))}
        className="rounded-lg border px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50">
        {finished ? s.restart : `${s.nextHop} →`}
      </button>
    </div>
  )
}

export function Routing({ lang }: { lang: Lang }) {
  const [dst, setDst] = useState('192.168.20.5')
  const res = routeLookup(ROUTES, dst)
  const s = STR[lang]

  const verdict =
    res.reason === 'connected'
      ? s.connectedVerdict(res.route!.network, res.route!.prefix, res.route!.iface)
      : res.reason === 'via'
        ? s.viaVerdict(res.route!.network, res.route!.prefix, res.route!.via!, res.route!.iface)
        : s.noneVerdict

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">{s.title}</p>

      <div className="rounded-lg border divide-y text-sm font-mono mb-4">
        {ROUTES.map((r) => (
          <div key={r.network + r.prefix} className="flex justify-between px-3 py-1.5">
            <span className="text-slate-700">
              {r.network}/{r.prefix}
            </span>
            <span className="text-slate-500">
              {r.via === null ? `${s.connected} · ${r.iface}` : `${s.via} ${r.via} · ${r.iface}`}
            </span>
          </div>
        ))}
      </div>

      <div className="flex flex-wrap items-end gap-2 mb-2">
        <label className="text-xs text-slate-600">
          {s.destIp}
          <input
            value={dst}
            onChange={(e) => setDst(e.target.value)}
            spellCheck={false}
            className="ml-1 w-36 border rounded px-2 py-1 text-sm font-mono"
          />
        </label>
        {PRESETS.map((p) => (
          <button
            key={p}
            onClick={() => setDst(p)}
            className="rounded-lg border px-2 py-1 text-xs font-mono hover:bg-slate-50"
          >
            {p}
          </button>
        ))}
      </div>

      <p className="text-xs text-slate-600">{verdict}</p>

      <ChallengeBox lang={lang} task={s.challenge}
        done={res.reason === 'via' && res.route?.prefix === 0} />

      <Traceroute lang={lang} />

      <DeviceCli prompt="Nordwind-R1#" run={(c) => runRouterCommand(ROUTES, c)} lang={lang} />
    </div>
  )
}
