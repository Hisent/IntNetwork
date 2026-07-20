import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { workshopApi } from '@/lib/workshopApi'
import type { Lang } from '@/lib/i18n'
import { VersionBadge } from '@/components/VersionBadge'

const COPY = {
  de: { eyebrow: 'Interne Lernplattform', title: 'Den passenden Workshop finden.', body: 'Wähle einen Workshop. Mit dem Kurs-Code deiner Trainerin oder deines Trainers startest du direkt im richtigen Kurs.', search: 'Workshop suchen …', open: 'Workshop ansehen', trainer: 'Trainer-Login', empty: 'Kein Workshop gefunden.' },
  en: { eyebrow: 'Internal learning platform', title: 'Find the workshop that fits.', body: 'Choose a workshop, then use the course code from your trainer to join the right course.', search: 'Search workshops …', open: 'View workshop', trainer: 'Trainer login', empty: 'No workshop found.' },
} as const

export function LandingPage() {
  const [lang, setLang] = useState<Lang>('de')
  const [query, setQuery] = useState('')
  const workshops = useQuery({ queryKey: ['workshops'], queryFn: () => workshopApi.list().then((r) => r.data) })
  const copy = COPY[lang]
  const visible = (workshops.data ?? []).filter((workshop) =>
    `${workshop.title.de} ${workshop.title.en} ${workshop.summary?.de ?? ''} ${workshop.summary?.en ?? ''}`
      .toLocaleLowerCase().includes(query.toLocaleLowerCase()))

  return (
    <main className="min-h-[100dvh] bg-slate-50 px-6 py-8 sm:px-10 sm:py-12">
      <div className="mx-auto max-w-5xl">
        <header className="mb-14 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3"><img src="/favicon.svg" alt="" className="h-9 w-9" /><span className="text-lg font-semibold tracking-tight">IntNetwork</span><VersionBadge tone="dark" /></div>
          <div className="flex items-center gap-3 text-xs font-semibold"><button onClick={() => setLang('de')} className={lang === 'de' ? 'text-teal-700' : 'text-slate-400'}>DE</button><button onClick={() => setLang('en')} className={lang === 'en' ? 'text-teal-700' : 'text-slate-400'}>EN</button><Link to="/trainer" className="ml-3 text-slate-500 hover:text-teal-700">{copy.trainer}</Link></div>
        </header>
        <section className="mb-10 max-w-2xl">
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.16em] text-teal-700">{copy.eyebrow}</p>
          <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl">{copy.title}</h1>
          <p className="mt-5 max-w-xl text-lg leading-relaxed text-slate-600">{copy.body}</p>
          <input aria-label={copy.search} value={query} onChange={(event) => setQuery(event.target.value)} placeholder={copy.search} className="mt-8 w-full rounded-xl border border-slate-300 bg-white px-4 py-3 outline-none focus:border-teal-600" />
        </section>
        {workshops.isLoading ? <p className="text-slate-500">…</p> : <div className="grid gap-5 md:grid-cols-2">
          {visible.map((workshop) => <Link key={workshop.key} to={`/workshops/${workshop.key}`} className={`group rounded-2xl border bg-white p-6 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md ${workshop.theme === 'claude' ? 'border-orange-200 hover:border-orange-400' : 'border-teal-200 hover:border-teal-500'}`}>
            <div className={`mb-8 h-2 w-16 rounded-full ${workshop.theme === 'claude' ? 'bg-orange-600' : 'bg-teal-600'}`} />
            <h2 className="text-2xl font-bold text-slate-900">{workshop.title[lang]}</h2>
            <p className="mt-3 min-h-12 leading-relaxed text-slate-600">{workshop.summary?.[lang]}</p>
            <span className={`mt-7 inline-block text-sm font-semibold ${workshop.theme === 'claude' ? 'text-orange-700' : 'text-teal-700'}`}>{copy.open} →</span>
          </Link>)}
        </div>}
        {!workshops.isLoading && visible.length === 0 && <p className="text-slate-500">{copy.empty}</p>}
      </div>
    </main>
  )
}
