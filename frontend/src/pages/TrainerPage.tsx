import { useId, useState, type ReactNode } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { authApi, errMsg } from '@/lib/api'
import { trainerApi, type Course } from '@/lib/trainerApi'
import { TrainerFeedback } from '@/components/TrainerFeedback'
import { useAuthStore } from '@/store/auth'
import { VersionBadge } from '@/components/VersionBadge'
import { workshopApi } from '@/lib/workshopApi'
import { BrandLogo } from '@/components/BrandLogo'
import { ThemeToggle } from '@/components/ThemeToggle'
import { Icon } from '@/components/Icon'

// --- kleine Bausteine ---------------------------------------------------------

function Field({ label, className = '', ...props }: { label: string } & React.InputHTMLAttributes<HTMLInputElement>) {
  const id = useId()
  return (
    <label htmlFor={id} className="flex min-w-40 flex-1 flex-col gap-1 text-xs font-medium text-slate-600">
      {label}
      <input id={id} className={`rounded-lg border px-3 py-2 text-sm font-normal text-slate-900 ${className}`} {...props} />
    </label>
  )
}

function Section({ title, action, children }: { title: string; action?: ReactNode; children: ReactNode }) {
  return (
    <section className="rounded-xl border bg-white p-4">
      <div className="mb-3 flex items-center justify-between gap-2">
        <h3 className="text-sm font-semibold text-slate-700">{title}</h3>
        {action}
      </div>
      {children}
    </section>
  )
}

function QueryState({ query, empty, children }: { query: { isLoading: boolean; isError: boolean }; empty?: boolean; children: ReactNode }) {
  if (query.isLoading) return <p className="text-sm text-slate-400">Lädt …</p>
  if (query.isError) return <p className="text-sm text-rose-600">Konnte nicht geladen werden.</p>
  if (empty) return <p className="text-sm text-slate-400">Nichts vorhanden.</p>
  return <>{children}</>
}

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
      className="shrink-0 font-mono text-sm text-teal-600 hover:text-teal-700 hover:underline"
    >
      {copied ? 'Kopiert ✓' : code}
    </button>
  )
}

// --- Login --------------------------------------------------------------------

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
        <Link to="/" className="mb-3"><BrandLogo className="h-9 text-lg" showName /></Link>
        <h1 className="text-xl font-bold text-slate-900">Trainer-Login</h1>
        <Field label="E-Mail" type="email" autoComplete="username" placeholder="trainer@beispiel.de" value={email} onChange={(e) => setEmail(e.target.value)} />
        <Field label="Passwort" type="password" autoComplete="current-password" placeholder="••••••••" value={pw} onChange={(e) => setPw(e.target.value)} />
        {err && <p className="text-sm text-red-600">{err}</p>}
        <button className="mt-1 rounded-lg bg-teal-600 hover:bg-teal-700 text-white py-2 font-medium">Anmelden</button>
      </form>
    </div>
  )
}

// --- Dashboard ----------------------------------------------------------------

