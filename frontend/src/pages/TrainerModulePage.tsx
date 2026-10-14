import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, useParams } from 'react-router-dom'
import { trainerApi, type QuizStats } from '@/lib/trainerApi'
import { TrainerBlocks } from '@/components/TrainerBlocks'
import { PageSkeleton } from '@/components/PageSkeleton'
import { LoadError } from '@/components/LoadError'
import { TrainerQuiz } from '@/components/TrainerQuiz'
import { useAuthStore } from '@/store/auth'
import { BrandLogo } from '@/components/BrandLogo'
import { WorkshopTheme } from '@/components/WorkshopTheme'
import { workshopTheme } from '@/lib/workshopTheme'
import { useDocumentLang, useDocumentTitle } from '@/lib/i18n'
import { TrainerLangToggle } from '@/components/TrainerLangToggle'
import { useTr } from '@/store/lang'
import type { Question } from '@/types'

// Ampelfarbe je Erfolgsquote: ab 70% grün, ab 40% gelb, darunter rot.
function rateColor(rate: number) {
  if (rate >= 0.7) return 'bg-green-500'
  if (rate >= 0.4) return 'bg-amber-500'
  return 'bg-rose-500'
}

// Ab diesem Anteil der Versuche gilt eine falsche Option als „attraktiver Distraktor“.
const ATTRACTIVE = 0.3

/** Je Option ein schmaler Balken (Anteil der Versuche), die Lösung mit ✓;
 *  falsche Optionen ab ATTRACTIVE hervorgehoben. Multiple Choice: Anteile summieren
 *  sich nicht zu 100 %. */
function OptionBars({ question, counts, attempts }: { question: Question; counts: number[]; attempts: number }) {
  const { tr } = useTr()
  if (question.type === 'number') return null
  const correct = (i: number) => (Array.isArray(question.answer) ? question.answer.includes(i) : question.answer === i)
  return (
    <ol className="mt-1.5 flex flex-col gap-1 pl-4">
      {question.options.map((option, i) => {
        const share = attempts ? (counts[i] ?? 0) / attempts : 0
        const attractive = !correct(i) && share >= ATTRACTIVE
        return (
          <li key={i} className={`rounded px-1 ${attractive ? 'bg-rose-50 ring-1 ring-rose-200' : ''}`}>
            <div className="flex items-center gap-2 text-xs text-slate-600">
              <span aria-hidden="true" className="w-4 shrink-0 font-semibold text-slate-500">{String.fromCharCode(65 + i)}</span>
              <span title={option} className="min-w-0 truncate">{option}</span>
              {/* Markierungen außerhalb des gekürzten Texts: bleiben auch bei 375 px sichtbar */}
              {correct(i) && <span className="-ml-1 shrink-0 font-semibold text-green-700"><span aria-hidden="true">✓</span><span className="sr-only">({tr('trCorrectOption')})</span></span>}
              {attractive && <span className="-ml-1 shrink-0 font-semibold text-rose-700">· {tr('trAttractiveDistractor')}</span>}
              <span className="flex-1" />
              <span className="w-16 shrink-0 text-right tabular-nums">{counts[i] ?? 0} · {Math.round(share * 100)} %</span>
            </div>
            <div className="ml-6 h-1 overflow-hidden rounded-full bg-slate-100">
              <div className={`h-full rounded-full ${correct(i) ? 'bg-green-500' : attractive ? 'bg-rose-500' : 'bg-slate-400'}`}
                style={{ width: `${Math.round(share * 100)}%` }} />
            </div>
          </li>
        )
      })}
    </ol>
  )
}

function QuizStatsBox({ stats, questions, courseFilter }: { stats: QuizStats; questions: Question[]; courseFilter: React.ReactNode }) {
  const { tr } = useTr()
  const byId = new Map(questions.map((q) => [q.id, q]))
  return (
    <div className="rounded-xl border bg-white p-4 mb-6 text-sm">
      <div className="flex flex-wrap items-center justify-between gap-x-3 gap-y-2 mb-1">
        <p className="font-semibold text-slate-700">
          {tr('trQuizResults')}
          <span className="ml-2 font-normal text-slate-500 whitespace-nowrap">{tr('trSubmissions', { n: stats.submissions })}</span>
        </p>
        {courseFilter}
      </div>
      {stats.submissions === 0 ? (
        <p className="text-xs text-slate-500">{tr('trNoSubmissions')}</p>
      ) : (
        <>
      <p className="text-xs text-slate-500 mb-3">
        {tr('trQuizRateHint')} {tr('trOptionsHint', { pct: ATTRACTIVE * 100 })}
      </p>
      <div className="flex flex-col gap-3">
        {stats.questions.map((q, i) => {
          const rate = q.attempts ? q.correct / q.attempts : 0
          const question = byId.get(q.id)
          return (
            <div key={q.id}>
              <div className="flex justify-between gap-3 text-xs text-slate-600 mb-0.5">
                <span title={q.prompt} className="truncate">{i + 1}. {q.prompt}</span>
                <span className="shrink-0 tabular-nums">{q.correct}/{q.attempts}</span>
              </div>
              <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
                <div className={`h-full rounded-full ${rateColor(rate)}`}
                  style={{ width: `${Math.round(rate * 100)}%` }} />
              </div>
              {q.options && question && q.attempts > 0 && <OptionBars question={question} counts={q.options} attempts={q.attempts} />}
            </div>
          )
        })}
      </div>
        </>
      )}
    </div>
  )
}

