import { useRef, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { errMsg } from '@/lib/api'
import { trainerApi } from '@/lib/trainerApi'
import { isPasskeyCancelled, registerPasskey } from '@/lib/passkey'
import { ConfirmDialog } from '@/components/ConfirmDialog'
import { Icon } from '@/components/Icon'
import { Field, Section, QueryState } from './shared'

// --- Verwaltung: Passkeys ------------------------------------------------------

export function PasskeyAdmin({ portalContainer }: { portalContainer: HTMLElement | null }) {
  const qc = useQueryClient()
  const status = useQuery({ queryKey: ['passkey-status'], queryFn: () => trainerApi.passkeyStatus().then((r) => r.data) })
  // Liste nur abfragen, wenn die Funktion serverseitig überhaupt aktiv ist —
  // sonst antwortet /trainer/passkey mit 503 statt einer leeren Liste.
  const passkeys = useQuery({
    queryKey: ['passkeys'],
    queryFn: () => trainerApi.listPasskeys().then((r) => r.data),
    enabled: status.data?.enabled === true,
  })
  const [label, setLabel] = useState('')
  const [error, setError] = useState('')
  const [registering, setRegistering] = useState(false)
  const remove = useMutation({
    mutationFn: (id: string) => trainerApi.deletePasskey(id),
    onSuccess: () => { setError(''); qc.invalidateQueries({ queryKey: ['passkeys'] }) },
    onError: (e) => setError(errMsg(e)),
  })
  // Gleiches Muster wie beim Teilnehmer-/Trainer-Löschen weiter oben: ein
  // Passkey ist ein eigenständiger Anmeldeweg, kein einfacher Datensatz —
  // Entfernen fragt über denselben ConfirmDialog nach.
  const [deleteTarget, setDeleteTarget] = useState<{ id: string; label: string } | null>(null)
  const deleteTriggerRef = useRef<HTMLButtonElement | null>(null)

  async function addPasskey(event: React.FormEvent) {
    event.preventDefault()
    if (registering) return
    setError(''); setRegistering(true)
    try {
      // Ohne Bezeichnung ablehnen wäre unnötige Reibung — "Passkey" ist ein
      // sinnvoller Standard, den man später umbenennen könnte, gäbe es dafür
      // einen Endpunkt (aktuell nicht Teil des Vertrags).
      await registerPasskey(label.trim() || 'Passkey')
      setLabel('')
      qc.invalidateQueries({ queryKey: ['passkeys'] })
    } catch (e) {
      if (!isPasskeyCancelled(e)) setError(errMsg(e, 'Registrierung fehlgeschlagen.'))
    } finally {
      setRegistering(false)
    }
  }

  return (
    <Section title="Passkeys">
      <p className="mb-3 text-xs text-[var(--wb-muted)]">
        Passkeys sind an diese Adresse gebunden — zieht die Instanz auf eine andere Domain um, müssen sie neu angelegt werden.
      </p>
      {!status.isLoading && !status.data?.enabled ? (
        <p className="text-sm text-[var(--wb-muted)]">Passkey-Anmeldung ist auf dieser Instanz nicht eingerichtet.</p>
      ) : (
        <>
          <QueryState query={passkeys} empty={passkeys.data?.length === 0}>
            <ul className="mb-3 flex flex-col gap-1.5">
              {passkeys.data?.map((p) => (
                <li key={p.id} className="flex items-center justify-between gap-2 text-sm">
                  <span className="min-w-0 truncate text-[var(--wb-ink)]">
                    {p.label}
                    <span className="ml-2 text-xs text-[var(--wb-muted)]">
                      angelegt {new Date(p.created_at).toLocaleDateString('de-DE')}
                      {' · '}
                      {p.last_used_at ? `zuletzt genutzt ${new Date(p.last_used_at).toLocaleDateString('de-DE')}` : 'noch nicht genutzt'}
                    </span>
                  </span>
                  <button
                    onClick={(e) => { deleteTriggerRef.current = e.currentTarget; setDeleteTarget({ id: p.id, label: p.label }) }}
                    aria-label={`Passkey „${p.label}“ entfernen`} className="shrink-0 text-rose-600 hover:text-rose-700"><Icon name="trash" className="h-4 w-4" /></button>
                </li>
              ))}
            </ul>
          </QueryState>
          <form onSubmit={addPasskey} className="flex flex-wrap items-end gap-2">
            <Field label="Bezeichnung" placeholder="Notebook" value={label} onChange={(e) => setLabel(e.target.value)} disabled={registering} />
            <button disabled={registering}
              className="wb-control inline-flex items-center gap-1 rounded-lg bg-[var(--wb-accent)] px-3 text-sm font-medium text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50">
              <Icon name="plus" className="h-4 w-4" /> {registering ? 'Registriert…' : 'Passkey hinzufügen'}
            </button>
          </form>
        </>
      )}
      {error && <p aria-live="polite" className="mt-2 text-sm text-rose-600">{error}</p>}
      <ConfirmDialog
        open={deleteTarget !== null}
        title="Passkey entfernen"
        description={<>Passkey „{deleteTarget?.label}“ endgültig entfernen? Danach bleiben nur noch das Passwort und die übrigen Passkeys zur Anmeldung.</>}
        confirmLabel="Endgültig entfernen"
        cancelLabel="Abbrechen"
        triggerRef={deleteTriggerRef}
        container={portalContainer}
        onConfirm={() => { if (deleteTarget) remove.mutate(deleteTarget.id); setDeleteTarget(null) }}
        onCancel={() => setDeleteTarget(null)}
      />
    </Section>
  )
}
