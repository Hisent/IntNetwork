import { useState } from 'react'
import { evaluate, type Rule, type ToolCall, type Effect } from '@/widgets/permissions/permissions'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const RULES: Rule[] = [
  { effect: 'deny', tool: 'Bash', glob: 'rm -rf *' },
  { effect: 'deny', tool: 'Read', glob: './.env' },
  { effect: 'ask', tool: 'Bash', glob: 'git push *' },
  { effect: 'allow', tool: 'Read', glob: 'src/*' },
]

const CALLS: ToolCall[] = [
  { tool: 'Bash', arg: 'rm -rf build' },
  { tool: 'Read', arg: 'src/app.ts' },
  { tool: 'Bash', arg: 'git push origin main' },
  { tool: 'Read', arg: './.env' },
  { tool: 'Bash', arg: 'ls -la' },
]

const STR = {
  de: {
    title: 'Permission-Simulator', rules: 'Regeln', calls: 'Beispiel-Aufruf klicken',
    result: 'Ergebnis', pick: 'Klick einen Aufruf.',
    challenge: 'Finde einen Aufruf, der von einer deny-Regel blockiert wird.',
  },
  en: {
    title: 'Permission Simulator', rules: 'Rules', calls: 'Click an example call',
    result: 'Result', pick: 'Click a call.',
    challenge: 'Find a call that a deny rule blocks.',
  },
} as const

const EFFECT_STYLE: Record<Effect, string> = {
  allow: 'text-green-700', ask: 'text-amber-700', deny: 'text-rose-700',
}

export function PermissionSim({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const [picked, setPicked] = useState<ToolCall | null>(null)
  const decision: Effect | null = picked ? evaluate(RULES, picked) : null

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-2">{s.title}</p>

      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400 mb-1">{s.rules}</p>
      <ul className="mb-3 text-xs font-mono space-y-0.5">
        {RULES.map((r, i) => (
          <li key={i} className={EFFECT_STYLE[r.effect]}>{r.effect}: {r.tool}({r.glob})</li>
        ))}
      </ul>

      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400 mb-1">{s.calls}</p>
      <div className="flex flex-wrap gap-1.5 mb-3">
        {CALLS.map((c, i) => (
          <button key={i} onClick={() => setPicked(c)}
            className={`rounded-lg border px-2 py-1 text-xs font-mono hover:bg-slate-50 ${
              picked === c ? 'border-teal-300 bg-teal-50' : ''}`}>
            {c.tool}: {c.arg}
          </button>
        ))}
      </div>

      <div className="rounded-lg border px-3 py-2 text-sm">
        <span className="text-slate-500">{s.result}: </span>
        {decision ? (
          <span className={`font-mono font-semibold ${EFFECT_STYLE[decision]}`}>{decision.toUpperCase()}</span>
        ) : (
          <span className="text-slate-400">{s.pick}</span>
        )}
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={decision === 'deny'} />
    </div>
  )
}