export function TrainerModulePage() {
  const { key = '' } = useParams()
  const { lang, tr } = useTr()
  useDocumentLang(lang)
  const { token, role } = useAuthStore()
  const [courseId, setCourseId] = useState<number | undefined>(undefined)
  const mod = useQuery({
    queryKey: ['trainer-module', key],
    queryFn: () => trainerApi.trainerModule(key).then((r) => r.data),
    enabled: role === 'trainer' && !!token,
  })
  useDocumentTitle(mod.data ? `${mod.data.title} · ${tr('trTrainer')}` : tr('trTrainer'))
  const courses = useQuery({
    queryKey: ['courses'],
    queryFn: () => trainerApi.listCourses().then((r) => r.data),
    enabled: role === 'trainer' && !!token,
  })
  const allModules = useQuery({
    queryKey: ['trainer-modules'],
    queryFn: () => trainerApi.trainerModules().then((r) => r.data),
    enabled: role === 'trainer' && !!token,
  })
  const stats = useQuery({
    queryKey: ['quiz-stats', key, courseId],
    queryFn: () => trainerApi.quizStats(key, courseId).then((r) => r.data),
    enabled: role === 'trainer' && !!token,
  })

  if (role !== 'trainer' || !token)
    return (
      <div className="p-10 text-slate-600">
        {tr('trTrainerOnly')} <Link to="/trainer" className="text-teal-600">{tr('trToLogin')}</Link>
      </div>
    )
  if (mod.isError && !mod.data) return <LoadError lang={lang} onRetry={() => mod.refetch()} />
  if (mod.isLoading || !mod.data) return <PageSkeleton />
  const m = mod.data

  return (
    <WorkshopTheme theme={workshopTheme(m.workshop_key)}><main id="main-content" tabIndex={-1} className="min-h-dvh bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between gap-4">
          <Link to="/trainer" className="text-sm text-slate-500 hover:text-slate-700">{tr('trBackTrainer')}</Link>
          <div className="flex items-center gap-3">
            <TrainerLangToggle />
            <Link to="/"><BrandLogo className="h-8 text-base" showName /></Link>
          </div>
        </div>
        <div className="flex items-start justify-between gap-3 mt-2 mb-4">
          <h1 className="text-2xl font-bold text-slate-900">
            {m.title} <span className="text-sm font-normal text-slate-500">{tr('trTrainerView')}</span>
          </h1>
          <Link to={`/trainer/modul/${key}/praesentieren`}
            className="shrink-0 rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium">
            {tr('trPresentBtn')}
          </Link>
        </div>

        <div className="rounded-xl border bg-white p-4 mb-6 text-sm">
          <div className="flex flex-wrap gap-x-6 gap-y-1 text-slate-600">
            <span>{tr('trPrerequisites')}: {m.prerequisites.length ? m.prerequisites.map((k) => allModules.data?.find((x) => x.key === k)?.title ?? k).join(', ') : '—'}</span>
            <span>{tr('trBlocksCount', { n: m.blocks.length })}</span>
            <span>{tr('trQuizQuestionsCount', { n: m.quiz.questions.length })}</span>
          </div>
          {m.goals && m.goals.length > 0 && (
            <div className="mt-2">
              <p className="font-semibold text-slate-700">{tr('trLearningGoals')}</p>
              <ul className="list-disc pl-5 text-slate-600">
                {m.goals.map((g, i) => <li key={i}>{g}</li>)}
              </ul>
            </div>
          )}
        </div>

        {stats.data && (
          <QuizStatsBox
            stats={stats.data}
            questions={m.quiz.questions}
            courseFilter={
              <select
                value={courseId ?? ''}
                onChange={(e) => setCourseId(e.target.value === '' ? undefined : Number(e.target.value))}
                aria-label={tr('trCourses')}
                className="min-w-0 max-w-full truncate rounded-lg border border-slate-200 px-2 py-1 text-xs text-slate-600 bg-white sm:max-w-xs"
              >
                <option value="">{tr('trAllCourses')}</option>
                {courses.data?.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            }
          />
        )}

        {m.scenario && (
          <div className="rounded-xl border border-teal-100 bg-teal-50 px-4 py-3 mb-6 text-sm text-teal-900">
            <Markdown>{m.scenario}</Markdown>
          </div>
        )}

        <TrainerBlocks blocks={m.blocks} />
        <TrainerQuiz questions={m.quiz.questions} />
      </div>
    </main></WorkshopTheme>
  )
}
