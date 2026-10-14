import { useRef, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { errMsg } from '@/lib/api'
import { trainerAccountsQuery as accountsQuery, trainerApi, useIsAdmin, type TrainerAccount } from '@/lib/trainerApi'
import { ConfirmDialog } from '@/components/ConfirmDialog'
import { Icon } from '@/components/Icon'
import { useTr } from '@/store/lang'
import { Field, Section, QueryState } from './shared'

// --- Verwaltung: Trainer-Zugänge ---------------------------------------------

export function TrainerAccounts({ portalContainer }: { portalContainer: HTMLElement | null }) {
  const { tr } = useTr()
  const qc = useQueryClient()
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const accounts = useQuery(accountsQuery)
  const isAdmin = useIsAdmin()
  const create = useMutation({
    mutationFn: () => trainerApi.createTrainerAccount(email.trim(), name.trim(), password),
    onSuccess: () => { setEmail(''); setName(''); setPassword(''); setError(''); qc.invalidateQueries({ queryKey: ['trainer-accounts'] }) },
    onError: (e) => setError(errMsg(e, tr('trErrorFallback'))),
  })
  const remove = useMutation({
    mutationFn: (id: number) => trainerApi.deleteTrainerAccount(id),
    onSuccess: () => { setError(''); qc.invalidateQueries({ queryKey: ['trainer-accounts'] }) },
    onError: (e) => setError(errMsg(e, tr('trErrorFallback'))),
  })
  const setRole = useMutation({
    mutationFn: ({ id, role }: { id: number; role: TrainerAccount['role'] }) => trainerApi.setTrainerRole(id, role),
    onSuccess: () => { setError(''); qc.invalidateQueries({ queryKey: ['trainer-accounts'] }) },
    onError: (e) => setError(errMsg(e, tr('trErrorFallback'))),
  })
  // Gleiches Sicherheitsniveau wie beim Teilnehmer-Löschen weiter oben in
  // dieser Datei: ein Trainer-Zugang ist der eigene Login-Zugriff, nicht nur
  // ein Datensatz — sofortiges Löschen per Klick (ohne Rückfrage) hätte hier
  // ein höheres Risiko als beim Teilnehmer. Derselbe ConfirmDialog statt
  // eines zweiten, damit sich beide Löschwege gleich anfühlen.
  const [deleteTarget, setDeleteTarget] = useState<{ id: number; name: string } | null>(null)
  const deleteTriggerRef = useRef<HTMLButtonElement | null>(null)
  return (
    <Section title={tr('trTrainerAccounts')}>
      <QueryState query={accounts} empty={accounts.data?.length === 0}>
        <div className="mb-3 flex flex-col gap-1.5">
          {accounts.data?.map((t) => (
            <div key={t.id} className="flex items-center justify-between gap-2 text-sm">
              <span className="text-[var(--wb-ink)]">{t.name} <span className="text-[var(--wb-muted)]">({t.email})</span>{t.is_self && <span className="text-[var(--wb-muted)]">{tr('trYouSuffix')}</span>}</span>
              <span className="flex items-center gap-2">
                {isAdmin ? (
                  <select value={t.role} disabled={setRole.isPending} aria-label={tr('trRoleOfAria', { name: t.name })}
                    onChange={(e) => setRole.mutate({ id: t.id, role: e.target.value as TrainerAccount['role'] })}
                    className="wb-control rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-2 py-1 text-xs text-[var(--wb-ink)]">
                    <option value="trainer">Trainer</option>
                    <option value="admin">Admin</option>
                  </select>
                ) : (
                  <span className="text-xs text-[var(--wb-muted)]">{t.role === 'admin' ? 'Admin' : 'Trainer'}</span>
                )}
                {/* Eigener Zugang: der Server lehnt Selbst-Löschen ohnehin ab (Aussperren). */}
                {isAdmin && !t.is_self && (
                  <button
                    onClick={(e) => { deleteTriggerRef.current = e.currentTarget; setDeleteTarget({ id: t.id, name: t.name }) }}
                    aria-label={tr('trRemoveAria', { name: t.name })} className="text-rose-600 hover:text-rose-700"><Icon name="trash" className="h-4 w-4" /></button>
                )}
              </span>
            </div>
          ))}
        </div>
      </QueryState>
      {isAdmin ? (
        <form onSubmit={(e) => { e.preventDefault(); if (email.trim() && name.trim() && password) create.mutate() }} className="flex flex-wrap items-end gap-2">
          <Field label={tr('trEmail')} type="email" autoComplete="off" placeholder={tr('trNewEmailPh')} value={email} onChange={(e) => setEmail(e.target.value)} />
          <Field label={tr('trNameLabel')} placeholder={tr('trFirstNamePh')} value={name} onChange={(e) => setName(e.target.value)} />
          <Field label={tr('trPassword')} type="password" autoComplete="new-password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button disabled={!email.trim() || !name.trim() || !password || create.isPending}
            className="wb-control inline-flex items-center gap-1 rounded-lg bg-[var(--wb-accent)] px-3 text-sm font-medium text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50">
            <Icon name="plus" className="h-4 w-4" /> {tr('trAddTrainer')}
          </button>
        </form>
      ) : (
        accounts.isSuccess && <p className="text-xs text-[var(--wb-muted)]">{tr('trAdminsOnlyAccounts')}</p>
      )}
      {error && <p className="mt-1 text-sm text-rose-600">{error}</p>}
      <ConfirmDialog
        open={deleteTarget !== null}
        title={tr('trRemoveAccount')}
        description={<>{tr('trRemoveAccountDesc', { name: deleteTarget?.name ?? '' })}</>}
        confirmLabel={tr('trRemovePermanently')}
        triggerRef={deleteTriggerRef}
        container={portalContainer}
        onConfirm={() => { if (deleteTarget) remove.mutate(deleteTarget.id); setDeleteTarget(null) }}
        onCancel={() => setDeleteTarget(null)}
      />
    </Section>
  )
}
