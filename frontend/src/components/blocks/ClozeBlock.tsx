import { useMemo, useState } from 'react'
import type { Lang } from '@/lib/i18n'
import { t } from '@/lib/i18n'
import { Icon } from '@/components/Icon'
import { clozeResult, gapSolution, parseCloze } from './exerciseLogic'
import type { ClozeData } from './types'

export default function ClozeBlock({ data, lang }: { data: ClozeData; lang: Lang }) {
  const de = lang === 'de'
  const parts = useMemo(() => parseCloze(data.text, new Set(data.gaps.map((g) => g.id))), [data])
  const [values, setValues] = useState<Record<string, string>>({})
  const [checked, setChecked] = useState(false)
  const [solved, setSolved] = useState(false)
  const result = useMemo(() => clozeResult(data, values), [data, values])
  const allCorrect = checked && Object.values(result).every(Boolean)
  const filled = data.gaps.every((g) => (values[g.id] ?? '').trim() !== '')
  const set = (id: string, v: string) => setValues((s) => ({ ...s, [id]: v }))

  // Auf der dunklen Code-Fläche (mono) andere Feldfarben als im Fließtext.
  const field = data.mono
    ? 'border-slate-500 bg-slate-800 text-slate-100'
    : 'border-slate-300 bg-white text-slate-800'
  const mark = (ok: boolean) => (ok ? 'border-green-400' : 'border-amber-400')

  const gapNumber = (id: string) => data.gaps.findIndex((g) => g.id === id) + 1

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{de ? 'Lückentext' : 'Fill the gaps'}</p>
      <p className="font-medium text-slate-800 mb-2">{data.prompt}</p>
      <div className={data.mono
        ? 'overflow-x-auto whitespace-pre-wrap rounded-lg bg-slate-900 p-3 font-mono text-sm leading-7 text-slate-100'
        : 'whitespace-pre-wrap text-slate-700 leading-9'}>
        {parts.map((part, i) => {
          if ('text' in part) return <span key={i}>{part.text}</span>
          const gap = data.gaps.find((g) => g.id === part.gap)
          if (!gap) return null
          const ok = result[gap.id]
          const label = `${de ? 'Lücke' : 'Gap'} ${gapNumber(gap.id)}`
          const cls = `mx-1 inline-block max-w-full rounded-md border-2 px-1.5 py-0.5 align-baseline text-sm ${data.mono ? 'font-mono' : ''} ${field} ${checked ? mark(ok) : ''}`
          return (
            <span key={i} className="inline-flex max-w-full items-center whitespace-nowrap">
              {gap.options ? (
                <select value={values[gap.id] ?? ''} disabled={checked} aria-label={label} aria-invalid={checked && !ok}
                  onChange={(e) => set(gap.id, e.target.value)} className={cls}>
                  <option value="">…</option>
                  {gap.options.map((o, oi) => <option key={oi} value={oi}>{o}</option>)}
                </select>
              ) : (
                <input value={values[gap.id] ?? ''} disabled={checked} aria-label={label} aria-invalid={checked && !ok}
                  onChange={(e) => set(gap.id, e.target.value)}
                  spellCheck={false} autoComplete="off" autoCapitalize="off"
                  size={Math.max(6, ...(gap.accept ?? []).map((a) => a.length + 1))} className={cls} />
              )}
              {checked && (
                <span className={`inline-flex items-center ${data.mono ? (ok ? 'text-green-400' : 'text-amber-400') : (ok ? 'text-green-600' : 'text-amber-600')}`}>
                  <Icon name={ok ? 'check' : 'close'} className="h-4 w-4" />
                  <span className="sr-only">{label}: {ok ? t(lang, 'correct') : t(lang, 'incorrect')}</span>
                </span>
              )}
              {solved && !ok && <span className={`mr-1 rounded px-1 text-sm ${data.mono ? 'font-mono text-green-400' : 'font-medium text-green-600'}`}>{gapSolution(gap)}</span>}
            </span>
          )
        })}
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-3 text-sm" aria-live="polite">
        {!checked ? (
          <button type="button" onClick={() => setChecked(true)} disabled={!filled}
            className="rounded-lg border border-teal-200 text-teal-700 px-3 py-1.5 text-sm font-medium hover:bg-teal-50 disabled:opacity-50">
            {t(lang, 'checkIt')}
          </button>
        ) : (
          <>
            <span className={`inline-flex items-center gap-1 font-medium ${allCorrect ? 'text-green-600' : 'text-amber-600'}`}>
              <Icon name={allCorrect ? 'check' : 'close'} className="h-4 w-4" />
              {allCorrect ? t(lang, 'correct') : `${Object.values(result).filter(Boolean).length} / ${data.gaps.length} ${de ? 'richtig' : 'correct'}`}
            </span>
            {!allCorrect && (
              <>
                <button type="button" onClick={() => { setChecked(false); setSolved(false) }} className="text-xs text-slate-500 underline hover:text-slate-700">
                  {t(lang, 'tryAgainShort')}
                </button>
                {!solved && (
                  <button type="button" onClick={() => setSolved(true)} className="text-xs text-slate-500 underline hover:text-slate-700">
                    {de ? 'Lösung zeigen' : 'Show solution'}
                  </button>
                )}
              </>
            )}
          </>
        )}
      </div>
      {checked && data.explanation && <p className="mt-2 text-sm text-slate-600 animate-fade-up">{data.explanation}</p>}
    </div>
  )
}
