import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, Navigate, useLocation, useParams } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { Blocks } from '@/components/Blocks'
import { BlockComments } from '@/components/BlockComments'
import { Quiz } from '@/components/Quiz'
import { loadRead, pruneOtherParticipants, toggleRead } from '@/lib/readProgress'
import { useModuleStateSync } from '@/lib/moduleStateSync'
import { ReviewWarmupBanner } from '@/components/ReviewCard'
import { PageSkeleton } from '@/components/PageSkeleton'
import { LoadError, ModuleMissing } from '@/components/LoadError'
import { localTitle, storeLang, t, useDocumentLang, useDocumentTitle, type Lang } from '@/lib/i18n'
import type { ApiError } from '@/lib/api'
import { jumpToBlock } from '@/lib/blockJump'
import { openPrerequisites } from '@/lib/lockedModules'
import { GlossaryPanel } from '@/components/GlossaryPanel'
import { termsForModule } from '@/lib/glossary'
import { Icon } from '@/components/Icon'
import type { Block, ModuleDetail, ModuleMeta, ProgressItem } from '@/types'
import { useAuthStore } from '@/store/auth'
import { LangToggle, WorkbenchProgress, WorkbenchSectionTitle, WorkbenchTopbar } from '@/components/workbench/WorkbenchShell'
import { readPercent } from '@/components/workbench/workbenchLogic'
import { groupModulesBySection, type ModuleSection } from '@/lib/moduleGroups'
import { modulePositions } from '@/lib/modulePosition'
import { WorkshopTheme } from '@/components/WorkshopTheme'
import { PrintContext, usePrintState } from '@/lib/printMode'
import { ParticipantPoll } from '@/components/LivePoll'
import { FollowBanner } from '@/components/FollowBanner'

