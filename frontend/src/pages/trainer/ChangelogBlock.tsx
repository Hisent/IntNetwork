import { useQuery } from '@tanstack/react-query'
import { trainerApi } from '@/lib/trainerApi'
import { useTr } from '@/store/lang'
import { Section, QueryState } from './shared'

// --- Verwaltung: Changelog -----------------------------------------------------
// Englisch ab v1.40.0 (title_en/text_en), ältere Einträge nur deutsch.

export function ChangelogBlock() {
  const { lang, tr } = useTr()
  const changelog = useQuery({ queryKey: ['changelog'], queryFn: () => trainerApi.changelog().then((r) => r.data) })
  return (
    <Section title={tr('trChangelog')}>
      <QueryState query={changelog} empty={changelog.data?.length === 0}>
        <details>
          <summary className="wb-control cursor-pointer select-none text-sm text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">{tr('trShowEntries', { n: changelog.data?.length ?? 0 })}</summary>
          <ul className="mt-3 flex max-h-96 flex-col divide-y divide-[var(--wb-border)] overflow-y-auto">
            {changelog.data?.map((e, i) => (
              <li key={i} className="py-2">
                <div className="flex items-baseline justify-between gap-2">
                  <span className="text-sm font-medium text-[var(--wb-ink)]">{(lang === 'en' && e.title_en) || e.title}</span>
                  <span className="shrink-0 text-xs text-[var(--wb-muted)]">{e.date}</span>
                </div>
                <p className="mt-1 text-sm text-[var(--wb-muted)]">{(lang === 'en' && e.text_en) || e.text}</p>
              </li>
            ))}
          </ul>
        </details>
      </QueryState>
    </Section>
  )
}
