import { useState } from 'react'

import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

type Step = {
  title: Record<Lang, string>
  context: Record<Lang, string>
  prompt: Record<Lang, string>
  options: Record<Lang, string[]>
  correct: number
  explanation: Record<Lang, string>
}

const STEPS: Step[] = [
  {
    title: { de: '1. Adressplan', en: '1. Address plan' },
    context: { de: 'Ein neuer Nordwind-Standort braucht 50 Büroplätze, 20 Lagergeräte und ein Gäste-WLAN für 12 Geräte. Verfügbar ist 192.168.40.0/24.', en: 'A new Nordwind site needs 50 office seats, 20 warehouse devices and guest Wi-Fi for 12 devices. Available is 192.168.40.0/24.' },
    prompt: { de: 'Welche Aufteilung ist passend und lässt Raum für Wachstum?', en: 'Which allocation fits and leaves room for growth?' },
    options: { de: ['Büro /26, Lager /27, Gäste /28', 'Büro /27, Lager /28, Gäste /29', 'Alle drei Bereiche teilen ein /24'], en: ['Office /26, warehouse /27, guest /28', 'Office /27, warehouse /28, guest /29', 'All three areas share one /24'] },
    correct: 0,
    explanation: { de: '/26 bietet 62, /27 30 und /28 14 nutzbare Hosts. Die Netze passen in das /24 und bleiben getrennt.', en: '/26 provides 62, /27 30 and /28 14 usable hosts. The networks fit into the /24 and stay separated.' },
  },
  {
    title: { de: '2. Sicherheitsentscheidung', en: '2. Security decision' },
    context: { de: 'Das Gäste-WLAN soll Internetzugang haben, aber keine Drucker oder Dateiablagen im Büro erreichen.', en: 'Guest Wi-Fi should have internet access but must not reach office printers or file storage.' },
    prompt: { de: 'Welche Regel setzt dieses Ziel zuverlässig um?', en: 'Which rule implements this goal reliably?' },
    options: { de: ['Eigenes Gäste-VLAN; Firewall erlaubt nur Gäste → Internet', 'Gleiches VLAN wie das Büro, aber ein langes WLAN-Passwort', 'Drucker erhalten einfach andere IP-Adressen'], en: ['Separate guest VLAN; firewall allows only guest → internet', 'Same VLAN as the office but with a long Wi-Fi password', 'Printers simply receive different IP addresses'] },
    correct: 0,
    explanation: { de: 'VLAN trennt die Broadcast-Domäne; die Firewall erzwingt die gewünschte Kommunikationsregel.', en: 'The VLAN separates the broadcast domain; the firewall enforces the intended communication rule.' },
  },
  {
    title: { de: '3. Paketreise', en: '3. Packet journey' },
    context: { de: 'Ein Laptop öffnet zum ersten Mal portal.nordwind.de; das Ziel liegt außerhalb des eigenen Subnetzes.', en: 'A laptop opens portal.nordwind.de for the first time; the destination is outside its own subnet.' },
    prompt: { de: 'Was passiert zuerst, bevor das erste TCP-Paket zum Webserver gesendet werden kann?', en: 'What happens first before the first TCP packet can be sent to the web server?' },
    options: { de: ['DNS löst den Namen auf; danach ermittelt ARP die MAC-Adresse des Gateways', 'NAT übersetzt sofort die private IP; DNS ist nur für E-Mails nötig', 'Der Switch kennt automatisch die MAC-Adresse jedes Webservers im Internet'], en: ['DNS resolves the name; then ARP finds the gateway’s MAC address', 'NAT immediately translates the private IP; DNS is only needed for email', 'The switch automatically knows every web server’s MAC address on the internet'] },
    correct: 0,
    explanation: { de: 'Der Host braucht die Ziel-IP aus DNS und adressiert den ersten Ethernet-Frame an das Gateway. NAT passiert später am Übergang ins Internet.', en: 'The host needs the destination IP from DNS and addresses the first Ethernet frame to the gateway. NAT happens later at the internet boundary.' },
  },
  {
    title: { de: '4. Störfall', en: '4. Incident' },
    context: { de: 'Nach dem Umzug meldet nur das Lager: Webseiten funktionieren nicht. IP und Gateway sind korrekt; ping 8.8.8.8 klappt; nslookup portal.nordwind.de läuft in einen Timeout.', en: 'After the move, only the warehouse reports that websites fail. IP and gateway are correct; ping 8.8.8.8 works; nslookup portal.nordwind.de times out.' },
    prompt: { de: 'Wo setzt du die Diagnose fort?', en: 'Where do you continue the diagnosis?' },
    options: { de: ['Beim DNS-Dienst bzw. seiner Erreichbarkeit aus dem Lager-VLAN', 'Am Netzwerkkabel jedes Lager-PCs', 'Beim Internet-Provider, weil keine Webseite lädt'], en: ['At the DNS service or its reachability from the warehouse VLAN', 'At every warehouse PC’s network cable', 'At the internet provider because no website loads'] },
    correct: 0,
    explanation: { de: 'IP-Konnektivität bis ins Internet ist vorhanden. Das Symptom grenzt den Fehler auf die Namensauflösung oder eine Regel zu ihr ein.', en: 'IP connectivity to the internet works. The symptom narrows the fault to name resolution or a rule affecting it.' },
  },
]

