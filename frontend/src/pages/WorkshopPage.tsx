import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { authApi, errMsg } from '@/lib/api'
import { workshopApi } from '@/lib/workshopApi'
import { useAuthStore } from '@/store/auth'
import { useDocumentLang, type Lang } from '@/lib/i18n'
import { PageSkeleton } from '@/components/PageSkeleton'
import { LoadError } from '@/components/LoadError'
import { WorkshopTheme } from '@/components/WorkshopTheme'
import { BrandLogo } from '@/components/BrandLogo'

export function WorkshopPage() {
  const { key = '' } = useParams()
  const nav = useNavigate()
  const setAuth = useAuthStore((state) => state.setAuth)
  const [lang, setLang] = useState<Lang>('de')
  useDocumentLang(lang)
  const [code, setCode] = useState('')
  const [name, setName] = useState('')
  const [resumeCode, setResumeCode] = useState('')
  const [error, setError] = useState('')
  const [issuedCode, setIssuedCode] = useState<string | null>(null)
  const workshop = useQuery({ queryKey: ['workshop', key], queryFn: () => workshopApi.get(key).then((r) => r.data) })

  if (workshop.isLoading) return <PageSkeleton />
  if (workshop.isError) return <LoadError lang={lang} onRetry={() => workshop.refetch()} />
  if (!workshop.data) return <main className="min-h-dvh bg-slate-50 p-8"><Link to="/" className="font-semibold text-teal-700">← Workshops</Link></main>

  const data = workshop.data
  const grouped = data.sections
    .map((section) => ({ ...section, modules: data.modules.filter((module) => module.order >= section.from && module.order <= section.to) }))
    .filter((section) => section.modules.length)
  const curriculum = grouped.length > 0 ? grouped : [{ key: 'all', from: 0, to: data.modules.length, title_de: 'Workshop-Inhalte', title_en: 'Workshop content', modules: data.modules }]

  async function join(event: React.FormEvent) {
    event.preventDefault()
    setError('')
    try {
      const result = await authApi.join(code, name, data.key, resumeCode)
      setAuth(result.data.access_token, 'participant', result.data.name)
      // Neuer/erstmaliger Beitritt liefert den persönlichen Code — einmal zeigen,
      // bevor es weitergeht. Normale Wiederaufnahme (Code stimmte) navigiert direkt.
      if (result.data.resume_code) setIssuedCode(result.data.resume_code)
      else nav('/lernen')
    } catch (reason) {
      setError(errMsg(reason, lang === 'de' ? 'Teilnahme nicht möglich.' : 'Unable to join.'))
    }
  }

  if (issuedCode) return (
    <WorkshopTheme theme={data.theme}>
      <main id="main-content" tabIndex={-1} className="grid min-h-[100dvh] place-items-center bg-[var(--workshop-accent-surface)] p-6">
        <div className="w-full max-w-md rounded-2xl border border-[var(--workshop-accent-line)] bg-white p-8 text-center shadow-lg">
          <BrandLogo className="mx-auto mb-4 h-9" />
          <h1 className="text-xl font-bold text-slate-900">{lang === 'de' ? 'Dein persönlicher Code' : 'Your personal code'}</h1>
          <p className="mt-2 text-sm text-slate-500">{lang === 'de'
            ? 'Notiere ihn dir. Du brauchst ihn, um später unter deinem Namen fortzusetzen.'
            : 'Note it down. You need it to resume under your name later.'}</p>
          <p className="my-6 select-all rounded-xl bg-[var(--workshop-accent-surface)] px-4 py-4 font-mono text-3xl font-bold tracking-[0.3em] text-[var(--workshop-accent)]">{issuedCode}</p>
          <button onClick={() => nav('/lernen')}
            className="w-full rounded-lg bg-[var(--workshop-accent)] px-4 py-2.5 font-semibold text-white hover:bg-[var(--workshop-accent-hover)]">
            {lang === 'de' ? 'Zum Workshop' : 'Start workshop'} →
          </button>
        </div>
      </main>
    </WorkshopTheme>
  )

  return (
    <WorkshopTheme theme={data.theme}>
      <main id="main-content" tabIndex={-1} className="min-h-[100dvh] bg-[var(--workshop-accent-surface)] px-5 py-6 sm:px-10 sm:py-8">
        <div className="mx-auto max-w-6xl">
          <header className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-4 sm:gap-6">
              <Link to="/" aria-label="IntLab"><BrandLogo className="h-9 text-lg" showName /></Link>
              <Link to="/" className="hidden text-sm font-semibold text-[var(--workshop-accent)] sm:block">← {lang === 'de' ? 'Alle Workshops' : 'All workshops'}</Link>
            </div>
            <div className="flex gap-2 text-xs font-semibold"><button onClick={() => setLang('de')} className={lang === 'de' ? 'text-[var(--workshop-accent)]' : 'text-slate-400'}>DE</button><button onClick={() => setLang('en')} className={lang === 'en' ? 'text-[var(--workshop-accent)]' : 'text-slate-400'}>EN</button></div>
          </header>

          <div className="mt-14 grid gap-12 lg:grid-cols-[minmax(0,1fr)_360px] lg:items-start">
            <section>
              <div className="mb-5 h-2 w-20 rounded-full bg-[var(--workshop-accent)]" />
              <p className="text-xs font-bold uppercase tracking-[0.16em] text-[var(--workshop-accent)]">{data.theme === 'claude' ? 'AI workshop' : 'Network workshop'}</p>
              <h1 className="mt-3 max-w-3xl text-4xl font-bold tracking-[-0.03em] text-slate-950 sm:text-6xl">{data.title[lang]}</h1>
              <p className="mt-5 max-w-2xl text-lg leading-relaxed text-slate-600">{data.summary?.[lang]}</p>
              <div className="mt-10 space-y-7">
                {curriculum.map((section) => <section key={section.key}><h2 className="text-xs font-bold uppercase tracking-[0.16em] text-slate-500">{lang === 'de' ? section.title_de : section.title_en}</h2><ol className="mt-3 divide-y divide-slate-200 rounded-xl border border-[var(--workshop-accent-line)] bg-white">{section.modules.map((module, index) => <li key={module.key} className="flex gap-4 px-4 py-3.5 text-slate-700"><span className="font-mono text-xs text-[var(--workshop-accent)]">{String(index + 1).padStart(2, '0')}</span><span>{module.title[lang]}</span></li>)}</ol></section>)}
              </div>
            </section>

            <aside className="h-fit border border-[var(--workshop-accent-line)] bg-white p-6 shadow-lg shadow-slate-900/5 lg:sticky lg:top-8">
              <p className="text-xs font-bold uppercase tracking-[0.16em] text-[var(--workshop-accent)]">{data.modules.length} {lang === 'de' ? 'Module' : 'modules'}</p>
              <h2 className="mt-3 text-2xl font-bold tracking-tight text-slate-950">{lang === 'de' ? 'Mit Kurs-Code teilnehmen' : 'Join with course code'}</h2>
              <p className="mt-2 text-sm leading-relaxed text-slate-500">{lang === 'de' ? 'Der Code ordnet dich dem richtigen Durchlauf zu.' : 'The code assigns you to the correct course run.'}</p>
              <form onSubmit={join} className="mt-6 space-y-4">
                <label className="block text-sm font-medium text-slate-700">{lang === 'de' ? 'Kurs-Code' : 'Course code'}<input required value={code} onChange={(event) => setCode(event.target.value.toUpperCase())} autoComplete="one-time-code" className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 font-mono uppercase tracking-widest outline-none focus:border-[var(--workshop-accent)] focus:ring-2 focus:ring-[var(--workshop-accent-soft)]" /></label>
                <label className="block text-sm font-medium text-slate-700">{lang === 'de' ? 'Dein Name' : 'Your name'}<input required value={name} onChange={(event) => setName(event.target.value)} autoComplete="name" className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-[var(--workshop-accent)] focus:ring-2 focus:ring-[var(--workshop-accent-soft)]" /></label>
                <label className="block text-sm font-medium text-slate-700">{lang === 'de' ? 'Wiederaufnahme-Code' : 'Resume code'} <span className="font-normal text-slate-400">({lang === 'de' ? 'nur beim erneuten Beitritt' : 'only when rejoining'})</span><input value={resumeCode} onChange={(event) => setResumeCode(event.target.value.toUpperCase())} autoComplete="off" className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2 font-mono uppercase tracking-widest outline-none focus:border-[var(--workshop-accent)] focus:ring-2 focus:ring-[var(--workshop-accent-soft)]" /></label>
                {error && <p role="alert" className="text-sm text-rose-600">{error}</p>}
                <button className="w-full rounded-lg bg-[var(--workshop-accent)] px-4 py-2.5 font-semibold text-white hover:bg-[var(--workshop-accent-hover)]">{lang === 'de' ? 'Workshop starten' : 'Start workshop'} →</button>
              </form>
            </aside>
          </div>
        </div>
      </main>
    </WorkshopTheme>
  )
}
