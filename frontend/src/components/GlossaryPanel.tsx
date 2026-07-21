import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'

import { GLOSSARY, termsForModule } from '@/lib/glossary'
import type { Lang } from '@/lib/i18n'

export function GlossaryPanel({ moduleKey, lang }: { moduleKey: string; lang: Lang }) {
  const [open, setOpen] = useState(false)
  const [all, setAll] = useState(false)
  const [search, setSearch] = useState('')
  const terms = (all ? GLOSSARY : termsForModule(moduleKey)).filter((term) => {
    const query = search.trim().toLocaleLowerCase()
    return !query || (term.label[lang] + ' ' + term.description[lang]).toLocaleLowerCase().includes(query)
  })
  useEffect(() => {
    if (!open) return
    const closeOnEscape = (event: KeyboardEvent) => { if (event.key === 'Escape') setOpen(false) }
    document.addEventListener('keydown', closeOnEscape)
    document.body.classList.add('overflow-hidden')
    return () => {
      document.removeEventListener('keydown', closeOnEscape)
      document.body.classList.remove('overflow-hidden')
    }
  }, [open])
  const copy = lang === 'de'
    ? { button: 'Glossar', title: 'Begriffe in diesem Modul', all: 'Alle Begriffe', contextual: 'Nur dieses Modul', empty: 'Für dieses Modul sind noch keine Begriffe hinterlegt.' }
    : { button: 'Glossary', title: 'Terms in this module', all: 'All terms', contextual: 'This module only', empty: 'No terms have been added for this module yet.' }

  return (
    <>
      <button onClick={() => setOpen(true)} className="rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-xs font-medium text-slate-600 hover:bg-slate-50">
        {copy.button}
      </button>
      {open && createPortal(
        <div className="fixed inset-0 z-[100] flex items-end justify-center bg-slate-900/30 p-4 sm:items-center" role="dialog" aria-modal="true" aria-labelledby="glossary-title"
          onMouseDown={(event) => { if (event.target === event.currentTarget) setOpen(false) }}>
          <div className="w-full max-w-lg rounded-2xl bg-white p-5 shadow-xl">
            <div className="mb-4 flex items-start justify-between gap-4">
              <div>
                <p id="glossary-title" className="font-semibold text-slate-900">{copy.title}</p>
                <button onClick={() => setAll((value) => !value)} className="mt-1 text-xs text-teal-700 hover:underline">
                  {all ? copy.contextual : copy.all}
                </button>
              </div>
              <button onClick={() => setOpen(false)} className="text-sm text-slate-400 hover:text-slate-700" aria-label="Schließen">✕</button>
            </div>
            <input autoFocus value={search} onChange={(event) => setSearch(event.target.value)}
              aria-label={lang === 'de' ? 'Begriff suchen' : 'Search term'}
              placeholder={lang === 'de' ? 'Begriff suchen …' : 'Search term …'}
              className="mb-3 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-700 focus:border-teal-500" />
            <div className="max-h-[60vh] space-y-3 overflow-y-auto pr-1">
              {terms.length === 0 && <p className="text-sm text-slate-500">{copy.empty}</p>}
              {terms.map((term) => (
                <article key={term.key} className="rounded-xl border border-slate-200 bg-slate-50 p-3">
                  <h2 className="text-sm font-semibold text-slate-800">{term.label[lang]}</h2>
                  <p className="mt-1 text-sm leading-relaxed text-slate-600">{term.description[lang]}</p>
                </article>
              ))}
            </div>
          </div>
        </div>,
        document.body,
      )}
    </>
  )
}
