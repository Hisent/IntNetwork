import { useEffect, useRef, useState } from 'react'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'
import {
  EPHEMERAL_PORTS, STORM_OVERLOAD_TICK, matchResponse, maskFromPrefix, relaySteps,
  stateTableAfter, statefulSteps, stormDisplay, type StatefulScenario,
} from './networkVisualsDynamicsLogic'

export type DynamicVisualMode = 'bitmask' | 'broadcast-storm' | 'dhcp-relay' | 'ephemeral-ports' | 'stateful-firewall'
const copy = {
  de: {
    'bitmask': ['Subnetzmaske als Bitmuster', 'Netz-Bits (teal) sind fest, Host-Bits (grau) sind frei.', 'Sieh dir mindestens drei verschiedene Präfixe an, darunter /28.'],
    'broadcast-storm': ['Broadcast-Sturm', 'Ohne STP verdoppeln sich kreisende Frames pro Tick, bis das Netz überlastet ist.', 'Lass den Sturm bis zur Überlastung eskalieren und trenne dann den Loop.'],
    'dhcp-relay': ['DHCP-Relay über VLAN-Grenzen', 'Ohne Relay endet der Discover-Broadcast am Router; mit Relay (ip helper-address) leitet der Router als Unicast weiter.', 'Spiele beide Varianten vollständig durch.'],
    'ephemeral-ports': ['Quell-Ports zuordnen', 'Jede Verbindung nutzt einen eigenen, festen Quell-Port; die Antwort findet über den Zielport zurück.', 'Öffne drei Verbindungen und ordne zwei Antwortpakete korrekt zu.'],
    'stateful-firewall': ['Stateful Firewall', 'Eine erlaubte ausgehende Verbindung erzeugt einen State-Eintrag; die Antwort passiert ohne eigene Regel.', 'Durchlaufe beide Szenarien: erlaubt mit State und Default-Deny ohne State.'],
    next: 'Nächster Schritt', reset: 'Zurücksetzen', prefix: 'Präfix', start: 'Sturm starten', pause: 'Pause', tick: 'Tick', cutLoop: 'Loop trennen', overloaded: 'Netz überlastet',
    relayOn: 'Relay (ip helper-address) konfiguriert', openTab: 'Neuen Tab öffnen', incoming: 'Ankommendes Antwortpaket', scenario: 'Szenario', allowOut: 'Erlaubte ausgehende Verbindung', denyIn: 'Externes SYN ohne State', stateTable: 'State-Tabelle', empty: '(leer)',
  },
  en: {
    'bitmask': ['Subnet mask as a bit pattern', 'Network bits (teal) are fixed, host bits (grey) are free.', 'Look at at least three different prefixes, including /28.'],
    'broadcast-storm': ['Broadcast storm', 'Without STP, circling frames double every tick until the network overloads.', 'Let the storm escalate to overload, then disconnect the loop.'],
    'dhcp-relay': ['DHCP relay across VLAN boundaries', 'Without relay the discover broadcast stops at the router; with relay (ip helper-address) the router forwards it as unicast.', 'Play through both variants completely.'],
    'ephemeral-ports': ['Match source ports', 'Every connection uses its own fixed source port; the reply finds its way back via the destination port.', 'Open three connections and match two response packets correctly.'],
    'stateful-firewall': ['Stateful firewall', 'An allowed outbound connection creates a state entry; the reply passes without its own rule.', 'Run through both scenarios: allowed with state, and default-deny without state.'],
    next: 'Next step', reset: 'Reset', prefix: 'Prefix', start: 'Start storm', pause: 'Pause', tick: 'Tick', cutLoop: 'Disconnect loop', overloaded: 'Network overloaded',
    relayOn: 'Relay (ip helper-address) configured', openTab: 'Open new tab', incoming: 'Incoming response packet', scenario: 'Scenario', allowOut: 'Allowed outbound connection', denyIn: 'External SYN without state', stateTable: 'State table', empty: '(empty)',
  },
} as const

