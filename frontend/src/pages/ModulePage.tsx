import { useEffect, useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, useParams } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { Blocks } from '@/components/Blocks'
import { BlockComments } from '@/components/BlockComments'
import { Quiz } from '@/components/Quiz'
import { loadRead, toggleRead } from '@/lib/readProgress'
import { PageSkeleton } from '@/components/PageSkeleton'
import { t, type Lang } from '@/lib/i18n'
import { GlossaryPanel } from '@/components/GlossaryPanel'
import { ExperienceSwitch } from '@/components/ExperienceSwitch'
import { useUiModeStore } from '@/store/uiMode'
import type { ReactNode } from 'react'
import type { Block, ModuleDetail, ModuleMeta, ProgressItem } from '@/types'
import { WorkbenchProgress, WorkbenchSectionTitle, WorkbenchTopbar } from '@/components/workbench/WorkbenchShell'
import { readPercent } from '@/components/workbench/workbenchLogic'
import { WorkshopTheme } from '@/components/WorkshopTheme'
import { BrandLogo } from '@/components/BrandLogo'

export function ModulePage() {
  const { key = '' } = useParams()
  const qc = useQueryClient()
  const mode = useUiModeStore((state) => state.mode)

  useEffect(() => {
    if (!key) return
    learnApi.heartbeat(key).catch(() => {})
    const id = setInterval(() => {
      learnApi.heartbeat(key).catch(() => {})
    }, 20_000)
    return () => clearInterval(id)
  }, [key])

  const [read, setRead] = useState<number[]>([])

  // Scroll-Fortschritt für die Sticky-Leiste (0–100 % der Seitenhöhe)
  const [scrollPct, setScrollPct] = useState(0)
  useEffect(() => {
    const onScroll = () => {
      const el = document.documentElement
      const max = el.scrollHeight - el.clientHeight
      setScrollPct(max > 0 ? Math.min(100, (el.scrollTop / max) * 100) : 0)
    }
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [key])
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data) })
  const courseId = me.data?.course_id
  useEffect(() => {
    if (courseId != null) setRead(loadRead(courseId, key))
  }, [courseId, key])
  const lang: Lang = me.data?.language ?? 'de'
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
  const progressByKey = new Map((me.data?.progress ?? []).map((item) => [item.module_key, item]))
  const moduleUnlocked = (moduleKey: string, prerequisites: string[]) =>
    moduleKey === key || prerequisites.every((prerequisite) => progressByKey.get(prerequisite)?.done)
  const setLang = useMutation({
    mutationFn: (l: Lang) => learnApi.setLanguage(l),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['me'] })
      qc.invalidateQueries({ queryKey: ['module'] })
    },
  })

  if (mod.isLoading || !mod.data) return <PageSkeleton />

  const commentsOn = features.data?.comments ?? false
  const textIndexes = mod.data.blocks.map((b, i) => (b.type === 'text' ? i : -1)).filter((i) => i >= 0)
  const readCount = read.filter((i) => textIndexes.includes(i)).length

  // Mini-Inhaltsverzeichnis aus den ##-Überschriften der Text-Blöcke
  const toc = mod.data.blocks.flatMap((b, i) =>
    b.type === 'text'
      ? [...b.value.matchAll(/^##\s+(.+)$/gm)].map((m) => ({ i, title: m[1].replace(/\*\*/g, '') }))
      : [])

  const content = (
    <div className="min-h-dvh bg-slate-50">
      <div className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="max-w-2xl mx-auto flex flex-wrap items-center gap-2 px-4 py-2 text-sm sm:flex-nowrap sm:justify-between sm:gap-3 sm:px-6">
          <BrandLogo className="h-7" />
          <span className="min-w-0 flex-1 truncate font-medium text-slate-700">{mod.data.title}</span>
          <div className="ml-auto flex min-w-0 items-center gap-2">
            <ExperienceSwitch lang={lang} confirmBeforeChange />
            {me.data?.workshop?.key === 'network' && <GlossaryPanel moduleKey={key} lang={lang} />}
            {textIndexes.length > 0 && (
              <span className="hidden text-xs text-slate-400 sm:inline">
                {readCount} / {textIndexes.length} {t(lang, 'read')}
              </span>
            )}
          </div>
        </div>
        <div className="h-0.5 bg-slate-100">
          <div className="h-full bg-teal-500" style={{ width: `${scrollPct}%` }} />
        </div>
      </div>

      <div className="p-6 pt-6 sm:p-10">
      <div className="mx-auto flex max-w-6xl items-start gap-8">
        <aside className="sticky top-20 hidden w-64 shrink-0 lg:block">
          <div className="rounded-2xl border border-slate-200 bg-white p-4">
            <p className="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-slate-400">
              {lang === 'de' ? 'Kursmodule' : 'Course modules'}
            </p>
            <nav className="flex max-h-[calc(100dvh-9rem)] flex-col gap-1 overflow-y-auto" aria-label={lang === 'de' ? 'Kursmodule' : 'Course modules'}>
              {sortedModules.map((item, index) => {
                const progress = progressByKey.get(item.key)
                const unlocked = moduleUnlocked(item.key, item.prerequisites)
                return (
                  <Link key={item.key} to={unlocked ? '/lernen/' + item.key : '#'}
                    onClick={(event) => { if (!unlocked) event.preventDefault() }}
                    aria-current={item.key === key ? 'page' : undefined}
                    className={'flex items-start gap-2 rounded-lg px-2.5 py-2 text-xs transition-colors ' + (
                      item.key === key ? 'bg-teal-50 font-semibold text-teal-800'
                        : unlocked ? 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                          : 'cursor-not-allowed text-slate-300'
                    )}>
                    <span className={'mt-0.5 flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-[10px] ' + (
                      progress?.done ? 'bg-green-100 text-green-700' : item.key === key ? 'bg-teal-600 text-white' : unlocked ? 'bg-slate-100 text-slate-500' : 'bg-slate-50 text-slate-300'
                    )}>{progress?.done ? '✓' : index + 1}</span>
                    <span className="min-w-0 flex-1">{lang === 'de' ? item.title : item.title_en}</span>
                    {progress?.best != null && <span className="shrink-0 text-[10px] text-slate-400">{progress.best}%</span>}
                  </Link>
                )
              })}
            </nav>
          </div>
        </aside>
      <main className="min-w-0 max-w-2xl flex-1 animate-fade-up">
        <div className="flex items-center justify-between mb-2">
          <Link to="/lernen" className="text-sm text-slate-400 hover:text-slate-600">← {t(lang, 'modules')}</Link>
          <div className="flex gap-1 text-xs font-medium">
            <button onClick={() => setLang.mutate('de')}
              className={`rounded px-2 py-1 border ${lang === 'de' ? 'bg-teal-600 text-white border-teal-600' : 'text-slate-500 border-slate-200 hover:bg-slate-50'}`}>
              DE
            </button>
            <button onClick={() => setLang.mutate('en')}
              className={`rounded px-2 py-1 border ${lang === 'en' ? 'bg-teal-600 text-white border-teal-600' : 'text-slate-500 border-slate-200 hover:bg-slate-50'}`}>
              EN
            </button>
          </div>
        </div>
        <details className="mb-4 rounded-xl border border-slate-200 bg-white px-4 py-3 lg:hidden">
          <summary className="cursor-pointer select-none text-sm font-medium text-slate-700">
            {lang === 'de' ? 'Kursnavigation' : 'Course navigation'}
          </summary>
          <nav className="mt-3 flex max-h-64 flex-col gap-1 overflow-y-auto" aria-label={lang === 'de' ? 'Kursnavigation' : 'Course navigation'}>
            {sortedModules.map((item, index) => {
              const unlocked = moduleUnlocked(item.key, item.prerequisites)
              return (
                <Link key={item.key} to={unlocked ? '/lernen/' + item.key : '#'} onClick={(event) => { if (!unlocked) event.preventDefault() }}
                  className={'rounded-lg px-2.5 py-2 text-xs ' + (item.key === key ? 'bg-teal-50 font-semibold text-teal-800' : unlocked ? 'text-slate-600' : 'text-slate-300')}>
                  {progressByKey.get(item.key)?.done ? '✓ ' : (index + 1) + '. '}{lang === 'de' ? item.title : item.title_en}
                </Link>
              )
            })}
          </nav>
        </details>
        <h1 className="text-2xl font-bold text-slate-900 mt-2 mb-4">{mod.data.title}</h1>
        {mod.data.scenario && (
          <div className="rounded-xl border border-teal-100 bg-teal-50 px-4 py-3 mb-6 text-sm text-teal-900">
            <Markdown>{mod.data.scenario}</Markdown>
          </div>
        )}
        {toc.length >= 4 && (
          <details className="mb-6 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm">
            <summary className="cursor-pointer select-none font-medium text-slate-700">
              {t(lang, 'tocTitle')}
            </summary>
            <ol className="mt-2 flex flex-col gap-1">
              {toc.map((h, n) => (
                <li key={`${h.i}-${n}`}>
                  <a href={`#block-${h.i}`} className="text-teal-700 hover:underline">
                    {h.title}
                  </a>
                </li>
              ))}
            </ol>
          </details>
        )}
        <Blocks
          blocks={mod.data.blocks}
          lang={lang}
          moduleKey={key}
          footer={(b, i) =>
            b.type === 'text' ? (
              <div className="flex flex-col gap-1">
                <button onClick={() => courseId != null && setRead(toggleRead(courseId, key, read, i))}
                  className={`self-start text-xs ${read.includes(i) ? 'text-teal-600 font-medium' : 'text-slate-400 hover:text-slate-600'}`}>
                  {read.includes(i) ? `✓ ${t(lang, 'read')}` : t(lang, 'markRead')}
                </button>
                {commentsOn && <BlockComments moduleKey={key} blockIndex={i} lang={lang} />}
              </div>
            ) : null
          }
        />
        <Quiz moduleKey={key} questions={mod.data.quiz.questions} lang={lang}
          onResult={(passed) => {
            setJustPassed(passed)
            // Fortschritt überall aktualisieren (LearnPage-Badges, Abschluss-Banner)
            qc.invalidateQueries({ queryKey: ['me'] })
          }} />

        <div className="mt-10 h-px bg-slate-200" aria-hidden="true" />

        <div className="mt-6 flex justify-end">
          {nextModule ? (
            <Link to={`/lernen/${nextModule.key}`}
              className={`rounded-xl px-5 py-3 font-medium transition-colors ${
                justPassed
                  ? 'bg-teal-600 hover:bg-teal-700 text-white shadow'
                  : 'border border-slate-300 bg-white text-slate-700 hover:bg-slate-50'
              }`}>
              {t(lang, 'nextModule')}: {lang === 'de' ? nextModule.title : nextModule.title_en} →
            </Link>
          ) : (
            <Link to="/lernen"
              className="rounded-xl border border-slate-300 bg-white px-5 py-3 font-medium text-slate-700 hover:bg-slate-50">
              {t(lang, 'backToOverview')} →
            </Link>
          )}
        </div>
      </main>
      </div>
      </div>
    </div>
  )

  const view = mode === 'workbench'
    ? <WorkbenchModuleView
        lang={lang}
        moduleKey={key}
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
        onToggleRead={(index) => courseId != null && setRead(toggleRead(courseId, key, read, index))}
        onQuizResult={(passed) => { setJustPassed(passed); qc.invalidateQueries({ queryKey: ['me'] }) }}
      />
    : <ClassicModuleView lang={lang}>{content}</ClassicModuleView>
  return <WorkshopTheme theme={me.data?.workshop?.theme}>{view}</WorkshopTheme>
}

export interface ModuleViewProps {
  lang: Lang
  children: ReactNode
}

export function ClassicModuleView({ children }: ModuleViewProps) {
  return children
}

export interface WorkbenchModuleProps {
  lang: Lang
  moduleKey: string
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

export function WorkbenchModuleView({ lang, moduleKey, module, modules, progress, read, textIndexes, toc, commentsOn, showGlossary, nextModule, justPassed, setLanguage, onToggleRead, onQuizResult }: WorkbenchModuleProps) {
  const readPct = readPercent(textIndexes, read)
  const languageControl = (
    <><div className="hidden sm:flex" aria-label={lang === 'de' ? 'Sprache' : 'Language'}>{(['de', 'en'] as Lang[]).map((value) => <button key={value} type="button" onClick={() => setLanguage(value)} aria-pressed={lang === value} className={`wb-control min-w-11 text-xs font-semibold uppercase ${lang === value ? 'text-[var(--wb-accent)]' : 'text-[var(--wb-muted)]'}`}>{value}</button>)}</div>{showGlossary && <div className="xl:hidden"><GlossaryPanel moduleKey={moduleKey} lang={lang} /></div>}</>
  )
  return (
    <div className="workbench">
      <WorkbenchTopbar lang={lang} title={module.title} actions={languageControl} confirmExperienceChange />
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

          <main className="wb-module-content">
            <Link to="/lernen" className="wb-control mb-2 inline-flex items-center text-sm font-medium text-[var(--wb-muted)] hover:text-[var(--wb-accent)]">← {t(lang, 'modules')}</Link>
            <p className="text-sm font-semibold text-[var(--wb-accent)]">{lang === 'de' ? `Modul ${module.order}` : `Module ${module.order}`}</p>
            <h1 className="mt-2 text-3xl font-bold leading-tight tracking-tight text-[var(--wb-ink)] sm:text-4xl">{module.title}</h1>
            {module.scenario && <div className="mt-5 border-l-2 border-[var(--wb-accent)] pl-4 text-sm leading-relaxed text-[var(--wb-muted)]"><Markdown>{module.scenario}</Markdown></div>}

            {toc.length >= 4 && <details className="wb-surface mt-6 p-4 xl:hidden"><summary className="wb-control flex cursor-pointer items-center font-semibold">{t(lang, 'tocTitle')}</summary><ol className="mt-2 space-y-1">{toc.map((item, index) => <li key={`${item.i}-${index}`}><a href={`#block-${item.i}`} className="wb-control flex items-center text-sm text-[var(--wb-accent)] hover:underline">{item.title}</a></li>)}</ol></details>}

            <div className="mt-8">
              <Blocks blocks={module.blocks} lang={lang} moduleKey={moduleKey} footer={(block: Block, index) => block.type === 'text' ? <div className="flex flex-col gap-1"><button onClick={() => onToggleRead(index)} className={`wb-control self-start text-xs font-medium ${read.includes(index) ? 'text-[var(--wb-success)]' : 'text-[var(--wb-muted)] hover:text-[var(--wb-accent)]'}`}>{read.includes(index) ? `✓ ${t(lang, 'read')}` : t(lang, 'markRead')}</button>{commentsOn && <BlockComments moduleKey={moduleKey} blockIndex={index} lang={lang} />}</div> : null} />
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
