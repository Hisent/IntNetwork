import { useState } from 'react'
import { assessPosture, CRITICAL_VIOLATION, type PostureState, type PostureViolation } from '@/widgets/nac/posture'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const DEFAULT_STATE: PostureState = {
  osPatched: true,
  avActive: true,
  firewallOn: true,
  diskEncrypted: true,
}

const STR = {
  de: {
    title: 'Posture Assessment — nicht nur WER, sondern in welchem ZUSTAND',
    subtitle: 'Setze den Zustand eines Endpunkts und sieh, ob er ins Produktivnetz darf oder in Quarantäne muss.',
    criteriaLabel: 'Zustand des Endpunkts',
    criteria: {
      osPatched: 'Betriebssystem-Patches aktuell',
      avActive: 'Antiviren-/EDR-Schutz aktiv und aktuell (kritisch)',
      firewallOn: 'Host-Firewall an',
      diskEncrypted: 'Festplattenverschlüsselung aktiv',
    },
    criticalHint: 'AV/EDR gilt als kritisches Kriterium: Fehlt es, reicht das allein für Quarantäne — unabhängig vom Rest.',
    resultLabel: 'Ergebnis',
    compliant: 'Compliant',
    nonCompliant: 'Non-Compliant',
    vlanLabel: 'Zugewiesenes VLAN',
    remediationTitle: 'Remediation — das fehlt noch',
    violations: {
      'os-outdated': 'Betriebssystem-Patches nachziehen',
      'av-inactive': 'AV/EDR aktivieren bzw. Signaturen aktualisieren',
      'firewall-off': 'Host-Firewall einschalten',
      'disk-not-encrypted': 'Festplattenverschlüsselung aktivieren',
    },
    noViolations: 'Keine offenen Punkte — alle Pflichtkriterien erfüllt.',
    agentTitle: 'Agent-based vs. agentless',
    agentText: 'Agent-based Posture prüft über einen (persistenten oder bei Bedarf herunterladbaren, "dissolvable") Client-Agenten direkt auf dem '
      + 'Endpunkt — detailliert, aber installationspflichtig. Agentless Posture erkennt den Zustand rein netzbasiert (z. B. über Traffic-Analyse, '
      + 'Scans oder Integrationen), ohne Software auf dem Endpunkt — breiter einsetzbar, aber mit weniger Tiefe.',
    challenge: 'Erzeuge einen non-compliant-Zustand und sieh dir die Remediation-Liste an.',
  },
  en: {
    title: 'Posture Assessment — not just WHO, but in what STATE',
    subtitle: 'Set the state of an endpoint and see whether it gets into the production network or must go into quarantine.',
    criteriaLabel: 'Endpoint state',
    criteria: {
      osPatched: 'OS patches up to date',
      avActive: 'Antivirus/EDR active and up to date (critical)',
      firewallOn: 'Host firewall on',
      diskEncrypted: 'Disk encryption active',
    },
    criticalHint: 'AV/EDR is treated as a critical criterion: if missing, that alone is enough for quarantine — regardless of the rest.',
    resultLabel: 'Result',
    compliant: 'Compliant',
    nonCompliant: 'Non-Compliant',
    vlanLabel: 'Assigned VLAN',
    remediationTitle: 'Remediation — still missing',
    violations: {
      'os-outdated': 'Install OS patches',
      'av-inactive': 'Enable AV/EDR or update signatures',
      'firewall-off': 'Turn on the host firewall',
      'disk-not-encrypted': 'Enable disk encryption',
    },
    noViolations: 'No open items — all mandatory criteria are met.',
    agentTitle: 'Agent-based vs. agentless',
    agentText: 'Agent-based posture checks the endpoint directly through a client agent (persistent, or a "dissolvable" one downloaded on '
      + 'demand) — detailed, but requires installation. Agentless posture detects state purely over the network (e.g. traffic analysis, scans, '
      + 'or integrations), without software on the endpoint — broader reach, but less depth.',
    challenge: 'Create a non-compliant state and look at the remediation list.',
  },
} as const

const CRITERIA_KEYS: (keyof PostureState)[] = ['osPatched', 'avActive', 'firewallOn', 'diskEncrypted']

export function NacPosture({ lang }: { lang: Lang }) {
  const [state, setState] = useState<PostureState>(DEFAULT_STATE)
  const [sawNonCompliant, setSawNonCompliant] = useState(false)
  const s = STR[lang]

  const toggle = (key: keyof PostureState) => {
    setState((prev) => {
      const next = { ...prev, [key]: !prev[key] }
      const r = assessPosture(next)
      if (!r.compliant) setSawNonCompliant(true)
      return next
    })
  }

  const result = assessPosture(state)

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <p className="mb-1.5 text-xs font-semibold text-slate-500" id="posture-criteria-label">{s.criteriaLabel}</p>
      <div className="flex flex-col gap-1.5 mb-1" role="group" aria-labelledby="posture-criteria-label">
        {CRITERIA_KEYS.map((key) => (
          <label
            key={key}
            className="flex items-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-sm cursor-pointer hover:bg-slate-50"
          >
            <input
              type="checkbox"
              checked={state[key]}
              onChange={() => toggle(key)}
              className="accent-teal-600"
            />
            <span className="text-slate-700">{s.criteria[key]}</span>
          </label>
        ))}
      </div>
      <p className="text-xs text-slate-500 mb-4 italic">{s.criticalHint}</p>

      <p className="mb-1.5 text-xs font-semibold text-slate-500">{s.resultLabel}</p>
      <div
        className={`rounded-lg border px-3 py-2 text-sm mb-2 ${
          result.compliant ? 'border-green-200 bg-green-50 text-green-800' : 'border-amber-200 bg-amber-50 text-amber-900'
        }`}
        aria-live="polite"
      >
        <p className="font-semibold">{result.compliant ? s.compliant : s.nonCompliant}</p>
        <p className="text-xs mt-0.5">{s.vlanLabel}: {result.vlan}</p>
        <p className="text-xs mt-1">{result.note[lang]}</p>
      </div>

      {!result.compliant && (
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 mb-4" aria-live="polite">
          <p className="text-sm font-semibold text-slate-800 mb-1.5">{s.remediationTitle}</p>
          <ul className="list-disc pl-5 text-xs text-slate-700 space-y-0.5">
            {result.violations.map((v: PostureViolation) => (
              <li key={v} className={v === CRITICAL_VIOLATION ? 'font-semibold text-amber-900' : undefined}>
                {s.violations[v]}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
        <p className="text-sm font-semibold text-slate-800 mb-1">{s.agentTitle}</p>
        <p className="text-xs text-slate-600">{s.agentText}</p>
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={sawNonCompliant} />
    </div>
  )
}
