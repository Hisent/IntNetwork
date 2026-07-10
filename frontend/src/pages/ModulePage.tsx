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
  useEffect(() => setRead(loadRead(key)), [key])

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

  return (
    <div className="min-h-dvh bg-slate-50">
      <div className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="max-w-2xl mx-auto flex items-center justify-between gap-3 px-6 py-2 text-sm">
          <span className="truncate font-medium text-slate-700">{mod.data.title}</span>
          <div className="flex shrink-0 items-center gap-2">
            <GlossaryPanel moduleKey={key} lang={lang} />
            {textIndexes.length > 0 && (
              <span className="text-xs text-slate-400">
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
                <button onClick={() => setRead(toggleRead(key, read, i))}
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
}
