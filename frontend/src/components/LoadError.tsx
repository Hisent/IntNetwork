import { Link } from 'react-router-dom'
import { t, useDocumentTitle, type Lang } from '@/lib/i18n'

// Ersetzt das frühere „Dauerskeleton bei API-Fehler": eine geladene Query, die
// fehlschlägt, zeigt jetzt eine echte Meldung mit Wiederholen-Knopf statt
// endlos zu laden.
export function LoadError({ onRetry, lang = 'de' }: { onRetry?: () => void; lang?: Lang }) {
  const en = lang === 'en'
  return (
    <main id="main-content" tabIndex={-1} className="min-h-dvh flex items-center justify-center bg-slate-50 p-6">
      <div className="max-w-sm text-center">
        <p className="text-lg font-semibold text-slate-900">{en ? 'Could not load' : 'Konnte nicht geladen werden'}</p>
        <p className="mt-2 text-sm text-slate-500">{en ? 'Please check your connection and try again.' : 'Bitte Verbindung prüfen und erneut versuchen.'}</p>
        <button
          onClick={onRetry ?? (() => window.location.reload())}
          className="mt-4 rounded-lg bg-teal-600 px-4 py-2 text-sm font-medium text-white hover:bg-teal-700">
          {en ? 'Retry' : 'Erneut versuchen'}
        </button>
      </div>
    </main>
  )
}

// 404 beim Laden eines Moduls ist kein Verbindungsproblem: das Modul ist im Kurs
// abgewählt oder die Adresse stimmt nicht. „Erneut versuchen“ hülfe nicht —
// stattdessen der Weg zurück zur Lernseite.
// `code` kommt vom Backend (module_not_enabled | module_unknown); ohne bekannten Code
// bleibt die Sammelmeldung.
export function ModuleMissing({ lang = 'de', code }: { lang?: Lang; code?: string }) {
  useDocumentTitle(t(lang, 'moduleMissingTitle'))
  const body = code === 'module_not_enabled' ? 'moduleNotEnabledBody' : code === 'module_unknown' ? 'moduleUnknownBody' : 'moduleMissingBody'
  return (
    <main id="main-content" tabIndex={-1} className="min-h-dvh flex items-center justify-center bg-slate-50 p-6">
      <div className="max-w-sm text-center">
        <h1 className="text-lg font-semibold text-slate-900">{t(lang, 'moduleMissingTitle')}</h1>
        <p className="mt-2 text-sm text-slate-500">{t(lang, body)}</p>
        <Link to="/lernen" className="mt-4 inline-block rounded-lg bg-teal-600 px-4 py-2 text-sm font-medium text-white hover:bg-teal-700">
          {t(lang, 'moduleMissingLink')}
        </Link>
      </div>
    </main>
  )
}
