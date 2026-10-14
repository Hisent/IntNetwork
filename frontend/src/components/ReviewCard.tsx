import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import type { Lang } from '@/lib/i18n'
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
  const de = lang === 'de'
  if (!data) return null
  const text = data.candidates === 0
    ? (de ? 'Sobald du ein Modul bestanden hast, kommen seine Fragen ein paar Stunden später hier zur Wiederholung — verteilt über die Tage.'
      : 'A few hours after you pass a module, its questions come back here for review — spread out over the days.')
    : data.due === 0
      ? (de ? 'Gerade ist nichts fällig. Schau später wieder vorbei.' : 'Nothing is due right now. Check back later.')
      : (de ? `${data.due} ${data.due === 1 ? 'Frage ist' : 'Fragen sind'} zur Wiederholung fällig.`
        : `${data.due} ${data.due === 1 ? 'question is' : 'questions are'} due for review.`)
  return (
    <section className={`wb-surface p-5 ${className}`} data-testid="review-card">
      <WorkbenchSectionTitle meta={data.due > 0 ? String(data.due) : undefined}>{de ? 'Wiederholen' : 'Review'}</WorkbenchSectionTitle>
      <p className="text-sm leading-relaxed text-[var(--wb-muted)]">{text}</p>
      {data.due > 0 && (
        <Link to={REVIEW_LINK} className="wb-control mt-3 inline-flex items-center gap-1.5 rounded-lg bg-[var(--wb-accent)] px-4 text-sm font-semibold text-white hover:bg-[var(--wb-accent-hover)]">
          {de ? 'Jetzt wiederholen' : 'Review now'}<Icon name="arrowRight" className="h-4 w-4" />
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
  const de = lang === 'de'
  const dismiss = () => {
    setDismissed(String(warmup.id))
    try { localStorage.setItem(DISMISSED, String(warmup.id)) } catch { /* nur für diese Sitzung */ }
  }
  return (
    <div role="status" className="wb-surface mb-5 flex flex-wrap items-center gap-3 border-[var(--wb-accent)] bg-[var(--wb-accent-soft)] p-4 text-sm print:hidden">
      <Icon name="lightbulb" className="h-5 w-5 shrink-0 text-[var(--wb-accent)]" />
      <p className="min-w-0 flex-1 text-[var(--wb-ink)]">
        <span className="font-semibold">{de ? 'Aufwärmrunde: ' : 'Warm-up: '}</span>
        {data.due > 0
          ? (de ? `Dein Trainer hat eine Wiederholung gestartet — ${data.due} Fragen warten auf dich.` : `Your trainer started a review round — ${data.due} questions are waiting for you.`)
          : (de ? 'Dein Trainer hat eine Wiederholung gestartet. Für dich ist gerade nichts fällig.' : 'Your trainer started a review round. Nothing is due for you right now.')}
      </p>
      {data.due > 0 && (
        <Link to={REVIEW_LINK} className="wb-control inline-flex items-center gap-1.5 rounded-lg bg-[var(--wb-accent)] px-4 font-semibold text-white hover:bg-[var(--wb-accent-hover)]">
          {de ? 'Los geht’s' : 'Start'}<Icon name="arrowRight" className="h-4 w-4" />
        </Link>
      )}
      <button type="button" onClick={dismiss} aria-label={de ? 'Hinweis ausblenden' : 'Dismiss notice'}
        className="wb-control grid place-items-center rounded-lg px-2 text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">
        <Icon name="close" className="h-4 w-4" />
      </button>
    </div>
  )
}
