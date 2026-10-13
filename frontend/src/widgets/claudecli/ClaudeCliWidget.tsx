import { useEffect, useState } from 'react'
import { createTerminalState, nextMode, runCommand, runTerminalCommand, type CliMode, type TerminalState } from '@/widgets/claudecli/claudeCli'
import { loadSnapshot, newSessionId } from '@/widgets/claudecli/cliSnapshot'
import { ChallengeBox } from '@/components/ChallengeBox'
import { useWidgetScope } from '@/lib/widgetScope'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'Claude-Code-CLI (Demo)', modeDefault: 'Manual', modePlan: 'Plan', modeAccept: 'Accept Edits', modeAuto: 'Auto', cycle: 'Shift+Tab: nächster Modus',
    modeLabel: 'Modus', hint: 'Virtuelle Shell: help, ls, cat README.md. Slash-Commands mit /help.',
    intro: 'Browser-Prototyp — keine echte Host-Shell. Tippe help für Befehle.',
    challenge: 'Wechsle in den Plan-Modus und rufe /context auf.',
    session: 'Session', reset: 'Session zurücksetzen', commandLabel: 'Befehlseingabe',
  },
  en: {
    title: 'Claude Code CLI (demo)', modeDefault: 'Manual', modePlan: 'Plan', modeAccept: 'Accept Edits', modeAuto: 'Auto', cycle: 'Shift+Tab: next mode',
    modeLabel: 'Mode', hint: 'Virtual shell: help, ls, cat README.md. Try slash commands with /help.',
    intro: 'Browser prototype — no real host shell. Type help for commands.',
    challenge: 'Switch to plan mode and run /context.',
    session: 'Session', reset: 'Reset session', commandLabel: 'Command input',
  },
} as const

export function ClaudeCli({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const scope = useWidgetScope()
  const storageKey = scope ? `intnetwork-cli-${scope}` : null
  const [snap] = useState(() => loadSnapshot(storageKey, s.intro))
  const [mode, setMode] = useState<CliMode>(snap.mode)
  const [lines, setLines] = useState<string[]>(snap.lines)
  const [input, setInput] = useState('')
  const [solved, setSolved] = useState(snap.solved)
  const [terminal, setTerminal] = useState<TerminalState>(snap.terminal)
  const [sessionId, setSessionId] = useState(snap.sessionId)

  // Session pro Teilnehmer persistieren; ohne Teilnehmerkontext (Trainer-Vorschau) nicht.
  useEffect(() => {
    if (!storageKey) return
    try {
      localStorage.setItem(storageKey, JSON.stringify({ mode, lines, terminal, solved, sessionId }))
    } catch {
      // Speicher voll/blockiert — die Session läuft für die Seite trotzdem weiter.
    }
  }, [storageKey, mode, lines, terminal, solved, sessionId])

  function submit() {
    const trimmed = input.trim()
    if (trimmed === '') return
    const terminalResult = trimmed.startsWith('/') ? undefined : runTerminalCommand(terminal, trimmed, lang)
    const res = terminalResult ?? runCommand(trimmed, mode, lang)
    if (trimmed === '/context' && mode === 'plan') setSolved(true)
    if (res.output === '__CLEAR__') {
      setLines([s.intro])
    } else {
      setLines((l) => [...l, mode + '> ' + trimmed, ...(res.output ? [res.output] : [])])
    }
    if (terminalResult) setTerminal(terminalResult.state)
    setInput('')
  }

  function resetSession() {
    setTerminal(createTerminalState())
    setLines([s.intro])
    setSolved(false)
    setSessionId(newSessionId())
  }

  const modes: [CliMode, string][] = [
    ['auto', s.modeAuto], ['default', s.modeDefault], ['acceptEdits', s.modeAccept], ['plan', s.modePlan],
  ]

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-2">{s.hint}</p>
      <div className="mb-2 flex items-center justify-between gap-2 text-[11px] text-slate-400">
        <span>{s.session}: <code className="font-mono text-slate-600">{sessionId}</code></span>
        <button type="button" onClick={resetSession} className="rounded border border-slate-200 px-2 py-1 hover:bg-slate-50">{s.reset}</button>
      </div>

      <div className="flex gap-1 mb-2 items-center">
        <span className="text-xs text-slate-500 mr-1">{s.modeLabel}:</span>
        {modes.map(([m, label]) => (
          <button key={m} onClick={() => setMode(m)}
            className={`rounded-lg border px-2 py-1 text-xs ${
              mode === m ? 'border-teal-300 bg-teal-50 text-teal-800' : 'hover:bg-slate-50'}`}>
            {label}
          </button>
        ))}
        <span className="ml-1 text-[11px] text-slate-400">{s.cycle}</span>
      </div>

      <div className="rounded-lg bg-slate-900 p-3 font-mono text-xs text-slate-100">
        <div className="max-h-56 overflow-y-auto whitespace-pre-wrap">{lines.join('\n')}</div>
        <div className="mt-1 flex gap-2">
          <span className="text-green-400">{mode}&gt;</span>
          <input
            value={input} onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') submit()
              else if (e.key === 'Tab' && e.shiftKey) { e.preventDefault(); setMode(nextMode) }
            }}
            spellCheck={false} autoComplete="off" aria-label={s.commandLabel}
            className="flex-1 bg-transparent text-slate-100 outline-none"
          />
        </div>
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={solved} />
    </div>
  )
}
