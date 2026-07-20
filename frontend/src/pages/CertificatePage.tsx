import { useQuery } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { useAuthStore } from '@/store/auth'
import { t, type Lang } from '@/lib/i18n'
import { WorkshopTheme } from '@/components/WorkshopTheme'

// Druckbares Abschluss-Zertifikat: erst verfügbar, wenn alle Module bestanden
// sind. „Drucken" nutzt den Browser-Dialog — PDF gibt es dort gratis dazu.
export function CertificatePage() {
  const nav = useNavigate()
  const { role, displayName } = useAuthStore()
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data) })
  const lang: Lang = me.data?.language ?? 'de'
  const mods = useQuery({ queryKey: ['modules', lang], queryFn: () => learnApi.listModules().then((r) => r.data) })

  if (role !== 'participant') { nav('/'); return null }
  if (me.isLoading || mods.isLoading || !mods.data) return <div className="p-10">{t(lang, 'loading')}</div>

  const isDone = (key: string) => me.data?.progress.find((p) => p.module_key === key)?.done ?? false
  const total = mods.data.length
  const allDone = total > 0 && mods.data.every((m) => isDone(m.key))
  const today = new Date().toLocaleDateString(lang === 'de' ? 'de-DE' : 'en-GB',
    { day: '2-digit', month: 'long', year: 'numeric' })
  const workshopTitle = me.data?.workshop?.title[lang] ?? 'IntNetwork'

  if (!allDone)
    return (
      <WorkshopTheme theme={me.data?.workshop?.theme}><div className="min-h-dvh bg-slate-50 flex items-center justify-center p-6">
        <div className="text-center">
          <p className="text-slate-600 mb-3">{t(lang, 'certNotYet')}</p>
          <Link to="/lernen" className="text-teal-600 hover:underline">← {t(lang, 'backToOverview')}</Link>
        </div>
      </div></WorkshopTheme>
    )

  return (
    <WorkshopTheme theme={me.data?.workshop?.theme}><div className="min-h-dvh bg-slate-100 flex flex-col items-center justify-center p-6 print:bg-white print:p-0">
      <div className="w-full max-w-2xl rounded-2xl border-4 border-double border-teal-600 bg-white p-10 sm:p-14 text-center shadow-lg print:shadow-none print:border-teal-700">
        <img src="/favicon.svg" alt="" className="h-12 w-12 mx-auto mb-4" />
        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-teal-600 mb-1">IntNetwork</p>
        <h1 className="text-4xl font-bold text-slate-900 mb-1">{t(lang, 'certTitle')}</h1>
        <p className="text-sm text-slate-500 mb-8">{t(lang, 'certSubtitle')}</p>

        <p className="text-2xl font-semibold text-slate-900 mb-4">{displayName}</p>
        <p className="text-slate-600 leading-relaxed mb-8">
          {lang === 'de' ? 'hat den Workshop' : 'has completed the workshop'} <b>{workshopTitle}</b> {lang === 'de' ? 'mit allen' : 'with all'} <b>{total}</b> {lang === 'de' ? 'Modulen erfolgreich abgeschlossen.' : 'modules successfully.'}
        </p>

        <div className="mx-auto mb-8 h-px w-40 bg-slate-200" />
        <p className="text-sm text-slate-500">
          {t(lang, 'certDate')} <b className="text-slate-700">{today}</b>
        </p>
      </div>

      <div className="mt-6 flex gap-3 print:hidden">
        <button onClick={() => window.print()}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 font-medium">
          🖨 {t(lang, 'certPrint')}
        </button>
        <Link to="/lernen"
          className="rounded-lg border border-slate-300 bg-white px-4 py-2 font-medium text-slate-700 hover:bg-slate-50">
          ← {t(lang, 'backToOverview')}
        </Link>
      </div>
    </div></WorkshopTheme>
  )
}
