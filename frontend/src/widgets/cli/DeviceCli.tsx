import { useEffect, useRef, useState } from 'react'
import type { Lang } from '@/lib/i18n'

export function DeviceCli({ prompt, run, lang = 'de' }: { prompt: string; run: (cmd: string) => string; lang?: Lang }) {
  const commandLabel = lang === 'de' ? 'Befehlseingabe' : 'Command input'
  const [lines, setLines] = useState<string[]>([lang === 'de' ? 'Tippe ? für die Befehlsliste.' : 'Type ? for the command list.'])
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

  function submit() {
    const out = run(input)
    setLines((l) => [...l, `${prompt} ${input}`, ...(out ? out.split('\n') : [])])
    if (input.trim()) setHist((h) => [input, ...h])
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
    <div className="mt-4 rounded-lg bg-slate-900 p-3 font-mono text-xs text-slate-100">
      <div ref={outputRef} role="log" aria-label={lang === 'de' ? 'Ausgabe' : 'Output'} className="max-h-64 overflow-y-auto whitespace-pre-wrap">{lines.join('\n')}</div>
      <div className="mt-1 flex gap-2">
        <span className="text-green-400">{prompt}</span>
        <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={onKey}
          spellCheck={false} autoComplete="off" aria-label={commandLabel}
          className="flex-1 bg-transparent text-slate-100 outline-none" />
      </div>
    </div>
  )
}