function TrainerDashboard({ onLogout }: { onLogout: () => void }) {
  const [selected, setSelected] = useState<number | null>(null)
  const courses = useQuery({ queryKey: ['courses'], queryFn: () => trainerApi.listCourses().then((r) => r.data) })
  const workshops = useQuery({ queryKey: ['workshops'], queryFn: () => workshopApi.list().then((r) => r.data) })
  const workshopTitle = (key: string | null) => workshops.data?.find((w) => w.key === key)?.title.de ?? 'Bestandskurs'
  const selectedCourse = courses.data?.find((c) => c.id === selected) ?? null

  return (
    <div className="min-h-dvh bg-slate-50 p-6 sm:p-10">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8 flex items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <Link to="/"><BrandLogo className="h-9 text-lg" showName /></Link>
            <h1 className="text-2xl font-bold text-slate-900">Trainer</h1>
            <VersionBadge tone="dark" />
          </div>
          <div className="flex items-center gap-2">
            <ThemeToggle className="text-slate-400" />
            <button onClick={onLogout} className="text-sm text-slate-400 hover:text-slate-600">Abmelden</button>
          </div>
        </header>

        {/* Master-Detail: Kurse wählen (links) → Kurs-Detail (rechts) */}
        <div className="grid gap-6 lg:grid-cols-[340px_minmax(0,1fr)] lg:items-start">
          <CourseList
            courses={courses} workshopTitle={workshopTitle} workshops={workshops.data ?? []}
            selected={selected} onSelect={setSelected} />
          <div className="min-w-0">
            {selectedCourse
              ? <CourseDetail course={selectedCourse} workshopTitle={workshopTitle} />
              : <div className="grid h-full min-h-48 place-items-center rounded-xl border border-dashed bg-white p-8 text-center text-sm text-slate-400">
                  Kurs links auswählen, um Module, Präsenz, Feedback und Fortschritt zu sehen.
                </div>}
          </div>
        </div>

        {/* Verwaltung: globale, kursunabhängige Bereiche */}
        <div className="mt-12">
          <h2 className="mb-4 text-xs font-bold uppercase tracking-[0.16em] text-slate-400">Verwaltung</h2>
          <div className="grid gap-6 lg:grid-cols-2">
            <ModuleAdmin workshops={workshops.data ?? []} />
            <TrainerAccounts />
            <SettingsBlock />
            <ChangelogBlock />
            <AuditLogBlock />
          </div>
        </div>
      </div>
    </div>
  )
}

// --- Kursliste (Master) -------------------------------------------------------

function CourseList({ courses, workshops, workshopTitle, selected, onSelect }: {
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
    <section className="rounded-xl border bg-white p-4 lg:sticky lg:top-6">
      <h3 className="mb-3 text-sm font-semibold text-slate-700">Kurse</h3>
      <form onSubmit={(e) => { e.preventDefault(); name.trim() && create.mutate() }} className="mb-4 flex flex-col gap-2">
        <Field label="Neuer Kurs" placeholder="Kurs-Name" value={name} onChange={(e) => setName(e.target.value)} />
        <label className="flex flex-col gap-1 text-xs font-medium text-slate-600">Workshop
          <select value={workshopKey} onChange={(e) => setWorkshopKey(e.target.value)} className="rounded-lg border px-3 py-2 text-sm font-normal text-slate-900">
            {workshops.map((w) => <option key={w.key} value={w.key}>{w.title.de}</option>)}
          </select>
        </label>
        <button disabled={!name.trim() || create.isPending}
          className="inline-flex items-center justify-center gap-1 rounded-lg bg-teal-600 px-4 py-2 text-sm font-medium text-white hover:bg-teal-700 disabled:opacity-50">
          <Icon name="plus" className="h-4 w-4" /> Kurs anlegen
        </button>
        {create.isError && <p className="text-xs text-rose-600">Anlegen fehlgeschlagen.</p>}
      </form>

      <QueryState query={courses} empty={courses.data?.length === 0}>
        <div className="flex flex-col gap-1.5">
          {courses.data?.map((c) => (
            <div key={c.id} role="button" tabIndex={0}
              onClick={() => onSelect(c.id)}
              onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && (e.preventDefault(), onSelect(c.id))}
              aria-pressed={selected === c.id}
              className={`cursor-pointer rounded-lg border p-3 transition-colors ${
                selected === c.id ? 'border-teal-400 bg-teal-50/70 ring-1 ring-teal-400/40' : 'border-slate-200 hover:bg-slate-50'}`}>
              <div className="flex items-center justify-between gap-2">
                <span className="min-w-0 truncate font-medium text-slate-800">{c.name}</span>
                <CopyCode code={c.join_code} />
              </div>
              <div className="mt-1 flex items-center gap-3 text-xs text-slate-400">
                <span>{workshopTitle(c.workshop_key)}</span>
                <span className="inline-flex items-center gap-1"><Icon name="users" className="h-3.5 w-3.5" />{c.participant_count ?? 0}</span>
              </div>
            </div>
          ))}
        </div>
      </QueryState>
    </section>
  )
}

// --- Kurs-Detail (Detail) -----------------------------------------------------

