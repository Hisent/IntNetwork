import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { t, tf, type Lang } from '@/lib/i18n'
import { Icon } from '@/components/Icon'
import { WorkbenchSectionTitle } from '@/components/workbench/WorkbenchShell'

// Wiederholung (spaced review, backend/app/services/review.py): Karte auf der Lernseite
// und Hinweis auf eine Aufwärmrunde des Trainers. Beide lesen denselben Status, der
// wie die Live-Abstimmung gepollt wird (ruht bei verstecktem Tab).
const REVIEW_LINK = '/lernen/ueben?modus=wiederholen'

function useReviewStatus() {
  return useQuery({ queryKey: ['review-status'], queryFn: () => learnApi.reviewStatus().then((r) => r.data), refetchInterval: 15_000, retry: false })
}

/** „Wiederholen“-Karte: wie viele Fragen fällig sind, Link zum persönlichen Satz. */
export function ReviewCard({ lang, className = '' }: { lang: Lang; className?: string }) {
  const { data } = useReviewStatus()
  if (!data) return null
  const text = data.candidates === 0 ? t(lang, 'reviewNone')
    : data.due === 0 ? t(lang, 'reviewNothingDue')
      : data.due === 1 ? t(lang, 'reviewDueOne') : tf(lang, 'reviewDueMany', { n: data.due })
  return (
    <section className={`wb-surface p-5 ${className}`} data-testid="review-card">
      <WorkbenchSectionTitle meta={data.due > 0 ? String(data.due) : undefined}>{t(lang, 'reviewTitle')}</WorkbenchSectionTitle>
      <p className="text-sm leading-relaxed text-[var(--wb-muted)]">{text}</p>
      {data.due > 0 && (
        <Link to={REVIEW_LINK} className="wb-control mt-3 inline-flex items-center gap-1.5 rounded-lg bg-[var(--wb-accent)] px-4 text-sm font-semibold text-white hover:bg-[var(--wb-accent-hover)]">
          {t(lang, 'reviewNow')}<Icon name="arrowRight" className="h-4 w-4" />
        </Link>
      )}
    </section>
  )
}

const DISMISSED = 'intnetwork-warmup-dismissed'

/** Nicht-blockierender Hinweis, solange der Trainer eine Aufwärmrunde laufen hat und
 *  der Teilnehmer darin noch nichts beantwortet bzw. ihn nicht weggeklickt hat. */
export function ReviewWarmupBanner({ lang }: { lang: Lang }) {
  const { data } = useReviewStatus()
  const [dismissed, setDismissed] = useState(() => { try { return localStorage.getItem(DISMISSED) } catch { return null } })
  const warmup = data?.warmup
  if (!warmup || warmup.answered > 0 || dismissed === String(warmup.id)) return null
  const dismiss = () => {
    setDismissed(String(warmup.id))
    try { localStorage.setItem(DISMISSED, String(warmup.id)) } catch { /* nur für diese Sitzung */ }
  }
  return (
    <div role="status" className="wb-surface mb-5 flex flex-wrap items-center gap-3 border-[var(--wb-accent)] bg-[var(--wb-accent-soft)] p-4 text-sm print:hidden">
      <Icon name="lightbulb" className="h-5 w-5 shrink-0 text-[var(--wb-accent)]" />
      <p className="min-w-0 flex-1 text-[var(--wb-ink)]">
        <span className="font-semibold">{t(lang, 'warmupLabel')}</span>
        {data.due > 0 ? tf(lang, 'warmupDue', { n: data.due }) : t(lang, 'warmupNothingDue')}
      </p>
      {data.due > 0 && (
        <Link to={REVIEW_LINK} className="wb-control inline-flex items-center gap-1.5 rounded-lg bg-[var(--wb-accent)] px-4 font-semibold text-white hover:bg-[var(--wb-accent-hover)]">
          {t(lang, 'warmupGo')}<Icon name="arrowRight" className="h-4 w-4" />
        </Link>
      )}
      <button type="button" onClick={dismiss} aria-label={t(lang, 'followDismiss')}
        className="wb-control grid place-items-center rounded-lg px-2 text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">
        <Icon name="close" className="h-4 w-4" />
      </button>
    </div>
  )
}
