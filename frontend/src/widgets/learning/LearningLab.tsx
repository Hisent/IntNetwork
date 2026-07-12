import { useState } from 'react'
import { ChallengeBox } from '@/components/ChallengeBox'
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

const tasks = {
  de: {
    route: 'Entscheide für das ausgewählte Ziel richtig zwischen Switch und Standard-Gateway.',
    policy: 'Erlaube Gästen nur den Internetzugang und dem Büro den ERP-Zugriff.',
    dhcp: 'Ordne das aktuelle Symptom der passenden ersten Diagnose zu.',
    dns: 'Löse den Namen auf und beobachte, ob der Resolver-Cache greift.',
    packet: 'Gehe die gesamte Reise des Webaufrufs bis zum Router/NAT durch.',
    subnet: 'Wähle die kleinsten Subnetze, die alle drei Abteilungen aufnehmen.',
    filter: 'Filtere alle Pakete von oder zu 192.168.20.34.',
    attack: 'Erkenne den Angriff auf die Gateway-MAC und wähle die Schutzmaßnahme.',
    ipv6: 'Wechsle zu IPv6 und vergleiche die Unterschiede bei der Zustellung.',
    evidence: 'Wähle nach dem erfolgreichen IP-Ping den nächsten Beweisschritt.',
  },
  en: {
    route: 'Choose correctly between switch delivery and the default gateway.',
    policy: 'Allow guests Internet only and allow office access to ERP.',
    dhcp: 'Match the current symptom to the appropriate first diagnostic step.',
    dns: 'Resolve the name and observe whether the resolver cache is used.',
    packet: 'Follow the entire web-request journey through router/NAT.',
    subnet: 'Choose the smallest subnets that fit all three departments.',
    filter: 'Filter all packets from or to 192.168.20.34.',
    attack: 'Recognise the gateway-MAC attack and choose its countermeasure.',
    ipv6: 'Switch to IPv6 and compare how delivery differs.',
    evidence: 'After a successful IP ping, choose the next evidence step.',
  },
} as const

export type DhcpSymptom = 'apipa' | 'existing-only' | 'names-fail'
export type DhcpDiagnosis = 'server' | 'pool' | 'dns'

export function diagnosisForSymptom(symptom: DhcpSymptom): DhcpDiagnosis {
  return symptom === 'apipa' ? 'server' : symptom === 'existing-only' ? 'pool' : 'dns'
}

export function isValidAddressFilter(value: string): boolean {
  const normalized = value.toLowerCase().replace(/[\s()]/g, '')
  const ip = '192.168.20.34'
  return normalized === `ip.addr==${ip}`
    || normalized === `ip.src==${ip}||ip.dst==${ip}`
    || normalized === `ip.dst==${ip}||ip.src==${ip}`
}

function Result({ ok, lang, hint }: { ok: boolean | null; lang: Lang; hint?: string }) {
  if (ok === null) return null
  return <p className={`mt-3 rounded-lg px-3 py-2 text-sm ${ok ? 'bg-green-50 text-green-800' : 'bg-amber-50 text-amber-800'}`}>
    {ok ? labels[lang].correct : `${labels[lang].wrong} ${hint ?? ''}`}
  </p>
}

