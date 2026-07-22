import { useQuery } from '@tanstack/react-query'
import { trainerApi } from '@/lib/trainerApi'
import { Section, QueryState } from './shared'

// --- Verwaltung: Changelog -----------------------------------------------------

export function ChangelogBlock() {
  const changelog = useQuery({ queryKey: ['changelog'], queryFn: () => trainerApi.changelog().then((r) => r.data) })
  return (
    <Section title="Änderungslog" className="opacity-90">
      <QueryState query={changelog} empty={changelog.data?.length === 0}>
        <details>
          <summary className="wb-control cursor-pointer select-none text-sm text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">{changelog.data?.length ?? 0} Einträge anzeigen</summary>
          <ul className="mt-3 flex max-h-96 flex-col divide-y divide-[var(--wb-border)] overflow-y-auto">
            {changelog.data?.map((e, i) => (
              <li key={i} className="py-2">
                <div className="flex items-baseline justify-between gap-2">
                  <span className="text-sm font-medium text-[var(--wb-ink)]">{e.title}</span>
                  <span className="shrink-0 text-xs text-[var(--wb-muted)]">{e.date}</span>
                </div>
                <p className="mt-1 text-sm text-[var(--wb-muted)]">{e.text}</p>
              </li>
            ))}
          </ul>
        </details>
      </QueryState>
    </Section>
  )
}
