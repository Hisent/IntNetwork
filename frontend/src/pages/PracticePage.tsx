import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link, Navigate } from 'react-router-dom'
import { learnApi, type PracticeQuestion } from '@/lib/learnApi'
import { errMsg } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { t, useDocumentLang, type Lang } from '@/lib/i18n'
import { WorkshopTheme } from '@/components/WorkshopTheme'
import { LoadError } from '@/components/LoadError'
import { PageSkeleton } from '@/components/PageSkeleton'
import { Icon } from '@/components/Icon'
import { WorkbenchTopbar } from '@/components/workbench/WorkbenchShell'
import { QuestionInput, isAnswered, shuffledIndices } from '@/components/Quiz'

type Mode = 'wrong' | 'mixed'
interface Feedback { correct: boolean; explanation: string | null }

// Übungsmodus: Fragen aus bereits bearbeiteten Modulen wiederholen. Bewertet
// wird je Frage serverseitig (die Lösung kommt nie zum Client); nichts davon
// zählt für Quiz-Ergebnis, Fortschritt oder Teilnahmebestätigung.
export function PracticePage() {
  const isParticipant = useAuthStore((state) => state.role) === 'participant'
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data), enabled: isParticipant })
  const lang: Lang = me.data?.language ?? 'de'
  useDocumentLang(lang)
  const de = lang === 'de'

  const [questions, setQuestions] = useState<PracticeQuestion[] | null>(null)
  const [index, setIndex] = useState(0)
  const [answer, setAnswer] = useState<unknown>(undefined)
  const [feedback, setFeedback] = useState<Feedback | null>(null)
  const [right, setRight] = useState(0)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const failed = de ? 'Das hat nicht geklappt. Bitte versuche es erneut.' : 'That did not work. Please try again.'

  const q = questions?.[index]
  // je Frage einmal mischen — die abgegebene Antwort bleibt der Original-Index
  const order = useMemo(() => (q && q.type !== 'number' ? shuffledIndices(q.options.length) : undefined), [q])

  async function start(mode: Mode) {
    setError(''); setBusy(true)
    try {
      const r = await learnApi.practice(mode)
      setQuestions(r.data.questions); setIndex(0); setAnswer(undefined); setFeedback(null); setRight(0)
    } catch (e) { setError(errMsg(e, failed)) } finally { setBusy(false) }
  }
  async function check() {
    if (!q) return
    setError(''); setBusy(true)
    try {
      const r = await learnApi.practiceCheck(q.id, answer)
      setFeedback(r.data)
      if (r.data.correct) setRight((n) => n + 1)
    } catch (e) { setError(errMsg(e, failed)) } finally { setBusy(false) }
  }
  const next = () => { setIndex((i) => i + 1); setAnswer(undefined); setFeedback(null) }

  if (!isParticipant) return <Navigate to="/" replace />
  if (me.isError) return <LoadError lang={lang} onRetry={() => me.refetch()} />
  if (me.isLoading) return <PageSkeleton />

  const button = 'wb-control inline-flex items-center justify-center gap-1.5 rounded-lg px-5 font-semibold disabled:cursor-not-allowed disabled:opacity-50'
  const primary = `${button} bg-[var(--wb-accent)] text-white hover:bg-[var(--wb-accent-hover)]`
  const secondary = `${button} border border-[var(--wb-border)] bg-[var(--wb-surface)] text-[var(--wb-ink)] hover:border-[var(--wb-accent)]`
  const finished = questions !== null && index >= questions.length

  return (
    <WorkshopTheme theme={me.data?.workshop?.theme}>
      <div className="workbench">
        <WorkbenchTopbar lang={lang} title={me.data?.workshop?.title[lang] ?? 'IntLab'} />
        <main id="main-content" tabIndex={-1} className="wb-shell">
          <div className="mx-auto max-w-[720px]">
            <Link to="/lernen" className="wb-control mb-2 inline-flex items-center gap-1 text-sm font-medium text-[var(--wb-muted)] hover:text-[var(--wb-accent)]"><Icon name="arrowLeft" className="h-4 w-4" />{t(lang, 'modules')}</Link>
            <h1 className="text-3xl font-bold leading-tight tracking-tight text-[var(--wb-ink)]">{de ? 'Üben & Wiederholen' : 'Practice & review'}</h1>
            <p className="mt-2 text-sm text-[var(--wb-muted)]">
              {de ? 'Fragen aus Modulen, deren Wissenscheck du schon einmal abgegeben hast. Zählt nicht für Fortschritt oder Teilnahmebestätigung.'
                : 'Questions from modules whose knowledge check you have already submitted. Does not count towards progress or your certificate.'}
            </p>

            {(questions === null || finished || questions.length === 0) && (
              <section className="wb-surface mt-6 p-5" aria-live="polite">
                {finished && questions.length > 0 && (
                  <p className="mb-4 text-lg font-semibold text-[var(--wb-ink)]">
                    {de ? `${right} von ${questions.length} richtig` : `${right} of ${questions.length} correct`}
                  </p>
                )}
                {questions?.length === 0 && (
                  <p className="mb-4 text-sm text-[var(--wb-muted)]">
                    {de ? 'Dafür gibt es gerade keine Fragen. Gib zuerst den Wissenscheck eines Moduls ab — oder wähle „Gemischtes Üben“.'
                      : 'There are no questions for this right now. Submit a module’s knowledge check first — or choose “Mixed practice”.'}
                  </p>
                )}
                <div className="flex flex-col gap-3 sm:flex-row">
                  <button type="button" className={primary} disabled={busy} onClick={() => start('wrong')}>
                    {de ? 'Falsch beantwortete wiederholen' : 'Review questions I got wrong'}
                  </button>
                  <button type="button" className={secondary} disabled={busy} onClick={() => start('mixed')}>
                    {de ? 'Gemischtes Üben' : 'Mixed practice'}
                  </button>
                </div>
              </section>
            )}

            {q && (
              <section className="mt-6">
                <p className="mb-2 flex items-baseline justify-between gap-3 text-xs text-[var(--wb-muted)]">
                  <Link to={`/lernen/${q.module_key}`} className="font-semibold text-[var(--wb-accent)] hover:underline">{q.module_title}</Link>
                  <span className="tabular-nums">{de ? 'Frage' : 'Question'} {index + 1} / {questions.length}</span>
                </p>
                {/* key: Eingaben der vorherigen Frage nicht mitnehmen */}
                <div key={q.id} className={`rounded-xl border p-4 ${feedback ? (feedback.correct ? 'border-green-300 bg-green-50/50' : 'border-amber-300 bg-amber-50/50') : 'border-slate-200 bg-white'}`}>
                  <p id={`quiz-${q.id}`} className="mb-2 font-medium text-slate-800">{q.prompt}</p>
                  <QuestionInput q={q} value={answer} locked={feedback !== null} order={order} onChange={setAnswer} />
                  <div aria-live="polite">
                    {feedback && (
                      <>
                        <p className={`mt-3 inline-flex items-center gap-1 text-sm font-semibold ${feedback.correct ? 'text-green-700' : 'text-amber-700'}`}>
                          <Icon name={feedback.correct ? 'check' : 'close'} className="h-4 w-4" />{feedback.correct ? t(lang, 'correct') : t(lang, 'incorrect')}
                        </p>
                        {feedback.explanation && (
                          <p className="mt-2 flex items-start gap-1.5 rounded-lg bg-white/70 px-3 py-2 text-sm leading-relaxed text-slate-700">
                            <Icon name="lightbulb" className="mt-0.5 h-4 w-4 shrink-0 text-teal-700" />
                            <span><span className="font-semibold">{de ? 'Erklärung: ' : 'Explanation: '}</span>{feedback.explanation}</span>
                          </p>
                        )}
                      </>
                    )}
                  </div>
                </div>
                <div className="mt-4 flex flex-wrap items-center gap-3">
                  {feedback === null
                    ? <button type="button" className={primary} disabled={busy || !isAnswered(q, answer)} onClick={check}>{busy ? t(lang, 'evaluating') : t(lang, 'checkIt')}</button>
                    : <button type="button" className={primary} autoFocus onClick={next}>{index + 1 < questions.length ? (de ? 'Nächste Frage' : 'Next question') : (de ? 'Auswertung' : 'Summary')}<Icon name="arrowRight" className="h-4 w-4" /></button>}
                  {feedback && !feedback.correct && (
                    <button type="button" className={secondary} onClick={() => { setFeedback(null); setAnswer(undefined) }}>{t(lang, 'tryAgainShort')}</button>
                  )}
                </div>
              </section>
            )}
            {error && <p role="alert" className="mt-4 rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-700">{error}</p>}
          </div>
        </main>
      </div>
    </WorkshopTheme>
  )
}
