import { useMemo, useState } from 'react'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'
import { decidingRule, rules, subnetSlices } from './networkVisualsLogic'

export type VisualMode = 'topology' | 'encapsulation' | 'subnet-map' | 'firewall-flow' | 'dns-tree'

const copy = {
  de: {
    topology: ['Live-Netzwerktopologie', 'Wähle einen Dienst und verfolge den Weg durch Nordwind.', 'Verfolge mindestens zwei unterschiedliche Dienste.'],
    encapsulation: ['Encapsulation Explorer', 'Beobachte, wie jede Schicht ihre Steuerinformationen ergänzt.', 'Packe die Anwendungsdaten vollständig bis zum Ethernet-Frame ein.'],
    subnet: ['Subnetz-Landkarte', 'Teile ein /24 sichtbar in kleinere, gleich große Netze.', 'Teile das Netz mindestens bis /27 auf.'],
    firewall: ['Firewall-Regelfluss', 'Ein Paket wird von oben nach unten bis zur ersten passenden Regel geprüft.', 'Prüfe ein Paket und identifiziere die entscheidende Regel.'],
    dns: ['DNS-Baum mit Cache', 'Vergleiche den vollständigen Weg mit einem Cache-Treffer.', 'Führe eine vollständige DNS-Auflösung bis zum autoritativen Server aus.'],
    next: 'Nächster Schritt', reset: 'Zurücksetzen', cache: 'Resolver-Cache enthält die Antwort',
  },
  en: {
    topology: ['Live network topology', 'Choose a service and follow its path through Nordwind.', 'Trace at least two different services.'],
    encapsulation: ['Encapsulation explorer', 'Watch each layer add its control information.', 'Wrap the application data all the way into an Ethernet frame.'],
    subnet: ['Subnet map', 'Split one /24 into smaller equal-sized networks.', 'Split the network to at least /27.'],
    firewall: ['Firewall rule flow', 'A packet is checked top-to-bottom until the first matching rule.', 'Inspect a packet and identify the deciding rule.'],
    dns: ['DNS tree with cache', 'Compare the full path with a cache hit.', 'Run a complete DNS lookup to the authoritative server.'],
    next: 'Next step', reset: 'Reset', cache: 'The resolver cache contains the answer',
  },
} as const

function Frame({ mode, lang, done, children }: { mode: VisualMode; lang: Lang; done: boolean; children: React.ReactNode }) {
  const key = mode === 'subnet-map' ? 'subnet' : mode === 'firewall-flow' ? 'firewall' : mode === 'dns-tree' ? 'dns' : mode
  const [title, subtitle, task] = copy[lang][key]
  return <section className="rounded-2xl border bg-white p-5">
    <p className="text-sm font-semibold text-slate-700">{title}</p>
    <p className="mt-1 text-sm text-slate-500">{subtitle}</p>
    <div className="mt-4">{children}</div>
    <ChallengeBox lang={lang} task={task} done={done} />
  </section>
}

const topologyPaths = {
  web: ['client', 'switch', 'firewall', 'internet'],
  dns: ['client', 'switch', 'router', 'dns'],
  erp: ['client', 'switch', 'router', 'erp'],
} as const