function Frame({ mode, lang, done, children }: { mode: DynamicVisualMode; lang: Lang; done: boolean; children: React.ReactNode }) {
  const [title, subtitle, task] = copy[lang][mode]
  return <section className="rounded-2xl border bg-white p-4 sm:p-5"><h3 className="text-sm font-semibold text-slate-700">{title}</h3><p className="mt-1 text-sm text-slate-500">{subtitle}</p><div className="mt-4">{children}</div><div aria-live="polite"><ChallengeBox lang={lang} task={task} done={done}/></div></section>
}
function Button({ lang, done, onClick, label }: { lang: Lang; done: boolean; onClick: () => void; label?: string }) {
  return <button type="button" onClick={onClick} className="mt-3 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{label ?? (done ? copy[lang].reset : copy[lang].next)}</button>
}

function Bitmask({ lang }: { lang: Lang }) {
  const [prefix, setPrefix] = useState(24)
  const [seen, setSeen] = useState<number[]>([24])
  const done = seen.length >= 3 && seen.includes(28)
  const result = maskFromPrefix(prefix)
  const change = (value: number) => { setPrefix(value); setSeen(s => s.includes(value) ? s : [...s, value]) }
  return <Frame mode="bitmask" lang={lang} done={done}>
    <label className="block text-sm font-medium text-slate-600">{copy[lang].prefix}: /{prefix}
      <input className="mt-2 block w-full accent-teal-600" type="range" min={8} max={30} step={1} value={prefix} onChange={e => change(Number(e.target.value))} aria-valuetext={`/${prefix}`}/>
    </label>
    <div className="mt-3 flex flex-wrap gap-2 font-mono text-xs" aria-live="polite">
      {result.binaryOctets.map((octet, octetIndex) => <div key={octetIndex} className="flex gap-0.5 rounded border border-slate-200 p-1.5">
        {octet.split('').map((bit, bitIndex) => <span key={bitIndex} className={`flex h-5 w-4 items-center justify-center rounded-sm ${bit === '1' ? 'bg-teal-500 text-white' : 'bg-slate-100 text-slate-400'}`}>{bit}</span>)}
      </div>)}
    </div>
    <p className="mt-3 text-sm text-slate-700"><strong>{result.dotted}</strong> = <code>/{prefix}</code> · {result.hosts} {lang === 'de' ? 'nutzbare Hosts' : 'usable hosts'}</p>
  </Frame>
}

function BroadcastStorm({ lang }: { lang: Lang }) {
  const [tick, setTick] = useState(0)
  const [running, setRunning] = useState(false)
  const [escalated, setEscalated] = useState(false)
  const [cut, setCut] = useState(false)
  const reducedMotion = typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)
  useEffect(() => {
    if (running && !reducedMotion) {
      intervalRef.current = setInterval(() => setTick(t => t + 1), 700)
      return () => { if (intervalRef.current) clearInterval(intervalRef.current) }
    }
    return undefined
  }, [running, reducedMotion])
  useEffect(() => { if (tick >= STORM_OVERLOAD_TICK) setEscalated(true) }, [tick])
  const cutLoop = () => { setRunning(false); if (tick >= STORM_OVERLOAD_TICK) setCut(true); setTick(0) }
  const done = escalated && cut
  return <Frame mode="broadcast-storm" lang={lang} done={done}>
    <p className="text-sm text-slate-600">Switch A ⇄ Switch B · {lang === 'de' ? 'zwei Leitungen (eine davon versehentlich ein Loop)' : 'two links (one of them an accidental loop)'}</p>
    <p className="mt-2 rounded-lg border border-teal-200 bg-teal-50 px-3 py-2 text-sm" aria-live="polite">{copy[lang].tick} {tick}: <strong>{stormDisplay(tick)}</strong> {lang === 'de' ? 'kreisende Frames' : 'circling frames'}{tick >= STORM_OVERLOAD_TICK && <span className="ml-2 font-semibold text-rose-600">{copy[lang].overloaded}</span>}</p>
    <p className="mt-2 text-xs text-slate-500">{lang === 'de' ? 'STP (Spanning Tree Protocol) erkennt solche Loops und blockiert vorbeugend einen Port.' : 'STP (Spanning Tree Protocol) detects such loops and preemptively blocks a port.'}</p>
    <div className="mt-3 flex flex-wrap gap-2">
      {reducedMotion
        ? <Button lang={lang} done={false} label={copy[lang].tick} onClick={() => setTick(t => t + 1)}/>
        : <Button lang={lang} done={false} label={running ? copy[lang].pause : copy[lang].start} onClick={() => setRunning(r => !r)}/>}
      <button type="button" onClick={cutLoop} className="mt-3 rounded-lg border border-rose-300 bg-rose-50 px-3 py-2 text-sm font-medium text-rose-700">{copy[lang].cutLoop}</button>
    </div>
  </Frame>
}

