import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authApi } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { t, type Lang } from '@/lib/i18n'
import { VersionBadge } from '@/components/VersionBadge'

const POINTS: Record<Lang, string[]> = {
  de: [
    '17 Module vom Ethernet-Frame bis zur Paket-Analyse.',
    'Simulatoren statt Folien: Switch, Router-CLI, Mini-Wireshark.',
    'Alles am Beispiel der Firma Nordwind Logistik.',
  ],
  en: [
    '17 modules from the Ethernet frame to packet analysis.',
    'Simulators instead of slides: switch, router CLI, mini Wireshark.',
    'All built around the fictional company Nordwind Logistik.',
  ],
}

export function LandingPage() {
  const nav = useNavigate()
  const setAuth = useAuthStore((s) => s.setAuth)
  const [lang, setLang] = useState<Lang>('de')
  const [code, setCode] = useState('')
  const [name, setName] = useState('')
  const [err, setErr] = useState('')

  async function join(e: React.FormEvent) {
    e.preventDefault()
    setErr('')
    try {
      const r = await authApi.join(code, name)
      setAuth(r.data.access_token, 'participant', r.data.name)
      nav('/lernen')
    } catch {
      setErr(t(lang, 'joinError'))
    }
  }

  return (
    <div className="min-h-[100dvh] grid md:grid-cols-2">
      {/* Markenseite */}
      <div className="grain relative flex flex-col justify-between overflow-hidden bg-gradient-to-br from-teal-600 to-teal-800 p-8 sm:p-12 text-white">
        <div aria-hidden="true" className="pointer-events-none absolute -top-32 -left-32 h-96 w-96 rounded-full bg-teal-400/25 blur-3xl" />
        <div aria-hidden="true" className="pointer-events-none absolute bottom-0 right-0 h-72 w-72 rounded-full bg-teal-950/40 blur-3xl" />
        <div className="animate-fade-up relative flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img src="/favicon.svg" alt="" className="h-9 w-9" />
            <span className="text-lg font-semibold tracking-tight">IntNetwork</span>
            <VersionBadge />
          </div>
          <div className="flex gap-1 text-xs font-medium">
            <button onClick={() => setLang('de')}
              className={`rounded px-2 py-1 ${lang === 'de' ? 'bg-white/20' : 'text-teal-100/70 hover:text-white'}`}>
              DE
            </button>
            <button onClick={() => setLang('en')}
              className={`rounded px-2 py-1 ${lang === 'en' ? 'bg-white/20' : 'text-teal-100/70 hover:text-white'}`}>
              EN
            </button>
          </div>
        </div>

        <div className="animate-fade-up relative max-w-md py-12">
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-[1.1]">
            {t(lang, 'heroTitle')}
          </h1>
          <p className="mt-4 text-teal-50/90 leading-relaxed">
            {t(lang, 'heroBody')}
          </p>
          <ul className="mt-8 flex flex-col divide-y divide-white/15 border-y border-white/15">
            {POINTS[lang].map((p) => (
              <li key={p} className="py-3 text-sm text-teal-50/90">{p}</li>
            ))}
          </ul>
        </div>

        <p className="animate-fade-up relative text-xs text-teal-100/70">
          {t(lang, 'internalNote')}
        </p>
      </div>

      {/* Beitreten */}
      <div className="flex items-center justify-center bg-slate-50 p-6 sm:p-10">
        <div className="animate-fade-up w-full max-w-sm">
          <h2 className="text-2xl font-bold text-slate-900">{t(lang, 'joinCourse')}</h2>
          <p className="text-sm text-slate-500 mt-1 mb-6">
            {t(lang, 'joinHint')}
          </p>

          <form onSubmit={join} className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <label htmlFor="code" className="text-sm font-medium text-slate-700">{t(lang, 'courseCode')}</label>
              <input
                id="code"
                className="border border-slate-300 rounded-lg px-3 py-2 uppercase tracking-widest font-mono focus:border-teal-500"
                placeholder="z. B. K7P2QM"
                value={code}
                onChange={(e) => setCode(e.target.value.toUpperCase())}
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label htmlFor="name" className="text-sm font-medium text-slate-700">{t(lang, 'yourName')}</label>
              <input
                id="name"
                className="border border-slate-300 rounded-lg px-3 py-2 focus:border-teal-500"
                placeholder="Vor- und Nachname"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            {err && <p className="text-sm text-rose-600">{err}</p>}

            <button className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white py-2.5 font-medium">
              {t(lang, 'join')}
            </button>
            <p className="text-xs text-slate-500">💡 {t(lang, 'resumeHint')}</p>
          </form>

          <div className="mt-6 border-t border-slate-200 pt-4">
            <button
              onClick={() => nav('/trainer')}
              className="text-sm text-slate-500 hover:text-teal-700"
            >
              {t(lang, 'trainerLogin')}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