function CourseDetail({ course, workshopTitle }: { course: Course; workshopTitle: (key: string | null) => string }) {
  const qc = useQueryClient()
  const cid = course.id
  const courseMods = useQuery({ queryKey: ['course-modules', cid], queryFn: () => trainerApi.courseModules(cid).then((r) => r.data) })
  const presence = useQuery({ queryKey: ['presence', cid], queryFn: () => trainerApi.coursePresence(cid).then((r) => r.data), refetchInterval: 10_000 })
  const dash = useQuery({ queryKey: ['dashboard', cid], queryFn: () => trainerApi.dashboard(cid).then((r) => r.data) })
  const features = useQuery({ queryKey: ['features'], queryFn: () => trainerApi.features().then((r) => r.data) })
  const toggleMod = useMutation({
    mutationFn: (v: { module_key: string; active: boolean }) => trainerApi.setCourseModule(cid, v.module_key, v.active),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['course-modules', cid] }),
  })
  const setApproval = useMutation({
    mutationFn: (v: boolean) => trainerApi.setCourseApproval(cid, v),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['courses'] }); qc.invalidateQueries({ queryKey: ['dashboard', cid] }) },
  })
  const approve = useMutation({
    mutationFn: (v: { pid: number; approved: boolean }) => trainerApi.approveParticipant(cid, v.pid, v.approved),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['dashboard', cid] }),
  })
  const [shownCode, setShownCode] = useState<{ name: string; code: string } | null>(null)
  const resetCode = useMutation({
    mutationFn: (pid: number) => trainerApi.resetResumeCode(cid, pid).then((r) => r.data),
    onSuccess: (d) => setShownCode({ name: dash.data?.participants.find((x) => x.id === d.id)?.name ?? '', code: d.resume_code }),
  })
  const removeParticipant = useMutation({
    mutationFn: (pid: number) => trainerApi.deleteParticipant(cid, pid),
    onSuccess: () => { setShownCode(null); qc.invalidateQueries({ queryKey: ['dashboard', cid] }); qc.invalidateQueries({ queryKey: ['courses'] }) },
  })
  const requireApproval = course.require_approval ?? false

  return (
    <div className="flex flex-col gap-6">
      <div className="rounded-xl border bg-white p-4">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h2 className="text-lg font-bold text-slate-900">{course.name}</h2>
          <span className="text-xs text-slate-400">{workshopTitle(course.workshop_key)} · {course.participant_count ?? 0} Teilnehmer · Code <span className="font-mono text-slate-500">{course.join_code}</span></span>
        </div>
      </div>

      <Section title="Gerade aktiv">
        <QueryState query={presence} empty={presence.data?.length === 0}>
          <div className="flex flex-col gap-1.5">
            {presence.data?.map((entry) => (
              <div key={entry.name} className="flex justify-between text-sm">
                <span className="text-slate-700">{entry.name}</span>
                <span className="text-slate-500">{entry.module_title}</span>
              </div>
            ))}
          </div>
        </QueryState>
      </Section>

      <Section title="Module in diesem Kurs">
        <QueryState query={courseMods} empty={courseMods.data?.length === 0}>
          <div className="grid gap-1.5 sm:grid-cols-2">
            {courseMods.data?.map((m) => (
              <label key={m.key} className="flex items-center gap-2 text-sm text-slate-700">
                <input type="checkbox" checked={m.active} disabled={toggleMod.isPending}
                  onChange={(e) => toggleMod.mutate({ module_key: m.key, active: e.target.checked })} />
                {m.title}
              </label>
            ))}
          </div>
        </QueryState>
      </Section>

      <Section title="Fortschritt" action={
        <label className="flex items-center gap-1.5 text-xs font-normal text-slate-500">
          <input type="checkbox" checked={requireApproval} disabled={setApproval.isPending}
            onChange={(e) => setApproval.mutate(e.target.checked)} />
          Freigabe für Bestätigung nötig
        </label>}>
        <ProgressTable dash={dash} requireApproval={requireApproval} onApprove={(pid, a) => approve.mutate({ pid, approved: a })} />
      </Section>

      <Section title="Teilnehmer verwalten">
        <QueryState query={dash} empty={dash.data?.participants.length === 0}>
          <div className="flex flex-col gap-1.5">
            {dash.data?.participants.map((p) => (
              <div key={p.id} className="flex items-center justify-between gap-2 text-sm">
                <span className="min-w-0 truncate text-slate-700">{p.name}</span>
                <div className="flex shrink-0 items-center gap-2">
                  <button onClick={() => resetCode.mutate(p.id)} disabled={resetCode.isPending}
                    className="text-xs text-slate-500 hover:text-teal-700">Code zurücksetzen</button>
                  <button onClick={() => window.confirm(`${p.name} inkl. Fortschritt endgültig löschen?`) && removeParticipant.mutate(p.id)}
                    aria-label={`${p.name} löschen`} className="text-rose-600 hover:text-rose-700"><Icon name="trash" className="h-4 w-4" /></button>
                </div>
              </div>
            ))}
          </div>
        </QueryState>
        {shownCode && (
          <p className="mt-3 rounded-lg bg-teal-50 px-3 py-2 text-sm text-teal-900">
            Neuer Wiederaufnahme-Code für <b>{shownCode.name}</b>: <code className="select-all font-mono font-bold">{shownCode.code}</code> — bitte persönlich weitergeben.
          </p>
        )}
      </Section>

      {features.data?.comments && (
        <Section title="Feedback"><TrainerFeedback courseId={cid} /></Section>
      )}
    </div>
  )
}

