import { useState } from 'react'
import type { AdhocPoll } from '@/types'

// Eigene Live-Abstimmung im Beamer-Modus (Trainer-UI, deutsch wie die Umgebung).
// Grenzen wie die API (routers/polls.py PollStart) — die API prüft selbst.
const KINDS: { kind: AdhocPoll['kind']; label: string }[] = [
  { kind: 'multi', label: 'Mehrfachauswahl' },
  { kind: 'scale', label: 'Skala' },
  { kind: 'text', label: 'Freitext' },
  { kind: 'words', label: 'Wortwolke' },
]

const input = 'mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-base text-slate-900'
const label = 'block text-sm font-medium text-slate-700'

export function PollComposer({ pending, onStart, onCancel }: { pending: boolean; onStart: (poll: AdhocPoll) => void; onCancel: () => void }) {
  const [kind, setKind] = useState<AdhocPoll['kind']>('multi')
  const [prompt, setPrompt] = useState('')
  const [options, setOptions] = useState('')
  const [maxSel, setMaxSel] = useState('')
  const [min, setMin] = useState(1)
  const [max, setMax] = useState(5)
  const [labelMin, setLabelMin] = useState('')
  const [labelMax, setLabelMax] = useState('')
  const lines = options.split('\n').map((o) => o.trim()).filter(Boolean)
  const ready = prompt.trim() !== '' && (kind !== 'multi' || (lines.length >= 2 && lines.length <= 10))

  function submit(e: React.FormEvent) {
    e.preventDefault()
    if (!ready) return
    const base = { kind, prompt: prompt.trim() }
    onStart(kind === 'multi' ? { ...base, options: lines, max_selections: maxSel ? Number(maxSel) : null }
      : kind === 'scale' ? { ...base, min, max, label_min: labelMin.trim(), label_max: labelMax.trim() }
        : base)
  }

  return (
    <form onSubmit={submit} aria-labelledby="composer-title" className="space-y-4 text-left">
      <h2 id="composer-title" className="text-2xl font-bold text-slate-900">Eigene Abstimmung</h2>
      <fieldset>
        <legend className={label}>Art</legend>
        <div className="mt-1 flex flex-wrap gap-2">
          {KINDS.map((k) => (
            <label key={k.kind} className={`flex min-h-11 cursor-pointer items-center gap-2 rounded-lg border px-3 text-sm ${kind === k.kind ? 'border-teal-600 bg-teal-50 text-teal-900' : 'border-slate-300 text-slate-700'}`}>
              <input type="radio" name="poll-kind" value={k.kind} checked={kind === k.kind} onChange={() => setKind(k.kind)} />
              {k.label}
            </label>
          ))}
        </div>
      </fieldset>
      <label className={label}>
        Frage
        <input value={prompt} onChange={(e) => setPrompt(e.target.value)} maxLength={300} required className={input} />
      </label>
      {kind === 'multi' && (
        <>
          <label className={label}>
            Antworten (eine je Zeile, 2 bis 10)
            <textarea value={options} onChange={(e) => setOptions(e.target.value)} rows={5} className={input} />
          </label>
          <label className={label}>
            Höchstens wählbar (leer = beliebig viele)
            <input type="number" min={1} max={Math.max(1, lines.length)} value={maxSel} onChange={(e) => setMaxSel(e.target.value)} className={`${input} max-w-32`} />
          </label>
        </>
      )}
      {kind === 'scale' && (
        <div className="grid gap-3 sm:grid-cols-2">
          <label className={label}>
            Von
            <select value={min} onChange={(e) => setMin(Number(e.target.value))} className={input}>
              {[0, 1].map((v) => <option key={v} value={v}>{v}</option>)}
            </select>
          </label>
          <label className={label}>
            Bis
            <select value={max} onChange={(e) => setMax(Number(e.target.value))} className={input}>
              {[2, 3, 4, 5, 6, 7, 8, 9, 10].map((v) => <option key={v} value={v}>{v}</option>)}
            </select>
          </label>
          <label className={label}>
            Beschriftung unten (optional)
            <input value={labelMin} onChange={(e) => setLabelMin(e.target.value)} maxLength={40} placeholder="z. B. gar nicht" className={input} />
          </label>
          <label className={label}>
            Beschriftung oben (optional)
            <input value={labelMax} onChange={(e) => setLabelMax(e.target.value)} maxLength={40} placeholder="z. B. sehr" className={input} />
          </label>
        </div>
      )}
      {kind === 'text' && <p className="text-sm text-slate-600">Teilnehmer schreiben eine kurze Antwort (höchstens 280 Zeichen). Vor und nach dem Auflösen lassen sich einzelne Antworten ausblenden.</p>}
      {kind === 'words' && <p className="text-sm text-slate-600">Teilnehmer nennen ein bis drei Wörter (je höchstens 30 Zeichen). Groß/klein und Leerzeichen werden vereinheitlicht.</p>}
      <div className="flex flex-wrap gap-3">
        <button type="submit" disabled={!ready || pending} className="min-h-11 rounded-lg bg-teal-600 px-5 font-medium text-white hover:bg-teal-700 disabled:opacity-50">
          Abstimmung starten
        </button>
        <button type="button" onClick={onCancel} className="min-h-11 rounded-lg border border-slate-300 px-5 text-slate-700 hover:bg-slate-50">
          Abbrechen
        </button>
      </div>
    </form>
  )
}
