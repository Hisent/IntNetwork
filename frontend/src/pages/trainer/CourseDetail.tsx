import { useEffect, useRef, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { trainerApi, type Course } from '@/lib/trainerApi'
import { TrainerFeedback } from '@/components/TrainerFeedback'
import { ConfirmDialog } from '@/components/ConfirmDialog'
import { Icon } from '@/components/Icon'
import { groupModulesBySection } from '@/lib/moduleGroups'
import { t } from '@/lib/i18n'
import type { ModuleMeta, Workshop } from '@/types'
import { Section, QueryState, CopyButton } from './shared'

// QR-Groesse: mittig im gewuenschten 160-200px-Fenster.
const INVITE_QR_PX = 176

// Lokal erzeugter QR-Code fuer den Einladungslink (CSP verbietet externe
// QR-Dienste wie api.qrserver.com — img-src ist nur 'self' data:, siehe
// nginx.conf). qrcode-generator ist dependency-frei und wird dynamisch
// importiert, damit die Encoding-Logik nicht im Haupt-Chunk landet (der
// Trainer-Bereich ist ohnehin schon als eigene Route lazy geladen).
function InviteQr({ link, alt }: { link: string; alt: string }) {
  const [dataUrl, setDataUrl] = useState<string | null>(null)
  useEffect(() => {
    let cancelled = false
    setDataUrl(null)
    import('qrcode-generator').then(({ default: qrcodeGen }) => {
      if (cancelled) return
      const qr = qrcodeGen(0, 'M')
      qr.addData(link)
      qr.make()
      // cellSize so waehlen, dass das fertige Bild ungefaehr INVITE_QR_PX
      // trifft — die Modulanzahl haengt von der Linklaenge ab (Auto-Version).
      const modules = qr.getModuleCount()
      const margin = 4
      const cellSize = Math.max(2, Math.round(INVITE_QR_PX / (modules + margin * 2)))
      setDataUrl(qr.createDataURL(cellSize, margin))
    })
    return () => { cancelled = true }
  }, [link])
  if (!dataUrl) {
    return <div className="shrink-0 animate-pulse rounded-lg bg-[var(--wb-subtle)]" style={{ width: INVITE_QR_PX, height: INVITE_QR_PX }} aria-hidden="true" />
  }
  return <img src={dataUrl} alt={alt} width={INVITE_QR_PX} height={INVITE_QR_PX} className="shrink-0 rounded-lg border border-[var(--wb-border)] bg-white p-2" />
}

// --- Kurs-Detail (Detail) -----------------------------------------------------

export function CourseDetail({ course, workshopTitle, workshops, portalContainer, onDeleted }: { course: Course; workshopTitle: (key: string | null) => string; workshops: Workshop[]; portalContainer: HTMLElement | null; onDeleted: () => void }) {
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
  // Löscht den gesamten Kurs (Backend-Cascade: Teilnehmer, Fortschritt,
  // Kommentare gehen mit). onDeleted hebt die Auswahl im Elternteil auf,
  // damit hier keine CourseDetail mit ungültiger Kurs-ID hängen bleibt.
  const [deleteCourseConfirm, setDeleteCourseConfirm] = useState(false)
  const deleteCourseTriggerRef = useRef<HTMLButtonElement | null>(null)
  const deleteCourse = useMutation({
    mutationFn: () => trainerApi.deleteCourse(cid),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['courses'] }); onDeleted() },
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
        <div className="mt-3 flex justify-end">
          <button
            onClick={(e) => { deleteCourseTriggerRef.current = e.currentTarget; setDeleteCourseConfirm(true) }}
            disabled={deleteCourse.isPending}
            className="wb-control inline-flex items-center gap-1.5 rounded-lg border border-rose-300 bg-rose-50 px-3 text-sm font-semibold text-rose-700 hover:border-rose-400 disabled:opacity-50">
            <Icon name="trash" className="h-4 w-4" /> Kurs löschen
          </button>
        </div>
        {deleteCourse.isError && <p className="mt-2 text-right text-sm text-rose-600">Löschen fehlgeschlagen.</p>}
      </div>

      {course.workshop_key && (
        <Section title={t('de', 'inviteTitle')}>
          {(() => {
            const inviteLink = `${window.location.origin}/workshops/${course.workshop_key}?code=${course.join_code}`
            return (
              <div className="flex flex-col gap-4 sm:flex-row sm:items-start">
                <div className="min-w-0 flex-1">
                  <p className="text-sm text-[var(--wb-muted)]">{t('de', 'inviteHint')}</p>
                  <label className="mt-3 block text-xs font-semibold uppercase tracking-wide text-[var(--wb-muted)]">{t('de', 'inviteLinkLabel')}</label>
                  <div className="mt-1 flex items-center gap-2 rounded-lg border border-[var(--wb-border)] bg-[var(--wb-subtle)] px-3 py-2">
                    <code className="min-w-0 flex-1 truncate text-sm text-[var(--wb-ink)]">{inviteLink}</code>
                    <CopyButton text={inviteLink} label={t('de', 'copyLink')} />
                  </div>
                  {requireApproval && <p className="mt-2 text-xs text-amber-700">{t('de', 'inviteApprovalNote')}</p>}
                </div>
                <InviteQr link={inviteLink} alt={t('de', 'inviteQrAlt')} />
              </div>
            )
          })()}
        </Section>
      )}

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

      <ConfirmDialog
        open={deleteCourseConfirm}
        title="Kurs löschen"
        description={<>„{course.name}“ endgültig löschen? ALLE Teilnehmer, ihr Fortschritt und alle Kommentare dieses Kurses werden unwiderruflich mitgelöscht.</>}
        confirmLabel="Endgültig löschen"
        cancelLabel="Abbrechen"
        triggerRef={deleteCourseTriggerRef}
        container={portalContainer}
        onConfirm={() => { deleteCourse.mutate(); setDeleteCourseConfirm(false) }}
        onCancel={() => setDeleteCourseConfirm(false)}
      />
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
