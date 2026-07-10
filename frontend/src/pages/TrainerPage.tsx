import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { authApi, errMsg } from '@/lib/api'
import { trainerApi } from '@/lib/trainerApi'
import { TrainerFeedback } from '@/components/TrainerFeedback'
import { useAuthStore } from '@/store/auth'
import { VersionBadge } from '@/components/VersionBadge'

function CopyCode({ code }: { code: string }) {
  const [copied, setCopied] = useState(false)
  return (
    <button
      onClick={(e) => {
        e.stopPropagation()
        navigator.clipboard.writeText(code)
        setCopied(true)
        setTimeout(() => setCopied(false), 1500)
      }}
      title="Kurs-Code kopieren"
      className="font-mono text-teal-600 hover:text-teal-700 hover:underline select-text"
    >
      {copied ? 'Kopiert ✓' : code}
    </button>
  )
}

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
    <div className="min-h-dvh flex items-center justify-center bg-slate-50 p-4">
      <form onSubmit={submit} className="w-full max-w-sm rounded-2xl bg-white shadow p-8 flex flex-col gap-3">
        <h1 className="text-xl font-bold text-slate-900">Trainer-Login</h1>
        <input className="border rounded-lg px-3 py-2" placeholder="E-Mail" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="border rounded-lg px-3 py-2" type="password" placeholder="Passwort" value={pw} onChange={(e) => setPw(e.target.value)} />
        {err && <p className="text-sm text-red-600">{err}</p>}
        <button className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white py-2 font-medium">Anmelden</button>
      </form>
    </div>
  )
}

