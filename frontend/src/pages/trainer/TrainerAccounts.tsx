import { useRef, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { errMsg } from '@/lib/api'
import { trainerApi } from '@/lib/trainerApi'
import { ConfirmDialog } from '@/components/ConfirmDialog'
import { Icon } from '@/components/Icon'
import { Field, Section, QueryState } from './shared'

// --- Verwaltung: Trainer-Zugänge ---------------------------------------------

export function TrainerAccounts({ portalContainer }: { portalContainer: HTMLElement | null }) {
  const qc = useQueryClient()
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const accounts = useQuery({ queryKey: ['trainer-accounts'], queryFn: () => trainerApi.listTrainerAccounts().then((r) => r.data) })
  const create = useMutation({
    mutationFn: () => trainerApi.createTrainerAccount(email.trim(), name.trim(), password),
    onSuccess: () => { setEmail(''); setName(''); setPassword(''); setError(''); qc.invalidateQueries({ queryKey: ['trainer-accounts'] }) },
    onError: (e) => setError(errMsg(e)),
  })
  const remove = useMutation({
    mutationFn: (id: number) => trainerApi.deleteTrainerAccount(id),
    onSuccess: () => { setError(''); qc.invalidateQueries({ queryKey: ['trainer-accounts'] }) },
    onError: (e) => setError(errMsg(e)),
  })
  // Gleiches Sicherheitsniveau wie beim Teilnehmer-Löschen weiter oben in
  // dieser Datei: ein Trainer-Zugang ist der eigene Login-Zugriff, nicht nur
  // ein Datensatz — sofortiges Löschen per Klick (ohne Rückfrage) hätte hier
  // ein höheres Risiko als beim Teilnehmer. Derselbe ConfirmDialog statt
  // eines zweiten, damit sich beide Löschwege gleich anfühlen.
  const [deleteTarget, setDeleteTarget] = useState<{ id: number; name: string } | null>(null)
  const deleteTriggerRef = useRef<HTMLButtonElement | null>(null)
  return (
    <Section title="Trainer-Zugänge">
      <QueryState query={accounts} empty={accounts.data?.length === 0}>
        <div className="mb-3 flex flex-col gap-1.5">
          {accounts.data?.map((t) => (
            <div key={t.id} className="flex items-center justify-between text-sm">
              <span className="text-[var(--wb-ink)]">{t.name} <span className="text-[var(--wb-muted)]">({t.email})</span></span>
              <button
                onClick={(e) => { deleteTriggerRef.current = e.currentTarget; setDeleteTarget({ id: t.id, name: t.name }) }}
                aria-label={`${t.name} entfernen`} className="text-rose-600 hover:text-rose-700"><Icon name="trash" className="h-4 w-4" /></button>
            </div>
          ))}
        </div>
      </QueryState>
      <form onSubmit={(e) => { e.preventDefault(); if (email.trim() && name.trim() && password) create.mutate() }} className="flex flex-wrap items-end gap-2">
        <Field label="E-Mail" type="email" autoComplete="off" placeholder="neu@beispiel.de" value={email} onChange={(e) => setEmail(e.target.value)} />
        <Field label="Name" placeholder="Vorname" value={name} onChange={(e) => setName(e.target.value)} />
        <Field label="Passwort" type="password" autoComplete="new-password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button disabled={!email.trim() || !name.trim() || !password || create.isPending}
          className="wb-control inline-flex items-center gap-1 rounded-lg bg-[var(--wb-accent)] px-3 text-sm font-medium text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50">
          <Icon name="plus" className="h-4 w-4" /> Trainer
        </button>
      </form>
      {error && <p className="mt-1 text-sm text-rose-600">{error}</p>}
      <ConfirmDialog
        open={deleteTarget !== null}
        title="Trainer-Zugang entfernen"
        description={<>Zugang von „{deleteTarget?.name}“ endgültig entfernen? Die Person kann sich danach nicht mehr anmelden.</>}
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
