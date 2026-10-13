import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { BrandLogo } from '@/components/BrandLogo'
import { Icon } from '@/components/Icon'
import { LangToggle } from '@/components/workbench/WorkbenchShell'
import { t, useDocumentLang, useDocumentTitle, usePublicLang } from '@/lib/i18n'

// Öffentliche Prüfseite (kein Login): eine Bestätigungs-ID wird gegen den
// unveränderlichen Zertifikatsdatensatz geprüft.
export function VerifyPage() {
  const { id } = useParams()
  const [lang, setLang] = usePublicLang()
  useDocumentLang(lang)
  useDocumentTitle(t(lang, 'verifyTitle'))
  const nav = useNavigate()
  const [input, setInput] = useState(id ?? '')
  const query = useQuery({
    queryKey: ['verify', id],
    queryFn: () => learnApi.verifyCertificate(id!).then((r) => r.data),
    enabled: !!id,
    retry: false,
  })
  // Busy-Anzeige folgt direkt dem Query-Status statt einem eigenen State: das
  // Absenden navigiert lediglich zu /verifizieren/:id, der eigentliche Request
  // läuft im useQuery oben. So bleibt der Knopf disabled, solange dieser Request
  // noch offen ist, ohne einen zweiten, redundanten Zustand zu pflegen.
  const busy = !!id && query.isFetching

  const date = query.data
    ? new Date(query.data.issued_at).toLocaleDateString(lang === 'de' ? 'de-DE' : 'en-GB', { day: '2-digit', month: 'long', year: 'numeric' })
    : ''

  return (
    <main id="main-content" tabIndex={-1} className="grid min-h-dvh place-items-center bg-slate-50 p-6">
      <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="mb-6 flex items-center justify-between gap-2">
          <Link to="/" className="inline-block"><BrandLogo className="h-8" showName /></Link>
          <LangToggle lang={lang} onChange={setLang} />
        </div>
        <h1 className="text-xl font-bold text-slate-900">{t(lang, 'verifyTitle')}</h1>
        <p className="mt-1 text-sm text-slate-500">{t(lang, 'verifyHint')}</p>

        <form
          onSubmit={(e) => { e.preventDefault(); if (input.trim() && !busy) nav(`/verifizieren/${encodeURIComponent(input.trim())}`) }}
          className="mt-5 flex gap-2">
          <input value={input} onChange={(e) => setInput(e.target.value)}
            aria-label={t(lang, 'verifyIdLabel')}
            placeholder={t(lang, 'verifyPlaceholder')}
            className="min-w-0 flex-1 rounded-lg border border-slate-300 px-3 py-2 font-mono text-sm outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100" />
          <button disabled={busy || !input.trim()} className="rounded-lg bg-teal-600 px-4 py-2 font-medium text-white hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed">{busy ? t(lang, 'verifyBusy') : t(lang, 'verifySubmit')}</button>
        </form>

        {id && query.isLoading && <p className="mt-6 text-sm text-slate-500">{t(lang, 'verifyBusy')}</p>}

        {id && query.isError && (
          <div className="mt-6 flex items-start gap-3 rounded-xl border border-rose-200 bg-rose-50 p-4">
            <span className="text-rose-500"><Icon name="alert" className="h-5 w-5" /></span>
            <div>
              <p className="font-semibold text-rose-700">{t(lang, 'verifyNotFound')}</p>
              <p className="text-sm text-rose-600">{t(lang, 'verifyNotFoundText')}</p>
            </div>
          </div>
        )}

        {query.data && (
          <div className="mt-6 rounded-xl border border-teal-200 bg-teal-50 p-5">
            <div className="flex items-center gap-2 text-teal-700">
              <Icon name="shield" className="h-5 w-5" />
              <span className="font-semibold">{t(lang, 'verifyValid')}</span>
            </div>
            <dl className="mt-4 space-y-2 text-sm">
              <div className="flex justify-between gap-4"><dt className="text-slate-500">{t(lang, 'verifyName')}</dt><dd className="font-medium text-slate-900">{query.data.participant_name}</dd></div>
              <div className="flex justify-between gap-4"><dt className="text-slate-500">{t(lang, 'verifyWorkshop')}</dt><dd className="text-right font-medium text-slate-900">{query.data.workshop_title}</dd></div>
              <div className="flex justify-between gap-4"><dt className="text-slate-500">{t(lang, 'modules')}</dt><dd className="font-medium text-slate-900">{query.data.module_count}</dd></div>
              <div className="flex justify-between gap-4"><dt className="text-slate-500">{t(lang, 'verifyIssued')}</dt><dd className="font-medium text-slate-900">{date}</dd></div>
            </dl>
          </div>
        )}
      </div>
    </main>
  )
}
