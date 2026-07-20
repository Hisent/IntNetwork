import { useEffect, useState } from 'react'
import { createTerminalState, runCommand, runTerminalCommand, type CliMode, type TerminalState } from '@/widgets/claudecli/claudeCli'
import { ChallengeBox } from '@/components/ChallengeBox'
import { useWidgetScope } from '@/lib/widgetScope'
import type { Lang } from '@/lib/i18n'

interface CliSnapshot { mode: CliMode; lines: string[]; terminal: TerminalState; solved: boolean; sessionId: string }

const newSessionId = () => Math.random().toString(36).slice(2, 8)

// Pro Teilnehmer gespeichert (localStorage, wie Lese-Merker/Reflexionen) — die
// Session überlebt Reload und gehört dem eingeloggten Teilnehmer, nicht dem Browser.
export function loadSnapshot(storageKey: string | null, intro: string): CliSnapshot {
  if (storageKey) {
    try {
      const raw = localStorage.getItem(storageKey)
      if (raw) {
        const p = JSON.parse(raw)
        if (p && p.terminal?.files && Array.isArray(p.lines)) {
          return { mode: p.mode ?? 'default', lines: p.lines, terminal: p.terminal,
            solved: !!p.solved, sessionId: p.sessionId ?? newSessionId() }
        }
      }
    } catch {
      // beschädigter Eintrag -> frische Session
    }
  }
  return { mode: 'default', lines: [intro], terminal: createTerminalState(), solved: false, sessionId: newSessionId() }
}

const STR = {
  de: {
    title: 'Claude-Code-CLI (Demo)', modeDefault: 'Vor Änderungen fragen', modePlan: 'Plan', modeAccept: 'Edits automatisch akzeptieren',
    modeLabel: 'Modus', hint: 'Virtuelle Shell: help, ls, cat README.md. Slash-Commands mit /help.',
    intro: 'Browser-Prototyp — keine echte Host-Shell. Tippe help für Befehle.',
    challenge: 'Wechsle in den Plan-Modus und rufe /context auf.',
    session: 'Session', reset: 'Session zurücksetzen',
  },
  en: {
    title: 'Claude Code CLI (demo)', modeDefault: 'Ask before edits', modePlan: 'Plan', modeAccept: 'Auto accept edits',
    modeLabel: 'Mode', hint: 'Virtual shell: help, ls, cat README.md. Try slash commands with /help.',
    intro: 'Browser prototype — no real host shell. Type help for commands.',
    challenge: 'Switch to plan mode and run /context.',
    session: 'Session', reset: 'Reset session',
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
    ['default', s.modeDefault], ['plan', s.modePlan], ['acceptEdits', s.modeAccept],
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
