import { useState } from 'react'
import type { Lang } from '@/lib/i18n'

type Mode = 'route' | 'policy' | 'dhcp' | 'dns' | 'packet' | 'subnet' | 'filter' | 'attack' | 'ipv6' | 'evidence'

const labels = {
  de: {
    route: ['Routing-Entscheidung', 'Liegt das Ziel im eigenen Netz oder muss das Gateway ran?'],
    policy: ['VLAN-/Firewall-Policy-Builder', 'Formuliere eine minimale, sichere Regelbasis.'],
    dhcp: ['DHCP-Störungs-Labor', 'Finde anhand des Symptoms die wahrscheinlichste Ursache.'],
    dns: ['DNS-Cache-Labor', 'Vergleiche eine Auflösung mit leerem und gefülltem Cache.'],
    packet: ['Paketreise-Zeitstrahl', 'Verfolge einen Webaufruf Schicht für Schicht.'],
    subnet: ['Subnetting-Anforderungsplaner', 'Wähle passende Netze für reale Abteilungen.'],
    filter: ['Wireshark-Filter-Challenge', 'Finde den passenden Display-Filter.'],
    attack: ['Angriff und Schutz', 'Ordne Bedrohung und Gegenmaßnahme ein.'],
    ipv6: ['IPv4/IPv6-Vergleichslabor', 'Schalte zwischen den beiden Kommunikationswegen um.'],
    evidence: ['Troubleshooting-Beweisbaum', 'Wähle den nächsten diagnostischen Schritt.'],
    check: 'Prüfen', next: 'Nächster Schritt', reset: 'Zurücksetzen', correct: '✓ Richtig', wrong: 'Noch nicht — prüfe den Hinweis.', choose: 'Auswählen',
  },
  en: {
    route: ['Routing decision', 'Is the destination local or does the gateway take over?'],
    policy: ['VLAN/firewall policy builder', 'Create a minimal, secure rule set.'],
    dhcp: ['DHCP fault lab', 'Use the symptom to find the most likely cause.'],
    dns: ['DNS cache lab', 'Compare a lookup with an empty and a populated cache.'],
    packet: ['Packet journey timeline', 'Follow a web request layer by layer.'],
    subnet: ['Subnetting requirements planner', 'Choose suitable networks for real departments.'],
    filter: ['Wireshark filter challenge', 'Find the matching display filter.'],
    attack: ['Attack and defense', 'Match the threat to the countermeasure.'],
    ipv6: ['IPv4/IPv6 comparison lab', 'Switch between the two communication paths.'],
    evidence: ['Troubleshooting evidence tree', 'Choose the next diagnostic step.'],
    check: 'Check', next: 'Next step', reset: 'Reset', correct: '✓ Correct', wrong: 'Not yet — check the hint.', choose: 'Choose',
  },
} as const

const steps = {
  de: ['Browser/Anwendung', 'DNS: Name wird zur IP', 'TCP: Verbindung zu Port 443', 'IP: Netz oder Gateway wählen', 'Ethernet/VLAN: Frame zum nächsten Hop', 'Router/NAT: weiter ins Internet'],
  en: ['Browser/application', 'DNS: resolve the name to an IP', 'TCP: connect to port 443', 'IP: choose local delivery or gateway', 'Ethernet/VLAN: frame to the next hop', 'Router/NAT: forward to the Internet'],
}

function Result({ ok, lang, hint }: { ok: boolean | null; lang: Lang; hint?: string }) {
  if (ok === null) return null
  return <p className={`mt-3 rounded-lg px-3 py-2 text-sm ${ok ? 'bg-green-50 text-green-800' : 'bg-amber-50 text-amber-800'}`}>
    {ok ? labels[lang].correct : `${labels[lang].wrong} ${hint ?? ''}`}
  </p>
}

