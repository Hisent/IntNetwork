import { useQuery } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { useAuthStore } from '@/store/auth'

export function LearnPage() {
  const nav = useNavigate()
  const { role, displayName } = useAuthStore()
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data) })
  const mods = useQuery({ queryKey: ['modules'], queryFn: () => learnApi.listModules().then((r) => r.data) })
  const company = useQuery({ queryKey: ['company'], queryFn: () => learnApi.company().then((r) => r.data) })

  if (role !== 'participant') { nav('/'); return null }

  const titleOf = (key: string) => mods.data?.find((m) => m.key === key)?.title ?? key
  const progressOf = (key: string) => me.data?.progress.find((p) => p.module_key === key)

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-slate-900">Hallo {displayName}</h1>
        <p className="text-slate-500 text-sm mb-6">Netzwerk-Grundlagen — am Beispiel einer echten Firma.</p>

        {company.data && (
          <div className="rounded-2xl border bg-white p-5 mb-8">
            <h2 className="font-semibold text-slate-900">{company.data.name}</h2>
            <p className="text-sm text-slate-600 mt-1">{company.data.blurb}</p>
            <p className="text-xs text-slate-500 mt-3">Standorte: {company.data.sites.join(', ')}</p>
            <div className="mt-2 flex flex-wrap gap-1.5">
              {company.data.devices.map((d) => (
                <span key={d} className="text-xs rounded-full bg-slate-100 text-slate-600 px-2 py-0.5">{d}</span>
              ))}
            </div>
          </div>
        )}

        <div className="flex flex-col gap-3">
          {mods.data?.map((m) => {
            const p = progressOf(m.key)
            return (
              <Link key={m.key} to={`/lernen/${m.key}`}
                className="rounded-xl border bg-white p-4 hover:shadow block">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-800">{m.title}</span>
                  <span className="text-sm text-slate-500">
                    {p?.done ? '✓ erledigt' : 'offen'}{p?.best != null ? ` · best ${p.best}%` : ''}
                  </span>
                </div>
                {m.prerequisites.length > 0 && (
                  <p className="text-xs text-slate-400 mt-1">setzt voraus: {m.prerequisites.map(titleOf).join(', ')}</p>
                )}
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  )
}
