import { useMemo } from 'react'
import { useExercise } from '@/lib/exerciseState'
import type { Lang } from '@/lib/i18n'
import { Icon } from '@/components/Icon'
import { DeviceCli } from '@/widgets/cli/DeviceCli'
import { chipCommands, literal, runCommand, taskDone } from './terminalLogic'
import type { TerminalData } from './types'

export default function TerminalBlock({ data, lang }: { data: TerminalData; lang: Lang }) {
  const de = lang === 'de'
  const chips = useMemo(() => chipCommands(data), [data])
  const chipLabels = useMemo(() => Object.fromEntries(data.commands.flatMap((c) => (c.label ? [[literal(c.cmd), c.label]] : []))), [data])
  const tasks = data.tasks ?? []
  // Gemerkt werden die Aufgaben (ausgeführte Befehle, Antworten) UND der Gerätezustand dahinter
  // (Flags aus sets/clears, Prompt) — sonst wären nach dem Neuladen Aufgaben abgehakt, deren
  // Wirkung fehlt, und die Folgeaufgabe nur durch Wiederholen lösbar. Nicht gemerkt: der Bildschirminhalt.
  const [saved, setState] = useExercise({ executed: [] as number[], answers: {} as Record<number, string>, flags: [] as string[], prompt: null as string | null },
    (s) => tasks.length > 0 && tasks.every((task, i) => taskDone(data, task, new Set(s.executed), s.answers[i])))
  // Gegen den aktuellen Inhalt und ältere/kaputte Speicherstände absichern (flags/prompt kamen später dazu).
  const state = useMemo(() => ({
    executed: Array.isArray(saved?.executed) ? saved.executed.filter((i) => i >= 0 && i < data.commands.length) : [],
    answers: saved?.answers && typeof saved.answers === 'object' ? saved.answers : {},
    flags: Array.isArray(saved?.flags) ? saved.flags : [],
    prompt: typeof saved?.prompt === 'string' ? saved.prompt : null,  // null = Start-Prompt des Inhalts
  }), [saved, data])
  const executed = useMemo(() => new Set(state.executed), [state.executed])
  const { answers, flags } = state
  const prompt = state.prompt ?? data.prompt

  const run = (cmd: string) => {
    const r = runCommand(data, cmd, lang, flags)
    if (r.index !== undefined || r.prompt || r.flags) {
      setState({
        ...state,
        executed: r.index === undefined || state.executed.includes(r.index) ? state.executed : [...state.executed, r.index],
        flags: r.flags ?? state.flags,
        prompt: r.prompt || state.prompt,
      })
    }
    return r.output
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">
        Terminal
        {/* jedes Terminal ist eine Simulation — das sagt sonst nur die Trainer-Notiz */}
        <span className="ml-2 font-normal normal-case tracking-normal text-slate-500">
          {de ? 'Simulation – Ausgaben sind fest hinterlegt und teils gekürzt' : 'Simulation – outputs are canned and partly shortened'}
        </span>
      </p>
      {data.title && <p className="font-medium text-slate-800">{data.title}</p>}
      {tasks.length > 0 && (
        <ul className="mt-2 flex flex-col gap-1.5" aria-live="polite">
          {tasks.map((task, i) => {
            const done = taskDone(data, task, executed, answers[i])
            return (
              <li key={i} className="flex items-start gap-2 text-sm">
                <span className={`${task.answers ? 'mt-[5px]' : ''} inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-full border ${done ? 'border-green-300 bg-green-50 text-green-800' : 'border-slate-300 text-slate-400'}`}>
                  {done && <Icon name="check" className="h-3.5 w-3.5" />}
                </span>
                {/* Text, Antwortfeld und Erklärung neben dem Haken — auch wenn der Text umbricht */}
                <div className="flex min-w-0 flex-1 flex-wrap items-center gap-x-2 gap-y-1">
                <span className={done ? 'text-slate-500' : 'text-slate-700'}>{task.text}</span>
                <span className="sr-only">{done ? (de ? '(erledigt)' : '(done)') : (de ? '(offen)' : '(open)')}</span>
                {task.answers && (
                  <input value={answers[i] ?? ''} disabled={done}
                    onChange={(e) => setState({ ...state, answers: { ...answers, [i]: e.target.value } })}
                    spellCheck={false} autoComplete="off" autoCapitalize="off"
                    placeholder={de ? 'Antwort' : 'Answer'} aria-label={`${de ? 'Antwort zu' : 'Answer for'}: ${task.text}`}
                    className="w-44 rounded-lg border border-slate-200 px-2 py-1 font-mono text-sm text-slate-700" />
                )}
                {done && task.explanation && <p className="w-full text-sm text-slate-600 animate-fade-up">{task.explanation}</p>}
                </div>
              </li>
            )
          })}
        </ul>
      )}
      <DeviceCli prompt={prompt} run={run} lang={lang} chips={chips} chipLabels={chipLabels} textClass="text-sm" nowrap={data.wrap === false}
        intro={data.intro ?? (de ? 'Tippe ? für die Befehlsliste oder klicke einen Befehl an.' : 'Type ? for the command list or click a command.')} />
    </div>
  )
}