function Shell({ mode, lang, children }: { mode: Mode; lang: Lang; children: React.ReactNode }) {
  const [title, subtitle] = labels[lang][mode]
  return <section className="rounded-2xl border border-teal-100 bg-white p-5 shadow-sm">
    <div className="mb-4"><p className="text-xs font-semibold uppercase tracking-widest text-teal-700">Learning Lab</p><h3 className="mt-1 text-lg font-bold text-slate-900">{title}</h3><p className="mt-1 text-sm text-slate-600">{subtitle}</p></div>
    {children}
  </section>
}

export function LearningLab({ mode, lang }: { mode: Mode; lang: Lang }) {
  if (mode === 'route') return <RouteLab lang={lang} />
  if (mode === 'policy') return <PolicyLab lang={lang} />
  if (mode === 'dhcp') return <DhcpLab lang={lang} />
  if (mode === 'dns') return <DnsLab lang={lang} />
  if (mode === 'packet') return <PacketLab lang={lang} />
  if (mode === 'subnet') return <SubnetLab lang={lang} />
  if (mode === 'filter') return <FilterLab lang={lang} />
  if (mode === 'attack') return <AttackLab lang={lang} />
  if (mode === 'ipv6') return <Ipv6Lab lang={lang} />
  return <EvidenceLab lang={lang} />
}

