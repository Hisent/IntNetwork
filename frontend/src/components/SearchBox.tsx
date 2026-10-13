import { useEffect, useId, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { GLOSSARY } from '@/lib/glossary'
import { Icon } from '@/components/Icon'
import { localTitle, t, type Lang } from '@/lib/i18n'
import { openPrerequisites } from '@/lib/lockedModules'
import type { ModuleMeta, ProgressItem } from '@/types'

const MIN = 2

// Suche über die Module des Kurses: Titel, Lernziele und Text-Blöcke kommen vom
// Server (/search, kursgefiltert), das Glossar liegt im Frontend und wird hier
// auf die Module des Kurses eingegrenzt. Treffer in einem Text-Block springen
// über dessen Kennung direkt zum Block (#b-<uid>, siehe ModulePage).
// Die Suche findet auch Module, deren Voraussetzung noch offen ist (die
// Reihenfolge ist Führung, keine Sperre) — solche Treffer sind gekennzeichnet.
export function SearchBox({ lang, modules, progress = [] }: { lang: Lang; modules: ModuleMeta[]; progress?: ProgressItem[] }) {
  const de = lang === 'de'
  const id = useId()
  const [input, setInput] = useState('')
  const [term, setTerm] = useState('')
  // erst suchen, wenn kurz nicht getippt wurde — schont das Rate-Limit des Klassenraums
  useEffect(() => {
    const timer = setTimeout(() => setTerm(input.trim()), 300)
    return () => clearTimeout(timer)
  }, [input])
  const active = term.length >= MIN
  const search = useQuery({
    queryKey: ['search', lang, term],
    queryFn: () => learnApi.search(term).then((r) => r.data),
    enabled: active,
    staleTime: 60_000,
  })
  const titles = new Map(modules.map((m) => [m.key, localTitle(m, lang)]))
  // Hinweis „Baut auf <Modul> auf“ für Treffer in Modulen mit offener Voraussetzung
  const buildsOn = (key: string) => {
    const module = modules.find((m) => m.key === key)
    const open = module ? openPrerequisites(module, progress, modules) : []
    if (open.length === 0) return null
    return (
      <span className="mt-0.5 flex items-center gap-1 text-xs text-[var(--wb-muted)]">
        <Icon name="lock" className="h-3.5 w-3.5 shrink-0" />
        {t(lang, 'buildsOn')} „{open.map((k) => titles.get(k) ?? k).join(', ')}“{t(lang, 'buildsOnEnd')}
      </span>
    )
  }
  const needle = term.toLowerCase()
  const terms = active
    ? GLOSSARY.filter((g) => g.modules.some((key) => titles.has(key))
      && (g.label[lang].toLowerCase().includes(needle) || g.description[lang].toLowerCase().includes(needle)))
    : []
  const hits = search.data?.hits ?? []
  const kindLabel = { title: de ? 'Modul' : 'Module', goal: de ? 'Lernziel' : 'Learning goal', text: de ? 'Text' : 'Text' }

  return (
    <section className="mb-8" role="search">
      <label htmlFor={id} className="sr-only">{de ? 'Kursinhalte durchsuchen' : 'Search course content'}</label>
      <div className="wb-surface flex items-center gap-2 px-3">
        <Icon name="search" className="h-4 w-4 shrink-0 text-[var(--wb-muted)]" />
        <input id={id} type="search" value={input} maxLength={80} onChange={(e) => setInput(e.target.value)}
          placeholder={de ? 'Kursinhalte durchsuchen …' : 'Search course content …'}
          className="wb-control min-w-0 flex-1 bg-transparent text-sm text-[var(--wb-ink)] outline-none placeholder:text-[var(--wb-muted)]" />
      </div>
      <div aria-live="polite">
        {active && (
          <div className="wb-surface mt-2 max-h-[60dvh] divide-y divide-[var(--wb-border)] overflow-y-auto">
            {search.isLoading && <p className="px-4 py-3 text-sm text-[var(--wb-muted)]">{de ? 'Sucht …' : 'Searching …'}</p>}
            {search.isError && <p className="px-4 py-3 text-sm text-[var(--wb-muted)]">{de ? 'Die Suche ist gerade nicht erreichbar. Bitte kurz warten.' : 'Search is unavailable right now. Please wait a moment.'}</p>}
            {search.data && hits.length === 0 && terms.length === 0 && (
              <p className="px-4 py-3 text-sm text-[var(--wb-muted)]">{de ? 'Keine Treffer in den Modulen deines Kurses.' : 'No matches in the modules of your course.'}</p>
            )}
            {terms.map((g) => {
              const key = g.modules.find((k) => titles.has(k))!
              return (
                <Link key={`g-${g.key}`} to={`/lernen/${key}`} className="wb-control block px-4 py-2 hover:bg-[var(--wb-accent-soft)]">
                  <span className="text-xs font-semibold text-[var(--wb-accent)]">{de ? 'Glossar' : 'Glossary'} · {titles.get(key)}</span>
                  <span className="block text-sm text-[var(--wb-ink)]"><strong>{g.label[lang]}</strong> — {g.description[lang]}</span>
                  {buildsOn(key)}
                </Link>
              )
            })}
            {hits.map((hit, i) => (
              <Link key={i} to={`/lernen/${hit.module_key}${hit.uid ? `#b-${hit.uid}` : ''}`} className="wb-control block px-4 py-2 hover:bg-[var(--wb-accent-soft)]">
                <span className="text-xs font-semibold text-[var(--wb-accent)]">{kindLabel[hit.kind]} · {hit.module_title}</span>
                <span className="block text-sm text-[var(--wb-ink)]">{hit.snippet}</span>
                {buildsOn(hit.module_key)}
              </Link>
            ))}
            {search.data?.more && <p className="px-4 py-2 text-xs text-[var(--wb-muted)]">{de ? 'Weitere Treffer — bitte den Suchbegriff eingrenzen.' : 'More matches — please narrow your search.'}</p>}
          </div>
        )}
      </div>
    </section>
  )
}
