import { useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { trainerApi } from '@/lib/trainerApi'
import { useAuthStore } from '@/store/auth'
import { VersionBadge } from '@/components/VersionBadge'
import { workshopApi } from '@/lib/workshopApi'
import { BrandLogo } from '@/components/BrandLogo'
import { ThemeToggle } from '@/components/ThemeToggle'
import { TrainerLogin } from './trainer/TrainerLogin'
import { CourseList } from './trainer/CourseList'
import { CourseDetail } from './trainer/CourseDetail'
import { ModuleAdmin } from './trainer/ModuleAdmin'
import { TrainerAccounts } from './trainer/TrainerAccounts'
import { PasskeyAdmin } from './trainer/PasskeyAdmin'
import { SettingsBlock } from './trainer/SettingsBlock'
import { ChangelogBlock } from './trainer/ChangelogBlock'
import { AuditLogBlock } from './trainer/AuditLogBlock'
// Eigenständiger Lazy-Chunk (siehe App.tsx) — ohne diesen Import würde ein
// Teilnehmer, der nie /lernen besucht, die Tokens hier nie geladen bekommen.
import '@/components/workbench/workbench.css'

export function TrainerPage() {
  const { token, role, setAuth, logout } = useAuthStore()
  if (role !== 'trainer' || !token) return <TrainerLogin onLogin={(t) => setAuth(t, 'trainer')} />
  return <TrainerDashboard onLogout={logout} />
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
    <div id="main-content" tabIndex={-1} className="workbench p-6 sm:p-10" ref={workbenchRootRef}>
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
              ? <CourseDetail course={selectedCourse} workshopTitle={workshopTitle} workshops={workshops.data ?? []} portalContainer={workbenchRootRef.current} onDeleted={() => setSelected(null)} />
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
            {/* Eigener Login-Zugriff des Trainers, aber Einrichtung passiert
                einmalig (nicht im Tagesgeschäft) — daher eigene Zeile statt
                Verdrängung von TrainerAccounts/SettingsBlock aus der Reihe. */}
            <PasskeyAdmin portalContainer={workbenchRootRef.current} />
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