function ProgressTable({ dash, requireApproval, onApprove }: {
  dash: ReturnType<typeof useQuery<import('@/lib/trainerApi').Dashboard>>
  requireApproval: boolean
  onApprove: (participantId: number, approved: boolean) => void
}) {
  return (
    <QueryState query={dash}>
      <div className="overflow-x-auto">
        <table className="w-full border-separate border-spacing-0 text-sm">
          <thead>
            <tr>
              <th className="sticky left-0 z-10 bg-slate-50 px-3 py-2 text-left font-semibold text-slate-600">Teilnehmer</th>
              {dash.data?.modules.map((m) => <th key={m.key} className="whitespace-nowrap bg-slate-50 px-3 py-2 text-xs font-medium text-slate-500">{m.title}</th>)}
              {requireApproval && <th className="whitespace-nowrap bg-slate-50 px-3 py-2 text-xs font-medium text-slate-500">Freigabe</th>}
            </tr>
          </thead>
          <tbody>
            {dash.data?.participants.map((p) => (
              <tr key={p.id}>
                <td className="sticky left-0 z-10 border-t bg-white px-3 py-2 font-medium text-slate-700">{p.name}</td>
                {dash.data!.modules.map((m) => {
                  const cell = p.cells[m.key]
                  return (
                    <td key={m.key} className="border-t px-3 py-2 text-center">
                      {cell?.done
                        ? <span className="inline-flex items-center gap-1 text-emerald-600"><Icon name="check" className="h-4 w-4" />{cell.best != null ? <span className="text-xs text-slate-400">{cell.best}%</span> : null}</span>
                        : <span className="text-slate-300">–</span>}
                    </td>
                  )
                })}
                {requireApproval && (
                  <td className="border-t px-3 py-2 text-center">
                    <input type="checkbox" checked={p.approved} onChange={(e) => onApprove(p.id, e.target.checked)}
                      aria-label={`${p.name} freigeben`} />
                  </td>
                )}
              </tr>
            ))}
            {dash.data?.participants.length === 0 && (
              <tr><td colSpan={(dash.data?.modules.length ?? 0) + (requireApproval ? 2 : 1)} className="px-3 py-6 text-center text-slate-400">Noch keine Teilnehmer.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </QueryState>
  )
}

// --- Verwaltung: Module -------------------------------------------------------

function ModuleAdmin({ workshops }: { workshops: { key: string; title: { de: string } }[] }) {
  const qc = useQueryClient()
  const navigate = useNavigate()
  const [newKey, setNewKey] = useState('')
  const [newTitle, setNewTitle] = useState('')
  const [moduleWorkshopKey, setModuleWorkshopKey] = useState('network')
  const presentMods = useQuery({ queryKey: ['trainer-modules'], queryFn: () => trainerApi.trainerModules().then((r) => r.data) })
  const createContent = useMutation({
    mutationFn: () => trainerApi.createContentModule(newKey.trim(), newTitle.trim(), moduleWorkshopKey),
    onSuccess: (r) => {
      setNewKey(''); setNewTitle('')
      qc.invalidateQueries({ queryKey: ['trainer-modules'] })
      navigate(`/trainer/modul/${r.data.key}/bearbeiten`)
    },
  })
  return (
    <Section title="Module präsentieren & bearbeiten">
      <QueryState query={presentMods} empty={presentMods.data?.length === 0}>
        <div className="flex flex-wrap gap-2">
          {presentMods.data?.map((m) => (
            <div key={m.key} className="flex items-center gap-1">
              <Link to={`/trainer/modul/${m.key}`} className="rounded-lg border px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-50">{m.title}</Link>
              <Link to={`/trainer/modul/${m.key}/bearbeiten`} title="Bearbeiten" aria-label={`${m.title} bearbeiten`}
                className="rounded-lg border px-2 py-1.5 text-slate-500 hover:bg-slate-50"><Icon name="pencil" className="h-4 w-4" /></Link>
            </div>
          ))}
        </div>
      </QueryState>
      <form onSubmit={(e) => { e.preventDefault(); newKey.trim() && newTitle.trim() && createContent.mutate() }} className="mt-4 flex flex-wrap items-end gap-2">
        <Field label="Key" placeholder="mein-modul" value={newKey} onChange={(e) => setNewKey(e.target.value)} />
        <Field label="Titel DE" placeholder="Mein Modul" value={newTitle} onChange={(e) => setNewTitle(e.target.value)} />
        <label className="flex flex-col gap-1 text-xs font-medium text-slate-600">Workshop
          <select value={moduleWorkshopKey} onChange={(e) => setModuleWorkshopKey(e.target.value)} className="rounded-lg border px-3 py-2 text-sm font-normal text-slate-900">
            {workshops.map((w) => <option key={w.key} value={w.key}>{w.title.de}</option>)}
          </select>
        </label>
        <button disabled={!newKey.trim() || !newTitle.trim() || createContent.isPending}
          className="inline-flex items-center gap-1 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white hover:bg-teal-700 disabled:opacity-50">
          <Icon name="plus" className="h-4 w-4" /> Neues Modul
        </button>
      </form>
      {createContent.isError && <p className="mt-1 text-sm text-rose-600">Anlegen fehlgeschlagen (Key ggf. vergeben).</p>}
    </Section>
  )
}

// --- Verwaltung: Trainer-Zugänge ---------------------------------------------

function TrainerAccounts() {
  const qc = useQueryClient()
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const accounts = useQuery({ queryKey: ['trainer-accounts'], queryFn: () => trainerApi.listTrainerAccounts().then((r) => r.data) })
  const create = useMutation({
    mutationFn: () => trainerApi.createTrainerAccount(email.trim(), name.trim(), password),
    onSuccess: () => { setEmail(''); setName(''); setPassword(''); setError(''); qc.invalidateQueries({ queryKey: ['trainer-accounts'] }) },
    onError: (e) => setError(errMsg(e)),
  })
  const remove = useMutation({
    mutationFn: (id: number) => trainerApi.deleteTrainerAccount(id),
    onSuccess: () => { setError(''); qc.invalidateQueries({ queryKey: ['trainer-accounts'] }) },
    onError: (e) => setError(errMsg(e)),
  })
  return (
    <Section title="Trainer-Zugänge">
      <QueryState query={accounts} empty={accounts.data?.length === 0}>
        <div className="mb-3 flex flex-col gap-1.5">
          {accounts.data?.map((t) => (
            <div key={t.id} className="flex items-center justify-between text-sm">
              <span className="text-slate-700">{t.name} <span className="text-slate-400">({t.email})</span></span>
              <button onClick={() => remove.mutate(t.id)} aria-label={`${t.name} entfernen`}
                className="text-rose-600 hover:text-rose-700"><Icon name="trash" className="h-4 w-4" /></button>
            </div>
          ))}
        </div>
      </QueryState>
      <form onSubmit={(e) => { e.preventDefault(); email.trim() && name.trim() && password && create.mutate() }} className="flex flex-wrap items-end gap-2">
        <Field label="E-Mail" type="email" autoComplete="off" placeholder="neu@beispiel.de" value={email} onChange={(e) => setEmail(e.target.value)} />
        <Field label="Name" placeholder="Vorname" value={name} onChange={(e) => setName(e.target.value)} />
        <Field label="Passwort" type="password" autoComplete="new-password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button disabled={!email.trim() || !name.trim() || !password || create.isPending}
          className="inline-flex items-center gap-1 rounded-lg bg-teal-600 px-3 py-2 text-sm font-medium text-white hover:bg-teal-700 disabled:opacity-50">
          <Icon name="plus" className="h-4 w-4" /> Trainer
        </button>
      </form>
      {error && <p className="mt-1 text-sm text-rose-600">{error}</p>}
    </Section>
  )
}

// --- Verwaltung: Einstellungen + Changelog -----------------------------------

function SettingsBlock() {
  const qc = useQueryClient()
  const features = useQuery({ queryKey: ['features'], queryFn: () => trainerApi.features().then((r) => r.data) })
  const toggle = useMutation({
    mutationFn: (v: boolean) => trainerApi.setFeature(v),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['features'] }),
  })
  return (
    <Section title="Einstellungen">
      <QueryState query={features}>
        <label className="flex items-center gap-2 text-sm text-slate-700">
          <input type="checkbox" checked={features.data?.comments ?? false} disabled={toggle.isPending}
            onChange={(e) => toggle.mutate(e.target.checked)} />
          Feedback-Kommentare für Teilnehmer aktiv
        </label>
      </QueryState>
    </Section>
  )
}

