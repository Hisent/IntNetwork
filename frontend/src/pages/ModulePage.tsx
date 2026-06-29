import { useQuery } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { Blocks } from '@/components/Blocks'
import { Quiz } from '@/components/Quiz'

export function ModulePage() {
  const { key = '' } = useParams()
  const mod = useQuery({ queryKey: ['module', key], queryFn: () => learnApi.getModule(key).then((r) => r.data) })

  if (mod.isLoading || !mod.data) return <div className="p-10">Lädt…</div>

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <Link to="/lernen" className="text-sm text-slate-400 hover:text-slate-600">← Module</Link>
        <h1 className="text-2xl font-bold text-slate-900 mt-2 mb-6">{mod.data.title}</h1>
        <Blocks blocks={mod.data.blocks} />
        <Quiz moduleKey={key} questions={mod.data.quiz.questions} />
      </div>
    </div>
  )
}
