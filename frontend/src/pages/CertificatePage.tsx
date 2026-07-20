import { useQuery } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { useAuthStore } from '@/store/auth'
import { t, type Lang } from '@/lib/i18n'
import { WorkshopTheme } from '@/components/WorkshopTheme'
import { BrandLogo } from '@/components/BrandLogo'
import { Icon } from '@/components/Icon'

// Druckbares Abschluss-Zertifikat: erst verfügbar, wenn alle Module bestanden
// sind. „Drucken" nutzt den Browser-Dialog — PDF gibt es dort gratis dazu.
export function CertificatePage() {
  const nav = useNavigate()
  const { role, displayName } = useAuthStore()
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data) })
  const lang: Lang = me.data?.language ?? 'de'
  const mods = useQuery({ queryKey: ['modules', lang], queryFn: () => learnApi.listModules().then((r) => r.data) })
  // allDone undefined-sicher, damit der cert-Hook vor den Early-Returns stehen kann
  // (Rules of Hooks). Ausstellen erst, wenn wirklich alle Module bestanden sind.
  const allDone = !!mods.data && mods.data.length > 0 &&
    mods.data.every((m) => me.data?.progress.find((p) => p.module_key === m.key)?.done)
  const cert = useQuery({ queryKey: ['certificate'], queryFn: () => learnApi.issueCertificate().then((r) => r.data), enabled: allDone })

  if (role !== 'participant') { nav('/'); return null }
  if (me.isLoading || mods.isLoading || !mods.data) return <div className="p-10">{t(lang, 'loading')}</div>

  const total = mods.data.length
  const today = new Date().toLocaleDateString(lang === 'de' ? 'de-DE' : 'en-GB',
    { day: '2-digit', month: 'long', year: 'numeric' })
  const workshopTitle = me.data?.workshop?.title[lang] ?? 'IntLab'

  // Kurs mit Trainerfreigabe: alle Module done, aber noch nicht freigegeben (409).
  const awaitingApproval = allDone && cert.isError
  if (!allDone || awaitingApproval)
    return (
      <WorkshopTheme theme={me.data?.workshop?.theme}><div className="min-h-dvh bg-slate-50 flex items-center justify-center p-6">
        <div className="max-w-md text-center">
          <p className="text-slate-600 mb-3">{awaitingApproval
            ? (lang === 'de' ? 'Alle Module geschafft! Die Teilnahmebestätigung wird nach der Freigabe durch die Kursleitung verfügbar.' : 'All modules done! The certificate becomes available once your trainer approves it.')
            : t(lang, 'certNotYet')}</p>
          <Link to="/lernen" className="text-teal-600 hover:underline">← {t(lang, 'backToOverview')}</Link>
        </div>
      </div></WorkshopTheme>
    )

  return (
    <WorkshopTheme theme={me.data?.workshop?.theme}><div className="min-h-dvh bg-slate-100 flex flex-col items-center justify-center p-6 print:bg-white print:p-0">
      <div className="w-full max-w-2xl rounded-2xl border-4 border-double border-teal-600 bg-white p-10 sm:p-14 text-center shadow-lg print:shadow-none print:border-teal-700">
        <BrandLogo className="mx-auto mb-4 h-12" />
        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-teal-600 mb-1">IntLab</p>
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
        {cert.data && (
          <p className="mt-4 text-xs text-slate-400">
            {lang === 'de' ? 'Prüf-ID' : 'Verification ID'}: <span className="select-all font-mono text-slate-500">{cert.data.id}</span>
            <br />
            {lang === 'de' ? 'Prüfbar unter' : 'Verify at'} {window.location.origin}/verifizieren/{cert.data.id}
          </p>
        )}
      </div>

      <div className="mt-6 flex gap-3 print:hidden">
        <button onClick={() => window.print()}
          className="inline-flex items-center gap-2 rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 font-medium">
          <Icon name="printer" className="h-4 w-4" /> {t(lang, 'certPrint')}
        </button>
        <Link to="/lernen"
          className="rounded-lg border border-slate-300 bg-white px-4 py-2 font-medium text-slate-700 hover:bg-slate-50">
          ← {t(lang, 'backToOverview')}
        </Link>
      </div>
    </div></WorkshopTheme>
  )
}