function ChangelogBlock() {
  const changelog = useQuery({ queryKey: ['changelog'], queryFn: () => trainerApi.changelog().then((r) => r.data) })
  return (
    <Section title="Änderungslog">
      <QueryState query={changelog} empty={changelog.data?.length === 0}>
        <details>
          <summary className="cursor-pointer select-none text-sm text-slate-500 hover:text-slate-700">{changelog.data?.length ?? 0} Einträge anzeigen</summary>
          <div className="mt-3 flex max-h-96 flex-col gap-2 overflow-y-auto">
            {changelog.data?.map((e, i) => (
              <div key={i} className="rounded-lg border bg-white p-3">
                <div className="flex items-baseline justify-between gap-2">
                  <span className="text-sm font-medium text-slate-800">{e.title}</span>
                  <span className="shrink-0 text-xs text-slate-400">{e.date}</span>
                </div>
                <p className="mt-1 text-sm text-slate-600">{e.text}</p>
              </div>
            ))}
          </div>
        </details>
      </QueryState>
    </Section>
  )
}

// --- Verwaltung: Audit-Protokoll ----------------------------------------------

function AuditLogBlock() {
  const audit = useQuery({ queryKey: ['audit-log'], queryFn: () => trainerApi.auditLog().then((r) => r.data) })
  return (
    <Section title="Protokoll">
      <QueryState query={audit} empty={audit.data?.length === 0}>
        <details>
          <summary className="cursor-pointer select-none text-sm text-slate-500 hover:text-slate-700">
            Letzte {audit.data?.length ?? 0} Aktionen anzeigen
          </summary>
          <div className="mt-3 flex max-h-96 flex-col gap-2 overflow-y-auto">
            {audit.data?.map((e) => (
              <div key={e.id} className="rounded-lg border bg-white p-3 text-sm">
                <div className="flex items-baseline justify-between gap-2">
                  <span className="font-medium text-slate-800">{e.action}</span>
                  <span className="shrink-0 text-xs text-slate-400">{new Date(e.created_at).toLocaleString('de-DE')}</span>
                </div>
                <p className="mt-1 text-slate-600">
                  {e.trainer_email}
                  {e.target ? <> · {e.target}</> : null}
                  {e.detail ? <> · {e.detail}</> : null}
                </p>
              </div>
            ))}
          </div>
        </details>
      </QueryState>
    </Section>
  )
}
