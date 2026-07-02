import { useState } from 'react'
import { SCENARIOS, canDiagnose, outputFor, MIN_EVIDENCE } from './troubleshoot'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'IT-Support-Simulator — finde den Fehler',
    subtitle: 'Drei echte Störungsmeldungen bei Nordwind. Sammle Beweise im Terminal, dann stelle deine Diagnose.',
    ticket: 'Störungsmeldung',
    terminalHint: 'Noch keine Befehle ausgeführt — klicke unten einen Befehl an.',
    evidence: `Führe mindestens ${MIN_EVIDENCE} Befehle aus, bevor du eine Diagnose stellst.`,
    diagnose: 'Deine Diagnose:',
    submit: 'Diagnose stellen',
    wrong: 'Das passt nicht zu den Ausgaben — sieh sie dir noch einmal genau an.',
    solvedTag: 'gelöst',
    challenge: 'Löse alle drei Störfälle mit der richtigen Diagnose.',
  },
  en: {
    title: 'IT support simulator — find the fault',
    subtitle: 'Three real trouble tickets at Nordwind. Gather evidence in the terminal, then make your diagnosis.',
    ticket: 'Trouble ticket',
    terminalHint: 'No commands run yet — click a command below.',
    evidence: `Run at least ${MIN_EVIDENCE} commands before making a diagnosis.`,
    diagnose: 'Your diagnosis:',
    submit: 'Submit diagnosis',
    wrong: 'That does not match the outputs — take another close look.',
    solvedTag: 'solved',
    challenge: 'Solve all three incidents with the correct diagnosis.',
  },
} as const

interface Progress {
  ran: string[]
  choice: number | null
  wrong: boolean
  solved: boolean
}

const fresh = (): Progress => ({ ran: [], choice: null, wrong: false, solved: false })

export function Troubleshoot({ lang }: { lang: Lang }) {
  const [active, setActive] = useState(0)
  const [progress, setProgress] = useState<Record<string, Progress>>(
    () => Object.fromEntries(SCENARIOS.map((sc) => [sc.id, fresh()])),
  )
  const s = STR[lang]
  const sc = SCENARIOS[active]
  const p = progress[sc.id]
  const update = (patch: Partial<Progress>) =>
    setProgress((prev) => ({ ...prev, [sc.id]: { ...prev[sc.id], ...patch } }))

  const run = (cmd: string) => {
    if (!p.ran.includes(cmd)) update({ ran: [...p.ran, cmd] })
  }
  const submit = () => {
    if (p.choice === null) return
    if (p.choice === sc.correct) update({ solved: true, wrong: false })
    else update({ wrong: true })
  }
  const allSolved = SCENARIOS.every((x) => progress[x.id].solved)

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <div className="flex flex-wrap gap-2 mb-4">
        {SCENARIOS.map((x, i) => (
          <button
            key={x.id}
            onClick={() => setActive(i)}
            className={`rounded-lg px-3 py-1.5 text-xs font-medium border transition-colors ${
              i === active
                ? 'bg-teal-600 border-teal-600 text-white'
                : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
            }`}
          >
            {x.title[lang]} {progress[x.id].solved && '✓'}
          </button>
        ))}
      </div>

      <div className="rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm text-amber-900 mb-3">
        <span className="mr-1" aria-hidden="true">📟</span>
        <span className="font-semibold">{s.ticket}:</span> {sc.symptom[lang]}
      </div>

      <div className="rounded-lg bg-slate-900 p-3 font-mono text-xs mb-2 min-h-[5rem]">
        {p.ran.length === 0 && <p className="text-slate-500">{s.terminalHint}</p>}
        {p.ran.map((cmd) => (
          <div key={cmd} className="mb-2">
            <p className="text-slate-400">C:\&gt; <span className="text-slate-100">{cmd}</span></p>
            <p className="text-green-400 whitespace-pre-wrap">{outputFor(sc, cmd, lang)}</p>
          </div>
        ))}
      </div>
      <div className="flex flex-wrap gap-2 mb-4">
        {sc.commands.map((c) => (
          <button
            key={c.cmd}
            onClick={() => run(c.cmd)}
            disabled={p.ran.includes(c.cmd) || p.solved}
            className="rounded border border-slate-300 bg-slate-50 px-2 py-1 font-mono text-xs text-slate-700 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-default"
          >
            {c.cmd}
          </button>
        ))}
      </div>

      {!canDiagnose(p.ran.length) ? (
        <p className="text-xs text-slate-500 italic">🔎 {s.evidence}</p>
      ) : (
        <div>
          <p className="text-xs font-semibold text-slate-500 mb-1.5">{s.diagnose}</p>
          <div className="flex flex-col gap-1.5 mb-2">
            {sc.diagnoses[lang].map((d, i) => (
              <label
                key={i}
                className={`flex items-start gap-2 rounded-lg border px-3 py-2 text-sm cursor-pointer transition-colors ${
                  p.solved && i === sc.correct
                    ? 'border-green-300 bg-green-50'
                    : p.choice === i
                      ? 'border-teal-300 bg-teal-50/60'
                      : 'border-slate-200 hover:bg-slate-50'
                }`}
              >
                <input
                  type="radio"
                  name={`diag-${sc.id}`}
                  checked={p.choice === i}
                  disabled={p.solved}
                  onChange={() => update({ choice: i, wrong: false })}
                  className="mt-0.5 accent-teal-600"
                />
                <span className="text-slate-700">{d}</span>
              </label>
            ))}
          </div>
          {!p.solved && (
            <button
              onClick={submit}
              disabled={p.choice === null}
              className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium disabled:opacity-40"
            >
              {s.submit}
            </button>
          )}
          {p.wrong && <p className="mt-2 text-sm text-rose-600">✗ {s.wrong}</p>}
          {p.solved && (
            <div className="mt-2 rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-900">
              <span className="font-semibold text-green-700">✓ {s.solvedTag}</span> — {sc.explanation[lang]}
            </div>
          )}
        </div>
      )}

      <ChallengeBox lang={lang} task={s.challenge} done={allSolved} />
    </div>
  )
}
