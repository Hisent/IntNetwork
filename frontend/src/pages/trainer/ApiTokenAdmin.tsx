import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { errMsg } from '@/lib/api'
import { trainerApi } from '@/lib/trainerApi'
import { Icon } from '@/components/Icon'
import { localeOf } from '@/lib/i18n'
import { useTr } from '@/store/lang'
import { Field, Section, QueryState } from './shared'

// --- Verwaltung: API-Tokens (MCP) ---------------------------------------------

export function ApiTokenAdmin() {
  const { lang, tr } = useTr()
  const qc = useQueryClient()
  const tokens = useQuery({ queryKey: ['api-tokens'], queryFn: () => trainerApi.apiTokens().then((r) => r.data) })
  const [name, setName] = useState('')
  const [error, setError] = useState('')
  // Klartext-Token nur im State: weg beim Schließen, nie nachladbar.
  const [created, setCreated] = useState<{ name: string; token: string } | null>(null)
  const create = useMutation({
    mutationFn: () => trainerApi.createApiToken(name.trim()).then((r) => r.data),
    onSuccess: (t) => {
      setName(''); setError(''); setCreated({ name: t.name, token: t.token })
      qc.invalidateQueries({ queryKey: ['api-tokens'] })
    },
    onError: (e) => setError(errMsg(e, tr('trErrorFallback'))),
  })
  const remove = useMutation({
    mutationFn: (id: number) => trainerApi.deleteApiToken(id),
    onSuccess: () => { setError(''); qc.invalidateQueries({ queryKey: ['api-tokens'] }) },
    onError: (e) => setError(errMsg(e, tr('trErrorFallback'))),
  })
  const command = created
    ? `claude mcp add --transport http lehrgang ${window.location.origin}/api/mcp --header "Authorization: Bearer ${created.token}"`
    : ''

  return (
    <Section title={tr('trApiTokens')}>
      <p className="mb-3 text-xs text-[var(--wb-muted)]">{tr('trApiTokensNote')}</p>
      <QueryState query={tokens} empty={tokens.data?.length === 0}>
        <ul className="mb-3 flex flex-col gap-1.5">
          {tokens.data?.map((t) => (
            <li key={t.id} className="flex items-center justify-between gap-2 text-sm">
              <span className="min-w-0 truncate text-[var(--wb-ink)]">
                {t.name} <span className="font-mono text-xs text-[var(--wb-muted)]">{t.prefix}…</span>
                <span className="ml-2 text-xs text-[var(--wb-muted)]">
                  {tr('trCreatedOn', { date: new Date(t.created_at).toLocaleDateString(localeOf(lang)) })}
                  {' · '}
                  {t.last_used_at ? tr('trLastUsed', { date: new Date(t.last_used_at).toLocaleDateString(localeOf(lang)) }) : tr('trNeverUsed')}
                </span>
              </span>
              <button onClick={() => remove.mutate(t.id)} aria-label={tr('trRevokeTokenAria', { name: t.name })}
                className="shrink-0 text-rose-600 hover:text-rose-700"><Icon name="trash" className="h-4 w-4" /></button>
            </li>
          ))}
        </ul>
      </QueryState>
      <form onSubmit={(e) => { e.preventDefault(); if (name.trim() && !create.isPending) create.mutate() }} className="flex flex-wrap items-end gap-2">
        <Field label={tr('trTokenName')} placeholder={tr('trTokenNamePh')} maxLength={60} value={name} onChange={(e) => setName(e.target.value)} />
        <button disabled={!name.trim() || create.isPending}
          className="wb-control inline-flex items-center gap-1 rounded-lg bg-[var(--wb-accent)] px-3 text-sm font-medium text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50">
          <Icon name="plus" className="h-4 w-4" /> {tr('trCreateToken')}
        </button>
      </form>
      {created && (
        <div role="status" className="mt-3 rounded-lg border border-[var(--wb-border)] bg-[var(--wb-subtle)] p-3 text-sm">
          <p className="font-medium text-[var(--wb-ink)]">{tr('trTokenCreated', { name: created.name })}</p>
          <p className="mb-2 text-xs font-semibold text-rose-600">{tr('trTokenShownOnce')}</p>
          <input readOnly value={created.token} aria-label={tr('trApiTokens')} onFocus={(e) => e.currentTarget.select()}
            className="wb-control mb-2 w-full rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-3 py-2 font-mono text-xs text-[var(--wb-ink)]" />
          <p className="mb-1 text-xs text-[var(--wb-muted)]">{tr('trTokenCommandHint')}</p>
          <code className="mb-2 block break-all rounded-lg bg-[var(--wb-surface)] p-2 font-mono text-xs text-[var(--wb-ink)]">{command}</code>
          <button type="button" onClick={() => setCreated(null)}
            className="wb-control rounded-lg border border-[var(--wb-border)] px-3 text-sm text-[var(--wb-ink)] hover:bg-[var(--wb-surface)]">{tr('trClose')}</button>
        </div>
      )}
      {error && <p aria-live="polite" className="mt-2 text-sm text-rose-600">{error}</p>}
    </Section>
  )
}
