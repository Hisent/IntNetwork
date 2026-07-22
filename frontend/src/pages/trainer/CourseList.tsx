import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { trainerApi, type Course } from '@/lib/trainerApi'
import { Icon } from '@/components/Icon'
import { CopyCode, Field, QueryState } from './shared'

// --- Kursliste (Master) -------------------------------------------------------

export function CourseList({ courses, workshops, workshopTitle, selected, onSelect }: {
  courses: ReturnType<typeof useQuery<Course[]>>
  workshops: { key: string; title: { de: string } }[]
  workshopTitle: (key: string | null) => string
  selected: number | null
  onSelect: (id: number) => void
}) {
  const qc = useQueryClient()
  const [name, setName] = useState('')
  const [workshopKey, setWorkshopKey] = useState('network')
  const create = useMutation({
    mutationFn: () => trainerApi.createCourse(name, workshopKey).then((r) => r.data),
    onSuccess: () => { setName(''); qc.invalidateQueries({ queryKey: ['courses'] }) },
  })

  return (
    <section className="wb-surface p-4 lg:sticky lg:top-6">
      <h3 className="mb-3 text-sm font-semibold text-[var(--wb-ink)]">Kurse</h3>
      <form onSubmit={(e) => { e.preventDefault(); if (name.trim()) create.mutate() }} className="mb-4 flex flex-col gap-2">
        <Field label="Neuer Kurs" placeholder="Kurs-Name" value={name} onChange={(e) => setName(e.target.value)} />
        <label className="flex flex-col gap-1 text-xs font-medium text-[var(--wb-muted)]">Workshop
          <select value={workshopKey} onChange={(e) => setWorkshopKey(e.target.value)} className="wb-control rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-3 py-2 text-sm font-normal text-[var(--wb-ink)]">
            {workshops.map((w) => <option key={w.key} value={w.key}>{w.title.de}</option>)}
          </select>
        </label>
        <button disabled={!name.trim() || create.isPending}
          className="wb-control inline-flex items-center justify-center gap-1 rounded-lg bg-[var(--wb-accent)] px-4 text-sm font-medium text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50">
          <Icon name="plus" className="h-4 w-4" /> Kurs anlegen
        </button>
        {create.isError && <p className="text-xs text-rose-600">Anlegen fehlgeschlagen.</p>}
      </form>

      <QueryState query={courses} empty={courses.data?.length === 0}>
        <ul className="flex flex-col gap-1.5">
          {courses.data?.map((c) => (
            <li key={c.id}
              className={`flex items-start justify-between gap-2 rounded-lg p-3 transition-colors ${
                selected === c.id ? 'bg-[var(--wb-accent-soft)] ring-1 ring-[var(--wb-accent)]/40' : 'hover:bg-[var(--wb-subtle)]'}`}>
              {/* Eigener <button> statt div[role=button] — kein verschachteltes
                  Interaktionselement mehr mit dem Kopieren-Button daneben. */}
              <button type="button" onClick={() => onSelect(c.id)} aria-pressed={selected === c.id}
                className="min-w-0 flex-1 text-left">
                <span className="block min-w-0 truncate font-medium text-[var(--wb-ink)]">{c.name}</span>
                <span className="mt-1 flex items-center gap-3 text-xs text-[var(--wb-muted)]">
                  <span>{workshopTitle(c.workshop_key)}</span>
                  <span className="inline-flex items-center gap-1"><Icon name="users" className="h-3.5 w-3.5" />{c.participant_count ?? 0}</span>
                </span>
              </button>
              <CopyCode code={c.join_code} />
            </li>
          ))}
        </ul>
      </QueryState>
    </section>
  )
}