export function ModulePage() {
  const { key = '' } = useParams()
  const qc = useQueryClient()
  // Ohne (oder nach abgelaufener) Teilnehmer-Sitzung zurück zur Startseite —
  // sonst bliebe nur „Konnte nicht geladen werden“ ohne Ausweg.
  const isParticipant = useAuthStore((state) => state.role) === 'participant'

  useEffect(() => {
    if (!key || !isParticipant) return
    // Modulwechsel ohne Ladezustand (Modul im Cache) behielte sonst die
    // Scrollposition vom Seitenende des vorherigen Moduls.
    window.scrollTo(0, 0)
  }, [key, isParticipant])

  const [read, setRead] = useState<number[]>([])
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data), enabled: isParticipant })
  const courseId = me.data?.course_id
  const participantId = me.data?.participant_id
  const scoped = participantId != null && courseId != null
  // Lese-/Übungsstand erst mit dem Server abgleichen (frisches Gerät: der Server gewinnt),
  // dann aus dem lokalen Cache anzeigen — bis dahin bleibt keyScope leer wie vor /me.
  const synced = useModuleStateSync(scoped ? `${participantId}-${courseId}` : '', key)
  // Reflexions-/Lese-Keys pro Teilnehmer trennen (geteilter Browser).
  const keyScope = scoped && synced ? `${participantId}-${courseId}` : ''
  useEffect(() => {
    if (!scoped) return
    // Genau hier wird die participantId app-weit zuerst bekannt — passender
    // Zeitpunkt, um Reste anderer Teilnehmer am geteilten Browser zu räumen.
    pruneOtherParticipants(participantId)
  }, [scoped, participantId])
  useEffect(() => {
    setRead(scoped && synced ? loadRead(participantId, courseId, key) : [])
  }, [scoped, synced, participantId, courseId, key])
  const lang: Lang = me.data?.language ?? 'de'
  useDocumentLang(lang)
  const mod = useQuery({
    queryKey: ['module', key, lang],
    queryFn: () => learnApi.getModule(key).then((r) => r.data),
    enabled: isParticipant,
    // Sprachwechsel: bis die andere Sprache da ist, bleibt der bisherige Inhalt DESSELBEN Moduls
    // stehen — sonst ersetzte das Lade-Skelett die Seite (Scrollposition 0, Quiz-Auswahl weg).
    placeholderData: (previous, previousQuery) => (previousQuery?.queryKey[1] === key ? previous : undefined),
  })
  const features = useQuery({ queryKey: ['features'], queryFn: () => learnApi.features().then((r) => r.data), enabled: isParticipant })
  const mods = useQuery({ queryKey: ['modules', lang], queryFn: () => learnApi.listModules().then((r) => r.data), enabled: isParticipant })
  const [justPassed, setJustPassed] = useState(false)
  useEffect(() => setJustPassed(false), [key])
  const printing = usePrintState()

  // Sprungziel eines Suchtreffers: #b-<Block-Kennung>. Der Block existiert erst,
  // wenn das Modul geladen ist — der Browser springt deshalb nicht von selbst.
  const { hash } = useLocation()
  const loaded = !!mod.data
  useEffect(() => {
    if (!loaded || !hash.startsWith('#b-')) return
    return jumpToBlock(decodeURIComponent(hash.slice(3)))
  }, [loaded, hash, key])
  useDocumentTitle(mod.data ? localTitle(mod.data, lang) : undefined)

  // Präsenz erst melden, wenn das Modul wirklich geladen ist — für ein abgewähltes
  // oder unbekanntes Modul antwortet der Heartbeat nur mit 404.
  useEffect(() => {
    if (!key || !isParticipant || !loaded) return
    // Nur melden, solange der Tab sichtbar ist: sonst zeigt die Präsenz im
    // Trainer-Bereich jeden als aktiv, der das Modul irgendwo im Hintergrund
    // offen hat. Beim Zurückkehren sofort melden, nicht erst nach 20 s.
    const beat = () => { if (!document.hidden) learnApi.heartbeat(key).catch(() => {}) }
    beat()
    const id = setInterval(beat, 20_000)
    document.addEventListener('visibilitychange', beat)
    return () => { clearInterval(id); document.removeEventListener('visibilitychange', beat) }
  }, [key, isParticipant, loaded])

  // Nächstes Modul in Kurs-Reihenfolge — Ziel des „Weiter“-Buttons unter dem Quiz.
  const nextModule = useMemo(() => {
    const sorted = [...(mods.data ?? [])].sort((a, b) => a.order - b.order)
    const idx = sorted.findIndex((m) => m.key === key)
    return idx >= 0 ? sorted[idx + 1] ?? null : null
  }, [mods.data, key])
  const sortedModules = useMemo(() => [...(mods.data ?? [])].sort((a, b) => a.order - b.order), [mods.data])
  const setLang = useMutation({
    mutationFn: (l: Lang) => { storeLang(l); return learnApi.setLanguage(l) },
    // Nur /me neu laden: die neue Sprache steht im Query-Key des Moduls und löst dessen
    // (einen) Abruf selbst aus — ein zusätzliches Invalidieren holte es doppelt.
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['me'] }) },
  })
  // Scroll-Erhalt beim Sprachwechsel: den obersten sichtbaren Block merken und, sobald der
  // Inhalt in der neuen Sprache steht (andere Textlängen), wieder an dieselbe Stelle rücken.
  const scrollAnchor = useRef<{ id: string; top: number; lang: Lang } | null>(null)
  const switchLanguage = (next: Lang) => {
    const el = [...document.querySelectorAll<HTMLElement>('[id^="block-"]')].find((b) => b.getBoundingClientRect().bottom > 0)
    scrollAnchor.current = el ? { id: el.id, top: el.getBoundingClientRect().top, lang: next } : null
    setLang.mutate(next)
  }
  useLayoutEffect(() => {
    const anchor = scrollAnchor.current
    if (!anchor || anchor.lang !== lang || mod.isPlaceholderData) return
    scrollAnchor.current = null
    const el = document.getElementById(anchor.id)
    if (el) window.scrollBy({ top: el.getBoundingClientRect().top - anchor.top, behavior: 'instant' })
  }, [lang, mod.isPlaceholderData, mod.data])

  if (!isParticipant) return <Navigate to="/" replace />
  if ((mod.error as ApiError | null)?.response?.status === 404) return <ModuleMissing lang={lang} code={(mod.error as ApiError).response?.data?.code} />
  if (mod.isError || me.isError) return <LoadError lang={lang} onRetry={() => { me.refetch(); mod.refetch() }} />
  // Erst nach dem Abgleich rendern: sonst landete eine Eingabe davor im noch leeren Scope.
  if (mod.isLoading || !mod.data || (scoped && !synced)) return <PageSkeleton />

  const commentsOn = features.data?.comments ?? false
  const textIndexes = mod.data.blocks.map((b, i) => (b.type === 'text' ? i : -1)).filter((i) => i >= 0)

  // Mini-Inhaltsverzeichnis aus den ##-Überschriften der Text-Blöcke
  const toc = mod.data.blocks.flatMap((b, i) =>
    b.type === 'text'
      ? [...b.value.matchAll(/^##\s+(.+)$/gm)].map((m) => ({ i, title: m[1].replace(/\*\*/g, '') }))
      : [])

  return (
    <WorkshopTheme theme={me.data?.workshop?.theme}>
      <PrintContext.Provider value={printing}>
      {/* key: Quiz-Ergebnis, Kurz-Checks und Reflexionen sind Zustand EINES Moduls —
          ohne Remount zeigte ein Wechsel zu einem bereits geladenen Modul das
          Quiz-Ergebnis des vorherigen und schrieb dessen Reflexionstext fort. */}
      <WorkbenchModuleView
        key={key}
        lang={lang}
        moduleKey={key}
        keyScope={keyScope}
        module={mod.data}
        modules={sortedModules}
        sections={me.data?.workshop?.sections}
        progress={me.data?.progress ?? []}
        read={read}
        textIndexes={textIndexes}
        toc={toc}
        commentsOn={commentsOn}
        showGlossary={termsForModule(key).length > 0}
        nextModule={nextModule}
        justPassed={justPassed}
        setLanguage={switchLanguage}
        onToggleRead={(index) => scoped && synced && setRead(toggleRead(participantId, courseId, key, read, index))}
        onQuizResult={(passed) => { setJustPassed(passed); qc.invalidateQueries({ queryKey: ['me'] }) }}
      />
      </PrintContext.Provider>
    </WorkshopTheme>
  )
}

export interface WorkbenchModuleProps {
  lang: Lang
  moduleKey: string
  keyScope: string
  module: ModuleDetail
  modules: ModuleMeta[]
  sections?: ModuleSection[]
  progress: ProgressItem[]
  read: number[]
  textIndexes: number[]
  toc: { i: number; title: string }[]
  commentsOn: boolean
  showGlossary: boolean
  nextModule: ModuleMeta | null
  justPassed: boolean
  setLanguage: (lang: Lang) => void
  onToggleRead: (index: number) => void
  onQuizResult: (passed: boolean) => void
}

// Gruppiert wie die Kursübersicht (LearnPage) — dieselbe Gliederungsfunktion,
// nur kompakter dargestellt (keine WorkbenchSectionTitle-Trennlinie, nur ein
// schmales Label je Gruppe), damit Sidebar und Übersicht keine zwei leicht
// unterschiedlichen Ansichten derselben Daten zeigen.
function WorkbenchModuleNav({ lang, current, modules, sections, progress }: { lang: Lang; current: string; modules: ModuleMeta[]; sections?: ModuleSection[]; progress: ProgressItem[] }) {
  const progressOf = (key: string) => progress.find((item) => item.module_key === key)
  const unlocked = (module: ModuleMeta) => module.key === current || openPrerequisites(module, progress, modules).length === 0
  const groups = groupModulesBySection(modules, sections)
  // Anzeigeposition (1..n) statt des internen `order`-Sortierschlüssels —
  // sonst zeigt der Claude-Workshop "101" statt "1" (siehe modulePosition.ts).
  const positions = modulePositions(modules)
  return (
    <nav aria-label={lang === 'de' ? 'Kursmodule' : 'Course modules'} className="space-y-3">
      {groups.map((group) => (
        <div key={group.key}>
          {groups.length > 1 && <p className="px-2 pb-1 text-[10px] font-semibold uppercase tracking-wide text-[var(--wb-muted)]">{lang === 'de' ? group.title_de : group.title_en}</p>}
          <div className="space-y-1">
            {group.modules.map((module) => {
              const available = unlocked(module)
              const itemProgress = progressOf(module.key)
              const rowClass = `wb-control grid grid-cols-[28px_minmax(0,1fr)] items-center gap-2 rounded-lg px-2 py-1.5 text-sm ${module.key === current ? 'bg-[var(--wb-accent-soft)] font-semibold text-[var(--wb-accent)]' : available ? 'text-[var(--wb-muted)] hover:bg-white hover:text-[var(--wb-ink)]' : 'cursor-not-allowed text-slate-400'}`
              const rowContent = <>
                  <span aria-hidden="true" className={`grid h-6 w-6 place-items-center rounded-md text-[10px] font-bold ${itemProgress?.done ? 'bg-emerald-100 text-[var(--wb-success)]' : module.key === current ? 'bg-[var(--wb-accent)] text-white' : 'bg-white'}`}>{itemProgress?.done ? <Icon name="check" className="h-3.5 w-3.5" /> : positions.get(module.key)}</span>
                  <span className="min-w-0">{localTitle(module, lang)}</span>
                </>
              return available
                ? <Link key={module.key} to={`/lernen/${module.key}`} aria-current={module.key === current ? 'page' : undefined} className={rowClass}>{rowContent}</Link>
                : <div key={module.key} aria-disabled="true" className={rowClass}>{rowContent}</div>
            })}
          </div>
        </div>
      ))}
    </nav>
  )
}

// Schmaler Balken am oberen Fensterrand: wie weit ist die Seite gescrollt? Reine
// Orientierung — „Gelesen“ (markierte Text-Blöcke) bleibt die eigene Anzeige darunter.
function ScrollProgress() {
  const [pct, setPct] = useState(0)
  useEffect(() => {
    const update = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight
      setPct(max > 0 ? Math.min(100, (window.scrollY / max) * 100) : 0)
    }
    update()
    window.addEventListener('scroll', update, { passive: true })
    window.addEventListener('resize', update)
    return () => { window.removeEventListener('scroll', update); window.removeEventListener('resize', update) }
  }, [])
  return <div aria-hidden="true" className="pointer-events-none fixed inset-x-0 top-0 z-40 h-[3px] print:hidden"><div className="h-full bg-[var(--wb-accent)]" style={{ width: `${pct}%` }} /></div>
}

