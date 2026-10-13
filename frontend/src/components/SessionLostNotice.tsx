import { useAuthStore } from '@/store/auth'
import { t, type Lang } from '@/lib/i18n'
import { Icon } from '@/components/Icon'

// Hinweis nach erzwungenem Abmelden (401 in lib/api.ts): ohne ihn landete ein
// Teilnehmer kommentarlos auf der Startseite. Bleibt bis zum Schließen oder
// erneuten Beitritt stehen (Start- und Beitrittsseite).
export function SessionLostNotice({ lang, className = '' }: { lang: Lang; className?: string }) {
  const lost = useAuthStore((state) => state.sessionLost)
  const dismiss = useAuthStore((state) => state.dismissSessionLost)
  if (!lost) return null
  return (
    <div role="status" className={`flex items-start gap-3 rounded-lg border border-amber-300 bg-amber-50 px-3 py-2 text-sm text-amber-900 ${className}`}>
      <p className="min-w-0 flex-1">{t(lang, 'sessionLost')}</p>
      <button type="button" onClick={dismiss} aria-label={t(lang, 'dismiss')} title={t(lang, 'dismiss')} className="-my-1 -mr-1 grid h-8 w-8 shrink-0 place-items-center rounded-lg hover:bg-amber-100">
        <Icon name="close" className="h-4 w-4" />
      </button>
    </div>
  )
}
