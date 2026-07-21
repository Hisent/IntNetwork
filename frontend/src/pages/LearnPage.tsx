import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { PageSkeleton } from '@/components/PageSkeleton'
import { LoadError } from '@/components/LoadError'
import type { Company, ModuleMeta, ProgressItem } from '@/types'
import { useAuthStore } from '@/store/auth'
import { t, useDocumentLang, type Lang } from '@/lib/i18n'
import { LangToggle, WorkbenchProgress, WorkbenchSectionTitle, WorkbenchTopbar } from '@/components/workbench/WorkbenchShell'
import { groupModulesBySection } from '@/lib/moduleGroups'
import { markLockedVisibility } from '@/lib/lockedModules'
import { WorkshopTheme } from '@/components/WorkshopTheme'

type Group = { key: string; title: string; mods: ModuleMeta[] }

export function LearnPage() {
  const nav = useNavigate()
  const qc = useQueryClient()
  const { role, displayName } = useAuthStore()
  const me = useQuery({ queryKey: ['me'], queryFn: () => learnApi.me().then((r) => r.data) })
  const lang: Lang = me.data?.language ?? 'de'
  useDocumentLang(lang)
  const mods = useQuery({ queryKey: ['modules', lang], queryFn: () => learnApi.listModules().then((r) => r.data) })
  const networkWorkshop = me.data?.workshop?.key === 'network'
  const company = useQuery({ queryKey: ['company', lang], queryFn: () => learnApi.company().then((r) => r.data), enabled: networkWorkshop })
  const links = useQuery({ queryKey: ['links', me.data?.workshop?.key], queryFn: () => learnApi.links().then((r) => r.data), enabled: !!me.data?.workshop })
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
  if (me.isError || mods.isError) return <LoadError lang={lang} onRetry={() => { me.refetch(); mods.refetch() }} />
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
  const grouped: Group[] = groupModulesBySection(sorted, me.data?.workshop?.sections)
    .map((g) => ({ key: g.key, title: lang === 'de' ? g.title_de : g.title_en, mods: g.modules }))
  const workshopTitle = me.data?.workshop?.title[lang] ?? 'IntLab'
  const workshopSummary = me.data?.workshop?.summary?.[lang] ?? t(lang, 'tagline')
  const completionText = lang === 'de' ? 'Alle Module dieses Workshops sind bestanden.' : 'All modules in this workshop are passed.'

  return (
    <WorkshopTheme theme={me.data?.workshop?.theme}>
      <WorkbenchLearnView
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
    </WorkshopTheme>
  )
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
  const isLocked = (module: ModuleMeta) => module.prerequisites.some((key) => !progressOf(key)?.done)
  const hasLocked = modules.some(isLocked)
  // Nur die nächsten paar gesperrten Module bleiben sichtbar (Kursreihenfolge)
  // — der Rest verschwindet hinter "Weitere Module anzeigen", damit der
  // erste Eindruck nach dem Beitritt nicht aus einer Wand aus "Voraussetzung
  // offen"-Zeilen besteht. Abgeschlossene/freigeschaltete Module sind davon
  // nie betroffen.
  const visibleKeys = new Set(
    markLockedVisibility(modules.map((module) => ({ key: module.key, locked: isLocked(module) })))
      .filter((entry) => entry.visible)
      .map((entry) => entry.key),
  )
  const langControl = <LangToggle lang={lang} onChange={setLanguage} />

  const renderModuleRow = (module: ModuleMeta) => {
    const itemProgress = progressOf(module.key)
    const locked = isLocked(module)
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
  }

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
          <div className="wb-surface p-5">
            <WorkbenchProgress value={donePct} label={t(lang, 'courseProgress')} />
            {/* Gesamtumfang bleibt ablesbar, auch wenn gesperrte Module weiter
                unten zusammengeklappt sind. */}
            <p className="mt-2 text-xs text-[var(--wb-muted)]">{doneCount}/{modules.length} {t(lang, 'modules')}</p>
          </div>
        </div>

        {complete && (
          <div className="wb-surface mb-6 flex flex-col gap-4 border-[var(--wb-accent)] bg-[var(--wb-accent-soft)] p-5 sm:flex-row sm:items-center sm:justify-between">
            <div><p className="font-semibold">{t(lang, 'courseComplete')}</p><p className="text-sm text-[var(--wb-muted)]">{completionText}</p></div>
            <Link to="/lernen/zertifikat" className="wb-control inline-flex items-center justify-center rounded-lg bg-[var(--wb-accent)] px-4 font-semibold text-white hover:bg-[var(--wb-accent-hover)]">{t(lang, 'certButton')}</Link>
          </div>
        )}

        <div className="grid min-w-0 gap-8 xl:grid-cols-[minmax(0,1fr)_320px]">
          <main id="main-content" tabIndex={-1} className="min-w-0">
            {continueAt && (
              <Link to={`/lernen/${continueAt.key}`} className="wb-surface wb-surface--highlight group mb-8 block border-[var(--wb-accent)] p-5 hover:border-[var(--wb-accent)]">
                <span className="text-xs font-semibold uppercase tracking-[0.14em] text-teal-200">{t(lang, 'continueHere')}</span>
                <span className="mt-2 flex items-center justify-between gap-4 text-xl font-semibold">
                  {lang === 'de' ? continueAt.title : continueAt.title_en}<span aria-hidden="true" className="text-teal-300 transition-transform group-hover:translate-x-1">→</span>
                </span>
              </Link>
            )}

            {hasLocked && <p className="mb-5 max-w-[65ch] text-sm text-[var(--wb-muted)]">{t(lang, 'lockedOrderHint')}</p>}

            <div className="space-y-8">
              {groups.map((group) => {
                const shownMods = group.mods.filter((module) => visibleKeys.has(module.key))
                const hiddenMods = group.mods.filter((module) => !visibleKeys.has(module.key))
                return (
                  <section key={group.key}>
                    <WorkbenchSectionTitle meta={`${group.mods.filter((m) => progressOf(m.key)?.done).length}/${group.mods.length}`}>{group.title}</WorkbenchSectionTitle>
                    <div className="wb-surface divide-y divide-[var(--wb-border)] overflow-hidden">
                      {shownMods.map(renderModuleRow)}
                      {hiddenMods.length > 0 && (
                        <details>
                          <summary className="wb-control flex cursor-pointer items-center px-4 py-3 text-sm font-medium text-[var(--wb-accent)] hover:underline">
                            {t(lang, 'showMoreModules')} ({hiddenMods.length})
                          </summary>
                          <div className="divide-y divide-[var(--wb-border)]">{hiddenMods.map(renderModuleRow)}</div>
                        </details>
                      )}
                    </div>
                  </section>
                )
              })}
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
