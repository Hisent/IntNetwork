import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authApi } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

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
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <div className="w-full max-w-sm rounded-2xl bg-white shadow p-8">
        <h1 className="text-2xl font-bold text-slate-900">IntNetwork</h1>
        <p className="text-slate-500 text-sm mb-6">Netzwerk-Grundlagen — Kurs beitreten</p>
        <form onSubmit={join} className="flex flex-col gap-3">
          <input className="border rounded-lg px-3 py-2 uppercase" placeholder="Kurs-Code"
            value={code} onChange={(e) => setCode(e.target.value.toUpperCase())} />
          <input className="border rounded-lg px-3 py-2" placeholder="Dein Name"
            value={name} onChange={(e) => setName(e.target.value)} />
          {err && <p className="text-sm text-red-600">{err}</p>}
          <button className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white py-2 font-medium">Beitreten</button>
        </form>
        <button onClick={() => nav('/trainer')} className="mt-4 text-xs text-slate-400 hover:text-slate-600">
          Trainer-Login
        </button>
      </div>
    </div>
  )
}