function Shell({ mode, lang, done, children }: { mode: Mode; lang: Lang; done: boolean; children: React.ReactNode }) {
  const [title, subtitle] = labels[lang][mode]
  return <section className="rounded-2xl border bg-white p-5">
    <div className="mb-4"><p className="text-sm font-semibold text-slate-700">{title}</p><p className="mt-1 text-sm text-slate-500">{subtitle}</p></div>
    {children}
    <ChallengeBox lang={lang} task={tasks[lang][mode]} done={done} />
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
  return <Shell mode="route" lang={lang} done={ok === true}><p className="mb-3 rounded-lg bg-slate-50 p-3 font-mono text-sm">Host: 192.168.10.37/24 · Ziel: {target === 'local' ? '192.168.10.80' : '192.168.20.80'}</p><div className="flex flex-wrap gap-2"><select value={target} onChange={e => { setTarget(e.target.value); setChoice('') }} className="rounded-lg border px-3 py-2 text-sm"><option value="local">192.168.10.80</option><option value="remote">192.168.20.80</option></select>{['local','remote'].map(v => <button key={v} onClick={() => setChoice(v)} className="rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{v === 'local' ? (lang === 'de' ? 'Direkt per Switch' : 'Direct via switch') : (lang === 'de' ? 'An Gateway' : 'To gateway')}</button>)}</div><Result lang={lang} ok={ok as boolean | null} hint={lang === 'de' ? 'Berechne beide Netzanteile mit /24.' : 'Calculate both network parts with /24.'} /></Shell>
}

function PolicyLab({ lang }: { lang: Lang }) {
  const [rules, setRules] = useState({ internet: false, erp: false, office: false }); const [ok, setOk] = useState<boolean | null>(null)
  return <Shell mode="policy" lang={lang} done={ok === true}><div className="space-y-2 text-sm text-slate-700">{[['internet', lang === 'de' ? 'Gäste → Internet erlauben' : 'Guests → allow Internet'], ['erp', lang === 'de' ? 'Gäste → ERP erlauben' : 'Guests → allow ERP'], ['office', lang === 'de' ? 'Büro → ERP erlauben' : 'Office → allow ERP']].map(([k, text]) => <label key={k} className="flex items-center gap-2"><input type="checkbox" checked={rules[k as keyof typeof rules]} onChange={e => setRules({ ...rules, [k]: e.target.checked })} />{text}</label>)}</div><button onClick={() => setOk(rules.internet && !rules.erp && rules.office)} className="mt-4 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{labels[lang].check}</button><Result lang={lang} ok={ok} hint={lang === 'de' ? 'Gäste brauchen Internet, aber keinen ERP-Zugriff.' : 'Guests need Internet, but not ERP access.'} /></Shell>
}

function DhcpLab({ lang }: { lang: Lang }) {
  const [symptom, setSymptom] = useState<DhcpSymptom>('apipa')
  const [answer, setAnswer] = useState<DhcpDiagnosis | ''>('')
  const ok = answer ? answer === diagnosisForSymptom(symptom) : null
  const symptoms: Record<DhcpSymptom, string> = lang === 'de'
    ? { apipa: 'Der neue Laptop erhält 169.254.83.12.', 'existing-only': 'Vorhandene Geräte funktionieren, neue erhalten keine Adresse.', 'names-fail': 'IP-Ziele sind erreichbar, Namen jedoch nicht.' }
    : { apipa: 'The new laptop receives 169.254.83.12.', 'existing-only': 'Existing devices work, but new devices receive no address.', 'names-fail': 'IP destinations are reachable, but names are not.' }
  const diagnoses: Record<DhcpDiagnosis, string> = lang === 'de'
    ? { server: 'DHCP-Erreichbarkeit prüfen', pool: 'Adress-Pool prüfen', dns: 'DNS-Konfiguration prüfen' }
    : { server: 'Check DHCP reachability', pool: 'Check the address pool', dns: 'Check DNS configuration' }
  return <Shell mode="dhcp" lang={lang} done={ok === true}>
    <label className="block text-xs font-medium text-slate-500">
      {lang === 'de' ? 'Beobachtung' : 'Observation'}
      <select value={symptom} onChange={e => { setSymptom(e.target.value as DhcpSymptom); setAnswer('') }} className="mt-1 w-full rounded-lg border px-3 py-2 text-sm text-slate-700">
        {Object.entries(symptoms).map(([key, value]) => <option key={key} value={key}>{value}</option>)}
      </select>
    </label>
    <div className="mt-3 flex flex-wrap gap-2">
      {(Object.keys(diagnoses) as DhcpDiagnosis[]).map(key => <button key={key} onClick={() => setAnswer(key)} className="rounded-lg border border-teal-200 px-3 py-2 text-sm text-teal-700">{diagnoses[key]}</button>)}
    </div>
    <Result lang={lang} ok={ok} hint={lang === 'de' ? 'Leite die Ursache aus dem beobachteten Verhalten ab.' : 'Infer the cause from the observed behaviour.'} />
  </Shell>
}

function DnsLab({ lang }: { lang: Lang }) {
  const [cached, setCached] = useState(false)
  const [prediction, setPrediction] = useState<'cache' | 'hierarchy' | ''>('')
  const [looked, setLooked] = useState(false)
  const items = cached ? (lang === 'de' ? ['Resolver-Cache trifft', 'Antwort sofort zurück'] : ['Resolver cache hit', 'Return the answer immediately']) : (lang === 'de' ? ['Resolver fragt Root/TLD/autoritativen Server', 'Antwort wird mit TTL gecacht'] : ['Resolver asks root/TLD/authoritative server', 'Answer is cached with a TTL'])
  const expected = cached ? 'cache' : 'hierarchy'
  const ok = looked ? prediction === expected : null
  return <Shell mode="dns" lang={lang} done={ok === true}>
    <label className="flex items-center gap-2 text-sm text-slate-700"><input type="checkbox" checked={cached} onChange={e => { setCached(e.target.checked); setPrediction(''); setLooked(false) }} />{lang === 'de' ? 'Cache ist bereits gefüllt' : 'Cache is already populated'}</label>
    <p className="mt-3 text-xs font-medium text-slate-500">{lang === 'de' ? 'Was passiert als Nächstes?' : 'What happens next?'}</p>
    <div className="mt-1 flex flex-wrap gap-2">
      <button onClick={() => { setPrediction('cache'); setLooked(false) }} className="rounded-lg border border-teal-200 px-3 py-2 text-sm text-teal-700">{lang === 'de' ? 'Antwort aus dem Cache' : 'Answer from cache'}</button>
      <button onClick={() => { setPrediction('hierarchy'); setLooked(false) }} className="rounded-lg border border-teal-200 px-3 py-2 text-sm text-teal-700">{lang === 'de' ? 'Hierarchie abfragen' : 'Query the hierarchy'}</button>
    </div>
    <button disabled={!prediction} onClick={() => setLooked(true)} className="mt-3 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white disabled:opacity-50">{lang === 'de' ? 'Auflösung starten' : 'Start lookup'}</button>
    {looked && <ol className="mt-3 list-decimal space-y-1 pl-5 text-sm text-slate-700">{items.map(i => <li key={i}>{i}</li>)}</ol>}
    <Result lang={lang} ok={ok} hint={lang === 'de' ? 'Die TTL bestimmt, wie lange eine vorhandene Antwort genutzt wird.' : 'The TTL determines how long an existing answer is reused.'} />
  </Shell>
}

function PacketLab({ lang }: { lang: Lang }) {
  const [step, setStep] = useState(0)
  const [decision, setDecision] = useState('')
  const list = steps[lang]
  const complete = step === list.length - 1 && decision === 'gateway'
  return <Shell mode="packet" lang={lang} done={complete}>
    <div className="space-y-2">{list.map((item, index) => <div key={item} className={`rounded-lg px-3 py-2 text-sm ${index <= step ? 'bg-teal-50 text-teal-900' : 'bg-slate-50 text-slate-400'}`}><span className="mr-2 font-mono">{index + 1}</span>{item}</div>)}</div>
    {step === list.length - 1 && <div className="mt-3"><p className="text-sm text-slate-700">{lang === 'de' ? 'Das Ziel liegt außerhalb des eigenen /24. Wohin geht der Ethernet-Frame zuerst?' : 'The destination is outside the local /24. Where does the Ethernet frame go first?'}</p><div className="mt-2 flex gap-2"><button onClick={() => setDecision('target')} className="rounded-lg border border-teal-200 px-3 py-2 text-sm text-teal-700">{lang === 'de' ? 'Direkt zum Ziel' : 'Directly to destination'}</button><button onClick={() => setDecision('gateway')} className="rounded-lg border border-teal-200 px-3 py-2 text-sm text-teal-700">{lang === 'de' ? 'Zum Standard-Gateway' : 'To the default gateway'}</button></div><Result lang={lang} ok={decision ? complete : null} /></div>}
    <button onClick={() => { if (step === list.length - 1) { setStep(0); setDecision('') } else setStep(step + 1) }} className="mt-4 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{step === list.length - 1 ? labels[lang].reset : labels[lang].next}</button>
  </Shell>
}

function SubnetLab({ lang }: { lang: Lang }) { const [plan, setPlan] = useState(''); const ok = plan ? plan === 'good' : null; return <Shell mode="subnet" lang={lang} done={ok === true}><p className="rounded-lg bg-slate-50 p-3 text-sm text-slate-700">{lang === 'de' ? 'Anforderungen: Büro 50 Hosts · Gäste 20 · Drucker 10' : 'Requirements: office 50 hosts · guests 20 · printers 10'}</p><select value={plan} onChange={e => setPlan(e.target.value)} className="mt-3 w-full rounded-lg border px-3 py-2 text-sm"><option value="">{labels[lang].choose}</option><option value="good">/26, /27, /28</option><option value="bad">/24, /24, /24</option></select><Result lang={lang} ok={ok} hint={lang === 'de' ? 'Wähle die kleinsten Netze, die alle Hosts aufnehmen.' : 'Choose the smallest networks that fit all hosts.'} /></Shell> }

function FilterLab({ lang }: { lang: Lang }) { const [value, setValue] = useState(''); const ok = value ? isValidAddressFilter(value) : null; return <Shell mode="filter" lang={lang} done={ok === true}><label className="block text-sm text-slate-700">{lang === 'de' ? 'Alle Pakete von oder zu 192.168.20.34 anzeigen:' : 'Show all packets from or to 192.168.20.34:'}<input value={value} onChange={e => setValue(e.target.value)} placeholder="ip.addr == …" className="mt-3 w-full rounded-lg border px-3 py-2 font-mono text-sm" /></label><Result lang={lang} ok={ok} hint={lang === 'de' ? 'Du kannst ip.addr oder eine Kombination aus ip.src und ip.dst verwenden.' : 'You can use ip.addr or combine ip.src and ip.dst.'} /></Shell> }

function AttackLab({ lang }: { lang: Lang }) { const [value, setValue] = useState(''); const ok = value ? value === 'arp' : null; const options = lang === 'de' ? [['arp', 'ARP-Spoofing → DHCP Snooping + Dynamic ARP Inspection'], ['dns', 'DNS-Fehler → größeres Subnetz'], ['vlan', 'VLAN-Fehler → mehr Broadcasts']] : [['arp', 'ARP spoofing → DHCP snooping + Dynamic ARP Inspection'], ['dns', 'DNS failure → larger subnet'], ['vlan', 'VLAN failure → more broadcasts']]; return <Shell mode="attack" lang={lang} done={ok === true}><p className="text-sm text-slate-700">{lang === 'de' ? 'Ein Angreifer fälscht im LAN die Gateway-MAC. Welche Bedrohung und welcher Schutz passen?' : 'An attacker spoofs the gateway MAC on the LAN. Which threat and protection fit?'}</p><label className="block"><span className="sr-only">{labels[lang].choose}</span><select value={value} onChange={e => setValue(e.target.value)} className="mt-3 w-full rounded-lg border px-3 py-2 text-sm"><option value="">{labels[lang].choose}</option>{options.map(([key, text]) => <option key={key} value={key}>{text}</option>)}</select></label><Result lang={lang} ok={ok} hint={lang === 'de' ? 'Die gefälschte Zuordnung IP → MAC ist ARP-Spoofing.' : 'The forged IP → MAC mapping is ARP spoofing.'} /></Shell> }

function Ipv6Lab({ lang }: { lang: Lang }) { const [v6, setV6] = useState(false); const [answer, setAnswer] = useState(''); const rowLabels = lang === 'de' ? ['Adressauflösung', 'Broadcast', 'Adressierung'] : ['Address resolution', 'Broadcast', 'Address assignment']; const rows = v6 ? [[rowLabels[0], 'NDP / Multicast'], [rowLabels[1], lang === 'de' ? 'nicht vorhanden' : 'not used'], [rowLabels[2], 'SLAAC / DHCPv6']] : [[rowLabels[0], 'ARP / Broadcast'], [rowLabels[1], lang === 'de' ? 'vorhanden' : 'used'], [rowLabels[2], lang === 'de' ? 'DHCP / statisch' : 'DHCP / static']]; const ok = answer ? answer === 'ndp' : null; return <Shell mode="ipv6" lang={lang} done={v6 && ok === true}><button onClick={() => { setV6(!v6); setAnswer('') }} className="rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white">{v6 ? 'IPv6' : 'IPv4'} ⇄ {v6 ? 'IPv4' : 'IPv6'}</button><div className="mt-4 overflow-x-auto"><table className="w-full text-left text-sm"><tbody>{rows.map(([a, b]) => <tr key={a} className="border-b"><th className="py-2 pr-4 font-medium text-slate-600">{a}</th><td className="py-2 text-slate-800">{b}</td></tr>)}</tbody></table></div>{v6 && <div className="mt-3"><p className="text-sm text-slate-700">{lang === 'de' ? 'Welches Verfahren ersetzt ARP?' : 'Which mechanism replaces ARP?'}</p><div className="mt-2 flex gap-2"><button onClick={() => setAnswer('arp')} className="rounded-lg border border-teal-200 px-3 py-2 text-sm text-teal-700">ARP</button><button onClick={() => setAnswer('ndp')} className="rounded-lg border border-teal-200 px-3 py-2 text-sm text-teal-700">NDP</button></div><Result lang={lang} ok={ok} /></div>}</Shell> }

function EvidenceLab({ lang }: { lang: Lang }) { const [value, setValue] = useState(''); const ok = value ? value === 'dns' : null; const choices = lang === 'de' ? { dns: 'nslookup ausführen', cable: 'Kabel prüfen', router: 'Gateway erneut pingen' } : { dns: 'Run nslookup', cable: 'Check the cable', router: 'Ping the gateway again' }; return <Shell mode="evidence" lang={lang} done={ok === true}><p className="text-sm text-slate-700">{lang === 'de' ? 'ping 8.8.8.8 funktioniert, aber www.nordwind.de nicht. Welcher Beweis folgt?' : 'ping 8.8.8.8 works, but www.nordwind.de does not. Which evidence comes next?'}</p><div className="mt-3 flex flex-wrap gap-2">{Object.entries(choices).map(([key, text]) => <button key={key} onClick={() => setValue(key)} className="rounded-lg border border-teal-200 px-3 py-2 text-sm text-teal-700">{text}</button>)}</div><Result lang={lang} ok={ok} hint={lang === 'de' ? 'Wenn eine IP erreichbar ist, ist die Namensauflösung der nächste Beweis.' : 'If an IP is reachable, name resolution is the next evidence.'} /></Shell> }

export function LearningLabForId({ id, lang }: { id: string; lang: Lang }) { return <LearningLab mode={id.replace('learning-', '') as Mode} lang={lang} /> }
