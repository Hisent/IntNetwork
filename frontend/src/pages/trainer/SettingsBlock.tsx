import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { trainerApi } from '@/lib/trainerApi'
import { Section, QueryState } from './shared'

// --- Verwaltung: Einstellungen ------------------------------------------------

export function SettingsBlock() {
  const qc = useQueryClient()
  const features = useQuery({ queryKey: ['features'], queryFn: () => trainerApi.features().then((r) => r.data) })
  const toggle = useMutation({
    mutationFn: (v: boolean) => trainerApi.setFeature(v),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['features'] }),
  })
  return (
    <Section title="Einstellungen">
      <QueryState query={features}>
        <label className="flex items-center gap-2 text-sm text-[var(--wb-ink)]">
          <input type="checkbox" checked={features.data?.comments ?? false} disabled={toggle.isPending}
            onChange={(e) => toggle.mutate(e.target.checked)} />
          Feedback-Kommentare für Teilnehmer aktiv
        </label>
      </QueryState>
    </Section>
  )
}
