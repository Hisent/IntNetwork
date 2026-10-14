import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { trainerApi, useIsAdmin } from '@/lib/trainerApi'
import { Section, QueryState } from './shared'

// --- Verwaltung: Einstellungen ------------------------------------------------

export function SettingsBlock() {
  const qc = useQueryClient()
  // Die Einstellungen gelten global für alle Kurse -> nur Admins dürfen schalten.
  const isAdmin = useIsAdmin()
  const features = useQuery({ queryKey: ['features'], queryFn: () => trainerApi.features().then((r) => r.data) })
  const toggle = useMutation({
    mutationFn: (v: boolean) => trainerApi.setFeature(v),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['features'] }),
  })
  return (
    <Section title="Einstellungen">
      <QueryState query={features}>
        <label className="flex items-center gap-2 text-sm text-[var(--wb-ink)]">
          <input type="checkbox" checked={features.data?.comments ?? false} disabled={!isAdmin || toggle.isPending}
            onChange={(e) => toggle.mutate(e.target.checked)} />
          Feedback-Kommentare für Teilnehmer aktiv
        </label>
        {!isAdmin && <p className="mt-2 text-xs text-[var(--wb-muted)]">Globale Einstellungen ändern nur Administratoren.</p>}
        {toggle.isError && <p role="alert" className="mt-2 text-sm text-rose-600">Speichern fehlgeschlagen.</p>}
      </QueryState>
    </Section>
  )
}
