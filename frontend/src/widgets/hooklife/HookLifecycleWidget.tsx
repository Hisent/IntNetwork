import { useState } from 'react'
import { timeline, type ActionId } from '@/widgets/hooklife/hookLifecycle'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'Hook-Lifecycle', hint: 'Aktion auslösen — sieh, welche Ereignisse feuern und wo ein Hook greift.',
    session: 'Session starten', prompt: 'Prompt senden', edit: 'Datei ändern', bash: 'Bash ausführen',
    fires: 'Hook feuert', challenge: 'Löse eine Aktion aus, bei der ein PreToolUse-Hook feuert.',
  },
  en: {
    title: 'Hook Lifecycle', hint: 'Trigger an action — see which events fire and where a hook runs.',
    session: 'Start session', prompt: 'Send prompt', edit: 'Edit file', bash: 'Run Bash',
    fires: 'hook fires', challenge: 'Trigger an action where a PreToolUse hook fires.',
  },
} as const

export function HookLifecycle({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const [action, setAction] = useState<ActionId>('edit')
  const steps = timeline(action, lang)
  const firedPre = steps.some((st) => st.event === 'PreToolUse' && st.fires)

  const actions: [ActionId, string][] = [
    ['session', s.session], ['prompt', s.prompt], ['edit', s.edit], ['bash', s.bash],
  ]

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-2">{s.hint}</p>

      <div className="flex flex-wrap gap-1.5 mb-3">
        {actions.map(([a, label]) => (
          <button key={a} onClick={() => setAction(a)}
            className={`rounded-lg border px-2 py-1 text-xs ${
              action === a ? 'border-teal-300 bg-teal-50 text-teal-800' : 'hover:bg-slate-50'}`}>
            {label}
          </button>
        ))}
      </div>

      <ol className="space-y-1">
        {steps.map((st, i) => (
          <li key={i}
            className={`flex items-center gap-2 rounded-lg border px-3 py-1.5 text-sm ${
              st.fires ? 'border-teal-200 bg-teal-50' : 'border-slate-200'}`}>
            <span className="font-mono text-xs text-slate-400">{i + 1}.</span>
            <span className="font-mono font-medium text-slate-800">{st.event}</span>
            <span className="text-xs text-slate-500">{st.detail}</span>
            {st.fires && <span className="ml-auto text-xs font-semibold text-teal-700">⚡ {s.fires}</span>}
          </li>
        ))}
      </ol>

      <ChallengeBox lang={lang} task={s.challenge} done={firedPre} />
    </div>
  )
}
