import { useMemo, useState, type ReactNode } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, Navigate } from 'react-router-dom'
import { learnApi, type AssessmentResult, type EvaluationInput } from '@/lib/learnApi'
import { errMsg } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { t, tf, useDocumentLang, useDocumentTitle, type Lang } from '@/lib/i18n'
import { WorkshopTheme } from '@/components/WorkshopTheme'
import { LoadError } from '@/components/LoadError'
import { PageSkeleton } from '@/components/PageSkeleton'
import { Icon } from '@/components/Icon'
import { WorkbenchTopbar } from '@/components/workbench/WorkbenchShell'
import { QuestionInput, isAnswered, shuffledIndices } from '@/components/Quiz'
import { useResultFocus } from '@/components/blocks/useResultFocus'

// Lernerfolg für Teilnehmer: Wissenstest (Eingangs-/Abschlusstest) und anonyme
// Kursbewertung. Beides öffnet der Trainer; die Kursseite (/lernen) zeigt dann
// eine Hinweiskarte. Zählt weder für Fortschritt noch Teilnahmebestätigung.

const button = 'wb-control inline-flex items-center justify-center gap-1.5 rounded-lg px-5 font-semibold disabled:cursor-not-allowed disabled:opacity-50'
const primary = `${button} bg-[var(--wb-accent)] text-white hover:bg-[var(--wb-accent-hover)]`

function useParticipantShell() {
  const isParticipant = useAuthStore((state) => state.role) === 'participant'
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data), enabled: isParticipant })
  const lang: Lang = me.data?.language ?? 'de'
  useDocumentLang(lang)
  return { isParticipant, me, lang }
}

function Shell({ lang, theme, workshopTitle, title, children }: { lang: Lang; theme?: Parameters<typeof WorkshopTheme>[0]['theme']; workshopTitle?: string; title: string; children: ReactNode }) {
  return (
    <WorkshopTheme theme={theme}>
      <div className="workbench">
        <WorkbenchTopbar lang={lang} title={workshopTitle ?? 'IntLab'} />
        <main id="main-content" tabIndex={-1} className="wb-shell">
          <div className="mx-auto max-w-[720px]">
            <Link to="/lernen" className="wb-control mb-2 inline-flex items-center gap-1 text-sm font-medium text-[var(--wb-muted)] hover:text-[var(--wb-accent)]"><Icon name="arrowLeft" className="h-4 w-4" />{t(lang, 'modules')}</Link>
            <h1 className="text-3xl font-bold leading-tight tracking-tight text-[var(--wb-ink)]">{title}</h1>
            {children}
          </div>
        </main>
      </div>
    </WorkshopTheme>
  )
}

