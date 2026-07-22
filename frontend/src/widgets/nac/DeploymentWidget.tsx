import { useState } from 'react'
import { outcome, type NacMode } from '@/widgets/nac/deployment'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const MODES: NacMode[] = ['monitor', 'low-impact', 'closed']

const STR = {
  de: {
    title: 'NAC-Einführung — Monitor → Low-Impact → Closed',
    subtitle: 'Dieselbe Situation, drei Einführungsstufen: Wähle einen Modus und ein Auth-Ergebnis und sieh, was mit dem Gerät passiert.',
    modeLabel: 'Einführungsmodus',
    modes: {
      monitor: { name: 'Monitor / Open Mode', desc: 'Nur protokollieren, nichts blocken.' },
      'low-impact': { name: 'Low-Impact Mode', desc: 'Begrenzter Zugang (dACL) schon vor der Auth.' },
      closed: { name: 'Closed Mode', desc: 'Kein Zugang ohne erfolgreiche Auth.' },
    },
    authLabel: 'Authentifizierungsergebnis',
    authOk: 'Authentifizierung erfolgreich',
    authFail: 'Authentifizierung schlägt fehl (z. B. kein Supplicant, Zertifikat abgelaufen)',
    resultLabel: 'Was passiert mit dem Gerät?',
    access: { full: 'Voller Zugriff', limited: 'Begrenzter Zugriff', none: 'Kein Zugriff' },
    logYes: 'Ereignis wird protokolliert',
    logNo: 'kein besonderer Log-Eintrag',
    explainTitle: 'Warum stufenweise ausrollen?',
    explainText: 'Ein direkter Sprung auf Closed Mode sperrt bei jedem übersehenen Gerät oder Supplicant-Problem echte Nutzer aus — '
      + 'Drucker, IoT-Geräte oder ältere Clients ohne 802.1X-Unterstützung verlieren sofort den Zugang. Monitor Mode zeigt zunächst nur, '
      + 'welche Geräte überhaupt scheitern würden, ohne jemanden auszusperren. Low-Impact Mode führt dann echte Konsequenzen ein, aber mit '
      + 'einem Sicherheitsnetz (begrenzter Zugang statt Totalausfall). Erst wenn beide Stufen sauber durchlaufen sind, folgt Closed Mode.',
    failOpenTitle: 'Fail-Open vs. Fail-Closed',
    failOpenText: 'Diese Modi regeln das Verhalten bei einem AUTH-Fehlschlag. Unabhängig davon muss man festlegen, was passiert, wenn der '
      + 'RADIUS-Server selbst komplett ausfällt: Fail-Open lässt dann alle Geräte durch (Verfügbarkeit vor Sicherheit — Betrieb läuft weiter, '
      + 'aber ungeprüft), Fail-Closed sperrt alle Geräte (Sicherheit vor Verfügbarkeit — nichts kommt mehr durch, auch keine legitimen Geräte). '
      + 'Diese Entscheidung trifft man zusätzlich zum gewählten Einführungsmodus.',
    challenge: 'Sieh dir den Fehlschlag-Fall in allen drei Modi an — Monitor, Low-Impact und Closed.',
  },
  en: {
    title: 'NAC rollout — Monitor → Low-Impact → Closed',
    subtitle: 'Same situation, three rollout stages: pick a mode and an auth outcome and see what happens to the device.',
    modeLabel: 'Deployment mode',
    modes: {
      monitor: { name: 'Monitor / Open Mode', desc: 'Log only, block nothing.' },
      'low-impact': { name: 'Low-Impact Mode', desc: 'Limited access (dACL) already before auth.' },
      closed: { name: 'Closed Mode', desc: 'No access without successful auth.' },
    },
    authLabel: 'Authentication outcome',
    authOk: 'Authentication succeeds',
    authFail: 'Authentication fails (e.g. no supplicant, expired certificate)',
    resultLabel: 'What happens to the device?',
    access: { full: 'Full access', limited: 'Limited access', none: 'No access' },
    logYes: 'Event is logged',
    logNo: 'no notable log entry',
    explainTitle: 'Why roll out in stages?',
    explainText: 'Jumping straight to Closed Mode locks out real users at every overlooked device or supplicant problem — printers, IoT '
      + 'devices, or older clients without 802.1X support lose access instantly. Monitor Mode first shows which devices would even fail, '
      + 'without locking anyone out. Low-Impact Mode then introduces real consequences, but with a safety net (limited access instead of a '
      + 'total outage). Only once both stages have run cleanly does Closed Mode follow.',
    failOpenTitle: 'Fail-Open vs. Fail-Closed',
    failOpenText: 'These modes govern behavior on an AUTH failure. Separately, you must decide what happens if the RADIUS server itself goes '
      + 'down entirely: Fail-Open then lets all devices through (availability over security — operations continue, but unchecked), '
      + 'Fail-Closed blocks all devices (security over availability — nothing gets through anymore, not even legitimate devices). This '
      + 'decision is made in addition to the chosen deployment mode.',
    challenge: 'Look at the failure case in all three modes — Monitor, Low-Impact and Closed.',
  },
} as const

