import { useState } from 'react'
import { assessPosture, isCritical, type PostureLevel, type PostureState, type PostureViolation } from '@/widgets/nac/posture'
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
    subtitle: 'Setze den Zustand eines Endpunkts und sieh, ob er vollen Zugriff behält, eine Frist bekommt oder in Quarantäne muss.',
    criteriaLabel: 'Zustand des Endpunkts',
    criteria: {
      osPatched: 'Betriebssystem-Patches aktuell',
      avActive: 'Antiviren-/EDR-Schutz aktiv und aktuell (kritisch)',
      firewallOn: 'Host-Firewall an',
      diskEncrypted: 'Festplattenverschlüsselung aktiv',
    },
    criticalHint: 'Abgestuft: Nur AV/EDR ist hier kritisch und führt sofort in die Quarantäne. Die anderen drei Kriterien lösen eine Remediation-Frist aus — erst nach deren Ablauf folgt die Quarantäne.',
    resultLabel: 'Ergebnis',
    levels: { compliant: 'Compliant — Vollzugriff', grace: 'Non-Compliant — Remediation-Frist', quarantine: 'Non-Compliant — Quarantäne' },
    graceLabel: (days: number) => `Frist: ${days} Tage, danach Quarantäne`,
    criticalTag: 'kritisch',
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
      + 'Endpunkt — detailliert, aber installationspflichtig. Agentless Posture kommt ohne NAC-eigene Software auf dem Endpunkt aus: Der Zustand '
      + 'wird von außen ermittelt — durch Abfrage vorhandener Systeme (z. B. MDM/UEM per API) oder netzbasiert (Profiling, Scans). Das reicht '
      + 'weiter, geht aber weniger tief.',
    challenge: 'Erzeuge beide Stufen: einmal eine Remediation-Frist, einmal die sofortige Quarantäne.',
  },
  en: {
    title: 'Posture Assessment — not just WHO, but in what STATE',
    subtitle: 'Set the state of an endpoint and see whether it keeps full access, gets a deadline, or must go into quarantine.',
    criteriaLabel: 'Endpoint state',
    criteria: {
      osPatched: 'OS patches up to date',
      avActive: 'Antivirus/EDR active and up to date (critical)',
      firewallOn: 'Host firewall on',
      diskEncrypted: 'Disk encryption active',
    },
    criticalHint: 'Graded: only AV/EDR is critical here and leads straight into quarantine. The other three criteria trigger a remediation deadline — quarantine only follows once it expires.',
    resultLabel: 'Result',
    levels: { compliant: 'Compliant — full access', grace: 'Non-compliant — remediation deadline', quarantine: 'Non-compliant — quarantine' },
    graceLabel: (days: number) => `Deadline: ${days} days, then quarantine`,
    criticalTag: 'critical',
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
      + 'demand) — detailed, but requires installation. Agentless posture works without NAC-specific software on the endpoint: state is '
      + 'determined from the outside — by querying existing systems (e.g. MDM/UEM via API) or network-based (profiling, scans). It reaches '
      + 'further, but goes less deep.',
    challenge: 'Produce both levels: a remediation deadline once, and immediate quarantine once.',
  },
}

const LEVEL_STYLE: Record<PostureLevel, string> = {
  compliant: 'border-green-200 bg-green-50 text-green-800',
  grace: 'border-amber-200 bg-amber-50 text-amber-900',
  quarantine: 'border-rose-300 bg-rose-50 text-rose-800',
}

const CRITERIA_KEYS: (keyof PostureState)[] = ['osPatched', 'avActive', 'firewallOn', 'diskEncrypted']

export function NacPosture({ lang }: { lang: Lang }) {
  const [state, setState] = useState<PostureState>(DEFAULT_STATE)
  const [seenLevels, setSeenLevels] = useState<Set<PostureLevel>>(new Set())
  const s = STR[lang]

  const toggle = (key: keyof PostureState) => {
    setState((prev) => {
      const next = { ...prev, [key]: !prev[key] }
      const { level } = assessPosture(next)
      setSeenLevels((seen) => (seen.has(level) ? seen : new Set(seen).add(level)))
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
        className={`rounded-lg border px-3 py-2 text-sm mb-2 ${LEVEL_STYLE[result.level]}`}
        aria-live="polite"
      >
        <p className="font-semibold">{s.levels[result.level]}</p>
        <p className="text-xs mt-0.5">{s.vlanLabel}: {result.vlan[lang]}</p>
        {result.graceDays !== null && <p className="text-xs mt-0.5">{s.graceLabel(result.graceDays)}</p>}
        <p className="text-xs mt-1">{result.note[lang]}</p>
      </div>

      {!result.compliant && (
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 mb-4" aria-live="polite">
          <p className="text-sm font-semibold text-slate-800 mb-1.5">{s.remediationTitle}</p>
          <ul className="list-disc pl-5 text-xs text-slate-700 space-y-0.5">
            {result.violations.map((v: PostureViolation) => (
              <li key={v} className={isCritical(v) ? 'font-semibold text-rose-800' : undefined}>
                {s.violations[v]}{isCritical(v) && ` (${s.criticalTag})`}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
        <p className="text-sm font-semibold text-slate-800 mb-1">{s.agentTitle}</p>
        <p className="text-xs text-slate-600">{s.agentText}</p>
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={seenLevels.has('grace') && seenLevels.has('quarantine')} />
    </div>
  )
}