export function AssessmentPage() {
  const qc = useQueryClient()
  const { isParticipant, me, lang } = useParticipantShell()
  const test = useQuery({ queryKey: ['assessment', lang], queryFn: () => learnApi.assessment().then((r) => r.data), enabled: isParticipant })
  const phase = test.data?.phase
  const title = phase === 'post' ? t(lang, 'taskPostTitle') : t(lang, 'taskPreTitle')
  useDocumentTitle(title)
  const [answers, setAnswers] = useState<Record<string, unknown>>({})
  const [result, setResult] = useState<AssessmentResult | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const shown = result ?? test.data?.result ?? null
  const focusRoot = useResultFocus<HTMLElement>(shown !== null)
  const questions = useMemo(() => test.data?.questions ?? [], [test.data])
  const order = useMemo(() => Object.fromEntries(questions.map((q) => [q.id, q.type === 'number' ? undefined : shuffledIndices(q.options.length)])), [questions])

  if (!isParticipant) return <Navigate to="/" replace />
  if (me.isError || test.isError) return <LoadError lang={lang} onRetry={() => { me.refetch(); test.refetch() }} />
  if (me.isLoading || test.isLoading) return <PageSkeleton />

  async function submit() {
    if (!phase) return
    setError(''); setBusy(true)
    try {
      const r = await learnApi.submitAssessment(phase, answers)
      setResult(r.data)
      qc.invalidateQueries({ queryKey: ['me'] })
    } catch (e) { setError(errMsg(e, t(lang, 'submitFailed'))) } finally { setBusy(false) }
  }

  const theme = me.data?.workshop?.theme
  const workshopTitle = me.data?.workshop?.title[lang]
  if (!test.data) {
    return <Shell lang={lang} theme={theme} workshopTitle={workshopTitle} title={t(lang, 'taskPreTitle')}><p className="wb-surface mt-6 p-5 text-sm text-[var(--wb-muted)]">{t(lang, 'testNotOpen')}</p></Shell>
  }
  const allAnswered = questions.every((q) => isAnswered(q, answers[q.id]))
  return (
    <Shell lang={lang} theme={theme} workshopTitle={workshopTitle} title={title}>
      <p className="mt-2 text-sm text-[var(--wb-muted)]">{phase === 'post' ? t(lang, 'testPostIntro') : t(lang, 'testPreIntro')}</p>
      <section ref={focusRoot} className="mt-6">
        {shown && (
          <div role="status" tabIndex={-1} className="wb-surface mb-6 p-5 outline-none">
            <p className="text-2xl font-bold text-[var(--wb-ink)]">{tf(lang, 'testResult', { score: shown.score, total: shown.total })}</p>
            {!shown.details && <p className="mt-1 text-sm text-[var(--wb-muted)]">{t(lang, 'testPreDone')}</p>}
          </div>
        )}
        {(!shown || shown.details) && (
          <div className="flex flex-col gap-4">
            {questions.map((q, i) => {
              const correct = shown?.details?.[q.id]
              const ring = shown ? (correct ? 'border-green-300 bg-green-50/50' : 'border-amber-300 bg-amber-50/50') : 'border-slate-200 bg-white'
              return (
                <div key={q.id} className={`rounded-xl border p-4 [overflow-wrap:anywhere] ${ring}`}>
                  <div className="mb-2 flex items-start justify-between gap-3">
                    <p id={`quiz-${q.id}`} className="font-medium text-slate-800"><span className="mr-1.5 text-slate-500">{i + 1}.</span>{q.prompt}</p>
                    {shown && (
                      <span className={`inline-flex shrink-0 items-center gap-1 rounded-full px-2 py-0.5 text-xs font-semibold ${correct ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
                        <Icon name={correct ? 'check' : 'close'} className="h-3.5 w-3.5" />{correct ? t(lang, 'correct') : t(lang, 'incorrect')}
                      </span>
                    )}
                  </div>
                  {!shown && <QuestionInput q={q} lang={lang} value={answers[q.id]} locked={busy} order={order[q.id]} onChange={(v) => setAnswers((a) => ({ ...a, [q.id]: v }))} />}
                  {shown?.explanations?.[q.id] && (
                    <p className="mt-2 flex items-start gap-1.5 rounded-lg bg-white/70 px-3 py-2 text-sm leading-relaxed text-slate-700">
                      <Icon name="lightbulb" className="mt-0.5 h-4 w-4 shrink-0 text-teal-700" />
                      <span><span className="font-semibold">{lang === 'de' ? 'Erklärung: ' : 'Explanation: '}</span>{shown.explanations[q.id]}</span>
                    </p>
                  )}
                </div>
              )
            })}
          </div>
        )}
        {!shown && (
          <div className="mt-6 flex flex-wrap items-center gap-3">
            <button type="button" className={primary} disabled={busy || !allAnswered} onClick={submit}>{busy ? t(lang, 'evaluating') : t(lang, 'testSubmit')}</button>
            {!allAnswered && <span className="text-xs text-[var(--wb-muted)]">{t(lang, 'answerAllHint')}</span>}
          </div>
        )}
        {error && <p role="alert" className="mt-4 rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-700">{error}</p>}
      </section>
    </Shell>
  )
}

/** Skala 1–5 als Radiogruppe mit Legende (Tastatur: Pfeiltasten innerhalb der Gruppe). */
function Scale({ name, legend, value, onChange, required, lang }: { name: string; legend: string; value: number | null; onChange: (v: number) => void; required?: boolean; lang: Lang }) {
  return (
    <fieldset className="mt-5">
      <legend className="text-sm font-semibold text-[var(--wb-ink)]">{legend} <span className="font-normal text-[var(--wb-muted)]">{required ? t(lang, 'evalRequired') : t(lang, 'evalOptional')}</span></legend>
      <div className="mt-2 flex flex-wrap gap-2">
        {[1, 2, 3, 4, 5].map((n) => (
          <label key={n} className={`wb-control inline-flex min-w-11 cursor-pointer items-center justify-center rounded-lg border px-3 font-semibold has-[:focus-visible]:ring-2 has-[:focus-visible]:ring-[var(--wb-accent)] ${value === n ? 'border-[var(--wb-accent)] bg-[var(--wb-accent)] text-white' : 'border-[var(--wb-border)] bg-[var(--wb-surface)] text-[var(--wb-ink)]'}`}>
            <input type="radio" name={name} value={n} checked={value === n} required={required} onChange={() => onChange(n)} className="sr-only" />
            {n}
          </label>
        ))}
      </div>
    </fieldset>
  )
}

export function EvaluationPage() {
  const qc = useQueryClient()
  const { isParticipant, me, lang } = useParticipantShell()
  const title = t(lang, 'taskEvalTitle')
  useDocumentTitle(title)
  const [form, setForm] = useState<Omit<EvaluationInput, 'overall'> & { overall: number | null }>({ overall: null, clarity: null, practice: null, pace: null, trainer: null, good: '', improve: '' })
  const [done, setDone] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const focusRoot = useResultFocus<HTMLElement>(done)

  if (!isParticipant) return <Navigate to="/" replace />
  if (me.isError) return <LoadError lang={lang} onRetry={() => me.refetch()} />
  if (me.isLoading) return <PageSkeleton />

  const set = (patch: Partial<typeof form>) => setForm((f) => ({ ...f, ...patch }))
  async function submit(e: React.FormEvent) {
    e.preventDefault()
    if (form.overall == null) return
    setError(''); setBusy(true)
    try {
      await learnApi.submitEvaluation({ ...form, overall: form.overall })
      setDone(true)
      qc.invalidateQueries({ queryKey: ['me'] })
    } catch (err) { setError(errMsg(err, t(lang, 'submitFailed'))) } finally { setBusy(false) }
  }
  const field = 'mt-2 w-full rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-3 py-2 text-sm text-[var(--wb-ink)] outline-none focus:border-[var(--wb-accent)] focus:ring-2 focus:ring-[var(--wb-accent-soft)]'
  const open = me.data?.tasks?.evaluation ?? false
  return (
    <Shell lang={lang} theme={me.data?.workshop?.theme} workshopTitle={me.data?.workshop?.title[lang]} title={title}>
      <section ref={focusRoot}>
        {done ? (
          <p role="status" tabIndex={-1} className="wb-surface mt-6 p-5 text-lg font-semibold text-[var(--wb-ink)] outline-none">{t(lang, 'evalThanks')}</p>
        ) : !open ? (
          <p className="wb-surface mt-6 p-5 text-sm text-[var(--wb-muted)]">{t(lang, 'evalClosed')}</p>
        ) : (
          <form onSubmit={submit} className="wb-surface mt-6 p-5">
            <p className="flex items-start gap-1.5 text-sm text-[var(--wb-muted)]"><Icon name="lock" className="mt-0.5 h-4 w-4 shrink-0" />{t(lang, 'evalAnonNote')}</p>
            <p className="mt-1 text-xs text-[var(--wb-muted)]">{t(lang, 'evalScaleHint')}</p>
            <Scale name="overall" legend={t(lang, 'evalOverall')} value={form.overall} onChange={(v) => set({ overall: v })} required lang={lang} />
            <Scale name="clarity" legend={t(lang, 'evalClarity')} value={form.clarity ?? null} onChange={(v) => set({ clarity: v })} lang={lang} />
            <Scale name="practice" legend={t(lang, 'evalPractice')} value={form.practice ?? null} onChange={(v) => set({ practice: v })} lang={lang} />
            <Scale name="trainer" legend={t(lang, 'evalTrainer')} value={form.trainer ?? null} onChange={(v) => set({ trainer: v })} lang={lang} />
            <fieldset className="mt-5">
              <legend className="text-sm font-semibold text-[var(--wb-ink)]">{t(lang, 'evalPace')} <span className="font-normal text-[var(--wb-muted)]">{t(lang, 'evalOptional')}</span></legend>
              <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1">
                {(['slow', 'ok', 'fast'] as const).map((k) => (
                  <label key={k} className="wb-control inline-flex cursor-pointer items-center gap-2 text-sm text-[var(--wb-ink)]">
                    <input type="radio" name="pace" checked={form.pace === k} onChange={() => set({ pace: k })} />
                    {t(lang, k === 'slow' ? 'paceSlow' : k === 'ok' ? 'paceOk' : 'paceFast')}
                  </label>
                ))}
              </div>
            </fieldset>
            <label className="mt-5 block text-sm font-semibold text-[var(--wb-ink)]">{t(lang, 'evalGood')} <span className="font-normal text-[var(--wb-muted)]">{t(lang, 'evalOptional')}</span>
              <textarea rows={3} maxLength={2000} value={form.good} onChange={(e) => set({ good: e.target.value })} className={field} />
            </label>
            <label className="mt-4 block text-sm font-semibold text-[var(--wb-ink)]">{t(lang, 'evalImprove')} <span className="font-normal text-[var(--wb-muted)]">{t(lang, 'evalOptional')}</span>
              <textarea rows={3} maxLength={2000} value={form.improve} onChange={(e) => set({ improve: e.target.value })} className={field} />
            </label>
            <button type="submit" className={`${primary} mt-6`} disabled={busy || form.overall == null}>{busy ? t(lang, 'evaluating') : t(lang, 'evalSubmit')}</button>
            {error && <p role="alert" className="mt-4 rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-700">{error}</p>}
          </form>
        )}
      </section>
    </Shell>
  )
}