const ACCESS_STYLE: Record<'full' | 'limited' | 'none', string> = {
  full: 'border-green-200 bg-green-50 text-green-800',
  limited: 'border-amber-200 bg-amber-50 text-amber-800',
  none: 'border-rose-200 bg-rose-50 text-rose-800',
}

export function NacDeployment({ lang }: { lang: Lang }) {
  const [mode, setMode] = useState<NacMode>('monitor')
  const [authOk, setAuthOk] = useState(true)
  const [seenFails, setSeenFails] = useState<Set<NacMode>>(new Set())
  const s = STR[lang]

  const pickMode = (m: NacMode) => {
    setMode(m)
    if (!authOk) setSeenFails((prev) => new Set(prev).add(m))
  }
  const pickAuth = (ok: boolean) => {
    setAuthOk(ok)
    if (!ok) setSeenFails((prev) => new Set(prev).add(mode))
  }

  const r = outcome(mode, authOk)
  const done = MODES.every((m) => seenFails.has(m))

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <p className="mb-1.5 text-xs font-semibold text-slate-500" id="nac-mode-label">{s.modeLabel}</p>
      <div className="flex flex-col gap-1.5 mb-4" role="radiogroup" aria-labelledby="nac-mode-label">
        {MODES.map((m) => (
          <label
            key={m}
            className={`flex items-start gap-2 rounded-lg border px-3 py-2 text-sm cursor-pointer transition-colors ${
              mode === m ? 'border-teal-300 bg-teal-50/60' : 'border-slate-200 hover:bg-slate-50'
            }`}
          >
            <input
              type="radio"
              name="nac-mode"
              checked={mode === m}
              onChange={() => pickMode(m)}
              className="mt-0.5 accent-teal-600"
            />
            <span>
              <span className="block font-medium text-slate-800">{s.modes[m].name}</span>
              <span className="block text-xs text-slate-500">{s.modes[m].desc}</span>
            </span>
          </label>
        ))}
      </div>

      <p className="mb-1.5 text-xs font-semibold text-slate-500" id="nac-auth-label">{s.authLabel}</p>
      <div className="flex flex-col gap-1.5 mb-4" role="radiogroup" aria-labelledby="nac-auth-label">
        <label
          className={`flex items-center gap-2 rounded-lg border px-3 py-2 text-sm cursor-pointer transition-colors ${
            authOk ? 'border-teal-300 bg-teal-50/60' : 'border-slate-200 hover:bg-slate-50'
          }`}
        >
          <input type="radio" name="nac-auth" checked={authOk} onChange={() => pickAuth(true)} className="accent-teal-600" />
          {s.authOk}
        </label>
        <label
          className={`flex items-center gap-2 rounded-lg border px-3 py-2 text-sm cursor-pointer transition-colors ${
            !authOk ? 'border-teal-300 bg-teal-50/60' : 'border-slate-200 hover:bg-slate-50'
          }`}
        >
          <input type="radio" name="nac-auth" checked={!authOk} onChange={() => pickAuth(false)} className="accent-teal-600" />
          {s.authFail}
        </label>
      </div>

      <p className="mb-1.5 text-xs font-semibold text-slate-500">{s.resultLabel}</p>
      <div className={`rounded-lg border px-3 py-2 text-sm mb-1 ${ACCESS_STYLE[r.access]}`} aria-live="polite">
        <p className="font-semibold">{s.access[r.access]}</p>
        <p className="text-xs mt-0.5">{r.log ? s.logYes : s.logNo}</p>
      </div>
      <p className="text-xs text-slate-600 mb-4" aria-live="polite">{r.note[lang]}</p>

      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 mb-3">
        <p className="text-sm font-semibold text-slate-800 mb-1">{s.explainTitle}</p>
        <p className="text-xs text-slate-600">{s.explainText}</p>
      </div>

      <div className="rounded-lg border border-amber-200 bg-amber-50 p-3">
        <p className="text-sm font-semibold text-amber-900 mb-1">{s.failOpenTitle}</p>
        <p className="text-xs text-amber-900">{s.failOpenText}</p>
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={done} />
    </div>
  )
}
