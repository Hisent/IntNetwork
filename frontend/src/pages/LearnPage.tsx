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
  const isDone = (key: string) => progressOf(key)?.done ?? false
  const prereqsMet = (keys: string[]) => keys.every(isDone)

  const total = mods.data?.length ?? 0
  const doneCount = mods.data?.filter((m) => isDone(m.key)).length ?? 0
  const donePct = total ? Math.round((doneCount / total) * 100) : 0

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
        <p className="text-slate-500 text-sm mb-4">{t(lang, 'tagline')}</p>

        {total > 0 && (
          <div className="mb-6">
            <div className="flex justify-between text-xs text-slate-500 mb-1">
              <span>{t(lang, 'courseProgress')}</span>
              <span>{doneCount} / {total} {t(lang, 'modulesDone')}</span>
            </div>
            <div className="h-2 rounded-full bg-slate-200 overflow-hidden">
              <div className="h-full bg-teal-500 rounded-full transition-all duration-500" style={{ width: `${donePct}%` }} />
            </div>
          </div>
        )}

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
            const locked = m.prerequisites.length > 0 && !prereqsMet(m.prerequisites)
            return (
              <Link key={m.key} to={`/lernen/${m.key}`}
                className="rounded-xl border bg-white p-4 hover:shadow block">
                <div className="flex items-center justify-between gap-3">
                  <span className="flex items-center gap-2 font-medium text-slate-800">
                    <span aria-hidden="true" className={`w-2 h-2 rounded-full shrink-0 ${p?.done ? 'bg-green-500' : locked ? 'bg-slate-300' : 'bg-teal-500'}`} />
                    {lang === 'de' ? m.title : m.title_en}
                  </span>
                  <span className="shrink-0 text-sm text-slate-500">
                    {p?.done ? `✓ ${t(lang, 'done')}` : t(lang, 'open')}{p?.best != null ? ` · ${t(lang, 'best')} ${p.best}%` : ''}
                  </span>
                </div>
                {m.prerequisites.length > 0 && (
                  <p className={`text-xs mt-1 flex items-center gap-1 ${locked ? 'text-amber-600' : 'text-slate-400'}`}>
                    <span aria-hidden="true">{locked ? '🔒' : '✓'}</span>
                    {t(lang, 'prerequisitesHint')}: {m.prerequisites.map(titleOf).join(', ')}
                  </p>
                )}
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  )
}