const COPY = {
  de: { title: 'Abschlussfallakte — neuer Standort', subtitle: 'Plane den Standort, sichere ihn ab und grenze anschließend eine Störung ein.', next: 'Nächster Schritt', retry: 'Noch einmal versuchen', solved: 'Fallakte abgeschlossen', challenge: 'Triff alle vier Entscheidungen richtig.' },
  en: { title: 'Capstone case file — new site', subtitle: 'Plan the site, secure it and then narrow down an incident.', next: 'Next step', retry: 'Try again', solved: 'Case file completed', challenge: 'Make all four decisions correctly.' },
} as const

export function Capstone({ lang }: { lang: Lang }) {
  const [step, setStep] = useState(0)
  const [picked, setPicked] = useState<number | null>(null)
  const [complete, setComplete] = useState(false)
  const s = COPY[lang]
  const current = STEPS[step]
  const correct = picked === current.correct
  const advance = () => {
    if (!correct) { setPicked(null); return }
    if (step === STEPS.length - 1) setComplete(true)
    else { setStep((n) => n + 1); setPicked(null) }
  }

  return (
    <div className="rounded-2xl border border-teal-200 bg-teal-50/40 p-5">
      <p className="mb-1 text-sm font-semibold text-teal-900">{s.title}</p>
      <p className="mb-4 text-xs text-slate-600">{s.subtitle}</p>
      <div className="mb-4 flex gap-1.5" aria-label="Fortschritt">
        {STEPS.map((_, i) => <div key={i} className={i < step || complete ? 'h-1.5 flex-1 rounded bg-teal-600' : i === step ? 'h-1.5 flex-1 rounded bg-teal-300' : 'h-1.5 flex-1 rounded bg-slate-200'} />)}
      </div>
      {!complete ? <>
        <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-teal-700">{current.title[lang]}</p>
        <p className="mb-3 rounded-lg bg-white/80 p-3 text-sm text-slate-700">{current.context[lang]}</p>
        <p className="mb-2 font-medium text-slate-800">{current.prompt[lang]}</p>
        <div className="flex flex-col gap-1.5">
          {current.options[lang].map((option, i) => <button key={option} disabled={picked !== null} onClick={() => setPicked(i)} className={picked === null ? 'rounded-lg border border-slate-200 bg-white px-3 py-2 text-left text-sm hover:bg-slate-50' : i === current.correct ? 'rounded-lg border border-green-300 bg-green-50 px-3 py-2 text-left text-sm text-green-900' : i === picked ? 'rounded-lg border border-amber-300 bg-amber-50 px-3 py-2 text-left text-sm text-amber-900' : 'rounded-lg border border-slate-100 bg-white px-3 py-2 text-left text-sm text-slate-400'}>{option}</button>)}
        </div>
        {picked !== null && <div className="mt-3 text-sm">
          <p className={correct ? 'text-green-700' : 'text-amber-700'}>{correct ? '✓ ' : '✗ '}{current.explanation[lang]}</p>
          <button onClick={advance} className="mt-2 rounded-lg bg-teal-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-teal-700">{correct ? s.next : s.retry}</button>
        </div>}
      </> : <div className="rounded-lg border border-green-200 bg-green-50 p-4 text-sm text-green-900">✓ <span className="font-semibold">{s.solved}</span></div>}
      <ChallengeBox lang={lang} task={s.challenge} done={complete} />
    </div>
  )
}
