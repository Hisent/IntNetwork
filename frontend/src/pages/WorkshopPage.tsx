import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { authApi, errMsg } from '@/lib/api'
import { workshopApi } from '@/lib/workshopApi'
import { useAuthStore } from '@/store/auth'
import type { Lang } from '@/lib/i18n'

export function WorkshopPage() {
  const { key = '' } = useParams()
  const nav = useNavigate()
  const setAuth = useAuthStore((state) => state.setAuth)
  const [lang, setLang] = useState<Lang>('de')
  const [code, setCode] = useState('')
  const [name, setName] = useState('')
  const [error, setError] = useState('')
  const workshop = useQuery({ queryKey: ['workshop', key], queryFn: () => workshopApi.get(key).then((r) => r.data) })
  if (workshop.isLoading) return <main className="p-10 text-slate-500">…</main>
  if (!workshop.data) return <main className="p-10"><Link to="/">← Workshops</Link></main>
  const data = workshop.data
  const isClaude = data.theme === 'claude'
  const accentText = isClaude ? 'text-orange-700' : 'text-teal-700'
  const accentBg = isClaude ? 'bg-orange-600' : 'bg-teal-600'
  const accentButton = isClaude ? 'bg-orange-600 hover:bg-orange-700' : 'bg-teal-600 hover:bg-teal-700'
  const accentFocus = isClaude ? 'focus:border-orange-600' : 'focus:border-teal-600'
  const grouped = data.sections.map((section) => ({ ...section, modules: data.modules.filter((module) => module.order >= section.from && module.order <= section.to) })).filter((section) => section.modules.length)
  async function join(event: React.FormEvent) {
    event.preventDefault(); setError('')
    try { const result = await authApi.join(code, name, data.key); setAuth(result.data.access_token, 'participant', result.data.name); nav('/lernen') }
    catch (reason) { setError(errMsg(reason, lang === 'de' ? 'Teilnahme nicht möglich.' : 'Unable to join.')) }
  }
  return <main className="min-h-[100dvh] bg-slate-50 px-6 py-8 sm:px-10 sm:py-12">
    <div className="mx-auto max-w-5xl"><header className="flex items-center justify-between"><Link to="/" className={`text-sm font-semibold ${accentText}`}>← {lang === 'de' ? 'Alle Workshops' : 'All workshops'}</Link><div className="flex gap-2 text-xs"><button onClick={() => setLang('de')} className={lang === 'de' ? accentText : 'text-slate-400'}>DE</button><button onClick={() => setLang('en')} className={lang === 'en' ? accentText : 'text-slate-400'}>EN</button></div></header>
      <div className="mt-14 grid gap-12 lg:grid-cols-[minmax(0,1fr)_340px]"><section><div className={`mb-5 h-2 w-20 rounded-full ${accentBg}`} /><h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">{data.title[lang]}</h1><p className="mt-5 text-lg leading-relaxed text-slate-600">{data.summary?.[lang]}</p><div className="mt-10 space-y-7">{grouped.map((section) => <section key={section.key}><h2 className="text-sm font-semibold uppercase tracking-[0.14em] text-slate-500">{lang === 'de' ? section.title_de : section.title_en}</h2><ol className="mt-3 divide-y rounded-xl border bg-white">{section.modules.map((module) => <li key={module.key} className="px-4 py-3 text-slate-700">{module.title[lang]}</li>)}</ol></section>)}</div></section>
        <aside className="h-fit rounded-2xl border bg-white p-6 shadow-sm lg:sticky lg:top-8"><h2 className="text-xl font-bold text-slate-900">{lang === 'de' ? 'Mit Kurs-Code teilnehmen' : 'Join with course code'}</h2><p className="mt-2 text-sm leading-relaxed text-slate-500">{lang === 'de' ? 'Der Code ordnet dich dem richtigen Durchlauf zu.' : 'The code assigns you to the correct course run.'}</p><form onSubmit={join} className="mt-6 space-y-4"><label className="block text-sm font-medium text-slate-700">{lang === 'de' ? 'Kurs-Code' : 'Course code'}<input value={code} onChange={(event) => setCode(event.target.value.toUpperCase())} className={`mt-1.5 block w-full rounded-lg border px-3 py-2 font-mono tracking-widest uppercase ${accentFocus}`} /></label><label className="block text-sm font-medium text-slate-700">{lang === 'de' ? 'Dein Name' : 'Your name'}<input value={name} onChange={(event) => setName(event.target.value)} className={`mt-1.5 block w-full rounded-lg border px-3 py-2 ${accentFocus}`} /></label>{error && <p className="text-sm text-rose-600">{error}</p>}<button className={`w-full rounded-lg px-4 py-2.5 font-semibold text-white ${accentButton}`}>{lang === 'de' ? 'Workshop starten' : 'Start workshop'} →</button></form></aside>
      </div></div>
  </main>
}
