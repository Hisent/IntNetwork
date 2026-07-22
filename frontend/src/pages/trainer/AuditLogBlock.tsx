import { useEffect, useState } from 'react'
import { trainerApi, type AuditLogEntry } from '@/lib/trainerApi'
import { useQuery } from '@tanstack/react-query'
import { Section, QueryState } from './shared'

// --- Verwaltung: Audit-Protokoll ----------------------------------------------

const AUDIT_PAGE_SIZE = 50

export function AuditLogBlock() {
  // Nachschlagewerk statt Analysewerkzeug: erste Seite laden, weitere Seiten
  // nur auf Anfrage per Button nachladen — kein Filter/Suchfeld, der
  // Backend-Endpunkt unterstützt limit/offset bereits (siehe trainer_audit.py).
  const first = useQuery({
    queryKey: ['audit-log', 'first'],
    queryFn: () => trainerApi.auditLog(AUDIT_PAGE_SIZE, 0).then((r) => r.data),
  })
  const [entries, setEntries] = useState<AuditLogEntry[]>([])
  const [hasMore, setHasMore] = useState(false)
  const [loadingMore, setLoadingMore] = useState(false)

  useEffect(() => {
    if (first.data) {
      setEntries(first.data)
      setHasMore(first.data.length === AUDIT_PAGE_SIZE)
    }
  }, [first.data])

  async function loadMore() {
    setLoadingMore(true)
    try {
      const next = await trainerApi.auditLog(AUDIT_PAGE_SIZE, entries.length).then((r) => r.data)
      setEntries((prev) => [...prev, ...next])
      setHasMore(next.length === AUDIT_PAGE_SIZE)
    } finally {
      setLoadingMore(false)
    }
  }

  return (
    <Section title="Protokoll" className="opacity-90">
      <QueryState query={first} empty={first.isSuccess && entries.length === 0}>
        <details>
          <summary className="wb-control cursor-pointer select-none text-sm text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">
            {entries.length}{hasMore ? '+' : ''} Aktionen anzeigen
          </summary>
          <ul className="mt-3 flex max-h-96 flex-col divide-y divide-[var(--wb-border)] overflow-y-auto" aria-live="polite">
            {entries.map((e) => (
              <li key={e.id} className="py-2 text-sm">
                <div className="flex items-baseline justify-between gap-2">
                  <span className="font-medium text-[var(--wb-ink)]">{e.action}</span>
                  <span className="shrink-0 text-xs text-[var(--wb-muted)]">{new Date(e.created_at).toLocaleString('de-DE')}</span>
                </div>
                <p className="mt-1 text-[var(--wb-muted)]">
                  {e.trainer_email}
                  {e.target ? <> · {e.target}</> : null}
                  {e.detail ? <> · {e.detail}</> : null}
                </p>
              </li>
            ))}
          </ul>
          {hasMore && (
            <button onClick={loadMore} disabled={loadingMore}
              className="mt-2 text-xs font-medium text-[var(--wb-accent)] hover:underline disabled:opacity-50">
              {loadingMore ? 'Lädt…' : 'Weitere laden'}
            </button>
          )}
        </details>
      </QueryState>
    </Section>
  )
}