function Topology({ lang }: { lang: Lang }) {
  const [service, setService] = useState<keyof typeof topologyPaths>('web')
  const [seen, setSeen] = useState<string[]>(['web'])
  const active: readonly string[] = topologyPaths[service]
  const nodes = [
    ['client', 70, 120, lang === 'de' ? 'Client' : 'Client'], ['switch', 210, 120, 'Switch'],
    ['router', 360, 65, 'Router'], ['firewall', 360, 175, 'Firewall'],
    ['dns', 535, 35, 'DNS'], ['erp', 535, 105, 'ERP'], ['internet', 535, 190, 'Internet'],
  ] as const
  const edges = [['client','switch'],['switch','router'],['switch','firewall'],['router','dns'],['router','erp'],['firewall','internet']] as const
  const pos = Object.fromEntries(nodes.map(([id, x, y]) => [id, { x, y }]))
  const edgeActive = (a: string, b: string) => active.some((id, index) => id === a && active[index + 1] === b)
  return <Frame mode="topology" lang={lang} done={seen.length >= 2}>
    <div className="flex flex-wrap gap-2" role="group" aria-label={lang === 'de' ? 'Dienst wählen' : 'Choose service'}>
      {(['web','dns','erp'] as const).map(key => <button key={key} aria-pressed={service === key} onClick={() => { setService(key); setSeen(current => current.includes(key) ? current : [...current, key]) }} className={`rounded-lg px-3 py-1.5 text-sm font-medium ${service === key ? 'bg-teal-600 text-white' : 'border border-teal-200 text-teal-700'}`}>{key.toUpperCase()}</button>)}
    </div>
    {/* Farben als Tailwind-Klassen statt fester Hex-Werte: nur so greifen die
        Dark-Mode-Palette und der Kursfarben-Override aus index.css. */}
    <svg viewBox="0 0 620 235" role="img" aria-label={`${service.toUpperCase()}: ${active.join(' → ')}`} className="mt-3 w-full">
      {edges.map(([a,b]) => <line key={`${a}-${b}`} x1={pos[a].x} y1={pos[a].y} x2={pos[b].x} y2={pos[b].y} className={edgeActive(a,b) ? 'stroke-teal-600' : 'stroke-slate-300'} strokeWidth={edgeActive(a,b) ? 5 : 2} />)}
      {nodes.map(([id,x,y,label]) => <g key={id}><circle cx={x} cy={y} r="28" className={active.includes(id) ? 'fill-teal-100 stroke-teal-600' : 'fill-slate-50 stroke-slate-400'} strokeWidth="2"/><text x={x} y={y + 4} textAnchor="middle" fontSize="12" className="fill-slate-700">{label}</text></g>)}
    </svg>
  </Frame>
}

const layers = [
  ['HTTP', 'GET /index.html'], ['TCP', 'Src 49152 · Dst 443'], ['IP', '192.168.10.37 → 203.0.113.11'], ['Ethernet', 'Client-MAC → Gateway-MAC'],
] as const

function Encapsulation({ lang }: { lang: Lang }) {
  const [step, setStep] = useState(0)
  return <Frame mode="encapsulation" lang={lang} done={step === layers.length - 1}>
    <div className="space-y-2" aria-live="polite">
      {layers.map(([name, value], index) => <div key={name} className={`rounded-lg border px-3 py-2 transition-all ${index <= step ? 'border-teal-300 bg-teal-50' : 'border-dashed border-slate-300 text-slate-500'}`} style={{ marginLeft: `${index * 12}px`, marginRight: `${index * 12}px` }}><div className="flex flex-wrap items-baseline justify-between gap-2"><strong className="text-sm text-slate-700">{name}</strong><code className="text-xs">{value}</code></div></div>)}
    </div>
    <button onClick={() => setStep(step === layers.length - 1 ? 0 : step + 1)} className="mt-4 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{step === layers.length - 1 ? copy[lang].reset : copy[lang].next}</button>
  </Frame>
}

function SubnetMap({ lang }: { lang: Lang }) {
  const [prefix, setPrefix] = useState(24)
  const slices = useMemo(() => subnetSlices(prefix), [prefix])
  return <Frame mode="subnet-map" lang={lang} done={prefix >= 27}>
    <label className="text-sm font-medium text-slate-600">{lang === 'de' ? 'Präfix' : 'Prefix'}: /{prefix}<input className="ml-3 align-middle accent-teal-600" type="range" min="24" max="28" value={prefix} onChange={event => setPrefix(Number(event.target.value))}/></label>
    <div className="mt-4 grid gap-1" style={{ gridTemplateColumns: `repeat(${Math.min(slices.length, 4)}, minmax(0, 1fr))` }}>{slices.map(slice => <div key={slice.network} className="min-w-0 rounded border border-teal-200 bg-teal-50 p-2 text-center"><code className="block break-all text-xs text-teal-900">{slice.network}</code><span className="text-xs text-slate-700">{slice.hosts} {lang === 'de' ? 'Hosts' : 'hosts'}</span></div>)}</div>
  </Frame>
}

