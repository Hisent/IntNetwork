import { useEffect, useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, useParams } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { Blocks } from '@/components/Blocks'
import { BlockComments } from '@/components/BlockComments'
import { Quiz } from '@/components/Quiz'
import { loadRead, pruneOtherParticipants, toggleRead } from '@/lib/readProgress'
import { PageSkeleton } from '@/components/PageSkeleton'
import { LoadError } from '@/components/LoadError'
import { t, useDocumentLang, type Lang } from '@/lib/i18n'
import { GlossaryPanel } from '@/components/GlossaryPanel'
import type { Block, ModuleDetail, ModuleMeta, ProgressItem } from '@/types'
import { WorkbenchProgress, WorkbenchSectionTitle, WorkbenchTopbar } from '@/components/workbench/WorkbenchShell'
import { readPercent } from '@/components/workbench/workbenchLogic'
import { WorkshopTheme } from '@/components/WorkshopTheme'

export function ModulePage() {
  const { key = '' } = useParams()
  const qc = useQueryClient()

  useEffect(() => {
    if (!key) return
    learnApi.heartbeat(key).catch(() => {})
    const id = setInterval(() => {
      learnApi.heartbeat(key).catch(() => {})
    }, 20_000)
    return () => clearInterval(id)
  }, [key])

  const [read, setRead] = useState<number[]>([])
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data) })
  const courseId = me.data?.course_id
  const participantId = me.data?.participant_id
  const scoped = participantId != null && courseId != null
  // Reflexions-/Lese-Keys pro Teilnehmer trennen (geteilter Browser).
  const keyScope = scoped ? `${participantId}-${courseId}` : ''
  useEffect(() => {
    if (!scoped) return
    // Genau hier wird die participantId app-weit zuerst bekannt — passender
    // Zeitpunkt, um Reste anderer Teilnehmer am geteilten Browser zu räumen.
    pruneOtherParticipants(participantId)
    setRead(loadRead(participantId, courseId, key))
  }, [scoped, participantId, courseId, key])
  const lang: Lang = me.data?.language ?? 'de'
  useDocumentLang(lang)
  const mod = useQuery({ queryKey: ['module', key, lang], queryFn: () => learnApi.getModule(key).then((r) => r.data) })
  const features = useQuery({ queryKey: ['features'], queryFn: () => learnApi.features().then((r) => r.data) })
  const mods = useQuery({ queryKey: ['modules', lang], queryFn: () => learnApi.listModules().then((r) => r.data) })
  const [justPassed, setJustPassed] = useState(false)
  useEffect(() => setJustPassed(false), [key])

  // Nächstes Modul in Kurs-Reihenfolge — Ziel des „Weiter“-Buttons unter dem Quiz.
  const nextModule = useMemo(() => {
    const sorted = [...(mods.data ?? [])].sort((a, b) => a.order - b.order)
    const idx = sorted.findIndex((m) => m.key === key)
    return idx >= 0 ? sorted[idx + 1] ?? null : null
  }, [mods.data, key])
  const sortedModules = useMemo(() => [...(mods.data ?? [])].sort((a, b) => a.order - b.order), [mods.data])
  const setLang = useMutation({
    mutationFn: (l: Lang) => learnApi.setLanguage(l),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['me'] })
      qc.invalidateQueries({ queryKey: ['module'] })
    },
  })

  if (mod.isError || me.isError) return <LoadError lang={lang} onRetry={() => { me.refetch(); mod.refetch() }} />
  if (mod.isLoading || !mod.data) return <PageSkeleton />

  const commentsOn = features.data?.comments ?? false
  const textIndexes = mod.data.blocks.map((b, i) => (b.type === 'text' ? i : -1)).filter((i) => i >= 0)

  // Mini-Inhaltsverzeichnis aus den ##-Überschriften der Text-Blöcke
  const toc = mod.data.blocks.flatMap((b, i) =>
    b.type === 'text'
      ? [...b.value.matchAll(/^##\s+(.+)$/gm)].map((m) => ({ i, title: m[1].replace(/\*\*/g, '') }))
      : [])

  return (
    <WorkshopTheme theme={me.data?.workshop?.theme}>
      <WorkbenchModuleView
        lang={lang}
        moduleKey={key}
        keyScope={keyScope}
        module={mod.data}
        modules={sortedModules}
        progress={me.data?.progress ?? []}
        read={read}
        textIndexes={textIndexes}
        toc={toc}
        commentsOn={commentsOn}
        showGlossary={me.data?.workshop?.key === 'network'}
        nextModule={nextModule}
        justPassed={justPassed}
        setLanguage={(value) => setLang.mutate(value)}
        onToggleRead={(index) => scoped && setRead(toggleRead(participantId, courseId, key, read, index))}
        onQuizResult={(passed) => { setJustPassed(passed); qc.invalidateQueries({ queryKey: ['me'] }) }}
      />
    </WorkshopTheme>
  )
}

export interface WorkbenchModuleProps {
  lang: Lang
  moduleKey: string
  keyScope: string
  module: ModuleDetail
  modules: ModuleMeta[]
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

function WorkbenchModuleNav({ lang, current, modules, progress }: { lang: Lang; current: string; modules: ModuleMeta[]; progress: ProgressItem[] }) {
  const progressOf = (key: string) => progress.find((item) => item.module_key === key)
  const unlocked = (module: ModuleMeta) => module.key === current || module.prerequisites.every((key) => progressOf(key)?.done)
  return (
    <nav aria-label={lang === 'de' ? 'Kursmodule' : 'Course modules'} className="space-y-1">
      {modules.map((module) => {
        const available = unlocked(module)
        const itemProgress = progressOf(module.key)
        const rowClass = `wb-control grid grid-cols-[28px_minmax(0,1fr)] items-center gap-2 rounded-lg px-2 py-1.5 text-sm ${module.key === current ? 'bg-[var(--wb-accent-soft)] font-semibold text-[var(--wb-accent)]' : available ? 'text-[var(--wb-muted)] hover:bg-white hover:text-[var(--wb-ink)]' : 'cursor-not-allowed text-slate-400'}`
        const rowContent = <>
            <span aria-hidden="true" className={`grid h-6 w-6 place-items-center rounded-md text-[10px] font-bold ${itemProgress?.done ? 'bg-emerald-100 text-[var(--wb-success)]' : module.key === current ? 'bg-[var(--wb-accent)] text-white' : 'bg-white'}`}>{itemProgress?.done ? '✓' : module.order}</span>
            <span className="min-w-0">{lang === 'de' ? module.title : module.title_en}</span>
          </>
        return available
          ? <Link key={module.key} to={`/lernen/${module.key}`} aria-current={module.key === current ? 'page' : undefined} className={rowClass}>{rowContent}</Link>
          : <div key={module.key} aria-disabled="true" className={rowClass}>{rowContent}</div>
      })}
    </nav>
  )
}

export function WorkbenchModuleView({ lang, moduleKey, keyScope, module, modules, progress, read, textIndexes, toc, commentsOn, showGlossary, nextModule, justPassed, setLanguage, onToggleRead, onQuizResult }: WorkbenchModuleProps) {
  const readPct = readPercent(textIndexes, read)
  const languageControl = (
    <><div className="hidden sm:flex" aria-label={lang === 'de' ? 'Sprache' : 'Language'}>{(['de', 'en'] as Lang[]).map((value) => <button key={value} type="button" onClick={() => setLanguage(value)} aria-pressed={lang === value} className={`wb-control min-w-11 text-xs font-semibold uppercase ${lang === value ? 'text-[var(--wb-accent)]' : 'text-[var(--wb-muted)]'}`}>{value}</button>)}</div>{showGlossary && <div className="xl:hidden"><GlossaryPanel moduleKey={moduleKey} lang={lang} /></div>}</>
  )
  return (
    <div className="workbench">
      <WorkbenchTopbar lang={lang} title={module.title} actions={languageControl} />
      <div className="h-1 bg-[var(--wb-subtle)]"><div className="h-full bg-[var(--wb-accent)]" style={{ width: `${readPct}%` }} /></div>
      <div className="wb-shell">
        <details className="wb-surface mb-5 p-3 lg:hidden">
          <summary className="wb-control flex cursor-pointer items-center px-2 font-semibold">{lang === 'de' ? 'Kursnavigation öffnen' : 'Open course navigation'}</summary>
          <div className="mt-2 max-h-[60dvh] overflow-y-auto border-t border-[var(--wb-border)] pt-3">
            <div className="mb-3 flex sm:hidden" aria-label={lang === 'de' ? 'Sprache' : 'Language'}>{(['de', 'en'] as Lang[]).map((value) => <button key={value} type="button" onClick={() => setLanguage(value)} aria-pressed={lang === value} className={`wb-control min-w-11 text-xs font-semibold uppercase ${lang === value ? 'text-[var(--wb-accent)]' : 'text-[var(--wb-muted)]'}`}>{value}</button>)}</div>
            <WorkbenchModuleNav lang={lang} current={moduleKey} modules={modules} progress={progress} />
          </div>
        </details>

        <div className="wb-module-grid">
          <aside className="sticky top-20 hidden max-h-[calc(100dvh-6rem)] overflow-y-auto lg:block">
            <WorkbenchSectionTitle>{lang === 'de' ? 'Kursmodule' : 'Course modules'}</WorkbenchSectionTitle>
            <WorkbenchModuleNav lang={lang} current={moduleKey} modules={modules} progress={progress} />
          </aside>

          <main id="main-content" tabIndex={-1} className="wb-module-content">
            <Link to="/lernen" className="wb-control mb-2 inline-flex items-center text-sm font-medium text-[var(--wb-muted)] hover:text-[var(--wb-accent)]">← {t(lang, 'modules')}</Link>
            <p className="text-sm font-semibold text-[var(--wb-accent)]">{lang === 'de' ? `Modul ${module.order}` : `Module ${module.order}`}</p>
            <h1 className="mt-2 text-3xl font-bold leading-tight tracking-tight text-[var(--wb-ink)] sm:text-4xl">{module.title}</h1>
            {module.scenario && <div className="mt-5 border-l-2 border-[var(--wb-accent)] pl-4 text-sm leading-relaxed text-[var(--wb-muted)]"><Markdown>{module.scenario}</Markdown></div>}

            {toc.length >= 4 && <details className="wb-surface mt-6 p-4 xl:hidden"><summary className="wb-control flex cursor-pointer items-center font-semibold">{t(lang, 'tocTitle')}</summary><ol className="mt-2 space-y-1">{toc.map((item, index) => <li key={`${item.i}-${index}`}><a href={`#block-${item.i}`} className="wb-control flex items-center text-sm text-[var(--wb-accent)] hover:underline">{item.title}</a></li>)}</ol></details>}

            <div className="mt-8">
              <Blocks blocks={module.blocks} lang={lang} moduleKey={moduleKey} keyScope={keyScope} footer={(block: Block, index) => block.type === 'text' ? <div className="flex flex-col gap-1"><button onClick={() => onToggleRead(index)} className={`wb-control self-start text-xs font-medium ${read.includes(index) ? 'text-[var(--wb-success)]' : 'text-[var(--wb-muted)] hover:text-[var(--wb-accent)]'}`}>{read.includes(index) ? `✓ ${t(lang, 'read')}` : t(lang, 'markRead')}</button>{commentsOn && <BlockComments moduleKey={moduleKey} blockIndex={index} lang={lang} />}</div> : null} />
            </div>

            <Quiz moduleKey={moduleKey} questions={module.quiz.questions} lang={lang} onResult={onQuizResult} />
            <div className="mt-10 border-t border-[var(--wb-border)] pt-6 text-right">
              {nextModule ? <Link to={`/lernen/${nextModule.key}`} className={`wb-control inline-flex max-w-full items-center justify-center rounded-lg px-5 text-center font-semibold ${justPassed ? 'bg-[var(--wb-accent)] text-white hover:bg-[var(--wb-accent-hover)]' : 'border border-[var(--wb-border)] bg-white text-[var(--wb-ink)] hover:border-[var(--wb-accent)]'}`}>{t(lang, 'nextModule')}: {lang === 'de' ? nextModule.title : nextModule.title_en} →</Link> : <Link to="/lernen" className="wb-control inline-flex items-center rounded-lg border border-[var(--wb-border)] bg-white px-5 font-semibold">{t(lang, 'backToOverview')} →</Link>}
            </div>
          </main>

          <aside className="sticky top-20 hidden max-h-[calc(100dvh-6rem)] space-y-5 overflow-y-auto xl:block">
            <section className="wb-surface p-4"><WorkbenchProgress value={readPct} label={lang === 'de' ? 'Gelesen' : 'Read'} />{showGlossary && <div className="mt-4"><GlossaryPanel moduleKey={moduleKey} lang={lang} /></div>}</section>
            {toc.length > 0 && <section><WorkbenchSectionTitle>{t(lang, 'tocTitle')}</WorkbenchSectionTitle><nav className="space-y-1">{toc.map((item, index) => <a key={`${item.i}-${index}`} href={`#block-${item.i}`} className="wb-control flex items-center border-l border-[var(--wb-border)] px-3 text-sm text-[var(--wb-muted)] hover:border-[var(--wb-accent)] hover:text-[var(--wb-accent)]">{item.title}</a>)}</nav></section>}
          </aside>
        </div>
      </div>
    </div>
  )
}
