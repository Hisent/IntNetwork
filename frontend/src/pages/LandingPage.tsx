import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { workshopApi } from '@/lib/workshopApi'
import type { Lang } from '@/lib/i18n'
import { VersionBadge } from '@/components/VersionBadge'
import { WorkshopTheme } from '@/components/WorkshopTheme'
import { BrandLogo } from '@/components/BrandLogo'

const COPY = {
  de: {
    eyebrow: 'IntLab / Learning hub',
    title: 'Lernen, das zu eurem Team passt.',
    body: 'Wähle einen Workshop und starte mit dem Kurs-Code deiner Trainerin oder deines Trainers direkt im passenden Durchlauf.',
    search: 'Workshops durchsuchen',
    open: 'Workshop ansehen',
    trainer: 'Trainer-Login',
    empty: 'Kein Workshop mit diesem Suchbegriff gefunden.',
    loading: 'Workshops werden geladen',
    catalog: 'Workshop-Katalog',
    available: 'verfügbare Workshops',
    join: 'Teilnahme per Kurs-Code',
    progress: 'Fortschritt im Browser gespeichert',
  },
  en: {
    eyebrow: 'IntLab / Learning hub',
    title: 'Learning that fits your team.',
    body: 'Choose a workshop and use your trainer’s course code to start in the right course run.',
    search: 'Search workshops',
    open: 'View workshop',
    trainer: 'Trainer login',
    empty: 'No workshop matches this search.',
    loading: 'Loading workshops',
    catalog: 'Workshop catalog',
    available: 'available workshops',
    join: 'Join with a course code',
    progress: 'Progress saved in this browser',
  },
} as const

function LoadingCards({ label }: { label: string }) {
  return (
    <div className="grid gap-4 md:grid-cols-2" aria-busy="true" aria-label={label}>
      {[0, 1].map((item) => (
        <div key={item} className="animate-pulse rounded-2xl border border-slate-200 bg-white p-6">
          <div className="h-2 w-16 rounded-full bg-slate-200" />
          <div className="mt-8 h-7 w-3/4 rounded bg-slate-200" />
          <div className="mt-4 h-12 rounded bg-slate-100" />
          <div className="mt-8 h-4 w-32 rounded bg-slate-200" />
        </div>
      ))}
    </div>
  )
}

export function LandingPage() {
  const [lang, setLang] = useState<Lang>('de')
  const [query, setQuery] = useState('')
  const workshops = useQuery({ queryKey: ['workshops'], queryFn: () => workshopApi.list().then((r) => r.data) })
  const copy = COPY[lang]
  const visible = (workshops.data ?? []).filter((workshop) =>
    `${workshop.title.de} ${workshop.title.en} ${workshop.summary?.de ?? ''} ${workshop.summary?.en ?? ''}`
      .toLocaleLowerCase()
      .includes(query.toLocaleLowerCase()),
  )

  return (
    <main className="grain relative min-h-[100dvh] overflow-hidden bg-[#eef4f3] px-5 py-6 sm:px-10 sm:py-8">
      <div className="relative mx-auto max-w-6xl">
        <header className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <BrandLogo className="h-9 text-lg" showName />
            <VersionBadge tone="dark" />
          </div>
          <div className="flex items-center gap-3 text-xs font-semibold">
            <button onClick={() => setLang('de')} className={lang === 'de' ? 'text-teal-700' : 'text-slate-400'}>DE</button>
            <button onClick={() => setLang('en')} className={lang === 'en' ? 'text-teal-700' : 'text-slate-400'}>EN</button>
            <Link to="/trainer" className="ml-2 text-slate-500 hover:text-teal-700">{copy.trainer}</Link>
          </div>
        </header>

        <section className="mt-12 grid gap-8 lg:grid-cols-[minmax(0,1fr)_360px] lg:items-end lg:gap-16 lg:pt-12">
          <div className="max-w-3xl">
            <p className="mb-4 text-xs font-bold uppercase tracking-[0.18em] text-teal-700">{copy.eyebrow}</p>
            <h1 className="max-w-3xl text-5xl font-bold leading-[0.98] tracking-[-0.04em] text-slate-950 sm:text-7xl">{copy.title}</h1>
            <p className="mt-6 max-w-2xl text-lg leading-relaxed text-slate-600">{copy.body}</p>
            <label className="relative mt-8 block max-w-xl">
              <span className="sr-only">{copy.search}</span>
              <input aria-label={copy.search} value={query} onChange={(event) => setQuery(event.target.value)} placeholder={copy.search} className="w-full rounded-xl border border-slate-300 bg-white/90 px-4 py-3.5 pr-12 text-slate-900 shadow-sm outline-none placeholder:text-slate-400 focus:border-teal-600 focus:ring-2 focus:ring-teal-100" />
              <span aria-hidden="true" className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">⌕</span>
            </label>
          </div>

          <aside className="border border-slate-800 bg-slate-950 p-6 text-white shadow-xl shadow-slate-900/10">
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-teal-300">{copy.catalog}</p>
            <p className="mt-7 text-5xl font-semibold tracking-tight">{workshops.data?.length ?? 0}</p>
            <p className="mt-1 text-sm text-slate-300">{copy.available}</p>
            <div className="mt-8 space-y-3 border-t border-slate-800 pt-5 text-sm text-slate-300">
              <p><span className="mr-2 text-teal-300">01</span>{copy.join}</p>
              <p><span className="mr-2 text-teal-300">02</span>{copy.progress}</p>
            </div>
          </aside>
        </section>

        <section className="mt-16 pb-12">
          {workshops.isLoading ? <LoadingCards label={copy.loading} /> : (
            <div className="grid gap-4 md:grid-cols-2">
              {visible.map((workshop) => (
                <WorkshopTheme key={workshop.key} theme={workshop.theme}>
                  <Link to={`/workshops/${workshop.key}`} className="group block rounded-2xl border border-[var(--workshop-accent-line)] bg-white p-6 shadow-sm transition hover:-translate-y-0.5 hover:border-[var(--workshop-accent)] hover:shadow-lg">
                    <div className="mb-8 h-2 w-16 rounded-full bg-[var(--workshop-accent)]" />
                    <div className="flex items-start justify-between gap-4">
                      <h2 className="text-2xl font-bold tracking-tight text-slate-950">{workshop.title[lang]}</h2>
                      <span className="rounded-full bg-[var(--workshop-accent-surface)] px-2.5 py-1 text-[11px] font-bold uppercase tracking-[0.12em] text-[var(--workshop-accent-ink)]">{workshop.theme === 'claude' ? 'AI' : 'NET'}</span>
                    </div>
                    <p className="mt-3 min-h-12 max-w-lg leading-relaxed text-slate-600">{workshop.summary?.[lang]}</p>
                    <span className="mt-7 inline-flex items-center gap-2 text-sm font-semibold text-[var(--workshop-accent)]">{copy.open}<span aria-hidden="true" className="transition-transform group-hover:translate-x-1">→</span></span>
                  </Link>
                </WorkshopTheme>
              ))}
            </div>
          )}
          {!workshops.isLoading && visible.length === 0 && <p className="border border-dashed border-slate-300 bg-white/60 p-6 text-slate-500">{copy.empty}</p>}
        </section>
      </div>
    </main>
  )
}