function RouteLab({ lang }: { lang: Lang }) {
  const [target, setTarget] = useState('local'); const [choice, setChoice] = useState('');
  const ok = choice ? choice === target : null
  return <Shell mode="route" lang={lang}><p className="mb-3 rounded-lg bg-slate-50 p-3 font-mono text-sm">Host: 192.168.10.37/24 · Ziel: {target === 'local' ? '192.168.10.80' : '192.168.20.80'}</p><div className="flex flex-wrap gap-2"><select value={target} onChange={e => { setTarget(e.target.value); setChoice('') }} className="rounded-lg border px-3 py-2 text-sm"><option value="local">192.168.10.80</option><option value="remote">192.168.20.80</option></select>{['local','remote'].map(v => <button key={v} onClick={() => setChoice(v)} className="rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{v === 'local' ? (lang === 'de' ? 'Direkt per Switch' : 'Direct via switch') : (lang === 'de' ? 'An Gateway' : 'To gateway')}</button>)}</div><Result lang={lang} ok={ok as boolean | null} hint={lang === 'de' ? 'Berechne beide Netzanteile mit /24.' : 'Calculate both network parts with /24.'} /></Shell>
}

function PolicyLab({ lang }: { lang: Lang }) {
  const [rules, setRules] = useState({ internet: true, erp: false, office: true }); const [ok, setOk] = useState<boolean | null>(null)
  return <Shell mode="policy" lang={lang}><div className="space-y-2 text-sm text-slate-700">{[['internet', lang === 'de' ? 'Gäste → Internet erlauben' : 'Guests → allow Internet'], ['erp', lang === 'de' ? 'Gäste → ERP erlauben' : 'Guests → allow ERP'], ['office', lang === 'de' ? 'Büro → ERP erlauben' : 'Office → allow ERP']].map(([k, text]) => <label key={k} className="flex items-center gap-2"><input type="checkbox" checked={rules[k as keyof typeof rules]} onChange={e => setRules({ ...rules, [k]: e.target.checked })} />{text}</label>)}</div><button onClick={() => setOk(rules.internet && !rules.erp && rules.office)} className="mt-4 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{labels[lang].check}</button><Result lang={lang} ok={ok} hint={lang === 'de' ? 'Gäste brauchen Internet, aber keinen ERP-Zugriff.' : 'Guests need Internet, but not ERP access.'} /></Shell>
}

function DhcpLab({ lang }: { lang: Lang }) {
  const [symptom, setSymptom] = useState('apipa'); const [answer, setAnswer] = useState(''); const ok = answer ? answer === symptom : null
  const options = lang === 'de' ? { apipa: '169.254.x.x-Adresse', pool: 'Pool erschöpft', dns: 'IP geht, Namen nicht' } : { apipa: '169.254.x.x address', pool: 'Pool exhausted', dns: 'IP works, names do not' }
  return <Shell mode="dhcp" lang={lang}><select value={symptom} onChange={e => { setSymptom(e.target.value); setAnswer('') }} className="w-full rounded-lg border px-3 py-2 text-sm">{Object.entries(options).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select><div className="mt-3 flex flex-wrap gap-2">{Object.keys(options).map(k => <button key={k} onClick={() => setAnswer(k)} className="rounded-lg border border-teal-200 px-3 py-2 text-sm text-teal-700">{k === 'apipa' ? 'DHCP prüfen' : k === 'pool' ? 'Pool prüfen' : 'DNS prüfen'}</button>)}</div><Result lang={lang} ok={ok} hint={lang === 'de' ? '169.254.x.x deutet auf fehlende DHCP-Antwort hin.' : '169.254.x.x points to a missing DHCP response.'} /></Shell>
}

function DnsLab({ lang }: { lang: Lang }) {
  const [cached, setCached] = useState(false); const [looked, setLooked] = useState(false)
  const items = cached ? (lang === 'de' ? ['Resolver-Cache trifft', 'Antwort sofort zurück'] : ['Resolver cache hit', 'Return the answer immediately']) : (lang === 'de' ? ['Resolver fragt Root/TLD/autoritativen Server', 'Antwort wird mit TTL gecacht'] : ['Resolver asks root/TLD/authoritative server', 'Answer is cached with a TTL'])
  return <Shell mode="dns" lang={lang}><label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={cached} onChange={e => { setCached(e.target.checked); setLooked(false) }} />{lang === 'de' ? 'Cache ist bereits gefüllt' : 'Cache is already populated'}</label><button onClick={() => setLooked(true)} className="mt-3 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{lang === 'de' ? 'Namen auflösen' : 'Resolve name'}</button>{looked && <ol className="mt-3 list-decimal space-y-1 pl-5 text-sm text-slate-700">{items.map(i => <li key={i}>{i}</li>)}</ol>}</Shell>
}

function PacketLab({ lang }: { lang: Lang }) { const [step, setStep] = useState(0); const list = steps[lang]; return <Shell mode="packet" lang={lang}><div className="space-y-2">{list.map((s, i) => <div key={s} className={`rounded-lg px-3 py-2 text-sm ${i <= step ? 'bg-teal-50 text-teal-900' : 'bg-slate-50 text-slate-400'}`}><span className="mr-2 font-mono">{i + 1}</span>{s}</div>)}</div><button onClick={() => setStep(step === list.length - 1 ? 0 : step + 1)} className="mt-4 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{step === list.length - 1 ? labels[lang].reset : labels[lang].next}</button></Shell> }

function SubnetLab({ lang }: { lang: Lang }) { const [plan, setPlan] = useState(''); const ok = plan ? plan === 'good' : null; return <Shell mode="subnet" lang={lang}><p className="rounded-lg bg-slate-50 p-3 text-sm text-slate-700">{lang === 'de' ? 'Anforderungen: Büro 50 Hosts · Gäste 20 · Drucker 10' : 'Requirements: office 50 hosts · guests 20 · printers 10'}</p><select value={plan} onChange={e => setPlan(e.target.value)} className="mt-3 w-full rounded-lg border px-3 py-2 text-sm"><option value="">{labels[lang].choose}</option><option value="good">/26, /27, /28</option><option value="bad">/24, /24, /24</option></select><Result lang={lang} ok={ok} hint={lang === 'de' ? 'Wähle die kleinsten Netze, die alle Hosts aufnehmen.' : 'Choose the smallest networks that fit all hosts.'} /></Shell> }

function FilterLab({ lang }: { lang: Lang }) { const [value, setValue] = useState(''); const ok = value.trim() === 'ip.addr == 192.168.20.34' ? true : value ? false : null; return <Shell mode="filter" lang={lang}><p className="text-sm text-slate-700">{lang === 'de' ? 'Alle Pakete von oder zu 192.168.20.34 anzeigen:' : 'Show all packets from or to 192.168.20.34:'}</p><input value={value} onChange={e => setValue(e.target.value)} placeholder="ip.addr == …" className="mt-3 w-full rounded-lg border px-3 py-2 font-mono text-sm" /><Result lang={lang} ok={ok} hint="ip.addr matches source or destination." /></Shell> }

function AttackLab({ lang }: { lang: Lang }) { const [value, setValue] = useState(''); const ok = value ? value === 'arp' : null; return <Shell mode="attack" lang={lang}><p className="text-sm text-slate-700">{lang === 'de' ? 'Ein Angreifer fälscht im LAN die Gateway-MAC. Welche Bedrohung und welcher Schutz passen?' : 'An attacker spoofs the gateway MAC on the LAN. Which threat and protection fit?'}</p><select value={value} onChange={e => setValue(e.target.value)} className="mt-3 w-full rounded-lg border px-3 py-2 text-sm"><option value="">{labels[lang].choose}</option><option value="arp">ARP-Spoofing → statische Prüfung/DAI</option><option value="dns">DNS → größeres Subnetz</option><option value="vlan">VLAN → mehr Broadcasts</option></select><Result lang={lang} ok={ok} hint={lang === 'de' ? 'Die gefälschte Zuordnung IP → MAC ist ARP-Spoofing.' : 'The forged IP → MAC mapping is ARP spoofing.'} /></Shell> }

function Ipv6Lab({ lang }: { lang: Lang }) { const [v6, setV6] = useState(false); const rows = v6 ? [['Adressauflösung', 'NDP / Multicast'], ['Broadcast', lang === 'de' ? 'nicht vorhanden' : 'not used'], ['Adressierung', 'SLAAC / DHCPv6']] : [['Adressauflösung', 'ARP / Broadcast'], ['Broadcast', lang === 'de' ? 'vorhanden' : 'used'], ['Adressierung', 'DHCP / statisch']]; return <Shell mode="ipv6" lang={lang}><button onClick={() => setV6(!v6)} className="rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{v6 ? 'IPv6' : 'IPv4'} ⇄ {v6 ? 'IPv4' : 'IPv6'}</button><div className="mt-4 overflow-x-auto"><table className="w-full text-left text-sm"><tbody>{rows.map(([a, b]) => <tr key={a} className="border-b"><th className="py-2 pr-4 font-medium text-slate-600">{a}</th><td className="py-2 text-slate-800">{b}</td></tr>)}</tbody></table></div></Shell> }

function EvidenceLab({ lang }: { lang: Lang }) { const [value, setValue] = useState(''); const ok = value ? value === 'dns' : null; return <Shell mode="evidence" lang={lang}><p className="text-sm text-slate-700">{lang === 'de' ? 'ping 8.8.8.8 funktioniert, aber www.nordwind.de nicht. Welcher Beweis folgt?' : 'ping 8.8.8.8 works, but www.nordwind.de does not. Which evidence comes next?'}</p><div className="mt-3 flex flex-wrap gap-2">{['dns','cable','router'].map(k => <button key={k} onClick={() => setValue(k)} className="rounded-lg border border-teal-200 px-3 py-2 text-sm text-teal-700">{k === 'dns' ? 'nslookup' : k === 'cable' ? 'Kabel prüfen' : 'Gateway pingen'}</button>)}</div><Result lang={lang} ok={ok} hint={lang === 'de' ? 'Wenn eine IP erreichbar ist, ist die Namensauflösung der nächste Beweis.' : 'If an IP is reachable, name resolution is the next evidence.'} /></Shell> }

export function LearningLabForId({ id, lang }: { id: string; lang: Lang }) { return <LearningLab mode={id.replace('learning-', '') as Mode} lang={lang} /> }
