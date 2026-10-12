import { useMemo, useState } from 'react'
import type { Lang } from '@/lib/i18n'
import { Icon } from '@/components/Icon'
import { DeviceCli } from '@/widgets/cli/DeviceCli'
import { chipCommands, runCommand, taskDone } from './terminalLogic'
import type { TerminalData } from './types'

export default function TerminalBlock({ data, lang }: { data: TerminalData; lang: Lang }) {
  const de = lang === 'de'
  const [prompt, setPrompt] = useState(data.prompt)
  const [executed, setExecuted] = useState<ReadonlySet<number>>(new Set())
  const [answers, setAnswers] = useState<Record<number, string>>({})
  const chips = useMemo(() => chipCommands(data), [data])
  const tasks = data.tasks ?? []

  const run = (cmd: string) => {
    const r = runCommand(data, cmd, lang)
    if (r.index !== undefined) {
      const index = r.index
      setExecuted((s) => new Set(s).add(index))
    }
    if (r.prompt) setPrompt(r.prompt)
    return r.output
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{de ? 'Terminal' : 'Terminal'}</p>
      {data.title && <p className="font-medium text-slate-800">{data.title}</p>}
      {tasks.length > 0 && (
        <ul className="mt-2 flex flex-col gap-1.5" aria-live="polite">
          {tasks.map((task, i) => {
            const done = taskDone(data, task, executed, answers[i])
            return (
              <li key={i} className="flex flex-wrap items-center gap-2 text-sm">
                <span className={`inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-full border ${done ? 'border-green-300 bg-green-50 text-green-800' : 'border-slate-300 text-slate-400'}`}>
                  {done && <Icon name="check" className="h-3.5 w-3.5" />}
                </span>
                <span className={done ? 'text-slate-500' : 'text-slate-700'}>{task.text}</span>
                <span className="sr-only">{done ? (de ? '(erledigt)' : '(done)') : (de ? '(offen)' : '(open)')}</span>
                {task.answers && (
                  <input value={answers[i] ?? ''} disabled={done}
                    onChange={(e) => setAnswers((a) => ({ ...a, [i]: e.target.value }))}
                    spellCheck={false} autoComplete="off" autoCapitalize="off"
                    placeholder={de ? 'Antwort' : 'Answer'} aria-label={`${de ? 'Antwort zu' : 'Answer for'}: ${task.text}`}
                    className="w-44 rounded-lg border border-slate-200 px-2 py-1 font-mono text-sm text-slate-700" />
                )}
              </li>
            )
          })}
        </ul>
      )}
      <DeviceCli prompt={prompt} run={run} lang={lang} chips={chips} textClass="text-sm"
        intro={data.intro ?? (de ? 'Tippe ? für die Befehlsliste oder klicke einen Befehl an.' : 'Type ? for the command list or click a command.')} />
    </div>
  )
}
