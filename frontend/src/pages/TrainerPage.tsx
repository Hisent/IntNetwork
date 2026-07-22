import { useEffect, useId, useRef, useState, type ReactNode } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { authApi, errMsg } from '@/lib/api'
import { t, type Lang } from '@/lib/i18n'
import { trainerApi, type Course } from '@/lib/trainerApi'
import { TrainerFeedback } from '@/components/TrainerFeedback'
import { useAuthStore } from '@/store/auth'
import { VersionBadge } from '@/components/VersionBadge'
import { workshopApi } from '@/lib/workshopApi'
import { BrandLogo } from '@/components/BrandLogo'
import { ThemeToggle } from '@/components/ThemeToggle'
import { Icon } from '@/components/Icon'
import { groupModulesByWorkshop } from '@/lib/trainerModules'
import { groupModulesBySection } from '@/lib/moduleGroups'
import { ConfirmDialog } from '@/components/ConfirmDialog'
import type { ModuleMeta, Workshop } from '@/types'
// Eigenständiger Lazy-Chunk (siehe App.tsx) — ohne diesen Import würde ein
// Teilnehmer, der nie /lernen besucht, die Tokens hier nie geladen bekommen.
import '@/components/workbench/workbench.css'

// --- kleine Bausteine ---------------------------------------------------------
// Ab hier durchgehend auf den Token-Klassen aus workbench.css (--wb-surface,
// --wb-ink, --wb-muted, --wb-border, --wb-accent, --wb-accent-soft) statt
// rohem slate/teal/white — damit sich das Trainer-Dashboard wie Teil derselben
// Anwendung anfühlt und Dark Mode ohne Sonderregeln erbt (Umschaltung über
// die .workbench-Wurzel in TrainerDashboard/TrainerLogin unten).

function Field({ label, className = '', ...props }: { label: string } & React.InputHTMLAttributes<HTMLInputElement>) {
  const id = useId()
  return (
    <label htmlFor={id} className="flex min-w-40 flex-1 flex-col gap-1 text-xs font-medium text-[var(--wb-muted)]">
      {label}
      <input id={id} className={`wb-control rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-3 py-2 text-sm font-normal text-[var(--wb-ink)] outline-none focus:border-[var(--wb-accent)] focus:ring-2 focus:ring-[var(--wb-accent-soft)] ${className}`} {...props} />
    </label>
  )
}

function Section({ title, action, children, className = '' }: { title: string; action?: ReactNode; children: ReactNode; className?: string }) {
  return (
    <section className={`wb-surface p-4 ${className}`}>
      <div className="mb-3 flex items-center justify-between gap-2">
        <h3 className="text-sm font-semibold text-[var(--wb-ink)]">{title}</h3>
        {action}
      </div>
      {children}
    </section>
  )
}

function QueryState({ query, empty, children }: { query: { isLoading: boolean; isError: boolean }; empty?: boolean; children: ReactNode }) {
  if (query.isLoading) return <p className="text-sm text-[var(--wb-muted)]">Lädt …</p>
  if (query.isError) return <p className="text-sm text-rose-600">Konnte nicht geladen werden.</p>
  if (empty) return <p className="text-sm text-[var(--wb-muted)]">Nichts vorhanden.</p>
  return <>{children}</>
}

