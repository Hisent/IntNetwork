import { useEffect, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { trainerApi } from '@/lib/trainerApi'
import { errMsg } from '@/lib/api'
import { PollOptions } from '@/components/LivePoll'
import type { LivePoll } from '@/types'
import { TrainerBlocks } from '@/components/TrainerBlocks'
import { MD_COMPONENTS } from '@/components/Blocks'
import { useAuthStore } from '@/store/auth'
import { BrandLogo } from '@/components/BrandLogo'
import { WorkshopTheme } from '@/components/WorkshopTheme'
import { workshopTheme } from '@/lib/workshopTheme'
import { slideKeyAction } from '@/lib/slideKeys'
import { modulePositions } from '@/lib/modulePosition'
import { LoadError } from '@/components/LoadError'
import { validPollCourse } from '@/lib/pollCourse'
import { useDocumentTitle } from '@/lib/i18n'

// Beamer-Modus: Folie 0 = Titel/Szenario/Lernziele, danach ein Block pro Folie.
// Navigation: Pfeiltasten/Leertaste, Esc beendet. Notizen bleiben einklappbar
// (TrainerBlocks) — auf dem Beamer also erst nach Klick sichtbar.
// Live-Abstimmung: braucht einen Kurs (?kurs=<id>, der Einstieg aus dem Kurs-Detail
// setzt ihn). Ohne Kurs bleibt die Präsentation wie bisher, nur ohne Abstimmung.
export function TrainerPresentPage() {
  const { key = '' } = useParams()
  const navigate = useNavigate()
  const { token, role } = useAuthStore()
  const [slide, setSlide] = useState(0)
  useEffect(() => setSlide(0), [key])

  const mod = useQuery({
    queryKey: ['trainer-module', key],
    queryFn: () => trainerApi.trainerModule(key).then((r) => r.data),
    enabled: role === 'trainer' && !!token,
  })
  // Für die Folien-Nummer „Modul n“: Position im Workshop statt des internen
  // order-Sortierschlüssels (101, 301 …) — siehe lib/modulePosition.ts.
  const allMods = useQuery({
    queryKey: ['trainer-modules'],
    queryFn: () => trainerApi.trainerModules().then((r) => r.data),
    enabled: role === 'trainer' && !!token,
  })
  const total = 1 + (mod.data?.blocks.length ?? 0)

  const qc = useQueryClient()
  const [params, setParams] = useSearchParams()
  const courses = useQuery({
    queryKey: ['courses'],
    queryFn: () => trainerApi.listCourses().then((r) => r.data),
    enabled: role === 'trainer' && !!token,
  })
  // ?kurs= nur übernehmen, wenn der Kurs zum Lehrgang dieses Moduls gehört; ein
  // fremder/unbekannter Wert wird aus der Adresse entfernt (sobald beides geladen ist).
  const rawCid = params.get('kurs')
  const cid = mod.data ? validPollCourse(rawCid, courses.data, mod.data.workshop_key) : null
  const cidRejected = rawCid != null && cid == null && !!mod.data && !!courses.data
  useEffect(() => {
    if (cidRejected) setParams({}, { replace: true })
  }, [cidRejected, setParams])
  useDocumentTitle(mod.data ? `${mod.data.title} · Präsentation` : undefined)
  const pollKey = ['trainer-poll', cid]
  const poll = useQuery({
    queryKey: pollKey,
    queryFn: () => trainerApi.poll(cid!).then((r) => r.data),
    enabled: role === 'trainer' && !!token && cid != null,
    refetchInterval: (query) => (query.state.data ? 2_000 : false),  // Zählung nur während einer Abstimmung nachladen
  })
  const setPoll = (data: LivePoll | null) => qc.setQueryData(pollKey, data)
  const startPoll = useMutation({
    mutationFn: (v: { source: 'quiz' | 'check'; ref: string }) => trainerApi.startPoll(cid!, key, v.source, v.ref).then((r) => r.data),
    onSuccess: setPoll,
  })
  const revealPoll = useMutation({ mutationFn: () => trainerApi.revealPoll(cid!).then((r) => r.data), onSuccess: setPoll })
  const closePoll = useMutation({ mutationFn: () => trainerApi.closePoll(cid!), onSuccess: () => setPoll(null) })
  // Schlägt die Abfrage fehl, ist der Stand unbekannt: nicht auf der (veralteten)
  // Abstimmungsansicht samt Tastensperre stehen bleiben, sondern zurück zu den
  // Folien und den Fehler dort melden. Die Abfrage läuft weiter und holt sich zurück.
  const pollFailed = cid != null && poll.isError
  const livePoll = cid != null && !pollFailed ? poll.data ?? null : null
  const pollRunning = !!livePoll
  // Tab schließen/neu laden bei offener Abstimmung: sie bliebe für die Teilnehmer
  // offen. (Im Kurs-Detail lässt sie sich notfalls ebenfalls beenden.)
  useEffect(() => {
    if (!pollRunning) return
    const warn = (e: BeforeUnloadEvent) => e.preventDefault()
    window.addEventListener('beforeunload', warn)
    return () => window.removeEventListener('beforeunload', warn)
  }, [pollRunning])

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      // Während einer Abstimmung gibt es keine Folie: Pfeile/Leertaste/Esc dürfen weder
      // darunter blättern noch die Präsentation verlassen — beendet wird per Knopf.
      if (pollRunning) return
      const action = slideKeyAction(e.key, e.target)
      if (action === 'next') {
        e.preventDefault()
        setSlide((s) => Math.min(s + 1, total - 1))
      } else if (action === 'prev') {
        e.preventDefault()
        setSlide((s) => Math.max(s - 1, 0))
      } else if (action === 'exit') {
        navigate(`/trainer/modul/${key}`)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [total, key, navigate, pollRunning])

  if (role !== 'trainer' || !token)
    return (
      <div className="p-10 text-slate-600">
        Nur für Trainer. <Link to="/trainer" className="text-teal-600">Zum Login</Link>
      </div>
    )
  if (mod.isError && !mod.data) return <LoadError onRetry={() => mod.refetch()} />
  if (mod.isLoading || !mod.data) return <div className="p-10">Lädt…</div>
  const m = mod.data
  const position = modulePositions((allMods.data ?? []).filter((x) => (x.workshop_key ?? null) === (m.workshop_key ?? null))).get(key)
  const block = slide > 0 ? m.blocks[slide - 1] : null
  // Auswahl-Check auf der aktuellen Folie, zu dem sich (mit Kurs) abstimmen lässt
  const pollCheck = cid != null && block?.type === 'check' && (block.kind ?? 'choice') === 'choice' && block.uid ? block : null
  const singles = m.quiz.questions.map((q, i) => ({ q, n: i + 1 })).filter(({ q }) => q.type === 'single')
  const courseOptions = (courses.data ?? []).filter((c) => (c.workshop_key ?? null) === (m.workshop_key ?? null))
  const courseName = courseOptions.find((c) => c.id === cid)?.name

  if (livePoll)
    return (
      <WorkshopTheme theme={workshopTheme(m.workshop_key)}><main id="main-content" tabIndex={-1} className="workbench flex flex-col">
        <div className="mx-auto flex w-full max-w-5xl flex-1 flex-col justify-center px-8 py-6 sm:px-14">
          <p className="text-sm font-semibold uppercase tracking-widest text-[var(--wb-accent)]">
            Live-Abstimmung{courseName ? ` · ${courseName}` : ''}
          </p>
          <h1 className="mt-3 text-3xl font-bold leading-tight sm:text-4xl">{livePoll.prompt}</h1>
          <div className="mt-8"><PollOptions poll={livePoll} lang="de" big /></div>
          <p className="mt-6 text-2xl font-semibold tabular-nums" data-testid="poll-votes">
            {livePoll.votes} {livePoll.votes === 1 ? 'Stimme' : 'Stimmen'}
          </p>
          {livePoll.status === 'revealed' && livePoll.explanation && (
            <p className="mt-4 border-l-4 border-[var(--wb-accent)] pl-4 text-xl leading-relaxed text-[var(--wb-muted)]">{livePoll.explanation}</p>
          )}
        </div>
        <div className="sticky bottom-0 flex flex-wrap items-center justify-end gap-3 border-t border-[var(--wb-border)] bg-[var(--wb-canvas)] px-6 py-3 text-sm">
          {/* Verlassen beendet die Abstimmung mit — sonst bliebe sie für die Teilnehmer offen und für den Trainer unsichtbar. */}
          <button type="button" onClick={() => closePoll.mutate(undefined, { onSuccess: () => navigate(`/trainer/modul/${key}`) })} disabled={closePoll.isPending}
            className="wb-control mr-auto rounded-lg px-3 text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">
            ✕ Abstimmung beenden und Präsentation verlassen
          </button>
          {(revealPoll.isError || closePoll.isError) && <p role="alert" className="text-[var(--wb-ink)]">Aktion fehlgeschlagen — bitte erneut versuchen.</p>}
          {livePoll.status === 'open' && (
            <button type="button" onClick={() => revealPoll.mutate()} disabled={revealPoll.isPending}
              className="wb-control rounded-lg bg-[var(--wb-accent)] px-5 font-semibold text-white hover:bg-[var(--wb-accent-hover)]">
              Auflösen
            </button>
          )}
          <button type="button" onClick={() => closePoll.mutate()} disabled={closePoll.isPending}
            className="wb-control rounded-lg border border-[var(--wb-border)] px-5 font-semibold hover:border-[var(--wb-accent)]">
            Abstimmung beenden
          </button>
        </div>
      </main></WorkshopTheme>
    )

  return (
    <WorkshopTheme theme={workshopTheme(m.workshop_key)}><main id="main-content" tabIndex={-1} className="min-h-[100dvh] bg-white flex flex-col">
      <div className="flex-1 flex items-center justify-center p-8 sm:p-14">
        <div className="w-full max-w-3xl text-lg">
          {slide === 0 ? (
            <div>
              <BrandLogo className="mb-8 h-10 text-lg" showName />
              <p className="text-sm font-semibold uppercase tracking-widest text-teal-700 mb-3">
                {position ? `Modul ${position}` : 'Modul'}
              </p>
              <h1 className="text-4xl sm:text-5xl font-bold text-slate-900 leading-tight mb-6">{m.title}</h1>
              {m.scenario && (
                <div className="rounded-2xl border border-teal-100 bg-teal-50 px-5 py-4 text-teal-900 mb-6">
                  <Markdown components={MD_COMPONENTS}>{m.scenario}</Markdown>
                </div>
              )}
              {m.goals && m.goals.length > 0 && (
                <ul className="flex flex-col gap-2 text-slate-700">
                  {m.goals.map((g, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span aria-hidden="true" className="text-teal-500 mt-0.5">◆</span>{g}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ) : (
            pollCheck ? (
              // TrainerBlocks zeigt die Lösung sofort — vor einer Abstimmung gehört sie nicht
              // auf den Beamer. Deshalb hier die Frage neutral (Buchstaben wie bei den
              // Teilnehmern); Lösung und Notiz bleiben hinter einem Klick.
              <>
                <div className="workbench !min-h-0 !bg-transparent">
                  <p className="text-sm font-semibold uppercase tracking-widest text-[var(--wb-accent)]">Kurz-Check</p>
                  <h2 className="mb-6 mt-2 text-3xl font-bold leading-tight">{pollCheck.prompt}</h2>
                  <PollOptions poll={{ id: 0, status: 'open', prompt: pollCheck.prompt, options: pollCheck.options }} lang="de" big />
                </div>
                <button type="button" onClick={() => startPoll.mutate({ source: 'check', ref: pollCheck.uid! })} disabled={startPoll.isPending}
                  className="mt-6 rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 text-base font-medium">
                  Abstimmung starten
                </button>
                <details className="mt-6 text-base">
                  <summary className="cursor-pointer text-sm text-slate-500">Lösung und Notiz anzeigen</summary>
                  <div className="mt-3"><TrainerBlocks blocks={[pollCheck]} /></div>
                </details>
              </>
            ) : <TrainerBlocks key={slide} blocks={[m.blocks[slide - 1]]} />  // key: jede Folie beginnt mit frischem Blockzustand
          )}
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-x-4 gap-y-2 border-t border-slate-100 px-6 py-2 text-sm text-slate-600">
        <label className="flex items-center gap-2">
          Kurs für Live-Abstimmung
          <select value={cid ?? ''} onChange={(e) => setParams(e.target.value ? { kurs: e.target.value } : {}, { replace: true })}
            className="max-w-56 rounded-lg border bg-white px-2 py-1.5 text-slate-700">
            <option value="">— ohne —</option>
            {courseOptions.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </label>
        {cid != null && singles.length > 0 && (
          <select aria-label="Quizfrage zur Abstimmung stellen" value="" disabled={startPoll.isPending}
            onChange={(e) => { if (e.target.value) startPoll.mutate({ source: 'quiz', ref: e.target.value }) }}
            className="max-w-72 rounded-lg border bg-white px-2 py-1.5 text-slate-700">
            <option value="">Quizfrage abstimmen …</option>
            {singles.map(({ q, n }) => <option key={q.id} value={q.id}>{n}. {q.prompt.length > 70 ? `${q.prompt.slice(0, 70)}…` : q.prompt}</option>)}
          </select>
        )}
        {startPoll.isError && <span role="alert" className="text-slate-900">{errMsg(startPoll.error, 'Abstimmung konnte nicht gestartet werden.')}</span>}
        {pollFailed && (
          <span role="alert" className="text-slate-900">
            Der Stand der Live-Abstimmung konnte nicht geladen werden — eine laufende Abstimmung ist für die Teilnehmer evtl. noch offen.{' '}
            <button type="button" onClick={() => poll.refetch()} className="font-semibold underline">Erneut versuchen</button>
          </span>
        )}
      </div>

      <div className="flex items-center justify-between border-t border-slate-100 px-6 py-3 text-sm">
        <Link to={`/trainer/modul/${key}`} className="text-slate-600 hover:text-slate-900">
          ✕ Beenden <span className="text-xs">(Esc)</span>
        </Link>
        <div className="flex items-center gap-3">
          <button onClick={() => setSlide((s) => Math.max(s - 1, 0))} disabled={slide === 0}
            className="rounded-lg border px-3 py-1.5 text-slate-700 hover:bg-slate-50 disabled:opacity-30">
            ← zurück
          </button>
          <span className="tabular-nums text-slate-500">{slide + 1} / {total}</span>
          <button onClick={() => setSlide((s) => Math.min(s + 1, total - 1))} disabled={slide === total - 1}
            className="rounded-lg border px-3 py-1.5 text-slate-700 hover:bg-slate-50 disabled:opacity-30">
            weiter →
          </button>
        </div>
        <span className="text-xs text-slate-500 hidden sm:block">Pfeiltasten / Leertaste</span>
      </div>
    </main></WorkshopTheme>
  )
}