function FirewallFlow({ lang }: { lang: Lang }) {
  const [source, setSource] = useState<'guest'|'office'>('guest')
  const [target, setTarget] = useState<'erp'|'internet'>('erp')
  const [port, setPort] = useState(443)
  const [step, setStep] = useState(-1)
  const decision = decidingRule({ source, target, port })
  const finished = step >= decision
  return <Frame mode="firewall-flow" lang={lang} done={finished}>
    <div className="flex flex-wrap gap-3"><label className="text-xs font-medium text-slate-500">{lang === 'de' ? 'Quelle' : 'Source'}<select value={source} onChange={event => { setSource(event.target.value as 'guest'|'office'); setStep(-1) }} className="ml-2 rounded border px-2 py-1 text-sm"><option value="guest">{lang === 'de' ? 'Gäste' : 'Guest'}</option><option value="office">{lang === 'de' ? 'Büro' : 'Office'}</option></select></label><label className="text-xs font-medium text-slate-500">{lang === 'de' ? 'Ziel' : 'Target'}<select value={target} onChange={event => { setTarget(event.target.value as 'erp'|'internet'); setStep(-1) }} className="ml-2 rounded border px-2 py-1 text-sm"><option value="erp">ERP</option><option value="internet">Internet</option></select></label><label className="text-xs font-medium text-slate-500">Port<select value={port} onChange={event => { setPort(Number(event.target.value)); setStep(-1) }} className="ml-2 rounded border px-2 py-1 text-sm"><option value="443">443</option><option value="23">23</option></select></label></div>
    <div className="mt-4 space-y-2">{rules.map((rule,index) => { const reached = index <= step; const matched = reached && index === decision; return <div key={rule.label.en} className={`flex items-center justify-between rounded-lg border px-3 py-2 text-sm ${matched ? (rule.action === 'ALLOW' ? 'border-green-300 bg-green-50' : 'border-rose-300 bg-rose-50') : reached ? 'border-slate-300 bg-slate-50' : 'border-dashed border-slate-300 text-slate-500'}`}><span>{index + 1}. {rule.label[lang]}</span><strong>{matched ? rule.action : reached ? (lang === 'de' ? 'kein Treffer' : 'no match') : '—'}</strong></div>})}</div>
    <button onClick={() => setStep(finished ? -1 : Math.min(step + 1, decision))} className="mt-3 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{finished ? copy[lang].reset : copy[lang].next}</button>
  </Frame>
}

function DnsTree({ lang }: { lang: Lang }) {
  const [cached, setCached] = useState(false)
  const [completed, setCompleted] = useState(false)
  const full = ['Resolver', 'Root', 'TLD .de', lang === 'de' ? 'Autoritativ' : 'Authoritative', '203.0.113.11']
  const path = cached ? ['Resolver', 'Cache', '203.0.113.11'] : full
  const [step, setStep] = useState(0)
  const advance = () => {
    const next = step === path.length - 1 ? 0 : step + 1
    if (!cached && next === path.length - 1) setCompleted(true)
    setStep(next)
  }
  return <Frame mode="dns-tree" lang={lang} done={completed}>
    <label className="flex items-center gap-2 text-sm text-slate-700"><input type="checkbox" checked={cached} onChange={event => { setCached(event.target.checked); setStep(0) }}/>{copy[lang].cache}</label>
    <div className="mt-5 flex flex-wrap items-center justify-center gap-2" aria-live="polite">{path.map((node,index) => <div key={node} className="flex items-center gap-2"><div className={`rounded-full border px-3 py-2 text-sm ${index <= step ? 'border-teal-400 bg-teal-50 text-teal-900' : 'border-dashed border-slate-300 text-slate-500'}`}>{node}</div>{index < path.length - 1 && <span className={index < step ? 'text-teal-600' : 'text-slate-500'} aria-hidden="true">→</span>}</div>)}</div>
    <button onClick={advance} className="mt-4 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{step === path.length - 1 ? copy[lang].reset : copy[lang].next}</button>
  </Frame>
}

export function NetworkVisual({ mode, lang }: { mode: VisualMode; lang: Lang }) {
  if (mode === 'topology') return <Topology lang={lang}/>
  if (mode === 'encapsulation') return <Encapsulation lang={lang}/>
  if (mode === 'subnet-map') return <SubnetMap lang={lang}/>
  if (mode === 'firewall-flow') return <FirewallFlow lang={lang}/>
  return <DnsTree lang={lang}/>
}

export function NetworkVisualForId({ id, lang }: { id: string; lang: Lang }) {
  const modes: Record<string, VisualMode> = {
    'visual-topology': 'topology',
    'visual-encapsulation': 'encapsulation',
    'visual-subnet-map': 'subnet-map',
    'visual-firewall-flow': 'firewall-flow',
    'visual-dns-tree': 'dns-tree',
  }
  const mode = modes[id]
  if (!mode) return null
  return <NetworkVisual mode={mode} lang={lang}/>
}
