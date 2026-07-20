import type { Lang } from '@/lib/i18n'

// Ersetzt das frühere „Dauerskeleton bei API-Fehler": eine geladene Query, die
// fehlschlägt, zeigt jetzt eine echte Meldung mit Wiederholen-Knopf statt
// endlos zu laden.
export function LoadError({ onRetry, lang = 'de' }: { onRetry?: () => void; lang?: Lang }) {
  const en = lang === 'en'
  return (
    <main className="min-h-dvh flex items-center justify-center bg-slate-50 p-6">
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
