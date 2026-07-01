import { useQuery } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, useParams } from 'react-router-dom'
import { trainerApi } from '@/lib/trainerApi'
import { TrainerBlocks } from '@/components/TrainerBlocks'
import { TrainerQuiz } from '@/components/TrainerQuiz'
import { useAuthStore } from '@/store/auth'

export function TrainerModulePage() {
  const { key = '' } = useParams()
  const { token, role } = useAuthStore()
  const mod = useQuery({
    queryKey: ['trainer-module', key],
    queryFn: () => trainerApi.trainerModule(key).then((r) => r.data),
    enabled: role === 'trainer' && !!token,
  })

  if (role !== 'trainer' || !token)
    return (
      <div className="p-10 text-slate-600">
        Nur für Trainer. <Link to="/trainer" className="text-teal-600">Zum Login</Link>
      </div>
    )
  if (mod.isLoading || !mod.data) return <div className="p-10">Lädt…</div>
  const m = mod.data

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <Link to="/trainer" className="text-sm text-slate-400 hover:text-slate-600">← Trainer</Link>
        <h1 className="text-2xl font-bold text-slate-900 mt-2 mb-4">
          {m.title} <span className="text-sm font-normal text-slate-400">· Trainer-Ansicht</span>
        </h1>

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

        {m.scenario && (
          <div className="rounded-xl border-l-4 border-teal-400 bg-teal-50 px-4 py-3 mb-6 text-sm text-slate-700">
            <Markdown>{m.scenario}</Markdown>
          </div>
        )}

        <TrainerBlocks blocks={m.blocks} />
        <TrainerQuiz questions={m.quiz.questions} />
      </div>
    </div>
  )
}
