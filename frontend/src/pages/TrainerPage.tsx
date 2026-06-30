import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { authApi } from '@/lib/api'
import { trainerApi } from '@/lib/trainerApi'
import { useAuthStore } from '@/store/auth'

export function TrainerPage() {
  const { token, role, setAuth, logout } = useAuthStore()
  if (role !== 'trainer' || !token) return <TrainerLogin onLogin={(t) => setAuth(t, 'trainer')} />
  return <TrainerDashboard onLogout={logout} />
}

function TrainerLogin({ onLogin }: { onLogin: (t: string) => void }) {
  const [email, setEmail] = useState('')
  const [pw, setPw] = useState('')
  const [err, setErr] = useState('')
  async function submit(e: React.FormEvent) {
    e.preventDefault(); setErr('')
    try { onLogin((await authApi.trainerLogin(email, pw)).data.access_token) }
    catch { setErr('Login fehlgeschlagen.') }
  }
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <form onSubmit={submit} className="w-full max-w-sm rounded-2xl bg-white shadow p-8 flex flex-col gap-3">
        <h1 className="text-xl font-bold text-slate-900">Trainer-Login</h1>
        <input className="border rounded-lg px-3 py-2" placeholder="E-Mail" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="border rounded-lg px-3 py-2" type="password" placeholder="Passwort" value={pw} onChange={(e) => setPw(e.target.value)} />
        {err && <p className="text-sm text-red-600">{err}</p>}
        <button className="rounded-lg bg-indigo-600 text-white py-2 font-medium">Anmelden</button>
      </form>
    </div>
  )
}

function TrainerDashboard({ onLogout }: { onLogout: () => void }) {
  const qc = useQueryClient()
  const [name, setName] = useState('')
  const [selected, setSelected] = useState<number | null>(null)
  const courses = useQuery({ queryKey: ['courses'], queryFn: () => trainerApi.listCourses().then((r) => r.data) })
  const create = useMutation({
    mutationFn: () => trainerApi.createCourse(name).then((r) => r.data),
    onSuccess: () => { setName(''); qc.invalidateQueries({ queryKey: ['courses'] }) },
  })
  const dash = useQuery({
    queryKey: ['dashboard', selected], enabled: selected !== null,
    queryFn: () => trainerApi.dashboard(selected as number).then((r) => r.data),
  })
  const changelog = useQuery({ queryKey: ['changelog'], queryFn: () => trainerApi.changelog().then((r) => r.data) })
  const courseMods = useQuery({
    queryKey: ['course-modules', selected], enabled: selected !== null,
    queryFn: () => trainerApi.courseModules(selected as number).then((r) => r.data),
  })
  const toggleMod = useMutation({
    mutationFn: (v: { module_key: string; active: boolean }) =>
      trainerApi.setCourseModule(selected as number, v.module_key, v.active),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['course-modules', selected] }),
  })

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-slate-900">Trainer</h1>
          <button onClick={onLogout} className="text-sm text-slate-400 hover:text-slate-600">Abmelden</button>
        </div>

        <div className="flex gap-2 mb-6">
          <input className="border rounded-lg px-3 py-2" placeholder="Neuer Kurs-Name" value={name} onChange={(e) => setName(e.target.value)} />
          <button onClick={() => name.trim() && create.mutate()} className="rounded-lg bg-indigo-600 text-white px-4 font-medium">Kurs anlegen</button>
        </div>

        <div className="flex flex-col gap-2 mb-8">
          {courses.data?.map((c) => (
            <button key={c.id} onClick={() => setSelected(c.id)}
              className={`rounded-xl border bg-white p-4 text-left flex justify-between ${selected === c.id ? 'ring-2 ring-indigo-500' : ''}`}>
              <span className="font-medium text-slate-800">{c.name}</span>
              <span className="font-mono text-indigo-600">{c.join_code}</span>
            </button>
          ))}
        </div>

        {courseMods.data && (
          <div className="rounded-xl border bg-white p-4 mb-6">
            <h3 className="text-sm font-semibold text-slate-700 mb-2">Module in diesem Kurs</h3>
            <div className="flex flex-col gap-1.5">
              {courseMods.data.map((m) => (
                <label key={m.key} className="flex items-center gap-2 text-sm text-slate-700">
                  <input type="checkbox" checked={m.active} disabled={toggleMod.isPending}
                    onChange={(e) => toggleMod.mutate({ module_key: m.key, active: e.target.checked })} />
                  {m.title}
                </label>
              ))}
            </div>
          </div>
        )}

        {dash.data && (
          <div className="overflow-x-auto rounded-xl border bg-white">
            <table className="w-full text-sm">
              <thead className="bg-slate-50">
                <tr>
                  <th className="text-left px-3 py-2">Teilnehmer</th>
                  {dash.data.modules.map((m) => <th key={m.key} className="px-3 py-2">{m.title}</th>)}
                </tr>
              </thead>
              <tbody>
                {dash.data.participants.map((p) => (
                  <tr key={p.name} className="border-t">
                    <td className="px-3 py-2 font-medium text-slate-700">{p.name}</td>
                    {dash.data!.modules.map((m) => {
                      const cell = p.cells[m.key]
                      return <td key={m.key} className="px-3 py-2 text-center">
                        {cell?.done ? '✓' : '–'}{cell?.best != null ? ` ${cell.best}%` : ''}
                      </td>
                    })}
                  </tr>
                ))}
                {dash.data.participants.length === 0 && (
                  <tr><td colSpan={dash.data.modules.length + 1} className="px-3 py-6 text-center text-slate-400">Noch keine Teilnehmer.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        )}

        {changelog.data && changelog.data.length > 0 && (
          <div className="mt-10">
            <h2 className="text-sm font-semibold text-slate-700 mb-3">Änderungslog</h2>
            <div className="flex flex-col gap-2">
              {changelog.data.map((e, i) => (
                <div key={i} className="rounded-xl border bg-white p-4">
                  <div className="flex items-baseline justify-between">
                    <span className="font-medium text-slate-800">{e.title}</span>
                    <span className="text-xs text-slate-400">{e.date}</span>
                  </div>
                  <p className="text-sm text-slate-600 mt-1">{e.text}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