function DhcpRelay({ lang }: { lang: Lang }) {
  const [relayOn, setRelayOn] = useState(false)
  const [step, setStep] = useState(0)
  const [doneNoRelay, setDoneNoRelay] = useState(false)
  const [doneRelay, setDoneRelay] = useState(false)
  const steps = relaySteps(relayOn, lang)
  const atEnd = step === steps.length - 1
  const toggle = (checked: boolean) => { setRelayOn(checked); setStep(0) }
  const advance = () => {
    if (atEnd) { setStep(0); return }
    const next = step + 1
    setStep(next)
    if (next === steps.length - 1) { if (relayOn) setDoneRelay(true); else setDoneNoRelay(true) }
  }
  return <Frame mode="dhcp-relay" lang={lang} done={doneNoRelay && doneRelay}>
    <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={relayOn} onChange={e => toggle(e.target.checked)}/>{copy[lang].relayOn}</label>
    <ol className="mt-3 space-y-2" aria-live="polite">
      {steps.map((item, index) => <li key={item} className={`rounded-lg border px-3 py-2 text-sm ${index <= step ? 'border-teal-300 bg-teal-50' : 'border-slate-200 text-slate-400'}`}><strong>{index + 1}.</strong> {item}</li>)}
    </ol>
    <Button lang={lang} done={atEnd} onClick={advance}/>
    <p className="mt-2 text-xs text-slate-500">{lang === 'de' ? 'Ohne Relay:' : 'Without relay:'} {doneNoRelay ? '✅' : '—'} · {lang === 'de' ? 'Mit Relay:' : 'With relay:'} {doneRelay ? '✅' : '—'}</p>
  </Frame>
}

function EphemeralPorts({ lang }: { lang: Lang }) {
  const [opened, setOpened] = useState(0)
  const [responseIndex, setResponseIndex] = useState(0)
  const [correct, setCorrect] = useState(0)
  const [wrongIndex, setWrongIndex] = useState<number | null>(null)
  const wrongTimer = useRef<ReturnType<typeof setTimeout> | null>(null)
  useEffect(() => () => { if (wrongTimer.current) clearTimeout(wrongTimer.current) }, [])
  const flows = EPHEMERAL_PORTS.slice(0, opened)
  const done = correct >= 2
  const openTab = () => { if (opened < 3) setOpened(o => o + 1) }
  const handleClick = (index: number) => {
    // Zuordnen erst, wenn alle drei Verbindungen offen sind und ein Antwortpaket angezeigt wird.
    if (opened < 3 || responseIndex >= 2) return
    const match = matchResponse(EPHEMERAL_PORTS[responseIndex], EPHEMERAL_PORTS)
    if (index === match) { setCorrect(c => c + 1); setResponseIndex(r => r + 1); setWrongIndex(null) }
    else {
      setWrongIndex(index)
      if (wrongTimer.current) clearTimeout(wrongTimer.current)
      wrongTimer.current = setTimeout(() => setWrongIndex(null), 500)
    }
  }
  return <Frame mode="ephemeral-ports" lang={lang} done={done}>
    <button type="button" onClick={openTab} className="rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white disabled:opacity-40" disabled={opened >= 3}>{copy[lang].openTab}</button>
    <div className="mt-3 flex flex-wrap gap-2" aria-live="polite">
      {flows.map((port, index) => { const matched = index < responseIndex; return <button type="button" key={port} aria-pressed={matched} onClick={() => handleClick(index)}
        className={`rounded border px-3 py-1.5 text-sm ${wrongIndex === index ? 'border-rose-400 bg-rose-50' : matched ? 'border-green-400 bg-green-50' : 'border-slate-200'}`}>
        {matched && '✓ '}192.168.10.37:{port} → 203.0.113.11:443
      </button> })}
    </div>
    {opened === 3 && responseIndex < 2 && <p className="mt-3 rounded-lg border border-teal-200 bg-teal-50 px-3 py-2 text-sm">{copy[lang].incoming}: 203.0.113.11:443 → 192.168.10.37:<strong>{EPHEMERAL_PORTS[responseIndex]}</strong></p>}
    <p className="mt-2 text-xs text-slate-500">{correct}/2 {lang === 'de' ? 'korrekt zugeordnet' : 'matched correctly'}</p>
  </Frame>
}

