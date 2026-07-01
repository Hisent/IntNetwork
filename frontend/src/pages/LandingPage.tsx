import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authApi } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

const POINTS = [
  '15 Module vom Ethernet-Frame bis zum VPN.',
  'Simulatoren statt Folien: Switch, Router-CLI, Subnetz-Rechner.',
  'Alles am Beispiel der Firma Nordwind Logistik.',
]

export function LandingPage() {
  const nav = useNavigate()
  const setAuth = useAuthStore((s) => s.setAuth)
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
      setErr('Kurs-Code ungültig oder Name fehlt.')
    }
  }

  return (
    <div className="min-h-[100dvh] grid md:grid-cols-2">
      {/* Markenseite */}
      <div className="relative flex flex-col justify-between overflow-hidden bg-gradient-to-br from-teal-600 to-teal-800 p-8 sm:p-12 text-white">
        <div className="animate-fade-up flex items-center gap-3">
          <img src="/favicon.svg" alt="" className="h-9 w-9" />
          <span className="text-lg font-semibold tracking-tight">IntNetwork</span>
        </div>

        <div className="animate-fade-up max-w-md py-12">
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-[1.1]">
            Netzwerk-Grundlagen, interaktiv.
          </h1>
          <p className="mt-4 text-teal-50/90 leading-relaxed">
            Ein Kurs, der Netzwerke nicht erklärt, sondern zeigt. Frames bauen,
            Switches lernen lassen, Pakete routen.
          </p>
          <ul className="mt-8 flex flex-col divide-y divide-white/15 border-y border-white/15">
            {POINTS.map((p) => (
              <li key={p} className="py-3 text-sm text-teal-50/90">{p}</li>
            ))}
          </ul>
        </div>

        <p className="animate-fade-up text-xs text-teal-100/70">
          Interne Schulung. Zugang per Kurs-Code.
        </p>
      </div>

      {/* Beitreten */}
      <div className="flex items-center justify-center bg-slate-50 p-6 sm:p-10">
        <div className="animate-fade-up w-full max-w-sm">
          <h2 className="text-2xl font-bold text-slate-900">Kurs beitreten</h2>
          <p className="text-sm text-slate-500 mt-1 mb-6">
            Code und Namen vom Trainer erhalten.
          </p>

          <form onSubmit={join} className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <label htmlFor="code" className="text-sm font-medium text-slate-700">Kurs-Code</label>
              <input
                id="code"
                className="border border-slate-300 rounded-lg px-3 py-2 uppercase tracking-widest font-mono focus:border-teal-500"
                placeholder="z. B. K7P2QM"
                value={code}
                onChange={(e) => setCode(e.target.value.toUpperCase())}
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label htmlFor="name" className="text-sm font-medium text-slate-700">Dein Name</label>
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
              Beitreten
            </button>
          </form>

          <div className="mt-6 border-t border-slate-200 pt-4">
            <button
              onClick={() => nav('/trainer')}
              className="text-sm text-slate-500 hover:text-teal-700"
            >
              Ich bin Trainer
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
