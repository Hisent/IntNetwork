import { useState } from 'react'
import { evaluatePolicy, type DeviceType, type PolicyInput, type PolicyOutcome } from '@/widgets/nac/policy'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'NAC-Policy — welches VLAN bekommt dieses Gerät?',
    subtitle: 'Stelle die Eigenschaften eines Geräts ein und sieh, welche Autorisierungsentscheidung '
      + 'die NAC-Policy trifft — und warum.',
    deviceType: 'Gerätetyp',
    managed: 'Verwalteter Laptop', iot: 'Drucker / IoT', byod: 'Unbekannt / BYOD',
    dot1x: '802.1X-fähig (hat einen Supplicant)',
    cert: 'Gültiges Zertifikat vorhanden (EAP-TLS)',
    compliant: 'Compliance-Status: konform',
    outcomeTitle: 'Ergebnis',
    reasonTitle: 'Begründung',
    vlanLabel: 'VLAN',
    outcomes: {
      full: 'Vollzugriff', quarantine: 'Quarantäne', guest: 'Gast', 'iot-mab': 'MAB / IoT', deny: 'Deny',
    } as Record<PolicyOutcome, string>,
    challenge: 'Erzeuge mindestens zwei verschiedene Ergebnisse, indem du die Eigenschaften änderst.',
  },
  en: {
    title: 'NAC policy — which VLAN does this device get?',
    subtitle: 'Set a device\'s properties and see which authorization decision the NAC policy makes '
      + '— and why.',
    deviceType: 'Device type',
    managed: 'Managed laptop', iot: 'Printer / IoT', byod: 'Unknown / BYOD',
    dot1x: '802.1X-capable (has a supplicant)',
    cert: 'Valid certificate present (EAP-TLS)',
    compliant: 'Compliance status: compliant',
    outcomeTitle: 'Outcome',
    reasonTitle: 'Reasoning',
    vlanLabel: 'VLAN',
    outcomes: {
      full: 'Full access', quarantine: 'Quarantine', guest: 'Guest', 'iot-mab': 'MAB / IoT', deny: 'Deny',
    } as Record<PolicyOutcome, string>,
    challenge: 'Produce at least two different outcomes by changing the device properties.',
  },
} as const

// Farbklassen je Ergebnis — nur neutral/rose/amber/green, keine teal-Varianten
// außerhalb der Allowlist.
const OUTCOME_STYLE: Record<PolicyOutcome, string> = {
  full: 'border-green-200 bg-green-50 text-green-800',
  quarantine: 'border-amber-300 bg-amber-50 text-amber-800',
  guest: 'border-amber-300 bg-amber-50 text-amber-800',
  'iot-mab': 'border-amber-300 bg-amber-50 text-amber-800',
  deny: 'border-rose-300 bg-rose-50 text-rose-800',
}

export function NacPolicy({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const [deviceType, setDeviceType] = useState<DeviceType>('managed')
  const [dot1xCapable, setDot1xCapable] = useState(true)
  const [hasCert, setHasCert] = useState(true)
  const [compliant, setCompliant] = useState(true)
  const [seenOutcomes, setSeenOutcomes] = useState<Set<PolicyOutcome>>(new Set())

  const input: PolicyInput = { deviceType, dot1xCapable, hasCert, compliant }
  const result = evaluatePolicy(input)

  if (!seenOutcomes.has(result.outcome)) {
    // Direkt beim Rendern nachtragen statt in einem Effect — es gibt keinen
    // sichtbaren Zwischenzustand, und ein Effect würde nur einen zusätzlichen
    // Render-Zyklus erzwingen, um exakt dasselbe zu erreichen.
    setSeenOutcomes((prev) => new Set(prev).add(result.outcome))
  }

  const done = seenOutcomes.size >= 2

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <fieldset className="mb-3">
        <legend className="text-xs font-semibold text-slate-500 mb-1">{s.deviceType}</legend>
        <div className="flex flex-wrap gap-2">
          {(['managed', 'iot', 'byod'] as DeviceType[]).map((dt) => (
            <label
              key={dt}
              className={`flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-sm cursor-pointer ${
                deviceType === dt ? 'border-teal-600 bg-teal-50/60 text-teal-800' : 'border-slate-200 text-slate-600'
              }`}
            >
              <input
                type="radio"
                name="nac-device-type"
                checked={deviceType === dt}
                onChange={() => setDeviceType(dt)}
              />
              {dt === 'managed' ? s.managed : dt === 'iot' ? s.iot : s.byod}
            </label>
          ))}
        </div>
      </fieldset>

      <div className="mb-4 flex flex-col gap-2">
        <label className="flex items-center gap-2 text-sm text-slate-700">
          <input type="checkbox" checked={dot1xCapable} onChange={(e) => setDot1xCapable(e.target.checked)} />
          {s.dot1x}
        </label>
        <label className="flex items-center gap-2 text-sm text-slate-700">
          <input type="checkbox" checked={hasCert} onChange={(e) => setHasCert(e.target.checked)} />
          {s.cert}
        </label>
        <label className="flex items-center gap-2 text-sm text-slate-700">
          <input type="checkbox" checked={compliant} onChange={(e) => setCompliant(e.target.checked)} />
          {s.compliant}
        </label>
      </div>

      <div className={`rounded-lg border-2 p-3 mb-3 ${OUTCOME_STYLE[result.outcome]}`} aria-live="polite">
        <p className="text-xs font-semibold uppercase tracking-wide opacity-80">{s.outcomeTitle}</p>
        <p className="text-lg font-bold mb-1">{s.outcomes[result.outcome]}</p>
        {result.vlan && <p className="text-sm mb-2"><span className="font-semibold">{s.vlanLabel}:</span> {result.vlan}</p>}
        <p className="text-xs font-semibold opacity-80">{s.reasonTitle}</p>
        <p className="text-sm">{result.reason[lang]}</p>
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={done} />
    </div>
  )
}
