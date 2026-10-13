import { Link } from 'react-router-dom'
import { BrandLogo } from '@/components/BrandLogo'
import { LangToggle } from '@/components/workbench/WorkbenchShell'
import { t, useDocumentLang, useDocumentTitle, usePublicLang } from '@/lib/i18n'

export function NotFoundPage() {
  const [lang, setLang] = usePublicLang()
  useDocumentLang(lang)
  useDocumentTitle(t(lang, 'notFoundTitle'))
  return (
    <main id="main-content" tabIndex={-1} className="min-h-dvh bg-slate-50 flex items-center justify-center p-6">
      <div className="text-center">
        <Link to="/" className="mb-8 inline-flex"><BrandLogo className="h-10 text-lg" showName /></Link>
        <p className="font-mono text-7xl font-bold text-teal-600 mb-3">404</p>
        <h1 className="font-medium text-slate-800 mb-1">{t(lang, 'notFoundTitle')}</h1>
        <p className="text-sm text-slate-500 mb-5">{t(lang, 'notFoundText')}</p>
        <Link to="/" className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 font-medium">
          {t(lang, 'toHome')}
        </Link>
        <LangToggle lang={lang} onChange={setLang} className="mt-6 flex justify-center" />
      </div>
    </main>
  )
}
