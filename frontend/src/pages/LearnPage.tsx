import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { PageSkeleton } from '@/components/PageSkeleton'
import type { Company, ModuleMeta, ProgressItem } from '@/types'
import { useAuthStore } from '@/store/auth'
import { t, type Lang } from '@/lib/i18n'
import { VersionBadge } from '@/components/VersionBadge'
import { ExperienceSwitch } from '@/components/ExperienceSwitch'
import { useUiModeStore } from '@/store/uiMode'
import type { ReactNode } from 'react'
import { WorkbenchProgress, WorkbenchSectionTitle, WorkbenchTopbar } from '@/components/workbench/WorkbenchShell'
import { WorkshopTheme } from '@/components/WorkshopTheme'

type Group = { key: string; title: string; mods: ModuleMeta[] }

export function LearnPage() {
  const nav = useNavigate()
  const qc = useQueryClient()
  const { role, displayName } = useAuthStore()
  const mode = useUiModeStore((state) => state.mode)
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data) })
  const lang: Lang = me.data?.language ?? 'de'
  const mods = useQuery({ queryKey: ['modules', lang], queryFn: () => learnApi.listModules().then((r) => r.data) })
  const networkWorkshop = me.data?.workshop?.key === 'network'
  const company = useQuery({ queryKey: ['company', lang], queryFn: () => learnApi.company().then((r) => r.data), enabled: networkWorkshop })
  const links = useQuery({ queryKey: ['links'], queryFn: () => learnApi.links().then((r) => r.data), enabled: networkWorkshop })
  const setLang = useMutation({
    mutationFn: (l: Lang) => learnApi.setLanguage(l),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['me'] })
      qc.invalidateQueries({ queryKey: ['modules'] })
      qc.invalidateQueries({ queryKey: ['company'] })
      qc.invalidateQueries({ queryKey: ['module'] })
    },
  })

  if (role !== 'participant') { nav('/'); return null }
  if (me.isLoading || mods.isLoading) return <PageSkeleton />

  const titleOf = (key: string) => {
    const m = mods.data?.find((x) => x.key === key)
    return m ? (lang === 'de' ? m.title : m.title_en) : key
  }
  const progressOf = (key: string) => me.data?.progress.find((p) => p.module_key === key)
  const isDone = (key: string) => progressOf(key)?.done ?? false
  const prereqsMet = (keys: string[]) => keys.every(isDone)

  const total = mods.data?.length ?? 0
  const doneCount = mods.data?.filter((m) => isDone(m.key)).length ?? 0
  const donePct = total ? Math.round((doneCount / total) * 100) : 0

  const sorted = [...(mods.data ?? [])].sort((a, b) => a.order - b.order)
  const isLocked = (m: ModuleMeta) => m.prerequisites.length > 0 && !prereqsMet(m.prerequisites)
  // „Hier weitermachen“: erstes offenes, nicht gesperrtes Modul in Kurs-Reihenfolge
  const continueAt = sorted.find((m) => !isDone(m.key) && !isLocked(m))
  const grouped: Group[] = (me.data?.workshop?.sections ?? [{ key: 'modules', from: -Infinity, to: Infinity, title_de: 'Module', title_en: 'Modules' }])
    .map((g) => ({ key: g.key, title: lang === 'de' ? g.title_de : g.title_en, mods: sorted.filter((m) => m.order >= g.from && m.order <= g.to) }))
    .filter((g) => g.mods.length > 0)
  const workshopTitle = me.data?.workshop?.title[lang] ?? 'IntNetwork'
  const workshopSummary = me.data?.workshop?.summary?.[lang] ?? t(lang, 'tagline')
  const completionText = lang === 'de' ? 'Alle Module dieses Workshops sind bestanden.' : 'All modules in this workshop are passed.'

  const content = (
    <div className="min-h-dvh bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <div className="flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-slate-900">{t(lang, 'hello')} {displayName}</h1>
            <VersionBadge tone="dark" />
          </div>
          <div className="flex w-full flex-wrap items-center gap-2 text-xs font-medium sm:w-auto sm:flex-nowrap">
            <ExperienceSwitch lang={lang} />
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
        <p className="text-slate-500 text-sm mb-4">{workshopSummary}</p>

        {total > 0 && doneCount === total && (
          <div className="mb-6 rounded-2xl border border-teal-200 bg-gradient-to-r from-teal-50 to-emerald-50 p-5 flex items-center gap-4">
            <span className="text-4xl" aria-hidden="true">🏆</span>
            <div className="flex-1">
              <p className="font-bold text-teal-900">{t(lang, 'courseComplete')}</p>
              <p className="text-sm text-teal-800">{completionText}</p>
            </div>
            <Link to="/lernen/zertifikat"
              className="shrink-0 rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-2 text-sm font-medium">
              {t(lang, 'certButton')} →
            </Link>
          </div>
        )}

        {total > 0 && (
          <div className="mb-6">
            <div className="flex justify-between text-xs text-slate-500 mb-1">
              <span>{t(lang, 'courseProgress')}</span>
              <span>{doneCount} / {total} {t(lang, 'modulesDone')}</span>
            </div>
            <div className="h-2 rounded-full bg-slate-200 overflow-hidden">
              <div className="h-full bg-teal-500 rounded-full transition-all duration-500" style={{ width: `${donePct}%` }} />
            </div>
          </div>
        )}

        {company.data && (
          <div className="rounded-2xl border bg-white p-5 mb-8">
            <h2 className="font-semibold text-slate-900">{company.data.name}</h2>
            <p className="text-sm text-slate-600 mt-1">{company.data.blurb}</p>
            <p className="text-xs text-slate-500 mt-3">{t(lang, 'sites')}: {company.data.sites.join(', ')}</p>
            <div className="mt-2 flex flex-wrap gap-1.5">
              {company.data.devices.map((d) => (
                <span key={d} className="text-xs rounded-full bg-slate-100 text-slate-600 px-2 py-0.5">{d}</span>
              ))}
            </div>
          </div>
        )}

        {continueAt && doneCount > 0 && (
          <Link to={`/lernen/${continueAt.key}`}
            className="mb-6 flex items-center justify-between gap-3 rounded-2xl bg-teal-600 hover:bg-teal-700 text-white p-5 shadow transition-colors">
            <span>
              <span className="block text-xs font-semibold uppercase tracking-wide text-teal-100">
                {t(lang, 'continueHere')}
              </span>
              <span className="text-lg font-bold">
                {lang === 'de' ? continueAt.title : continueAt.title_en}
              </span>
            </span>
            <span aria-hidden="true" className="text-2xl">→</span>
          </Link>
        )}

        <div className="flex flex-col gap-6">
          {grouped.map((g) => (
            <div key={g.key}>
              <h2 className="text-xs font-semibold uppercase tracking-wide text-slate-400 mb-2">
                {g.title}
              </h2>
              <div className="flex flex-col gap-3">
                {g.mods.map((m) => {
                  const p = progressOf(m.key)
                  const locked = isLocked(m)
                  return (
                    <Link key={m.key} to={`/lernen/${m.key}`}
                      className="rounded-xl border bg-white p-4 hover:shadow block">
                      <div className="flex items-center justify-between gap-3">
                        <span className="flex items-center gap-2 font-medium text-slate-800">
                          <span aria-hidden="true" className={`w-2 h-2 rounded-full shrink-0 ${p?.done ? 'bg-green-500' : locked ? 'bg-slate-300' : 'bg-teal-500'}`} />
                          {lang === 'de' ? m.title : m.title_en}
                        </span>
                        <span className="shrink-0 text-sm text-slate-500">
                          {p?.done ? `✓ ${t(lang, 'done')}` : t(lang, 'open')}{p?.best != null ? ` · ${t(lang, 'best')} ${p.best}%` : ''}
                        </span>
                      </div>
                      {m.prerequisites.length > 0 && (
                        <p className={`text-xs mt-1 flex items-center gap-1 ${locked ? 'text-amber-600' : 'text-slate-400'}`}>
                          <span aria-hidden="true">{locked ? '🔒' : '✓'}</span>
                          {t(lang, 'prerequisitesHint')}: {m.prerequisites.map(titleOf).join(', ')}
                        </p>
                      )}
                    </Link>
                  )
                })}
              </div>
            </div>
          ))}
        </div>

        {links.data && links.data.length > 0 && (
          <div className="mt-10">
            <h2 className="font-semibold text-slate-900">{t(lang, 'linksTitle')}</h2>
            <p className="text-sm text-slate-500 mb-4">{t(lang, 'linksIntro')}</p>
            <div className="flex flex-col gap-4">
              {links.data.map((cat) => (
                <div key={cat.category.de} className="rounded-2xl border bg-white p-5">
                  <h3 className="text-sm font-semibold text-slate-700 mb-2">{cat.category[lang]}</h3>
                  <div className="flex flex-col gap-2">
                    {cat.items.map((item) => (
                      <a key={item.url} href={item.url} target="_blank" rel="noopener noreferrer"
                        className="group text-sm">
                        <span className="font-medium text-teal-700 group-hover:underline">
                          {item.title} <span aria-hidden="true" className="text-teal-400">↗</span>
                        </span>
                        <span className="text-slate-600"> — {item.desc[lang]}</span>
                      </a>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )

  const view = mode === 'workbench'
    ? <WorkbenchLearnView
        lang={lang}
        displayName={displayName}
        modules={sorted}
        groups={grouped}
        progress={me.data?.progress ?? []}
        company={company.data}
        links={links.data ?? []}
        doneCount={doneCount}
        donePct={donePct}
        continueAt={continueAt}
        titleOf={titleOf}
        workshopTitle={workshopTitle}
        workshopSummary={workshopSummary}
        completionText={completionText}
        setLanguage={(value) => setLang.mutate(value)}
      />
    : <ClassicLearnView lang={lang}>{content}</ClassicLearnView>
  return <WorkshopTheme theme={me.data?.workshop?.theme}>{view}</WorkshopTheme>
}

export interface LearnViewProps {
  lang: Lang
  children: ReactNode
}

export function ClassicLearnView({ children }: LearnViewProps) {
  return children
}

export interface WorkbenchLearnProps {
  lang: Lang
  displayName: string | null
  modules: ModuleMeta[]
  groups: Group[]
  progress: ProgressItem[]
  company?: Company
  links: { category: Record<Lang, string>; items: { url: string; title: string; desc: Record<Lang, string> }[] }[]
  doneCount: number
  donePct: number
  continueAt?: ModuleMeta
  titleOf: (key: string) => string
  workshopTitle: string
  workshopSummary: string
  completionText: string
  setLanguage: (lang: Lang) => void
}

export function WorkbenchLearnView({ lang, displayName, modules, groups, progress, company, links, doneCount, donePct, continueAt, titleOf, workshopTitle, workshopSummary, completionText, setLanguage }: WorkbenchLearnProps) {
  const progressOf = (key: string) => progress.find((item) => item.module_key === key)
  const complete = modules.length > 0 && doneCount === modules.length
  const langControl = (
    <div className="flex" aria-label={lang === 'de' ? 'Sprache' : 'Language'}>
      {(['de', 'en'] as Lang[]).map((value) => (
        <button key={value} type="button" onClick={() => setLanguage(value)} aria-pressed={lang === value}
          className={`wb-control min-w-11 px-2 text-xs font-semibold uppercase ${lang === value ? 'text-[var(--wb-accent)]' : 'text-[var(--wb-muted)]'}`}>
          {value}
        </button>
      ))}
    </div>
  )

  return (
    <div className="workbench">
      <WorkbenchTopbar lang={lang} title={workshopTitle} actions={langControl} />
      <div className="wb-shell">
        <div className="mb-8 grid gap-5 lg:grid-cols-[minmax(0,1fr)_320px] lg:items-end">
          <div>
            <p className="mb-2 text-sm font-medium text-[var(--wb-accent)]">{workshopTitle}</p>
            <h1 className="max-w-3xl text-3xl font-bold leading-tight tracking-tight text-[var(--wb-ink)] sm:text-4xl">
              {t(lang, 'hello')} {displayName ?? ''}
            </h1>
            <p className="mt-2 max-w-[65ch] text-[var(--wb-muted)]">{workshopSummary}</p>
          </div>
          <div className="wb-surface p-5"><WorkbenchProgress value={donePct} label={t(lang, 'courseProgress')} /></div>
        </div>

        {complete && (
          <div className="wb-surface mb-6 flex flex-col gap-4 border-[var(--wb-accent)] bg-[var(--wb-accent-soft)] p-5 sm:flex-row sm:items-center sm:justify-between">
            <div><p className="font-semibold">{t(lang, 'courseComplete')}</p><p className="text-sm text-[var(--wb-muted)]">{completionText}</p></div>
            <Link to="/lernen/zertifikat" className="wb-control inline-flex items-center justify-center rounded-lg bg-[var(--wb-accent)] px-4 font-semibold text-white hover:bg-[var(--wb-accent-hover)]">{t(lang, 'certButton')}</Link>
          </div>
        )}

        <div className="grid min-w-0 gap-8 xl:grid-cols-[minmax(0,1fr)_320px]">
          <main className="min-w-0">
            {continueAt && (
              <Link to={`/lernen/${continueAt.key}`} className="wb-surface group mb-8 block border-[var(--wb-accent)] bg-[var(--wb-ink)] p-5 text-white hover:border-[var(--wb-accent)]">
                <span className="text-xs font-semibold uppercase tracking-[0.14em] text-teal-200">{t(lang, 'continueHere')}</span>
                <span className="mt-2 flex items-center justify-between gap-4 text-xl font-semibold">
                  {lang === 'de' ? continueAt.title : continueAt.title_en}<span aria-hidden="true" className="text-teal-300 transition-transform group-hover:translate-x-1">→</span>
                </span>
              </Link>
            )}

            <div className="space-y-8">
              {groups.map((group) => (
                <section key={group.key}>
                  <WorkbenchSectionTitle meta={`${group.mods.filter((m) => progressOf(m.key)?.done).length}/${group.mods.length}`}>{group.title}</WorkbenchSectionTitle>
                  <div className="wb-surface divide-y divide-[var(--wb-border)] overflow-hidden">
                    {group.mods.map((module) => {
                      const itemProgress = progressOf(module.key)
                      const locked = module.prerequisites.some((key) => !progressOf(key)?.done)
                      const rowClass = 'wb-control grid min-w-0 gap-1 px-4 py-3 sm:grid-cols-[40px_minmax(0,1fr)_auto] sm:items-center sm:gap-3'
                      const rowContent = <>
                          <span aria-hidden="true" className={`row-span-2 grid h-8 w-8 place-items-center rounded-lg text-xs font-bold ${itemProgress?.done ? 'bg-emerald-100 text-[var(--wb-success)]' : locked ? 'bg-[var(--wb-subtle)] text-[var(--wb-muted)]' : 'bg-[var(--wb-accent-soft)] text-[var(--wb-accent)]'}`}>
                            {itemProgress?.done ? '✓' : module.order}
                          </span>
                          <span className="min-w-0 font-medium text-[var(--wb-ink)]">{lang === 'de' ? module.title : module.title_en}</span>
                          <span className="text-xs tabular-nums text-[var(--wb-muted)]">{itemProgress?.best != null ? `${t(lang, 'best')} ${itemProgress.best}%` : locked ? (lang === 'de' ? 'Voraussetzung offen' : 'Prerequisite open') : t(lang, 'open')}</span>
                          {module.prerequisites.length > 0 && <span className="min-w-0 text-xs text-[var(--wb-muted)] sm:col-start-2">{t(lang, 'prerequisitesHint')}: {module.prerequisites.map(titleOf).join(', ')}</span>}
                        </>
                      return locked
                        ? <div key={module.key} aria-disabled="true" className={`${rowClass} cursor-not-allowed opacity-65`}>{rowContent}</div>
                        : <Link key={module.key} to={`/lernen/${module.key}`} className={`${rowClass} hover:bg-[var(--wb-accent-soft)]`}>{rowContent}</Link>
                    })}
                  </div>
                </section>
              ))}
            </div>
          </main>

          <aside className="min-w-0 space-y-5 xl:sticky xl:top-20 xl:self-start">
            {company && <section className="wb-surface p-5"><WorkbenchSectionTitle>{company.name}</WorkbenchSectionTitle><p className="text-sm leading-relaxed text-[var(--wb-muted)]">{company.blurb}</p><p className="mt-4 text-xs font-semibold text-[var(--wb-ink)]">{t(lang, 'sites')}</p><p className="mt-1 text-sm text-[var(--wb-muted)]">{company.sites.join(', ')}</p><div className="mt-3 flex flex-wrap gap-2">{company.devices.map((device) => <span key={device} className="rounded-md bg-[var(--wb-subtle)] px-2 py-1 text-xs text-[var(--wb-muted)]">{device}</span>)}</div></section>}
            {links.length > 0 && <details className="wb-surface p-5"><summary className="wb-control flex cursor-pointer items-center font-semibold">{t(lang, 'linksTitle')}</summary><div className="mt-3 space-y-4">{links.map((category) => <div key={category.category.de}><p className="text-xs font-semibold text-[var(--wb-muted)]">{category.category[lang]}</p>{category.items.map((item) => <a key={item.url} href={item.url} target="_blank" rel="noreferrer" className="wb-control flex items-center text-sm font-medium text-[var(--wb-accent)] hover:underline">{item.title}<span aria-hidden="true" className="ml-auto">↗</span></a>)}</div>)}</div></details>}
          </aside>
        </div>
      </div>
    </div>
  )
}
