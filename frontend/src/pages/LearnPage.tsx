import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { useAuthStore } from '@/store/auth'
import { t, type Lang } from '@/lib/i18n'

export function LearnPage() {
  const nav = useNavigate()
  const qc = useQueryClient()
  const { role, displayName } = useAuthStore()
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data) })
  const lang: Lang = me.data?.language ?? 'de'
  const mods = useQuery({ queryKey: ['modules', lang], queryFn: () => learnApi.listModules().then((r) => r.data) })
  const company = useQuery({ queryKey: ['company', lang], queryFn: () => learnApi.company().then((r) => r.data) })
  const setLang = useMutation({
    mutationFn: (l: Lang) => learnApi.setLanguage(l),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['me'] })
      qc.invalidateQueries({ queryKey: ['modules'] })
      qc.invalidateQueries({ queryKey: ['company'] })
      qc.invalidateQueries({ queryKey: ['module'] })
    },
  })

  if (role !== 'participant') { nav('/'); return null }

  const titleOf = (key: string) => {
    const m = mods.data?.find((x) => x.key === key)
    return m ? (lang === 'de' ? m.title : m.title_en) : key
  }
  const progressOf = (key: string) => me.data?.progress.find((p) => p.module_key === key)

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-slate-900">{t(lang, 'hello')} {displayName}</h1>
          <div className="flex gap-1 text-xs font-medium">
            <button onClick={() => setLang.mutate('de')}
              className={`rounded px-2 py-1 border ${lang === 'de' ? 'bg-teal-600 text-white border-teal-600' : 'text-slate-500 border-slate-200 hover:bg-slate-50'}`}>
              DE
            </button>
            <button onClick={() => setLang.mutate('en')}
              className={`rounded px-2 py-1 border ${lang === 'en' ? 'bg-teal-600 text-white border-teal-600' : 'text-slate-500 border-slate-200 hover:bg-slate-50'}`}>
              EN
            </button>
          </div>
        </div>
        <p className="text-slate-500 text-sm mb-6">{t(lang, 'tagline')}</p>

        {company.data && (
          <div className="rounded-2xl border bg-white p-5 mb-8">
            <h2 className="font-semibold text-slate-900">{company.data.name}</h2>
            <p className="text-sm text-slate-600 mt-1">{company.data.blurb}</p>
            <p className="text-xs text-slate-500 mt-3">{t(lang, 'sites')}: {company.data.sites.join(', ')}</p>
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
                  <span className="font-medium text-slate-800">{lang === 'de' ? m.title : m.title_en}</span>
                  <span className="text-sm text-slate-500">
                    {p?.done ? `✓ ${t(lang, 'done')}` : t(lang, 'open')}{p?.best != null ? ` · ${t(lang, 'best')} ${p.best}%` : ''}
                  </span>
                </div>
                {m.prerequisites.length > 0 && (
                  <p className="text-xs text-slate-400 mt-1">{t(lang, 'prerequisitesHint')}: {m.prerequisites.map(titleOf).join(', ')}</p>
                )}
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  )
}
