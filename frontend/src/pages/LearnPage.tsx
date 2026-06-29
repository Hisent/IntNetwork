import { useQuery } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { useAuthStore } from '@/store/auth'

export function LearnPage() {
  const nav = useNavigate()
  const { role, displayName } = useAuthStore()
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data) })
  const mods = useQuery({ queryKey: ['modules'], queryFn: () => learnApi.listModules().then((r) => r.data) })

  if (role !== 'participant') { nav('/'); return null }

  const progressOf = (key: string) => me.data?.progress.find((p) => p.module_key === key)

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-slate-900">Hallo {displayName}</h1>
        <p className="text-slate-500 text-sm mb-6">Wähle ein Modul.</p>
        <div className="flex flex-col gap-3">
          {mods.data?.map((m) => {
            const p = progressOf(m.key)
            return (
              <Link key={m.key} to={`/lernen/${m.key}`}
                className="rounded-xl border bg-white p-4 flex items-center justify-between hover:shadow">
                <span className="font-medium text-slate-800">{m.title}</span>
                <span className="text-sm text-slate-500">
                  {p?.done ? '✓ erledigt' : 'offen'}{p?.best != null ? ` · best ${p.best}%` : ''}
                </span>
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  )
}