export function WorkbenchModuleView({ lang, moduleKey, keyScope, module, modules, sections, progress, read, textIndexes, toc, commentsOn, showGlossary, nextModule, justPassed, setLanguage, onToggleRead, onQuizResult }: WorkbenchModuleProps) {
  const readPct = readPercent(textIndexes, read)
  // Position in der Kursreihenfolge (1..n) statt des internen `order`-Werts
  // (siehe modulePosition.ts) — betrifft auch den Claude-Workshop (order 101+).
  const position = modulePositions(modules).get(moduleKey) ?? module.order
  const title = localTitle(module, lang)
  // noch offene Voraussetzungen, soweit sie zum Kurs gehören
  const openKeys = openPrerequisites(module, progress, modules)
  const buildsOn = modules.filter((m) => openKeys.includes(m.key))
  const languageControl = (
    <><LangToggle lang={lang} onChange={setLanguage} className="hidden sm:flex" />{showGlossary && <div className="xl:hidden"><GlossaryPanel moduleKey={moduleKey} workshopKey={module.workshop_key} lang={lang} /></div>}</>
  )
  return (
    <div className="workbench">
      <ScrollProgress />
      {/* Live-Abstimmung des Trainers; direkt in der .workbench-Wurzel (Tokens, inert für die Geschwister) */}
      <ParticipantPoll moduleKey={moduleKey} lang={lang} />
      <WorkbenchTopbar lang={lang} title={title} actions={languageControl} />
      <div className="h-1 bg-[var(--wb-subtle)] print:hidden"><div className="h-full bg-[var(--wb-accent)]" style={{ width: `${readPct}%` }} /></div>
      <div className="wb-shell">
        <FollowBanner lang={lang} current={moduleKey} modules={modules} progress={progress} />
        <details id="module-nav" className="wb-surface mb-5 scroll-mt-20 p-3 lg:hidden print:hidden">
          <summary className="wb-control flex cursor-pointer items-center px-2 font-semibold">{lang === 'de' ? 'Kursnavigation öffnen' : 'Open course navigation'}</summary>
          <div className="mt-2 max-h-[60dvh] overflow-y-auto border-t border-[var(--wb-border)] pt-3">
            <LangToggle lang={lang} onChange={setLanguage} className="mb-3 flex sm:hidden" />
            <WorkbenchModuleNav lang={lang} current={moduleKey} modules={modules} sections={sections} progress={progress} />
          </div>
        </details>

        <ReviewWarmupBanner lang={lang} />
        <div className="wb-module-grid">
          <aside aria-label={lang === 'de' ? 'Modulübersicht' : 'Course overview'} className="sticky top-20 hidden max-h-[calc(100dvh-6rem)] overflow-y-auto lg:block print:hidden">
            <WorkbenchSectionTitle>{lang === 'de' ? 'Kursmodule' : 'Course modules'}</WorkbenchSectionTitle>
            <WorkbenchModuleNav lang={lang} current={moduleKey} modules={modules} sections={sections} progress={progress} />
          </aside>

          <main id="main-content" tabIndex={-1} className="wb-module-content">
            <div className="mb-2 flex items-center justify-between gap-3 print:hidden">
              <Link to="/lernen" className="wb-control inline-flex items-center gap-1 text-sm font-medium text-[var(--wb-muted)] hover:text-[var(--wb-accent)]"><Icon name="arrowLeft" className="h-4 w-4" />{t(lang, 'modules')}</Link>
              {/* Druckansicht = Spickzettel: Theorie, Diagramme, eigene Notizen (siehe print:-Klassen und lib/printMode.ts) */}
              <button type="button" onClick={() => window.print()} className="wb-control inline-flex items-center gap-1.5 text-sm font-medium text-[var(--wb-muted)] hover:text-[var(--wb-accent)]"><Icon name="printer" className="h-4 w-4" />{lang === 'de' ? 'Drucken / PDF' : 'Print / PDF'}</button>
            </div>
            <p className="text-sm font-semibold text-[var(--wb-accent)]">{lang === 'de' ? `Modul ${position}` : `Module ${position}`}</p>
            <h1 className="mt-2 text-3xl font-bold leading-tight tracking-tight text-[var(--wb-ink)] sm:text-4xl">{title}</h1>
            {/* Die Reihenfolge ist Führung, keine Sperre (Suche und Links führen auch hierher) — nur ehrlich sagen, worauf das Modul aufbaut. */}
            {buildsOn.length > 0 && (
              <p className="mt-3 text-sm text-[var(--wb-muted)] print:hidden">
                <Icon name="lock" className="mr-1.5 inline h-4 w-4 align-text-bottom" />{t(lang, 'moduleBuildsOn')}{' '}
                {buildsOn.map((m, index) => <span key={m.key}>{index > 0 && ', '}<Link to={`/lernen/${m.key}`} className="font-medium text-[var(--wb-accent)] hover:underline">{localTitle(m, lang)}</Link></span>)}
                {t(lang, 'buildsOnEnd')}.
              </p>
            )}
            {module.scenario && <div className="wb-scenario mt-5 border-l-2 border-[var(--wb-accent)] pl-4 text-sm leading-relaxed text-[var(--wb-muted)]"><Markdown>{module.scenario}</Markdown></div>}

            {module.goals && module.goals.length > 0 && (
              <section className="mt-6" aria-labelledby="module-goals">
                <h2 id="module-goals" className="text-sm font-semibold text-[var(--wb-ink)]">{lang === 'de' ? 'Lernziele' : 'Learning goals'}</h2>
                <ul className="mt-2 space-y-1.5 text-sm leading-relaxed text-[var(--wb-muted)]">
                  {module.goals.map((goal, index) => <li key={index} className="flex items-start gap-2"><Icon name="target" className="mt-0.5 h-4 w-4 shrink-0 text-[var(--wb-accent)]" />{goal}</li>)}
                </ul>
              </section>
            )}

            {toc.length >= 4 && <details className="wb-surface mt-6 p-4 xl:hidden print:hidden"><summary className="wb-control flex cursor-pointer items-center font-semibold">{t(lang, 'tocTitle')}</summary><ol className="mt-2 space-y-1">{toc.map((item, index) => <li key={`${item.i}-${index}`}><a href={`#block-${item.i}`} className="wb-control flex items-center text-sm text-[var(--wb-accent)] hover:underline">{item.title}</a></li>)}</ol></details>}

            <div className="mt-8">
              <Blocks blocks={module.blocks} lang={lang} moduleKey={moduleKey} keyScope={keyScope} footer={(block: Block, index) => block.type === 'text' ? <div className="flex flex-col gap-1 print:hidden"><button onClick={() => onToggleRead(index)} className={`wb-control inline-flex items-center gap-1 self-start text-xs font-medium ${read.includes(index) ? 'text-[var(--wb-success)]' : 'text-[var(--wb-muted)] hover:text-[var(--wb-accent)]'}`}>{read.includes(index) && <Icon name="check" className="h-3.5 w-3.5" />}{read.includes(index) ? t(lang, 'read') : t(lang, 'markRead')}</button>{commentsOn && <BlockComments moduleKey={moduleKey} blockIndex={index} lang={lang} />}</div> : null} />
            </div>

            {/* nur im Druck: die Begriffe des Moduls als Abschluss des Spickzettels */}
            {showGlossary && (
              <section className="mt-8 hidden print:block">
                <h2 className="text-sm font-semibold text-[var(--wb-ink)]">{lang === 'de' ? 'Begriffe' : 'Terms'}</h2>
                <dl className="mt-2 space-y-1 text-sm">
                  {termsForModule(moduleKey).map((term) => <div key={term.key}><dt className="inline font-semibold">{term.label[lang]}: </dt><dd className="inline text-[var(--wb-muted)]">{term.description[lang]}</dd></div>)}
                </dl>
              </section>
            )}

            {/* Quiz, Weiter-Link und Navigation gehören nicht auf den Spickzettel (keine Fragen, keine Lösungen). */}
            <div className="print:hidden">
            <Quiz moduleKey={moduleKey} questions={module.quiz.questions} lang={lang} onResult={onQuizResult} />
            </div>
            <div className="mt-10 border-t border-[var(--wb-border)] pt-6 text-right print:hidden">
              {nextModule ? <Link to={`/lernen/${nextModule.key}`} className={`wb-control inline-flex max-w-full items-center justify-center gap-1.5 rounded-lg px-5 text-center font-semibold ${justPassed ? 'bg-[var(--wb-accent)] text-white hover:bg-[var(--wb-accent-hover)]' : 'border border-[var(--wb-border)] bg-white text-[var(--wb-ink)] hover:border-[var(--wb-accent)]'}`}>{t(lang, 'nextModule')}: {localTitle(nextModule, lang)}<Icon name="arrowRight" className="h-4 w-4" /></Link> : <Link to="/lernen" className="wb-control inline-flex items-center gap-1.5 rounded-lg border border-[var(--wb-border)] bg-white px-5 font-semibold">{t(lang, 'backToOverview')}<Icon name="arrowRight" className="h-4 w-4" /></Link>}
            </div>

            {/* Auf schmalen Viewports (Sidebar nicht permanent sichtbar) ein
                kurzer Rückweg zur Kursnavigation, statt vollständigen
                Hochscrollens nach einer Unterbrechung im Quiz. */}
            <a href="#module-nav" className="wb-control mt-4 flex items-center justify-center gap-1.5 text-sm font-medium text-[var(--wb-muted)] hover:text-[var(--wb-accent)] lg:hidden print:hidden">
              <Icon name="arrowUp" className="h-4 w-4" />{lang === 'de' ? 'Zur Kursnavigation' : 'To course navigation'}
            </a>
          </main>

          <aside aria-label={lang === 'de' ? 'Auf dieser Seite' : 'On this page'} className="sticky top-20 hidden max-h-[calc(100dvh-6rem)] space-y-5 overflow-y-auto xl:block print:hidden">
            <section className="wb-surface p-4"><WorkbenchProgress value={readPct} label={lang === 'de' ? 'Gelesen' : 'Read'} />{showGlossary && <div className="mt-4"><GlossaryPanel moduleKey={moduleKey} workshopKey={module.workshop_key} lang={lang} /></div>}</section>
            {toc.length > 0 && <section><WorkbenchSectionTitle>{t(lang, 'tocTitle')}</WorkbenchSectionTitle><nav aria-label={t(lang, 'tocTitle')} className="space-y-1">{toc.map((item, index) => <a key={`${item.i}-${index}`} href={`#block-${item.i}`} className="wb-control flex items-center border-l border-[var(--wb-border)] px-3 text-sm text-[var(--wb-muted)] hover:border-[var(--wb-accent)] hover:text-[var(--wb-accent)]">{item.title}</a>)}</nav></section>}
          </aside>
        </div>
      </div>
    </div>
  )
}
