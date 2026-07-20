import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, useParams } from 'react-router-dom'
import { trainerApi, type QuizStats } from '@/lib/trainerApi'
import { TrainerBlocks } from '@/components/TrainerBlocks'
import { PageSkeleton } from '@/components/PageSkeleton'
import { TrainerQuiz } from '@/components/TrainerQuiz'
import { useAuthStore } from '@/store/auth'
import { BrandLogo } from '@/components/BrandLogo'
import { WorkshopTheme } from '@/components/WorkshopTheme'
import { workshopTheme } from '@/lib/workshopTheme'

// Ampelfarbe je Erfolgsquote: ab 70% grün, ab 40% gelb, darunter rot.
function rateColor(rate: number) {
  if (rate >= 0.7) return 'bg-green-500'
  if (rate >= 0.4) return 'bg-amber-500'
  return 'bg-rose-500'
}

function QuizStatsBox({ stats, courseFilter }: { stats: QuizStats; courseFilter: React.ReactNode }) {
  return (
    <div className="rounded-xl border bg-white p-4 mb-6 text-sm">
      <div className="flex items-center justify-between gap-3 mb-1">
        <p className="font-semibold text-slate-700">
          Quiz-Ergebnisse
          <span className="ml-2 font-normal text-slate-400">{stats.submissions} Abgabe(n)</span>
        </p>
        {courseFilter}
      </div>
      {stats.submissions === 0 ? (
        <p className="text-xs text-slate-500">Noch keine Quiz-Abgaben{' '}— ggf. anderen Kurs wählen.</p>
      ) : (
        <>
      <p className="text-xs text-slate-500 mb-3">
        Anteil richtiger Antworten je Frage — rote Balken zeigen, wo es hakt.
      </p>
      <div className="flex flex-col gap-2">
        {stats.questions.map((q, i) => {
          const rate = q.attempts ? q.correct / q.attempts : 0
          return (
            <div key={q.id}>
              <div className="flex justify-between gap-3 text-xs text-slate-600 mb-0.5">
                <span className="truncate">{i + 1}. {q.prompt}</span>
                <span className="shrink-0 tabular-nums">{q.correct}/{q.attempts}</span>
              </div>
              <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
                <div className={`h-full rounded-full ${rateColor(rate)}`}
                  style={{ width: `${Math.round(rate * 100)}%` }} />
              </div>
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
  const { token, role } = useAuthStore()
  const [courseId, setCourseId] = useState<number | undefined>(undefined)
  const mod = useQuery({
    queryKey: ['trainer-module', key],
    queryFn: () => trainerApi.trainerModule(key).then((r) => r.data),
    enabled: role === 'trainer' && !!token,
  })
  const courses = useQuery({
    queryKey: ['courses'],
    queryFn: () => trainerApi.listCourses().then((r) => r.data),
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
        Nur für Trainer. <Link to="/trainer" className="text-teal-600">Zum Login</Link>
      </div>
    )
  if (mod.isLoading || !mod.data) return <PageSkeleton />
  const m = mod.data

  return (
    <WorkshopTheme theme={workshopTheme(m.workshop_key)}><div className="min-h-dvh bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between gap-4">
          <Link to="/trainer" className="text-sm text-slate-400 hover:text-slate-600">← Trainer</Link>
          <Link to="/"><BrandLogo className="h-8 text-base" showName /></Link>
        </div>
        <div className="flex items-start justify-between gap-3 mt-2 mb-4">
          <h1 className="text-2xl font-bold text-slate-900">
            {m.title} <span className="text-sm font-normal text-slate-400">· Trainer-Ansicht</span>
          </h1>
          <Link to={`/trainer/modul/${key}/praesentieren`}
            className="shrink-0 rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium">
            ▶ Präsentieren
          </Link>
        </div>

        <div className="rounded-xl border bg-white p-4 mb-6 text-sm">
          <div className="flex flex-wrap gap-x-6 gap-y-1 text-slate-600">
            <span>Voraussetzungen: {m.prerequisites.length ? m.prerequisites.join(', ') : '—'}</span>
            <span>{m.blocks.length} Blöcke</span>
            <span>{m.quiz.questions.length} Quiz-Fragen</span>
          </div>
          {m.goals && m.goals.length > 0 && (
            <div className="mt-2">
              <p className="font-semibold text-slate-700">Lernziele</p>
              <ul className="list-disc pl-5 text-slate-600">
                {m.goals.map((g, i) => <li key={i}>{g}</li>)}
              </ul>
            </div>
          )}
        </div>

        {stats.data && (
          <QuizStatsBox
            stats={stats.data}
            courseFilter={
              <select
                value={courseId ?? ''}
                onChange={(e) => setCourseId(e.target.value === '' ? undefined : Number(e.target.value))}
                className="rounded-lg border border-slate-200 px-2 py-1 text-xs text-slate-600 bg-white"
              >
                <option value="">Alle Kurse</option>
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
    </div></WorkshopTheme>
  )
}
