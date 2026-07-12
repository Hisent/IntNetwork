import { useState } from 'react'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'
import { arpSteps, ipv6Stages, leasePhase, matchingRoute, matchingRoutes, natJourney, routeOptions, slaacAddress, tcpPackets, translatedPort, vlanHops } from './networkVisualsMoreLogic'

export type MoreVisualMode = 'vlan-tag-path' | 'arp-resolution' | 'route-match' | 'nat-translation' | 'dhcp-lease' | 'tcp-session' | 'ipv6-autoconfig'
const copy = {
  de: {
    'vlan-tag-path': ['VLAN-Tag-Pfad', 'Access-Links übertragen Frames ungetaggt, der Trunk trägt das 802.1Q-Tag.', 'Vergleiche alle drei Hops.'],
    'arp-resolution': ['ARP-Auflösung', 'Request per Broadcast, Reply per Unicast, danach Cache-Eintrag.', 'Führe die Auflösung bis zum ARP-Cache durch.'],
    'route-match': ['Routing-Entscheidung', 'Alle Präfixe werden binär geprüft; der längste Treffer gewinnt.', 'Vergleiche zwei verschiedene Ziele.'],
    'nat-translation': ['NAT/PAT-Übersetzung', 'Der öffentliche Port ordnet auch Rückpakete der richtigen internen Verbindung zu.', 'Verfolge Hin- und Rückweg zweier Verbindungen.'],
    'dhcp-lease': ['DHCP-Lease-Zeitachse', 'T1 startet Renew, T2 Rebind; ohne Antwort läuft die Lease ab.', 'Erreiche Renew, Rebind und Expiry.'],
    'tcp-session': ['TCP-Sitzung', 'Segmente und Zustände beider Endpunkte bleiben getrennt sichtbar.', 'Durchlaufe Handshake und geordneten Verbindungsabbau.'],
    'ipv6-autoconfig': ['IPv6-Autokonfiguration', 'Link-Local, DAD und Router-Kommunikation gehen der bevorzugten globalen Adresse voraus.', 'Führe SLAAC bis zum Status preferred aus.'],
    next: 'Nächster Schritt', reset: 'Zurücksetzen', destination: 'Zieladresse', add: 'Verbindung erzeugen', reachable: 'DHCP-Server erreichbar', time: 'Lease-Laufzeit', winner: 'Gewinner', matches: 'Treffer',
  },
  en: {
    'vlan-tag-path': ['VLAN tag path', 'Access links carry frames untagged; the trunk carries the 802.1Q tag.', 'Compare all three hops.'],
    'arp-resolution': ['ARP resolution', 'Request by broadcast, reply by unicast, then a cache entry.', 'Complete resolution through to the ARP cache.'],
    'route-match': ['Routing decision', 'Every prefix is checked in binary; the longest match wins.', 'Compare two different destinations.'],
    'nat-translation': ['NAT/PAT translation', 'The public port maps return packets to the correct internal connection.', 'Trace both directions for two connections.'],
    'dhcp-lease': ['DHCP lease timeline', 'T1 starts renew, T2 rebind; without a reply the lease expires.', 'Reach renew, rebind and expiry.'],
    'tcp-session': ['TCP session', 'Segments and both endpoint states remain visibly separate.', 'Complete the handshake and orderly connection close.'],
    'ipv6-autoconfig': ['IPv6 autoconfiguration', 'Link-local, DAD and router communication precede the preferred global address.', 'Run SLAAC through to the preferred state.'],
    next: 'Next step', reset: 'Reset', destination: 'Destination', add: 'Create connection', reachable: 'DHCP server reachable', time: 'Lease elapsed', winner: 'Winner', matches: 'Matches',
  },
} as const

