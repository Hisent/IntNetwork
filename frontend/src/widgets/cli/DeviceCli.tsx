import { useEffect, useRef, useState } from 'react'
import type { Lang } from '@/lib/i18n'

// `intro`, `chips`, `chipLabels`, `textClass` und `nowrap` sind optional und kommen vom deklarativen
// terminal-Block (components/blocks/TerminalBlock.tsx); die Geräte-Widgets
// nutzen die Komponente unverändert ohne sie.
export function DeviceCli({ prompt, run, lang = 'de', intro, chips, chipLabels, textClass = 'text-xs', nowrap = false }: {
  prompt: string
  run: (cmd: string) => string
  lang?: Lang
  intro?: string
  /** Befehle zum Anklicken (Beamer/Tablet) */
  chips?: string[]
  /** Kurzbeschriftung je Chip-Befehl; ausgeführt und angezeigt wird der volle Befehl */
  chipLabels?: Record<string, string>
  textClass?: string
  /** breite Tabellen-Ausgaben: nicht umbrechen, das Log scrollt waagerecht in sich */
  nowrap?: boolean
}) {
  const commandLabel = lang === 'de' ? 'Befehlseingabe' : 'Command input'
  const [lines, setLines] = useState<string[]>([intro ?? (lang === 'de' ? 'Tippe ? für die Befehlsliste.' : 'Type ? for the command list.')])
  const [input, setInput] = useState('')
  const [hist, setHist] = useState<string[]>([])
  const [hi, setHi] = useState(-1)
  // Ab ~16 Zeilen scrollt die Ausgabe: ohne Nachführen verschwand die Antwort
  // auf den gerade getippten Befehl unter dem Rand (am Beamer besonders störend).
  const outputRef = useRef<HTMLDivElement>(null)
  useEffect(() => {
    const el = outputRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [lines])

  function submit(cmd = input) {
    const out = run(cmd)
    setLines((l) => [...l, `${prompt} ${cmd}`, ...(out ? out.split('\n') : [])])
    if (cmd.trim()) setHist((h) => [cmd, ...h])
    setHi(-1)
    setInput('')
  }

  function onKey(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter') submit()
    else if (e.key === 'ArrowUp') {
      e.preventDefault()
      const ni = Math.min(hi + 1, hist.length - 1)
      if (ni >= 0) { setHi(ni); setInput(hist[ni]) }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault()
      const ni = hi - 1
      setHi(ni)
      setInput(ni >= 0 ? hist[ni] : '')
    }
  }

  return (
    <div className={`mt-4 rounded-lg bg-slate-900 p-3 font-mono ${textClass} text-slate-100`}>
      <div ref={outputRef} role="log" tabIndex={nowrap ? 0 : undefined} aria-label={lang === 'de' ? 'Ausgabe' : 'Output'} className={`max-h-64 ${nowrap ? 'overflow-auto whitespace-pre' : 'overflow-y-auto whitespace-pre-wrap break-words'}`}>{lines.join('\n')}</div>
      <div className="mt-1 flex gap-2">
        <span className="text-green-400">{prompt}</span>
        <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={onKey}
          spellCheck={false} autoComplete="off" autoCapitalize="off" aria-label={commandLabel}
          className="min-w-0 flex-1 bg-transparent text-slate-100 outline-none" />
      </div>
      {chips && chips.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5 border-t border-slate-800 pt-3" role="group" aria-label={lang === 'de' ? 'Befehle zum Anklicken' : 'Commands to click'}>
          {chips.map((c) => (
            <button key={c} type="button" onClick={() => submit(c)} title={chipLabels?.[c] ? c : undefined}
              className="max-w-full rounded-md border border-slate-600 px-2 py-1 text-left text-slate-100 [overflow-wrap:anywhere] hover:bg-slate-800">
              {chipLabels?.[c] ?? c}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
