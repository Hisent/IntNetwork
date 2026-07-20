import { useState } from 'react'
import { runCommand, type CliMode } from '@/widgets/claudecli/claudeCli'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'Claude-Code-CLI (Demo)', modeNormal: 'Normal', modePlan: 'Plan', modeAccept: 'Auto-Accept',
    modeLabel: 'Modus', hint: 'Slash-Commands ausprobieren (/help). Modus oben umschalten.',
    intro: 'Tippe /help für die Befehlsliste.',
    challenge: 'Wechsle in den Plan-Modus und rufe /context auf.',
  },
  en: {
    title: 'Claude Code CLI (demo)', modeNormal: 'Normal', modePlan: 'Plan', modeAccept: 'Auto-accept',
    modeLabel: 'Mode', hint: 'Try slash commands (/help). Toggle the mode above.',
    intro: 'Type /help for the command list.',
    challenge: 'Switch to plan mode and run /context.',
  },
} as const

export function ClaudeCli({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const [mode, setMode] = useState<CliMode>('normal')
  const [lines, setLines] = useState<string[]>([s.intro])
  const [input, setInput] = useState('')
  const [solved, setSolved] = useState(false)

  function submit() {
    const trimmed = input.trim()
    if (trimmed === '') return
    const res = runCommand(trimmed, mode, lang)
    if (trimmed === '/context' && mode === 'plan') setSolved(true)
    if (res.output === '__CLEAR__') {
      setLines([s.intro])
    } else {
      setLines((l) => [...l, `${mode}> ${trimmed}`, ...(res.output ? [res.output] : [])])
    }
    setInput('')
  }

  const modes: [CliMode, string][] = [
    ['normal', s.modeNormal], ['plan', s.modePlan], ['accept', s.modeAccept],
  ]

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-2">{s.hint}</p>

      <div className="flex gap-1 mb-2 items-center">
        <span className="text-xs text-slate-500 mr-1">{s.modeLabel}:</span>
        {modes.map(([m, label]) => (
          <button key={m} onClick={() => setMode(m)}
            className={`rounded-lg border px-2 py-1 text-xs ${
              mode === m ? 'border-teal-300 bg-teal-50 text-teal-800' : 'hover:bg-slate-50'}`}>
            {label}
          </button>
        ))}
      </div>

      <div className="rounded-lg bg-slate-900 p-3 font-mono text-xs text-slate-100">
        <div className="max-h-56 overflow-y-auto whitespace-pre-wrap">{lines.join('\n')}</div>
        <div className="mt-1 flex gap-2">
          <span className="text-green-400">{mode}&gt;</span>
          <input
            value={input} onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') submit() }}
            spellCheck={false} autoComplete="off"
            className="flex-1 bg-transparent text-slate-100 outline-none"
          />
        </div>
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={solved} />
    </div>
  )
}