function StatefulFirewall({ lang }: { lang: Lang }) {
  const [scenario, setScenario] = useState<StatefulScenario>('allow-out')
  const [step, setStep] = useState(0)
  const [doneAllow, setDoneAllow] = useState(false)
  const [doneDeny, setDoneDeny] = useState(false)
  const steps = statefulSteps(scenario, lang)
  const atEnd = step === steps.length - 1
  const table = stateTableAfter(scenario, step)
  const switchScenario = (value: StatefulScenario) => { setScenario(value); setStep(0) }
  const advance = () => {
    if (atEnd) { setStep(0); return }
    const next = step + 1
    setStep(next)
    if (next === steps.length - 1) { if (scenario === 'allow-out') setDoneAllow(true); else setDoneDeny(true) }
  }
  return <Frame mode="stateful-firewall" lang={lang} done={doneAllow && doneDeny}>
    <div className="flex gap-2 text-sm">
      <button type="button" aria-pressed={scenario === 'allow-out'} onClick={() => switchScenario('allow-out')} className={`rounded border px-3 py-1.5 ${scenario === 'allow-out' ? 'border-teal-500 bg-teal-50' : 'border-slate-200'}`}>{copy[lang].allowOut}</button>
      <button type="button" aria-pressed={scenario === 'deny-in'} onClick={() => switchScenario('deny-in')} className={`rounded border px-3 py-1.5 ${scenario === 'deny-in' ? 'border-teal-500 bg-teal-50' : 'border-slate-200'}`}>{copy[lang].denyIn}</button>
    </div>
    <ol className="mt-3 space-y-2" aria-live="polite">
      {steps.map((item, index) => <li key={item} className={`rounded-lg border px-3 py-2 text-sm ${index <= step ? 'border-teal-300 bg-teal-50' : 'border-slate-200 text-slate-400'}`}><strong>{index + 1}.</strong> {item}</li>)}
    </ol>
    <p className="mt-3 text-xs font-semibold text-slate-500">{copy[lang].stateTable}</p>
    <div className="mt-1 space-y-1" aria-live="polite">
      {table.length === 0
        ? <p className="text-sm text-slate-400">{copy[lang].empty}</p>
        : table.map(entry => <p key={entry.flow} className={`rounded border px-3 py-2 font-mono text-xs ${entry.highlighted ? 'border-green-400 bg-green-50 font-semibold' : 'border-slate-200'}`}>{entry.flow}</p>)}
    </div>
    <Button lang={lang} done={atEnd} onClick={advance}/>
    <p className="mt-2 text-xs text-slate-500">allow-out: {doneAllow ? '✅' : '—'} · deny-in: {doneDeny ? '✅' : '—'}</p>
  </Frame>
}

const visuals: Record<DynamicVisualMode, (props: { lang: Lang }) => React.ReactNode> = {
  'bitmask': Bitmask, 'broadcast-storm': BroadcastStorm, 'dhcp-relay': DhcpRelay,
  'ephemeral-ports': EphemeralPorts, 'stateful-firewall': StatefulFirewall,
}
const ids: Record<string, DynamicVisualMode> = {
  'visual-bitmask': 'bitmask', 'visual-broadcast-storm': 'broadcast-storm', 'visual-dhcp-relay': 'dhcp-relay',
  'visual-ephemeral-ports': 'ephemeral-ports', 'visual-stateful-firewall': 'stateful-firewall',
}
export function NetworkVisualDynamicForId({ id, lang }: { id: string; lang: Lang }) {
  const mode = ids[id]; if (!mode) return null; const Visual = visuals[mode]; return <Visual lang={lang}/>
}