function TrainerDashboard({ onLogout }: { onLogout: () => void }) {
  const qc = useQueryClient()
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [selected, setSelected] = useState<number | null>(null)
  const [newKey, setNewKey] = useState('')
  const [newTitle, setNewTitle] = useState('')
  const createContent = useMutation({
    mutationFn: () => trainerApi.createContentModule(newKey.trim(), newTitle.trim()),
    onSuccess: (r) => {
      setNewKey('')
      setNewTitle('')
      qc.invalidateQueries({ queryKey: ['trainer-modules'] })
      navigate(`/trainer/modul/${r.data.key}/bearbeiten`)
    },
  })
  const [taEmail, setTaEmail] = useState('')
  const [taName, setTaName] = useState('')
  const [taPassword, setTaPassword] = useState('')
  const [taError, setTaError] = useState('')
  const trainerAccounts = useQuery({
    queryKey: ['trainer-accounts'],
    queryFn: () => trainerApi.listTrainerAccounts().then((r) => r.data),
  })
  const createTrainerAccount = useMutation({
    mutationFn: () => trainerApi.createTrainerAccount(taEmail.trim(), taName.trim(), taPassword),
    onSuccess: () => {
      setTaEmail(''); setTaName(''); setTaPassword(''); setTaError('')
      qc.invalidateQueries({ queryKey: ['trainer-accounts'] })
    },
    onError: (e) => setTaError(errMsg(e)),
  })
  const deleteTrainerAccount = useMutation({
    mutationFn: (id: number) => trainerApi.deleteTrainerAccount(id),
    onSuccess: () => { setTaError(''); qc.invalidateQueries({ queryKey: ['trainer-accounts'] }) },
    onError: (e) => setTaError(errMsg(e)),
  })
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
  const presentMods = useQuery({ queryKey: ['trainer-modules'], queryFn: () => trainerApi.trainerModules().then((r) => r.data) })
  const features = useQuery({ queryKey: ['features'], queryFn: () => trainerApi.features().then((r) => r.data) })
  const toggleFeature = useMutation({
    mutationFn: (v: boolean) => trainerApi.setFeature(v),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['features'] }),
  })
  const courseMods = useQuery({
    queryKey: ['course-modules', selected], enabled: selected !== null,
    queryFn: () => trainerApi.courseModules(selected as number).then((r) => r.data),
  })
  const presence = useQuery({
    queryKey: ['presence', selected], enabled: selected !== null,
    queryFn: () => trainerApi.coursePresence(selected as number).then((r) => r.data),
    refetchInterval: 10_000,
  })
  const toggleMod = useMutation({
    mutationFn: (v: { module_key: string; active: boolean }) =>
      trainerApi.setCourseModule(selected as number, v.module_key, v.active),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['course-modules', selected] }),
  })

  return (
    <div className="min-h-dvh bg-slate-50 p-6 sm:p-10">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-slate-900">Trainer</h1>
            <VersionBadge tone="dark" />
          </div>
          <button onClick={onLogout} className="text-sm text-slate-400 hover:text-slate-600">Abmelden</button>
        </div>

        <div className="flex gap-2 mb-6">
          <input className="border rounded-lg px-3 py-2" placeholder="Neuer Kurs-Name" value={name} onChange={(e) => setName(e.target.value)} />
          <button onClick={() => name.trim() && create.mutate()} className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-4 font-medium">Kurs anlegen</button>
        </div>

        <div className="flex flex-col gap-2 mb-8">
          {courses.data?.map((c) => (
            <div key={c.id} role="button" tabIndex={0}
              onClick={() => setSelected(c.id)}
              onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && setSelected(c.id)}
              className={`rounded-xl border bg-white p-4 text-left flex justify-between items-center cursor-pointer ${selected === c.id ? 'ring-2 ring-teal-500' : ''}`}>
              <span className="font-medium text-slate-800">{c.name}</span>
              <CopyCode code={c.join_code} />
            </div>
          ))}
        </div>

        {features.data && (
          <label className="flex items-center gap-2 text-sm text-slate-700 mb-6">
            <input
              type="checkbox"
              checked={features.data.comments}
              disabled={toggleFeature.isPending}
              onChange={(e) => toggleFeature.mutate(e.target.checked)}
            />
            Feedback-Kommentare aktiv
          </label>
        )}

        <div className="rounded-xl border bg-white p-4 mb-6">
          <h3 className="text-sm font-semibold text-slate-700 mb-2">Trainer-Zugänge</h3>
          <div className="flex flex-col gap-1.5 mb-3">
            {trainerAccounts.data?.map((t) => (
              <div key={t.id} className="flex justify-between items-center text-sm">
                <span className="text-slate-700">{t.name} <span className="text-slate-400">({t.email})</span></span>
                <button onClick={() => deleteTrainerAccount.mutate(t.id)}
                  className="text-xs text-rose-600 hover:text-rose-700">entfernen</button>
              </div>
            ))}
          </div>
          <div className="flex gap-2 flex-wrap">
            <input className="border rounded-lg px-3 py-1.5 text-sm" placeholder="E-Mail"
              value={taEmail} onChange={(e) => setTaEmail(e.target.value)} />
            <input className="border rounded-lg px-3 py-1.5 text-sm" placeholder="Name"
              value={taName} onChange={(e) => setTaName(e.target.value)} />
            <input className="border rounded-lg px-3 py-1.5 text-sm" type="password" placeholder="Passwort"
              value={taPassword} onChange={(e) => setTaPassword(e.target.value)} />
            <button onClick={() => taEmail.trim() && taName.trim() && taPassword && createTrainerAccount.mutate()}
              className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium">
              + Trainer hinzufügen
            </button>
          </div>
          {taError && <p className="text-sm text-red-600 mt-1">{taError}</p>}
        </div>

        {presentMods.data && (
          <div className="rounded-xl border bg-white p-4 mb-6">
            <h3 className="text-sm font-semibold text-slate-700 mb-2">Module präsentieren</h3>
            <div className="flex flex-wrap gap-2">
              {presentMods.data.map((m) => (
                <div key={m.key} className="flex items-center gap-1">
                  <Link to={`/trainer/modul/${m.key}`}
                    className="rounded-lg border px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-50">
                    {m.title}
                  </Link>
                  <Link to={`/trainer/modul/${m.key}/bearbeiten`} title="Bearbeiten"
                    className="rounded-lg border px-2 py-1.5 text-sm text-slate-500 hover:bg-slate-50">
                    ✎
                  </Link>
                </div>
              ))}
            </div>
            <div className="flex gap-2 mt-3">
              <input className="border rounded-lg px-3 py-1.5 text-sm" placeholder="Key (z.B. mein-modul)"
                value={newKey} onChange={(e) => setNewKey(e.target.value)} />
              <input className="border rounded-lg px-3 py-1.5 text-sm" placeholder="Titel DE"
                value={newTitle} onChange={(e) => setNewTitle(e.target.value)} />
              <button onClick={() => newKey.trim() && newTitle.trim() && createContent.mutate()}
                className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium">
                + Neues Modul
              </button>
            </div>
            {createContent.isError && (
              <p className="text-sm text-red-600 mt-1">Fehler beim Anlegen (Key ggf. bereits vergeben).</p>
            )}
          </div>
        )}

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

        {selected !== null && features.data?.comments && (
          <div className="rounded-xl border bg-white p-4 mb-6">
            <h3 className="text-sm font-semibold text-slate-700 mb-3">Feedback</h3>
            <TrainerFeedback courseId={selected} />
          </div>
        )}

        {selected !== null && (
          <div className="rounded-xl border bg-white p-4 mb-6">
            <h3 className="text-sm font-semibold text-slate-700 mb-2">Gerade aktiv</h3>
            {presence.data && presence.data.length > 0 ? (
              <div className="flex flex-col gap-1.5">
                {presence.data.map((entry) => (
                  <div key={entry.name} className="flex justify-between text-sm">
                    <span className="text-slate-700">{entry.name}</span>
                    <span className="text-slate-500">{entry.module_title}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-400">Niemand gerade aktiv.</p>
            )}
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
          <details className="mt-10">
            <summary className="text-sm font-semibold text-slate-700 mb-3 cursor-pointer select-none">
              Änderungslog
            </summary>
            <div className="flex flex-col gap-2 mt-3">
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
          </details>
        )}
      </div>
    </div>
  )
}