function Frame({ mode, lang, done, children }: { mode: MoreVisualMode; lang: Lang; done: boolean; children: React.ReactNode }) {
  const [title, subtitle, task] = copy[lang][mode]
  return <section className="rounded-2xl border bg-white p-4 sm:p-5"><h3 className="text-sm font-semibold text-slate-700">{title}</h3><p className="mt-1 text-sm text-slate-500">{subtitle}</p><div className="mt-4">{children}</div><div aria-live="polite"><ChallengeBox lang={lang} task={task} done={done}/></div></section>
}
function Button({ lang, done, onClick }: { lang: Lang; done: boolean; onClick: () => void }) { return <button type="button" onClick={onClick} className="mt-3 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{done ? copy[lang].reset : copy[lang].next}</button> }

function VlanTagPath({ lang }: { lang: Lang }) {
  const [hop, setHop] = useState(0); const done = hop === vlanHops.length - 1; const current = vlanHops[hop]
  return <Frame mode="vlan-tag-path" lang={lang} done={done}><div className="space-y-2" aria-live="polite">{vlanHops.map((item,index) => <div key={item.from} className={`rounded-lg border px-3 py-2 text-sm ${index === hop ? 'border-teal-400 bg-teal-50' : 'border-slate-200'}`}><strong>{item.from} → {item.to}</strong><span className="ml-2 text-slate-500">{item.link}</span><p className="text-slate-600">{item.action[lang]} · <strong>{item.tagged ? 'TAG VLAN 20' : lang === 'de' ? 'ungetaggt' : 'untagged'}</strong></p></div>)}</div><p className="sr-only">{current.action[lang]}</p><Button lang={lang} done={done} onClick={() => setHop(done ? 0 : hop + 1)}/></Frame>
}
function ArpResolution({ lang }: { lang: Lang }) {
  const [step, setStep] = useState(0); const steps = arpSteps[lang]; const done = step === steps.length - 1
  return <Frame mode="arp-resolution" lang={lang} done={done}><ol className="space-y-2" aria-live="polite">{steps.map((item,index) => <li key={item} className={`rounded-lg border px-3 py-2 text-sm ${index <= step ? 'border-teal-300 bg-teal-50' : 'border-slate-200 text-slate-400'}`}><strong>{index + 1}.</strong> {item}</li>)}</ol><Button lang={lang} done={done} onClick={() => setStep(done ? 0 : step + 1)}/></Frame>
}
function RouteMatch({ lang }: { lang: Lang }) {
  const targets = ['10.20.30.42','10.20.80.9','203.0.113.8']; const [target, setTarget] = useState(targets[0]); const [seen, setSeen] = useState<string[]>([targets[0]])
  const winner = matchingRoute(target); const matches = matchingRoutes(target)
  return <Frame mode="route-match" lang={lang} done={seen.length >= 2}><label className="text-sm font-medium text-slate-600">{copy[lang].destination}<select value={target} onChange={e => { setTarget(e.target.value); setSeen(s => s.includes(e.target.value) ? s : [...s,e.target.value]) }} className="ml-2 rounded border px-2 py-1">{targets.map(value => <option key={value}>{value}</option>)}</select></label><div className="mt-3 space-y-1" aria-live="polite">{routeOptions.map(route => { const match = matches.includes(route); return <p key={route.prefix} className={`rounded border px-3 py-2 text-sm ${route.prefix === winner ? 'border-green-400 bg-green-50 font-semibold' : match ? 'border-teal-300 bg-teal-50' : 'border-slate-200 text-slate-400'}`}>{route.prefix} → {route.via} · {route.prefix === winner ? copy[lang].winner : match ? copy[lang].matches : '—'}</p> })}</div></Frame>
}
function NatTranslation({ lang }: { lang: Lang }) {
  const [ports, setPorts] = useState<number[]>([]); const [selected, setSelected] = useState(0); const done = ports.length >= 2 && selected === 1
  const add = () => { if (ports.length >= 2) { setPorts([]); setSelected(0) } else setPorts(p => [...p, p.length ? 51513 : 51512]) }
  return <Frame mode="nat-translation" lang={lang} done={done}><div className="flex flex-wrap gap-2">{ports.map((port,index) => <button type="button" aria-pressed={selected === index} key={port} onClick={() => setSelected(index)} className={`rounded border px-3 py-1.5 text-sm ${selected === index ? 'border-teal-500 bg-teal-50' : 'border-slate-200'}`}>Flow {index + 1}: {translatedPort(port)}</button>)}</div>{ports.length > 0 && <ol className="mt-3 space-y-2" aria-live="polite">{natJourney(ports[selected]).map((step,index) => <li key={step} className="break-all rounded border border-slate-200 px-3 py-2 text-sm"><strong>{index < 2 ? '→' : '←'}</strong> <code>{step}</code></li>)}</ol>}<button type="button" onClick={add} className="mt-3 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{ports.length >= 2 ? copy[lang].reset : copy[lang].add}</button></Frame>
}
function DhcpLease({ lang }: { lang: Lang }) {
  const [percent,setPercent] = useState(0); const [server,setServer] = useState(false); const [seen,setSeen] = useState<string[]>([]); const phase = leasePhase(percent,server)
  const labels = { de: { bound:'Lease gültig',renew:'Renew: Unicast an ursprünglichen Server',rebind:'Rebind: Broadcast an alle Server',expired:'Lease abgelaufen – Adresse nicht mehr nutzen' }, en: { bound:'Lease valid',renew:'Renew: unicast to original server',rebind:'Rebind: broadcast to all servers',expired:'Lease expired – stop using the address' } } as const
  const change = (value:number) => { setPercent(value); const p=leasePhase(value,server); setSeen(s => s.includes(p) ? s : [...s,p]) }
  return <Frame mode="dhcp-lease" lang={lang} done={['renew','rebind','expired'].every(p => seen.includes(p))}><label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={server} onChange={e => { setServer(e.target.checked); setSeen([]) }}/>{copy[lang].reachable}</label><label className="mt-3 block text-sm font-medium text-slate-600">{copy[lang].time}: {percent}%<input className="mt-2 block w-full accent-teal-600" type="range" min="0" max="100" step="12.5" value={percent} onChange={e => change(Number(e.target.value))}/></label><div className="mt-2 grid grid-cols-4 text-xs text-slate-500"><span>0%</span><span className="text-center">T1 50%</span><span className="text-center">T2 87.5%</span><span className="text-right">100%</span></div><p className={`mt-3 rounded-lg border px-3 py-2 text-sm ${phase === 'expired' ? 'border-rose-300 bg-rose-50' : 'border-teal-300 bg-teal-50'}`} aria-live="polite">{labels[lang][phase]}{server && percent >= 50 ? lang === 'de' ? ' · ACK setzt die Lease zurück' : ' · ACK resets the lease' : ''}</p></Frame>
}
function TcpSession({ lang }: { lang: Lang }) {
  const [step,setStep] = useState(0); const done = step === tcpPackets.length - 1; const current=tcpPackets[step]
  return <Frame mode="tcp-session" lang={lang} done={done}><div className="grid grid-cols-[1fr_auto_1fr] items-center gap-2 text-center"><strong>Client</strong><span className="text-xs text-slate-500">{lang === 'de' ? 'Segment' : 'Segment'}</span><strong>Server</strong><span className="rounded bg-slate-100 p-2 text-xs">{current.client}</span><span className="rounded bg-teal-50 px-3 py-2 text-sm" aria-live="polite">{current.from === 'Client' ? '→' : '←'} {current.packet}</span><span className="rounded bg-slate-100 p-2 text-xs">{current.server}</span></div>{current.client === 'TIME-WAIT' && <p className="mt-2 text-sm text-amber-700">TIME_WAIT: {lang === 'de' ? 'verspätete Segmente abwarten' : 'wait for delayed segments'}</p>}<Button lang={lang} done={done} onClick={() => setStep(done ? 0 : step + 1)}/></Frame>
}
function Ipv6Autoconfig({ lang }: { lang: Lang }) {
  const [step,setStep]=useState(0); const stages=ipv6Stages[lang]; const done=step===stages.length-1; const address=slaacAddress('2001:db8:20::','a8bb:ccff:fedd:ee01')
  return <Frame mode="ipv6-autoconfig" lang={lang} done={done}><ol className="space-y-2" aria-live="polite">{stages.map((item,index)=><li key={item} className={`break-all rounded-lg border px-3 py-2 text-sm ${index<=step?'border-teal-300 bg-teal-50':'border-slate-200 text-slate-400'}`}>{index+1}. {item}{index===stages.length-1 && <>: <code>{address}</code></>}</li>)}</ol><Button lang={lang} done={done} onClick={()=>setStep(done?0:step+1)}/></Frame>
}
const visuals: Record<MoreVisualMode,(props:{lang:Lang})=>React.ReactNode>={'vlan-tag-path':VlanTagPath,'arp-resolution':ArpResolution,'route-match':RouteMatch,'nat-translation':NatTranslation,'dhcp-lease':DhcpLease,'tcp-session':TcpSession,'ipv6-autoconfig':Ipv6Autoconfig}
const ids: Record<string,MoreVisualMode>={'visual-vlan-tag-path':'vlan-tag-path','visual-arp-resolution':'arp-resolution','visual-route-match':'route-match','visual-nat-translation':'nat-translation','visual-dhcp-lease':'dhcp-lease','visual-tcp-session':'tcp-session','visual-ipv6-autoconfig':'ipv6-autoconfig'}
export function NetworkVisualMoreForId({id,lang}:{id:string;lang:Lang}) { const mode=ids[id]; if(!mode)return null; const Visual=visuals[mode]; return <Visual lang={lang}/> }
