import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { dismiss, followHref, followTarget, loadDismissed } from '@/lib/follow'
import { localTitle, t, tf, type Lang } from '@/lib/i18n'
import { Icon } from '@/components/Icon'
import type { ModuleMeta, ProgressItem } from '@/types'

/** „Folgt mir“: Hinweis, bei welchem Modul der Trainer gerade ist. Nur ein Angebot —
 *  navigiert nie selbst, nimmt keinen Fokus; je Modul wegklickbar. Fragt alle 10 s
 *  nach (ruht bei verstecktem Tab, wie die Live-Abstimmung). Braucht --wb-*-Tokens. */
export function FollowBanner({ lang, current, modules, progress }: { lang: Lang; current: string | null; modules: ModuleMeta[]; progress: ProgressItem[] }) {
  const { data: follow } = useQuery({ queryKey: ['follow'], queryFn: () => learnApi.follow().then((r) => r.data), refetchInterval: 10_000, retry: false })
  const [dismissed, setDismissed] = useState(loadDismissed)
  const target = followTarget(follow, current, modules, progress, dismissed)
  // Live-Region bleibt stehen, nur der Inhalt wechselt — so wird das Erscheinen angesagt.
  return (
    <div role="status" className="print:hidden">
      {target && follow && (
        <div className="wb-surface mb-5 flex flex-wrap items-center gap-x-3 gap-y-2 border-[var(--wb-accent)] px-4 py-3 text-sm">
          <Icon name="users" className="h-4 w-4 shrink-0 text-[var(--wb-accent)]" />
          <p className="min-w-0 flex-1 text-[var(--wb-ink)] [overflow-wrap:anywhere]">{tf(lang, 'followBanner', { title: localTitle(target, lang) })}</p>
          <div className="flex items-center gap-2">
            <Link to={followHref(follow)} className="wb-control inline-flex items-center gap-1.5 rounded-lg bg-[var(--wb-accent)] px-4 font-semibold text-white hover:bg-[var(--wb-accent-hover)]">
              {t(lang, 'followGo')}<Icon name="arrowRight" className="h-4 w-4" />
            </Link>
            <button type="button" onClick={() => setDismissed(dismiss(dismissed, target.key))} aria-label={t(lang, 'followDismiss')}
              className="wb-control inline-grid min-w-11 place-items-center rounded-lg text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">
              <Icon name="close" className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
