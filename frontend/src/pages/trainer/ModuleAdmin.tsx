import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { errMsg } from '@/lib/api'
import { trainerApi, useIsAdmin } from '@/lib/trainerApi'
import { Icon } from '@/components/Icon'
import { groupModulesByWorkshop } from '@/lib/trainerModules'
import { useTr } from '@/store/lang'
import { Field, Section, QueryState } from './shared'

// --- Verwaltung: Module -------------------------------------------------------

type AdminWorkshop = { key: string; title: Record<'de' | 'en', string>; status?: 'draft' | 'published'; owner_name?: string | null; editable?: boolean }

export function ModuleAdmin({ workshops }: { workshops: AdminWorkshop[] }) {
  const { lang, tr } = useTr()
  const qc = useQueryClient()
  const navigate = useNavigate()
  const isAdmin = useIsAdmin()
  // nicht editierbar: fremde Entwürfe und (für Nicht-Admins) ausgelieferte Workshops — Server lehnt Speichern mit 403 ab
  const readOnly = new Set(workshops.filter((w) => w.editable === false).map((w) => w.key))
  const drafts = workshops.filter((w) => w.status === 'draft')
  const publish = useMutation({
    mutationFn: (key: string) => trainerApi.publishWorkshop(key),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['trainer-workshops'] }),
  })
  const [newKey, setNewKey] = useState('')
  const [newTitle, setNewTitle] = useState('')
  const [moduleWorkshopKey, setModuleWorkshopKey] = useState('network')
  const [filter, setFilter] = useState('')
  // Welche Workshop-Gruppen der Nutzer manuell aufgeklappt hat (Key der
  // Gruppe). Start: leer, also alle Gruppen zu.
  const [openGroups, setOpenGroups] = useState<Set<string>>(new Set())
  const presentMods = useQuery({ queryKey: ['trainer-modules'], queryFn: () => trainerApi.trainerModules().then((r) => r.data) })
  const createContent = useMutation({
    mutationFn: () => trainerApi.createContentModule(newKey.trim(), newTitle.trim(), moduleWorkshopKey),
    onSuccess: (r) => {
      setNewKey(''); setNewTitle('')
      qc.invalidateQueries({ queryKey: ['trainer-modules'] })
      navigate(`/trainer/modul/${r.data.key}/bearbeiten`)
    },
  })
  // Bei ~35 Modulen über zwei Workshops verteilt skaliert eine flache Pill-Wand
  // nicht mehr — daher Gruppierung nach Workshop plus Titel-Filter.
  const needle = filter.trim().toLowerCase()
  const filtered = presentMods.data?.filter((m) => m.title.toLowerCase().includes(needle)) ?? []
  const groups = groupModulesByWorkshop(filtered, workshops)
  // Gruppen sind <details>: standardmäßig zu (spart Tab-Stopps auf dem Weg zu
  // den Karten darunter — bei ~35 Zeilen mit je zwei fokussierbaren Elementen
  // macht das den Unterschied zwischen ~70 und wenigen Tabs). Sobald gesucht
  // wird, klappen Treffergruppen automatisch auf, damit der Filter sofort
  // etwas zeigt; manuelles Auf-/Zuklappen bleibt über openGroups erhalten.
  const isGroupOpen = (key: string) => needle !== '' || openGroups.has(key)
  return (
    <Section title={tr('trModulesTitle')}>
      <label className="mb-3 flex max-w-xs flex-col gap-1 text-xs font-medium text-[var(--wb-muted)]">
        {tr('trFindModule')}
        <input value={filter} onChange={(e) => setFilter(e.target.value)} placeholder={tr('trFilterTitlePh')}
          className="wb-control rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-3 py-2 text-sm font-normal text-[var(--wb-ink)]" />
      </label>
      {drafts.length > 0 && (
        <ul aria-label={tr('trDraftWorkshops')} className="mb-3 flex flex-col divide-y divide-[var(--wb-border)] rounded-lg border border-[var(--wb-border)] px-3">
          {drafts.map((w) => (
            <li key={w.key} className="flex items-center justify-between gap-2 py-1.5 text-sm">
              <span className="min-w-0 truncate text-[var(--wb-ink)]">
                {w.title[lang]}
                <span className="ml-2 rounded bg-amber-100 px-1.5 py-0.5 text-xs font-medium text-amber-800">{tr('trDraft')}</span>
                {w.owner_name && <span className="ml-2 text-xs text-[var(--wb-muted)]">{tr('trOwnedBy', { name: w.owner_name })}</span>}
              </span>
              {isAdmin && (
                <button onClick={() => publish.mutate(w.key)} disabled={publish.isPending}
                  className="wb-control shrink-0 rounded-lg bg-[var(--wb-accent)] px-3 text-xs font-medium text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50">{tr('trPublish')}</button>
              )}
            </li>
          ))}
        </ul>
      )}
      {publish.isError && <p className="mb-2 text-sm text-rose-600">{errMsg(publish.error, tr('trPublishFailed'))}</p>}
      <QueryState query={presentMods} empty={presentMods.data?.length === 0}>
        {filtered.length === 0
          ? <p className="text-sm text-[var(--wb-muted)]">{tr('trNoModulesFound')}</p>
          : <div className="flex flex-col gap-2">
              {groups.map((g) => (
                <details key={g.key} className="group" open={isGroupOpen(g.key)}
                  onToggle={(e) => {
                    const isOpen = e.currentTarget.open
                    setOpenGroups((prev) => {
                      const next = new Set(prev)
                      if (isOpen) next.add(g.key); else next.delete(g.key)
                      return next
                    })
                  }}>
                  {/* Label allein hätte hier über den Zustand gelogen (bleibt
                      als reiner Gruppentitel korrekt, aber ohne jede
                      Rückmeldung ob auf-/zugeklappt). Pfeil dreht sich rein
                      über CSS (group-open:), NICHT über ein kontrolliertes
                      open-Prop — sonst würde ein Tastendruck im Suchfeld
                      (das isGroupOpen()/open oben steuert) den Pfeil aus dem
                      Tritt bringen, während <details> selbst uncontrolled
                      bleiben muss (siehe onToggle-Kommentar in ModuleAdmin). */}
                  <summary className="wb-control flex cursor-pointer select-none items-center gap-2 rounded-lg px-1 text-xs font-semibold uppercase tracking-wide text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">
                    <Icon name="arrowRight" className="h-3.5 w-3.5 shrink-0 transition-transform duration-150 group-open:rotate-90" />
                    {g.title} <span className="font-normal normal-case tracking-normal">({g.modules.length})</span>
                  </summary>
                  <ul className="flex flex-col divide-y divide-[var(--wb-border)]">
                    {g.modules.map((m) => (
                      <li key={m.key} className="flex items-center justify-between gap-2 py-1.5">
                        <Link to={`/trainer/modul/${m.key}`} title={m.title} className="min-w-0 truncate text-sm text-[var(--wb-ink)] hover:text-[var(--wb-accent-hover)] hover:underline">{m.title}</Link>
                        {!(m.workshop_key && readOnly.has(m.workshop_key)) && <Link to={`/trainer/modul/${m.key}/bearbeiten`} title={tr('trEdit')} aria-label={tr('trEditModuleAria', { title: m.title })}
                          className="shrink-0 rounded-lg p-1.5 text-[var(--wb-muted)] hover:bg-[var(--wb-subtle)] hover:text-[var(--wb-ink)]"><Icon name="pencil" className="h-4 w-4" /></Link>}
                      </li>
                    ))}
                  </ul>
                </details>
              ))}
            </div>}
      </QueryState>
      <form onSubmit={(e) => { e.preventDefault(); if (newKey.trim() && newTitle.trim()) createContent.mutate() }} className="mt-4 flex flex-wrap items-end gap-2">
        <Field label="Key" placeholder={tr('trModuleKeyPh')} value={newKey} onChange={(e) => setNewKey(e.target.value)} />
        <Field label={tr('trTitleDe')} placeholder={tr('trModuleTitlePh')} value={newTitle} onChange={(e) => setNewTitle(e.target.value)} />
        <label className="flex flex-col gap-1 text-xs font-medium text-[var(--wb-muted)]">{tr('trWorkshop')}
          <select value={moduleWorkshopKey} onChange={(e) => setModuleWorkshopKey(e.target.value)} className="wb-control rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-3 py-2 text-sm font-normal text-[var(--wb-ink)]">
            {workshops.map((w) => <option key={w.key} value={w.key}>{w.title[lang]}{w.status === 'draft' ? tr('trDraftSuffix') : ''}</option>)}
          </select>
        </label>
        <button disabled={!newKey.trim() || !newTitle.trim() || createContent.isPending}
          className="wb-control inline-flex items-center gap-1 rounded-lg bg-[var(--wb-accent)] px-3 text-sm font-medium text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50">
          <Icon name="plus" className="h-4 w-4" /> {tr('trNewModule')}
        </button>
      </form>
      {createContent.isError && <p className="mt-1 text-sm text-rose-600">{tr('trCreateModuleFailed')}</p>}
    </Section>
  )
}