function CopyCode({ code, lang = 'de' as Lang }: { code: string; lang?: Lang }) {
  const [copied, setCopied] = useState(false)
  return (
    <span className="relative inline-flex shrink-0">
      <button
        onClick={(e) => {
          e.stopPropagation()
          navigator.clipboard.writeText(code)
          setCopied(true)
          setTimeout(() => setCopied(false), 1500)
        }}
        title="Kurs-Code kopieren"
        className="font-mono text-sm text-[var(--wb-accent)] hover:text-[var(--wb-accent-hover)] hover:underline"
      >
        {copied ? `${t(lang, 'copiedCode')} ✓` : code}
      </button>
      <span aria-live="polite" className="sr-only">{copied ? t(lang, 'copiedCode') : ''}</span>
    </span>
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
  const [busy, setBusy] = useState(false)
  async function submit(e: React.FormEvent) {
    e.preventDefault()
    if (busy) return
    setErr(''); setBusy(true)
    try { onLogin((await authApi.trainerLogin(email, pw)).data.access_token) }
    catch { setErr('Login fehlgeschlagen.') }
    finally { setBusy(false) }
  }
  return (
    <div className="workbench flex min-h-dvh items-center justify-center p-4">
      <form onSubmit={submit} className="wb-surface flex w-full max-w-sm flex-col gap-3 p-8 shadow">
        <Link to="/" className="mb-3"><BrandLogo className="h-9 text-lg" showName /></Link>
        <h1 className="text-xl font-bold text-[var(--wb-ink)]">Trainer-Login</h1>
        <Field label="E-Mail" type="email" autoComplete="username" placeholder="trainer@beispiel.de" value={email} onChange={(e) => setEmail(e.target.value)} />
        <Field label="Passwort" type="password" autoComplete="current-password" placeholder="••••••••" value={pw} onChange={(e) => setPw(e.target.value)} />
        {err && <p className="text-sm text-rose-600">{err}</p>}
        <button disabled={busy} className="wb-control mt-1 rounded-lg bg-[var(--wb-accent)] py-2 font-medium text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50 disabled:cursor-not-allowed">{busy ? 'Meldet an…' : 'Anmelden'}</button>
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
  // Portal-Ziel für ConfirmDialog: die --wb-*-Tokens werden nur innerhalb
  // dieser .workbench-Wurzel definiert (siehe workbench.css). Ein Portal nach
  // document.body (wie GlossaryPanel.tsx es macht) läge außerhalb davon und
  // die Dialogkarte bliebe ohne Hintergrundfarbe.
  const workbenchRootRef = useRef<HTMLDivElement | null>(null)

  return (
    <div className="workbench p-6 sm:p-10" ref={workbenchRootRef}>
      <div className="mx-auto max-w-6xl">
        <header className="mb-8 flex items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <Link to="/"><BrandLogo className="h-9 text-lg" showName /></Link>
            <h1 className="text-2xl font-bold text-[var(--wb-ink)]">Trainer</h1>
            <VersionBadge tone="dark" />
          </div>
          <div className="flex items-center gap-2">
            <ThemeToggle className="text-[var(--wb-muted)]" />
            <button onClick={onLogout} className="text-sm text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">Abmelden</button>
          </div>
        </header>

        {/* Master-Detail: Kurse wählen (links) → Kurs-Detail (rechts) */}
        <h2 className="mb-4 text-xs font-bold uppercase tracking-[0.16em] text-[var(--wb-muted)]">Kursübersicht</h2>
        <div className="grid gap-6 lg:grid-cols-[340px_minmax(0,1fr)] lg:items-start">
          <CourseList
            courses={courses} workshopTitle={workshopTitle} workshops={workshops.data ?? []}
            selected={selected} onSelect={setSelected} />
          <div className="min-w-0">
            {selectedCourse
              ? <CourseDetail course={selectedCourse} workshopTitle={workshopTitle} workshops={workshops.data ?? []} portalContainer={workbenchRootRef.current} />
              : <div className="grid h-full min-h-48 place-items-center rounded-xl border border-dashed border-[var(--wb-border)] p-8 text-center text-sm text-[var(--wb-muted)]">
                  Kurs links auswählen, um Module, Präsenz, Feedback und Fortschritt zu sehen.
                </div>}
          </div>
        </div>

        {/* Verwaltung: globale, kursunabhängige Bereiche. Gewichtet statt
            gleichrangig aneinandergereiht — siehe Begründung je Zeile unten. */}
        <div className="mt-12">
          <h2 className="mb-4 text-xs font-bold uppercase tracking-[0.16em] text-[var(--wb-muted)]">Verwaltung</h2>
          <div className="flex flex-col gap-6">
            {/* Primär: Modulverwaltung ist das täglich genutzte Werkzeug
                (Content-Erstellung/-Pflege) — volle Breite, oben, ungeklappt. */}
            <ModuleAdmin workshops={workshops.data ?? []} />
            {/* Sekundär: beide werden regelmäßig, aber deutlich seltener als
                Module gebraucht (neuer Trainer-Zugang, gelegentliche
                Einstellung) — gleichrangig nebeneinander, kleiner als oben. */}
            <div className="grid gap-6 lg:grid-cols-2">
              <TrainerAccounts portalContainer={workbenchRootRef.current} />
              <SettingsBlock />
            </div>
            {/* Tertiär: reine Nachschlage-Protokolle, kein Werkzeug für den
                Alltag — nachrangig platziert und per <details> geschlossen. */}
            <div className="grid gap-6 lg:grid-cols-2">
              <ChangelogBlock />
              <AuditLogBlock />
            </div>
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
    <section className="wb-surface p-4 lg:sticky lg:top-6">
      <h3 className="mb-3 text-sm font-semibold text-[var(--wb-ink)]">Kurse</h3>
      <form onSubmit={(e) => { e.preventDefault(); name.trim() && create.mutate() }} className="mb-4 flex flex-col gap-2">
        <Field label="Neuer Kurs" placeholder="Kurs-Name" value={name} onChange={(e) => setName(e.target.value)} />
        <label className="flex flex-col gap-1 text-xs font-medium text-[var(--wb-muted)]">Workshop
          <select value={workshopKey} onChange={(e) => setWorkshopKey(e.target.value)} className="wb-control rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-3 py-2 text-sm font-normal text-[var(--wb-ink)]">
            {workshops.map((w) => <option key={w.key} value={w.key}>{w.title.de}</option>)}
          </select>
        </label>
        <button disabled={!name.trim() || create.isPending}
          className="wb-control inline-flex items-center justify-center gap-1 rounded-lg bg-[var(--wb-accent)] px-4 text-sm font-medium text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50">
          <Icon name="plus" className="h-4 w-4" /> Kurs anlegen
        </button>
        {create.isError && <p className="text-xs text-rose-600">Anlegen fehlgeschlagen.</p>}
      </form>

      <QueryState query={courses} empty={courses.data?.length === 0}>
        <ul className="flex flex-col gap-1.5">
          {courses.data?.map((c) => (
            <li key={c.id}
              className={`flex items-start justify-between gap-2 rounded-lg p-3 transition-colors ${
                selected === c.id ? 'bg-[var(--wb-accent-soft)] ring-1 ring-[var(--wb-accent)]/40' : 'hover:bg-[var(--wb-subtle)]'}`}>
              {/* Eigener <button> statt div[role=button] — kein verschachteltes
                  Interaktionselement mehr mit dem Kopieren-Button daneben. */}
              <button type="button" onClick={() => onSelect(c.id)} aria-pressed={selected === c.id}
                className="min-w-0 flex-1 text-left">
                <span className="block min-w-0 truncate font-medium text-[var(--wb-ink)]">{c.name}</span>
                <span className="mt-1 flex items-center gap-3 text-xs text-[var(--wb-muted)]">
                  <span>{workshopTitle(c.workshop_key)}</span>
                  <span className="inline-flex items-center gap-1"><Icon name="users" className="h-3.5 w-3.5" />{c.participant_count ?? 0}</span>
                </span>
              </button>
              <CopyCode code={c.join_code} />
            </li>
          ))}
        </ul>
      </QueryState>
    </section>
  )
}

// --- Kurs-Detail (Detail) -----------------------------------------------------

function CourseDetail({ course, workshopTitle, workshops, portalContainer }: { course: Course; workshopTitle: (key: string | null) => string; workshops: Workshop[]; portalContainer: HTMLElement | null }) {
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

  // Eigener Bestätigungsdialog statt window.confirm() für die einzige
  // unwiderrufliche Aktion hier: Teilnehmer inkl. Fortschritt löschen.
  // deleteTarget hält Name+ID für den Dialogtext, deleteTriggerRef das
  // anklickte <button>-Element, damit der Fokus beim Schließen dorthin
  // zurückkehrt (statt auf ein generisches Element).
  const [deleteTarget, setDeleteTarget] = useState<{ id: number; name: string } | null>(null)
  const deleteTriggerRef = useRef<HTMLButtonElement | null>(null)

  // "Module in diesem Kurs" gehört zu genau einem Workshop (der des Kurses) —
  // anders als ModuleAdmin unten, das über ALLE Workshops hinweg gruppiert.
  // Trotzdem sind es bei network/claude-code je ~17-18 Module, flach als
  // Checkbox-Wand kaum überblickbar. Statt ModuleAdmins Suchfeld + zuklappbare
  // Gruppen (gedacht für Content-Pflege über 30+ Module) reicht hier die
  // ohnehin vorhandene Tages-/Themen-Gliederung des Workshops
  // (groupModulesBySection, dieselbe wie in LearnPage/ModulePage für
  // Teilnehmer) — 4-6 Module je Abschnitt bleiben auf einen Blick lesbar.
  // Kein Suchfeld (bei dieser Größe kein Skalierungsproblem) und Gruppen
  // bleiben offen statt <details>: hier soll ein Trainer mehrere Module in
  // Folge an-/abwählen, nicht erst pro Abschnitt aufklappen.
  const courseModulesByKey = new Map(courseMods.data?.map((m) => [m.key, m]))
  const courseModuleMetas: ModuleMeta[] = (courseMods.data ?? []).map((m) => (
    { key: m.key, title: m.title, title_en: m.title, order: m.order, prerequisites: [], workshop_key: m.workshop_key ?? undefined }
  ))
  const courseWorkshop = workshops.find((w) => w.key === course.workshop_key)
  const courseModuleGroups = groupModulesBySection(courseModuleMetas, courseWorkshop?.sections)

  return (
    <div className="flex flex-col gap-6">
      <div className="wb-surface p-4">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h2 className="text-lg font-bold text-[var(--wb-ink)]">{course.name}</h2>
          <span className="text-xs text-[var(--wb-muted)]">{workshopTitle(course.workshop_key)} · {course.participant_count ?? 0} Teilnehmer · Code <span className="font-mono">{course.join_code}</span></span>
        </div>
      </div>

      <Section title="Gerade aktiv">
        <QueryState query={presence} empty={presence.data?.length === 0}>
          <div className="flex flex-col gap-1.5">
            {presence.data?.map((entry) => (
              <div key={entry.name} className="flex justify-between text-sm">
                <span className="text-[var(--wb-ink)]">{entry.name}</span>
                <span className="text-[var(--wb-muted)]">{entry.module_title}</span>
              </div>
            ))}
          </div>
        </QueryState>
      </Section>

      <Section title="Module in diesem Kurs">
        <QueryState query={courseMods} empty={courseMods.data?.length === 0}>
          <div className="flex flex-col gap-3">
            {courseModuleGroups.map((g) => (
              <div key={g.key}>
                {courseModuleGroups.length > 1 && (
                  <p className="mb-1 px-0.5 text-[10px] font-semibold uppercase tracking-wide text-[var(--wb-muted)]">{g.title_de}</p>
                )}
                <div className="grid gap-1.5 sm:grid-cols-2">
                  {g.modules.map((meta) => {
                    const m = courseModulesByKey.get(meta.key)
                    if (!m) return null
                    return (
                      <label key={m.key} className="flex items-center gap-2 text-sm text-[var(--wb-ink)]">
                        <input type="checkbox" checked={m.active} disabled={toggleMod.isPending}
                          onChange={(e) => toggleMod.mutate({ module_key: m.key, active: e.target.checked })} />
                        {m.title}
                      </label>
                    )
                  })}
                </div>
              </div>
            ))}
          </div>
        </QueryState>
      </Section>

      <Section title="Fortschritt" action={
        <label className="flex items-center gap-1.5 text-xs font-normal text-[var(--wb-muted)]">
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
                <span className="min-w-0 truncate text-[var(--wb-ink)]">{p.name}</span>
                <div className="flex shrink-0 items-center gap-2">
                  <button onClick={() => resetCode.mutate(p.id)} disabled={resetCode.isPending}
                    className="text-xs text-[var(--wb-muted)] hover:text-[var(--wb-accent-hover)]">Code zurücksetzen</button>
                  <button
                    onClick={(e) => { deleteTriggerRef.current = e.currentTarget; setDeleteTarget({ id: p.id, name: p.name }) }}
                    aria-label={`${p.name} löschen`} className="text-rose-600 hover:text-rose-700"><Icon name="trash" className="h-4 w-4" /></button>
                </div>
              </div>
            ))}
          </div>
        </QueryState>
        {shownCode && (
          <p className="mt-3 rounded-lg bg-[var(--wb-accent-soft)] px-3 py-2 text-sm text-[var(--wb-ink)]">
            Neuer Wiederaufnahme-Code für <b>{shownCode.name}</b>: <code className="select-all font-mono font-bold">{shownCode.code}</code> — bitte persönlich weitergeben.
          </p>
        )}
        <ConfirmDialog
          open={deleteTarget !== null}
          title="Teilnehmer löschen"
          description={<>„{deleteTarget?.name}“ endgültig löschen? Fortschritt, Quizergebnisse und Teilnahmebestätigung gehen unwiderruflich mit verloren.</>}
          confirmLabel="Endgültig löschen"
          cancelLabel="Abbrechen"
          triggerRef={deleteTriggerRef}
          container={portalContainer}
          onConfirm={() => { if (deleteTarget) removeParticipant.mutate(deleteTarget.id); setDeleteTarget(null) }}
          onCancel={() => setDeleteTarget(null)}
        />
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
  // Scroll-Andeutung statt hartem Abbruch am Kartenrand: klassischer CSS-only
  // "Scroll-Schatten" (vier Hintergrund-Ebenen, zwei davon scroll-fix
  // positioniert, zwei mit dem Inhalt mitscrollend). Der Trick blendet den
  // Schatten automatisch aus, sobald man an den jeweiligen Rand gescrollt
  // ist bzw. wenn gar nichts zu scrollen ist — keine JS-Scroll-Messung nötig.
  // Farben über --wb-surface/--wb-border, damit es in beiden Themes passt.
  // Wichtig: die globale Regel ".workbench table" (workbench.css) setzt JEDE
  // Tabelle in diesem Bereich selbst auf display:block + overflow-x:auto —
  // dadurch scrollt hier tatsächlich die <table>, nicht der umgebende
  // .overflow-x-auto-Div (der bleibt ohne eigenen Overflow). Der Schatten muss
  // deshalb an der Tabelle selbst hängen, sonst bewegt er sich nie mit.
  const scrollShadowStyle: React.CSSProperties = {
    backgroundImage:
      'linear-gradient(to right, var(--wb-surface) 30%, transparent),' +
      'linear-gradient(to left, var(--wb-surface) 30%, transparent),' +
      'radial-gradient(farthest-side at 0 50%, var(--wb-border), transparent),' +
      'radial-gradient(farthest-side at 100% 50%, var(--wb-border), transparent)',
    backgroundPosition: 'left, right, left, right',
    backgroundRepeat: 'no-repeat',
    backgroundColor: 'var(--wb-surface)',
    backgroundSize: '32px 100%, 32px 100%, 12px 100%, 12px 100%',
    backgroundAttachment: 'local, local, scroll, scroll',
  }
  return (
    <QueryState query={dash}>
      <div className="overflow-x-auto">
        <table className="w-full border-separate border-spacing-0 text-sm" style={scrollShadowStyle}>
          <thead>
            <tr>
              <th className="sticky left-0 z-10 bg-[var(--wb-subtle)] px-3 py-2 text-left font-semibold text-[var(--wb-ink)]">Teilnehmer</th>
              {dash.data?.modules.map((m) => <th key={m.key} className="whitespace-nowrap bg-[var(--wb-subtle)] px-3 py-2 text-xs font-medium text-[var(--wb-muted)]">{m.title}</th>)}
              {requireApproval && <th className="whitespace-nowrap bg-[var(--wb-subtle)] px-3 py-2 text-xs font-medium text-[var(--wb-muted)]">Freigabe</th>}
            </tr>
          </thead>
          <tbody>
            {dash.data?.participants.map((p) => (
              <tr key={p.id}>
                <td className="sticky left-0 z-10 border-t border-[var(--wb-border)] bg-[var(--wb-surface)] px-3 py-2 font-medium text-[var(--wb-ink)]">{p.name}</td>
                {dash.data!.modules.map((m) => {
                  const cell = p.cells[m.key]
                  return (
                    <td key={m.key} className="border-t border-[var(--wb-border)] px-3 py-2 text-center">
                      {cell?.done
                        ? <span className="inline-flex items-center gap-1 text-[var(--wb-success)]"><Icon name="check" className="h-4 w-4" />{cell.best != null ? <span className="text-xs text-[var(--wb-muted)]">{cell.best}%</span> : null}</span>
                        : <span className="text-[var(--wb-muted)] opacity-50">–</span>}
                    </td>
                  )
                })}
                {requireApproval && (
                  <td className="border-t border-[var(--wb-border)] px-3 py-2 text-center">
                    <input type="checkbox" checked={p.approved} onChange={(e) => onApprove(p.id, e.target.checked)}
                      aria-label={`${p.name} freigeben`} />
                  </td>
                )}
              </tr>
            ))}
            {dash.data?.participants.length === 0 && (
              <tr><td colSpan={(dash.data?.modules.length ?? 0) + (requireApproval ? 2 : 1)} className="px-3 py-6 text-center text-[var(--wb-muted)]">Noch keine Teilnehmer.</td></tr>
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
  const [filter, setFilter] = useState('')
  // Welche Workshop-Gruppen der Nutzer manuell aufgeklappt hat (Key der
  // Gruppe). Start: leer, also alle Gruppen zu.
  const [openGroups, setOpenGroups] = useState<Set<string>>(new Set())
  const presentMods = useQuery({ queryKey: ['trainer-modules'], queryFn: () => trainerApi.trainerModules().then((r) => r.data) })
  const createContent = useMutation({
    mutationFn: () => trainerApi.createContentModule(newKey.trim(), newTitle.trim(), moduleWorkshopKey),
    onSuccess: (r) => {
      setNewKey(''); setNewTitle('')
      qc.invalidateQueries({ queryKey: ['trainer-modules'] })
      navigate(`/trainer/modul/${r.data.key}/bearbeiten`)
    },
  })
  // Bei ~35 Modulen über zwei Workshops verteilt skaliert eine flache Pill-Wand
  // nicht mehr — daher Gruppierung nach Workshop plus Titel-Filter.
  const needle = filter.trim().toLowerCase()
  const filtered = presentMods.data?.filter((m) => m.title.toLowerCase().includes(needle)) ?? []
  const groups = groupModulesByWorkshop(filtered, workshops)
  // Gruppen sind <details>: standardmäßig zu (spart Tab-Stopps auf dem Weg zu
  // den Karten darunter — bei ~35 Zeilen mit je zwei fokussierbaren Elementen
  // macht das den Unterschied zwischen ~70 und wenigen Tabs). Sobald gesucht
  // wird, klappen Treffergruppen automatisch auf, damit der Filter sofort
  // etwas zeigt; manuelles Auf-/Zuklappen bleibt über openGroups erhalten.
  const isGroupOpen = (key: string) => needle !== '' || openGroups.has(key)
  return (
    <Section title="Module präsentieren & bearbeiten">
      <label className="mb-3 flex max-w-xs flex-col gap-1 text-xs font-medium text-[var(--wb-muted)]">
        Modul suchen
        <input value={filter} onChange={(e) => setFilter(e.target.value)} placeholder="Titel filtern …"
          className="wb-control rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-3 py-2 text-sm font-normal text-[var(--wb-ink)]" />
      </label>
      <QueryState query={presentMods} empty={presentMods.data?.length === 0}>
        {filtered.length === 0
          ? <p className="text-sm text-[var(--wb-muted)]">Keine Module gefunden.</p>
          : <div className="flex flex-col gap-2">
              {groups.map((g) => (
                <details key={g.key} className="group" open={isGroupOpen(g.key)}
                  onToggle={(e) => {
                    const isOpen = e.currentTarget.open
                    setOpenGroups((prev) => {
                      const next = new Set(prev)
                      if (isOpen) next.add(g.key); else next.delete(g.key)
                      return next
                    })
                  }}>
                  {/* Label allein hätte hier über den Zustand gelogen (bleibt
                      als reiner Gruppentitel korrekt, aber ohne jede
                      Rückmeldung ob auf-/zugeklappt). Pfeil dreht sich rein
                      über CSS (group-open:), NICHT über ein kontrolliertes
                      open-Prop — sonst würde ein Tastendruck im Suchfeld
                      (das isGroupOpen()/open oben steuert) den Pfeil aus dem
                      Tritt bringen, während <details> selbst uncontrolled
                      bleiben muss (siehe onToggle-Kommentar in ModuleAdmin). */}
                  <summary className="wb-control flex cursor-pointer select-none items-center gap-2 rounded-lg px-1 text-xs font-semibold uppercase tracking-wide text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">
                    <Icon name="arrowRight" className="h-3.5 w-3.5 shrink-0 transition-transform duration-150 group-open:rotate-90" />
                    {g.title} <span className="font-normal normal-case tracking-normal">({g.modules.length})</span>
                  </summary>
                  <ul className="flex flex-col divide-y divide-[var(--wb-border)]">
                    {g.modules.map((m) => (
                      <li key={m.key} className="flex items-center justify-between gap-2 py-1.5">
                        <Link to={`/trainer/modul/${m.key}`} className="min-w-0 truncate text-sm text-[var(--wb-ink)] hover:text-[var(--wb-accent-hover)] hover:underline">{m.title}</Link>
                        <Link to={`/trainer/modul/${m.key}/bearbeiten`} title="Bearbeiten" aria-label={`${m.title} bearbeiten`}
                          className="shrink-0 rounded-lg p-1.5 text-[var(--wb-muted)] hover:bg-[var(--wb-subtle)] hover:text-[var(--wb-ink)]"><Icon name="pencil" className="h-4 w-4" /></Link>
                      </li>
                    ))}
                  </ul>
                </details>
              ))}
            </div>}
      </QueryState>
      <form onSubmit={(e) => { e.preventDefault(); newKey.trim() && newTitle.trim() && createContent.mutate() }} className="mt-4 flex flex-wrap items-end gap-2">
        <Field label="Key" placeholder="mein-modul" value={newKey} onChange={(e) => setNewKey(e.target.value)} />
        <Field label="Titel DE" placeholder="Mein Modul" value={newTitle} onChange={(e) => setNewTitle(e.target.value)} />
        <label className="flex flex-col gap-1 text-xs font-medium text-[var(--wb-muted)]">Workshop
          <select value={moduleWorkshopKey} onChange={(e) => setModuleWorkshopKey(e.target.value)} className="wb-control rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-3 py-2 text-sm font-normal text-[var(--wb-ink)]">
            {workshops.map((w) => <option key={w.key} value={w.key}>{w.title.de}</option>)}
          </select>
        </label>
        <button disabled={!newKey.trim() || !newTitle.trim() || createContent.isPending}
          className="wb-control inline-flex items-center gap-1 rounded-lg bg-[var(--wb-accent)] px-3 text-sm font-medium text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50">
          <Icon name="plus" className="h-4 w-4" /> Neues Modul
        </button>
      </form>
      {createContent.isError && <p className="mt-1 text-sm text-rose-600">Anlegen fehlgeschlagen (Key ggf. vergeben).</p>}
    </Section>
  )
}

// --- Verwaltung: Trainer-Zugänge ---------------------------------------------

function TrainerAccounts({ portalContainer }: { portalContainer: HTMLElement | null }) {
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
  // Gleiches Sicherheitsniveau wie beim Teilnehmer-Löschen weiter oben in
  // dieser Datei: ein Trainer-Zugang ist der eigene Login-Zugriff, nicht nur
  // ein Datensatz — sofortiges Löschen per Klick (ohne Rückfrage) hätte hier
  // ein höheres Risiko als beim Teilnehmer. Derselbe ConfirmDialog statt
  // eines zweiten, damit sich beide Löschwege gleich anfühlen.
  const [deleteTarget, setDeleteTarget] = useState<{ id: number; name: string } | null>(null)
  const deleteTriggerRef = useRef<HTMLButtonElement | null>(null)
  return (
    <Section title="Trainer-Zugänge">
      <QueryState query={accounts} empty={accounts.data?.length === 0}>
        <div className="mb-3 flex flex-col gap-1.5">
          {accounts.data?.map((t) => (
            <div key={t.id} className="flex items-center justify-between text-sm">
              <span className="text-[var(--wb-ink)]">{t.name} <span className="text-[var(--wb-muted)]">({t.email})</span></span>
              <button
                onClick={(e) => { deleteTriggerRef.current = e.currentTarget; setDeleteTarget({ id: t.id, name: t.name }) }}
                aria-label={`${t.name} entfernen`} className="text-rose-600 hover:text-rose-700"><Icon name="trash" className="h-4 w-4" /></button>
            </div>
          ))}
        </div>
      </QueryState>
      <form onSubmit={(e) => { e.preventDefault(); email.trim() && name.trim() && password && create.mutate() }} className="flex flex-wrap items-end gap-2">
        <Field label="E-Mail" type="email" autoComplete="off" placeholder="neu@beispiel.de" value={email} onChange={(e) => setEmail(e.target.value)} />
        <Field label="Name" placeholder="Vorname" value={name} onChange={(e) => setName(e.target.value)} />
        <Field label="Passwort" type="password" autoComplete="new-password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button disabled={!email.trim() || !name.trim() || !password || create.isPending}
          className="wb-control inline-flex items-center gap-1 rounded-lg bg-[var(--wb-accent)] px-3 text-sm font-medium text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50">
          <Icon name="plus" className="h-4 w-4" /> Trainer
        </button>
      </form>
      {error && <p className="mt-1 text-sm text-rose-600">{error}</p>}
      <ConfirmDialog
        open={deleteTarget !== null}
        title="Trainer-Zugang entfernen"
        description={<>Zugang von „{deleteTarget?.name}“ endgültig entfernen? Die Person kann sich danach nicht mehr anmelden.</>}
        confirmLabel="Endgültig entfernen"
        cancelLabel="Abbrechen"
        triggerRef={deleteTriggerRef}
        container={portalContainer}
        onConfirm={() => { if (deleteTarget) remove.mutate(deleteTarget.id); setDeleteTarget(null) }}
        onCancel={() => setDeleteTarget(null)}
      />
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
        <label className="flex items-center gap-2 text-sm text-[var(--wb-ink)]">
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
    <Section title="Änderungslog" className="opacity-90">
      <QueryState query={changelog} empty={changelog.data?.length === 0}>
        <details>
          <summary className="wb-control cursor-pointer select-none text-sm text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">{changelog.data?.length ?? 0} Einträge anzeigen</summary>
          <ul className="mt-3 flex max-h-96 flex-col divide-y divide-[var(--wb-border)] overflow-y-auto">
            {changelog.data?.map((e, i) => (
              <li key={i} className="py-2">
                <div className="flex items-baseline justify-between gap-2">
                  <span className="text-sm font-medium text-[var(--wb-ink)]">{e.title}</span>
                  <span className="shrink-0 text-xs text-[var(--wb-muted)]">{e.date}</span>
                </div>
                <p className="mt-1 text-sm text-[var(--wb-muted)]">{e.text}</p>
              </li>
            ))}
          </ul>
        </details>
      </QueryState>
    </Section>
  )
}

// --- Verwaltung: Audit-Protokoll ----------------------------------------------

const AUDIT_PAGE_SIZE = 50

function AuditLogBlock() {
  // Nachschlagewerk statt Analysewerkzeug: erste Seite laden, weitere Seiten
  // nur auf Anfrage per Button nachladen — kein Filter/Suchfeld, der
  // Backend-Endpunkt unterstützt limit/offset bereits (siehe trainer_audit.py).
  const first = useQuery({
    queryKey: ['audit-log', 'first'],
    queryFn: () => trainerApi.auditLog(AUDIT_PAGE_SIZE, 0).then((r) => r.data),
  })
  const [entries, setEntries] = useState<import('@/lib/trainerApi').AuditLogEntry[]>([])
  const [hasMore, setHasMore] = useState(false)
  const [loadingMore, setLoadingMore] = useState(false)

  useEffect(() => {
    if (first.data) {
      setEntries(first.data)
      setHasMore(first.data.length === AUDIT_PAGE_SIZE)
    }
  }, [first.data])

  async function loadMore() {
    setLoadingMore(true)
    try {
      const next = await trainerApi.auditLog(AUDIT_PAGE_SIZE, entries.length).then((r) => r.data)
      setEntries((prev) => [...prev, ...next])
      setHasMore(next.length === AUDIT_PAGE_SIZE)
    } finally {
      setLoadingMore(false)
    }
  }

  return (
    <Section title="Protokoll" className="opacity-90">
      <QueryState query={first} empty={first.isSuccess && entries.length === 0}>
        <details>
          <summary className="wb-control cursor-pointer select-none text-sm text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">
            {entries.length}{hasMore ? '+' : ''} Aktionen anzeigen
          </summary>
          <ul className="mt-3 flex max-h-96 flex-col divide-y divide-[var(--wb-border)] overflow-y-auto">
            {entries.map((e) => (
              <li key={e.id} className="py-2 text-sm">
                <div className="flex items-baseline justify-between gap-2">
                  <span className="font-medium text-[var(--wb-ink)]">{e.action}</span>
                  <span className="shrink-0 text-xs text-[var(--wb-muted)]">{new Date(e.created_at).toLocaleString('de-DE')}</span>
                </div>
                <p className="mt-1 text-[var(--wb-muted)]">
                  {e.trainer_email}
                  {e.target ? <> · {e.target}</> : null}
                  {e.detail ? <> · {e.detail}</> : null}
                </p>
              </li>
            ))}
          </ul>
          {hasMore && (
            <button onClick={loadMore} disabled={loadingMore}
              className="mt-2 text-xs font-medium text-[var(--wb-accent)] hover:underline disabled:opacity-50">
              {loadingMore ? 'Lädt…' : 'Weitere laden'}
            </button>
          )}
        </details>
      </QueryState>
    </Section>
  )
}
