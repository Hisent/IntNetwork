import { useMemo, useState } from 'react'
import type { Question } from '@/types'
import { learnApi } from '@/lib/learnApi'
import { errMsg } from '@/lib/api'
import { t, type Lang } from '@/lib/i18n'
import { termsForModule } from '@/lib/glossary'
import { Icon } from '@/components/Icon'

interface Result {
  score: number
  total: number
  passed: boolean
  best: number
  details: Record<string, boolean>
}

function isAnswered(q: Question, value: unknown): boolean {
  if (q.type === 'multi') return Array.isArray(value) && value.length > 0
  if (q.type === 'number') return value !== undefined && value !== ''
  return value !== undefined
}

// Fisher-Yates: gibt die Original-Indizes in gemischter Reihenfolge zurueck.
// Gemischt wird nur die Anzeige; die abgegebene Antwort bleibt der Original-
// Index, also bewertet der Server unveraendert. Bricht die Positions-Verzerrung
// (im Content stand die richtige Antwort fast immer an Stelle 2).
export function shuffledIndices(n: number): number[] {
  const a = Array.from({ length: n }, (_, i) => i)
  for (let i = n - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

function hintFor(type: Question['type'], termLabels: string[], lang: Lang, level: number): string {
  const concepts = termLabels.join(', ')
  if (lang === 'de') {
    if (level === 1) return concepts ? 'Ordne die Frage zuerst diesen Begriffen zu: ' + concepts + '.' : 'Ordne die Frage zuerst dem Lernziel dieses Moduls zu.'
    return type === 'number'
      ? 'Rechne in kleinen Schritten und prüfe, welche Einheit oder welches Präfix gefragt ist.'
      : 'Lies jede Antwort wörtlich: Suche nach einer Aussage, die zum Kernbegriff passt, und streiche klare Widersprüche.'
  }
  if (level === 1) return concepts ? 'First connect this question to these terms: ' + concepts + '.' : 'First connect the question to this module’s learning goal.'
  return type === 'number'
    ? 'Calculate in small steps and check which unit or prefix the question asks for.'
    : 'Read every option literally: find the statement that fits the core term and eliminate clear contradictions.'
}

export function Quiz({ moduleKey, questions, lang, onResult }: {
  moduleKey: string; questions: Question[]; lang: Lang; onResult?: (passed: boolean) => void
}) {
  const [answers, setAnswers] = useState<Record<string, unknown>>({})
  const [result, setResult] = useState<Result | null>(null)
  const [best, setBest] = useState<number | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [hintLevels, setHintLevels] = useState<Record<string, number>>({})

  const set = (id: string, value: unknown) => setAnswers((a) => ({ ...a, [id]: value }))
  const toggleMulti = (id: string, optIndex: number) =>
    setAnswers((a) => {
      const cur = (a[id] as number[]) ?? []
      return { ...a, [id]: cur.includes(optIndex) ? cur.filter((o) => o !== optIndex) : [...cur, optIndex] }
    })

  async function submit() {
    setError('')
    setBusy(true)
    try {
      const r = await learnApi.submitQuiz(moduleKey, answers)
      setResult(r.data)
      setBest(r.data.best)
      onResult?.(r.data.passed)
    } catch (error) {
      setError(errMsg(error, lang === 'de'
        ? 'Der Wissenscheck konnte nicht gespeichert werden. Bitte versuche es erneut.'
        : 'The knowledge check could not be saved. Please try again.'))
    } finally {
      setBusy(false)
    }
  }

  function retry() {
    setAnswers({})
    setResult(null)
    setHintLevels({})
    setError('')
  }

  // einmal pro Modul mischen (nicht bei jedem Render); Sprachwechsel laedt die
  // Fragen neu und mischt dann ebenfalls neu — beides unkritisch.
  const optionOrder = useMemo(() => {
    const m: Record<string, number[]> = {}
    for (const q of questions) if (q.type !== 'number') m[q.id] = shuffledIndices(q.options.length)
    return m
  }, [questions])

  const locked = result !== null
  const answeredCount = questions.filter((q) => isAnswered(q, answers[q.id])).length
  const allAnswered = answeredCount === questions.length
  const progressPct = questions.length ? Math.round((answeredCount / questions.length) * 100) : 0
  const termLabels = termsForModule(moduleKey).slice(0, 3).map((term) => term.label[lang])
  const wrongQuestions = result ? questions.filter((question) => !result.details[question.id]) : []

  return (
    <section className="mt-14">
      {/* Übergang vom Lernstoff zum Abschluss — statt unvermittelt ein Kasten */}
      <div className="mb-6 flex items-center gap-3">
        <span className="inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-widest text-teal-700">
          <svg viewBox="0 0 20 20" className="w-3.5 h-3.5" fill="currentColor" aria-hidden="true">
            <path fillRule="evenodd" d="M16.7 5.3a1 1 0 010 1.4l-7.5 7.5a1 1 0 01-1.4 0L3.3 9.7a1 1 0 011.4-1.4l3.1 3.1 6.8-6.8a1 1 0 011.4 0z" clipRule="evenodd" />
          </svg>
          {t(lang, 'knowledgeCheck')}
        </span>
        <div className="h-px flex-1 bg-slate-200" aria-hidden="true" />
      </div>

      {/* Kein umschließender Karten-Rahmen mehr: die einzelnen Fragen tragen
          bereits eigene Karten (rounded-xl border), ein zusätzlicher äußerer
          Rahmen erzeugte "Karte in Karte". Die Übergangs-Trennlinie oben
          reicht als Gruppierung. */}
      <div>
      <div className="flex items-baseline justify-between gap-3 mb-5">
        <p className="text-sm text-slate-500">{t(lang, 'knowledgeCheckIntro')}</p>
        {best != null && <span className="shrink-0 text-sm text-slate-500">{t(lang, 'bestSoFar')}: <b className="tabular-nums">{best}%</b></span>}
      </div>

      {!locked && (
        <div className="mb-6">
          <div className="flex justify-between text-xs text-slate-500 mb-1">
            <span>{answeredCount} / {questions.length} {t(lang, 'answeredProgress')}</span>
            <span>{progressPct}%</span>
          </div>
          <div className="h-1.5 rounded-full bg-slate-200 overflow-hidden">
            <div className="h-full bg-teal-500 rounded-full transition-all duration-300" style={{ width: `${progressPct}%` }} />
          </div>
        </div>
      )}

      <div className="flex flex-col gap-4">
        {questions.map((q, qi) => {
          const correct = result?.details[q.id]
          const ring = locked ? (correct ? 'border-green-300 bg-green-50/50' : 'border-amber-300 bg-amber-50/50') : 'border-slate-200 bg-white'
          return (
            <div key={q.id} className={`rounded-xl border ${ring} p-4 transition-colors`}>
              <div className="flex items-start justify-between gap-3 mb-2">
                <p className="font-medium text-slate-800">
                  <span className="text-slate-400 mr-1.5">{qi + 1}.</span>{q.prompt}
                </p>
                {locked && (
                  <span className={`shrink-0 inline-flex items-center gap-1 text-xs font-semibold rounded-full px-2 py-0.5 ${correct ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
                    <Icon name={correct ? 'check' : 'close'} className="h-3.5 w-3.5" />{correct ? t(lang, 'correct') : t(lang, 'incorrect')}
                  </span>
                )}
              </div>
              {q.type === 'number' ? (
                <input type="number" disabled={locked} className="border rounded-lg px-3 py-1.5 w-32 disabled:bg-slate-100"
                  aria-label={q.prompt}
                  value={(answers[q.id] as string) ?? ''}
                  onChange={(e) => set(q.id, e.target.value)} />
              ) : (
                <div className="flex flex-col gap-1.5">
                  {(optionOrder[q.id] ?? q.options.map((_, i) => i)).map((i) => (
                    <label key={i} className={`flex items-center gap-2 ${locked ? 'text-slate-500' : 'text-slate-700 cursor-pointer'}`}>
                      <input
                        type={q.type === 'single' ? 'radio' : 'checkbox'}
                        name={q.id}
                        disabled={locked}
                        checked={q.type === 'single' ? answers[q.id] === i : ((answers[q.id] as number[]) ?? []).includes(i)}
                        onChange={() => (q.type === 'single' ? set(q.id, i) : toggleMulti(q.id, i))}
                      />
                      {q.options[i]}
                    </label>
                  ))}
                </div>
              )}
              {!locked && (
                <div className="mt-3">
                  {hintLevels[q.id] ? (
                    <p className="flex items-start gap-1.5 rounded-lg bg-teal-50 px-3 py-2 text-xs leading-relaxed text-teal-900">
                      <Icon name="lightbulb" className="mt-0.5 h-3.5 w-3.5 shrink-0" />{hintFor(q.type, termLabels, lang, hintLevels[q.id])}
                    </p>
                  ) : null}
                  <button
                    onClick={() => setHintLevels((levels) => ({ ...levels, [q.id]: Math.min((levels[q.id] ?? 0) + 1, 2) }))}
                    className="mt-1.5 text-xs font-medium text-teal-700 hover:underline"
                  >
                    {lang === 'de'
                      ? (hintLevels[q.id] === 1 ? 'Konkreteren Hinweis zeigen' : 'Hinweis anzeigen')
                      : (hintLevels[q.id] === 1 ? 'Show a more specific hint' : 'Show hint')}
                  </button>
                </div>
              )}
            </div>
          )
        })}
      </div>

      {!locked ? (
        <div className="mt-6">
          <div className="flex items-center gap-3">
            <button onClick={submit} disabled={busy || !allAnswered}
              className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-5 py-2 font-medium disabled:opacity-50 disabled:cursor-not-allowed">
              {busy ? t(lang, 'evaluating') : t(lang, 'submit')}
            </button>
            {!allAnswered && <span className="text-xs text-slate-400">{t(lang, 'answerAllHint')}</span>}
          </div>
          {error && <p role="alert" className="mt-3 rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-700">{error}</p>}
        </div>
      ) : (
        <div className="mt-6 animate-fade-up" aria-live="polite">
          <div className={`rounded-2xl px-5 py-4 flex items-center justify-between gap-4 ${result.passed ? 'bg-green-50 border border-green-200' : 'bg-amber-50 border border-amber-200'}`}>
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-500 font-semibold">{t(lang, 'yourResult')}</p>
              <p className={`text-2xl font-bold ${result.passed ? 'text-green-600' : 'text-amber-600'}`}>
                {result.score} / {result.total}
                <span className="ml-2 inline-flex items-center gap-1 text-base font-medium">{result.passed ? <><Icon name="check" className="h-4 w-4" />{t(lang, 'passed')}</> : t(lang, 'notPassedYet')}</span>
              </p>
            </div>
            <button onClick={retry} className="shrink-0 rounded-lg border border-slate-300 bg-white text-slate-700 px-4 py-2 font-medium hover:bg-slate-50">
              {t(lang, 'retry')}
            </button>
          </div>
          {wrongQuestions.length > 0 && (
            <div className="mt-3 rounded-xl border border-teal-200 bg-teal-50 p-4">
              <p className="text-sm font-semibold text-teal-900">
                {lang === 'de' ? 'Gezielte Wiederholung' : 'Targeted review'}
              </p>
              <p className="mt-1 text-sm text-teal-800">
                {lang === 'de' ? 'Diese Fragen waren noch nicht richtig. Wiederhole zuerst die zugehörigen Begriffe:' : 'These questions were not correct yet. Review the related terms first:'}
              </p>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {termLabels.map((label) => <span key={label} className="rounded-full bg-white px-2 py-0.5 text-xs font-medium text-teal-800">{label}</span>)}
              </div>
              <button onClick={() => document.getElementById('block-0')?.scrollIntoView({ behavior: 'smooth' })}
                className="mt-3 inline-flex items-center gap-1 text-sm font-medium text-teal-700 hover:underline">
                {lang === 'de' ? 'Zum Lernstoff zurück' : 'Back to the learning material'}<Icon name="arrowUp" className="h-3.5 w-3.5" />
              </button>
            </div>
          )}
        </div>
      )}
      </div>
    </section>
  )
}
