import { useMemo } from 'react'
import { useExercise } from '@/lib/exerciseState'
import type { Lang } from '@/lib/i18n'
import { t } from '@/lib/i18n'
import { Icon } from '@/components/Icon'
import { shuffledIndices } from '@/components/Quiz'
import { assignPair, matchResult } from './exerciseLogic'
import type { MatchData } from './types'

const LETTERS = 'ABCDEFGH'

// Zuordnung ohne Drag&Drop: Begriff wählen, dann Beschreibung wählen. Alles sind
// echte <button>, also per Tab/Enter/Leertaste bedienbar.
export default function MatchBlock({ data, lang }: { data: MatchData; lang: Lang }) {
  const de = lang === 'de'
  const n = data.pairs.length
  // order[k] = Paar-Index der Beschreibung an Anzeigeposition k
  const fresh = () => ({ order: shuffledIndices(n), assignment: Array<number | null>(n).fill(null), active: 0 as number | null, checked: false })
  const [{ order, assignment, active, checked }, setState] = useExercise(fresh,
    (s) => s.checked && matchResult(s.assignment).every(Boolean))
  const setActive = (next: number | null) => setState((s) => ({ ...s, active: next }))
  const setChecked = (next: boolean) => setState((s) => ({ ...s, checked: next }))
  const result = useMemo(() => matchResult(assignment), [assignment])
  const letterOf = (pair: number) => LETTERS[order.indexOf(pair)]
  const complete = assignment.every((r) => r !== null)
  const allCorrect = checked && result.every(Boolean)

  const pick = (right: number) => {
    if (checked || active === null) return
    const next = assignPair(assignment, active, right)
    const open = next.findIndex((r, i) => r === null && i !== active)
    setState((s) => ({ ...s, assignment: next, active: open >= 0 ? open : null }))
  }
  const reset = () => setState(fresh())

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{de ? 'Zuordnen' : 'Match'}</p>
      <p className="font-medium text-slate-800 mb-1">{data.prompt}</p>
      <p className="text-xs text-slate-400 mb-3">{de ? 'Erst einen Begriff wählen, dann die passende Beschreibung.' : 'Pick a term first, then its matching description.'}</p>
      <div className="grid gap-4 sm:grid-cols-[minmax(0,2fr)_minmax(0,3fr)]">
        <ul className="flex min-w-0 flex-col gap-1.5" aria-label={de ? 'Begriffe' : 'Terms'}>
          {data.pairs.map((p, i) => {
            const r = assignment[i]
            return (
              <li key={i}>
                <button type="button" disabled={checked} aria-pressed={active === i} onClick={() => setActive(i)}
                  className={`flex w-full items-center gap-2 rounded-lg border px-3 py-1.5 text-left text-sm ${
                    checked ? (result[i] ? 'border-green-300 bg-green-50 text-green-800' : 'border-amber-300 bg-amber-50 text-amber-800')
                    : active === i ? 'border-teal-600 bg-teal-50 text-teal-900'
                    : 'border-slate-200 text-slate-700 hover:bg-slate-50'}`}>
                  <span className="min-w-0 flex-1 font-medium [overflow-wrap:anywhere]">{p.left}</span>
                  <span className="shrink-0 font-mono text-xs" aria-hidden="true">{r === null ? '→ ?' : `→ ${letterOf(r)}`}</span>
                  <span className="sr-only">{r === null ? (de ? 'noch nicht zugeordnet' : 'not matched yet') : `${de ? 'zugeordnet' : 'matched to'} ${letterOf(r)}`}</span>
                  {checked && (
                    <>
                      <Icon name={result[i] ? 'check' : 'close'} className="h-4 w-4 shrink-0" />
                      <span className="sr-only">{result[i] ? t(lang, 'correct') : t(lang, 'incorrect')}</span>
                    </>
                  )}
                </button>
              </li>
            )
          })}
        </ul>
        <ul className="flex min-w-0 flex-col gap-1.5" aria-label={de ? 'Beschreibungen' : 'Descriptions'}>
          {order.map((pair, k) => {
            const used = assignment.includes(pair)
            return (
              <li key={pair}>
                <button type="button" disabled={checked || active === null} onClick={() => pick(pair)}
                  className={`flex w-full items-start gap-2 rounded-lg border px-3 py-1.5 text-left text-sm ${
                    used ? 'border-slate-200 bg-slate-50 text-slate-500' : 'border-slate-200 text-slate-700 hover:bg-slate-50'}`}>
                  <span className="shrink-0 font-mono text-xs font-semibold text-teal-700 mt-0.5">{LETTERS[k]}</span>
                  <span className="min-w-0 flex-1 [overflow-wrap:anywhere]">{data.pairs[pair].right}</span>
                </button>
              </li>
            )
          })}
        </ul>
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-3 text-sm" aria-live="polite">
        {!checked ? (
          <button type="button" onClick={() => setChecked(true)} disabled={!complete}
            className="rounded-lg border border-teal-200 text-teal-700 px-3 py-1.5 text-sm font-medium hover:bg-teal-50 disabled:opacity-50">
            {t(lang, 'checkIt')}
          </button>
        ) : (
          <span className={`inline-flex items-center gap-1 font-medium ${allCorrect ? 'text-green-600' : 'text-amber-600'}`}>
            <Icon name={allCorrect ? 'check' : 'close'} className="h-4 w-4" />
            {allCorrect ? t(lang, 'correct') : `${result.filter(Boolean).length} / ${n} ${de ? 'richtig' : 'correct'}`}
          </span>
        )}
        {(checked || assignment.some((r) => r !== null)) && (
          <button type="button" onClick={reset} className="text-xs text-slate-500 underline hover:text-slate-700">
            {de ? 'Zurücksetzen' : 'Reset'}
          </button>
        )}
      </div>
      {checked && data.explanation && <p className="mt-2 text-sm text-slate-600 animate-fade-up">{data.explanation}</p>}
    </div>
  )
}
