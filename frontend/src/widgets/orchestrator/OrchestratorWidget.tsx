import { useState } from 'react'
import { TASKS, wallClock } from '@/widgets/orchestrator/orchestrator'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'Agent-Orchestrierung', hint: 'Drei unabhängige Teilaufgaben — vergleiche nacheinander vs. parallel.',
    sequential: 'Nacheinander', parallel: 'Parallel', wall: 'Gesamtzeit (Einheiten)',
    lead: 'Lead-Agent verteilt an Subagents:', challenge: 'Schalte auf „Parallel“ und sieh den Zeitvorteil.',
  },
  en: {
    title: 'Agent Orchestration', hint: 'Three independent subtasks — compare sequential vs parallel.',
    sequential: 'Sequential', parallel: 'Parallel', wall: 'Total time (units)',
    lead: 'Lead agent delegates to subagents:', challenge: 'Switch to “Parallel” and see the time saved.',
  },
} as const

export function Orchestrator({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const [mode, setMode] = useState<'sequential' | 'parallel'>('sequential')
  const total = wallClock(TASKS, mode)
  const de = lang !== 'en'
  const maxCost = Math.max(...TASKS.map((t) => t.cost))

  const modes: ['sequential' | 'parallel', string][] = [
    ['sequential', s.sequential], ['parallel', s.parallel],
  ]

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-2">{s.hint}</p>

      <div className="flex gap-1 mb-3">
        {modes.map(([m, label]) => (
          <button key={m} onClick={() => setMode(m)}
            className={`rounded-lg border px-2 py-1 text-xs ${
              mode === m ? 'border-teal-300 bg-teal-50 text-teal-800' : 'hover:bg-slate-50'}`}>
            {label}
          </button>
        ))}
      </div>

      <p className="text-xs text-slate-500 mb-1">{s.lead}</p>
      <div className="space-y-1 mb-3">
        {TASKS.map((t, i) => (
          <div key={i} className="flex items-center gap-2">
            <span className="w-56 shrink-0 text-xs text-slate-700">{de ? t.de : t.en}</span>
            <div className="h-3 rounded bg-teal-200" style={{ width: `${(t.cost / maxCost) * 60}%` }} />
            <span className="text-xs font-mono text-slate-500">{t.cost}</span>
          </div>
        ))}
      </div>

      <div className="rounded-lg border px-3 py-2 text-sm">
        <span className="text-slate-500">{s.wall}: </span>
        <span className="font-mono font-semibold text-slate-800">{total}</span>
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={mode === 'parallel'} />
    </div>
  )
}
