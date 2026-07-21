import { Link } from 'react-router-dom'
import { BrandLogo } from '@/components/BrandLogo'

export function NotFoundPage() {
  return (
    <main id="main-content" tabIndex={-1} className="min-h-dvh bg-slate-50 flex items-center justify-center p-6">
      <div className="text-center">
        <Link to="/" className="mb-8 inline-flex"><BrandLogo className="h-10 text-lg" showName /></Link>
        <p className="font-mono text-7xl font-bold text-teal-600 mb-3">404</p>
        <p className="font-medium text-slate-800 mb-1">Seite nicht gefunden · Page not found</p>
        <p className="text-sm text-slate-500 mb-5">
          NXDOMAIN — dieser Name löst zu keiner Seite auf.
        </p>
        <Link to="/" className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 font-medium">
          ← Zur Startseite
        </Link>
      </div>
    </main>
  )
}
