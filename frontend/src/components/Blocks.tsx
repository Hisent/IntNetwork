import { Suspense, useState, type ReactNode } from 'react'
import Markdown from 'react-markdown'
import type { Block } from '@/types'
import { WIDGETS } from '@/widgets/registry'
import { t, type Lang } from '@/lib/i18n'

export const MD_COMPONENTS = {
  h2: (p: object) => <h2 className="text-xl font-bold text-slate-900 mt-2 mb-1" {...p} />,
  h3: (p: object) => <h3 className="text-base font-semibold text-slate-800 mt-2 mb-1" {...p} />,
  p: (p: object) => <p className="text-slate-700 leading-relaxed" {...p} />,
  ul: (p: object) => <ul className="list-disc pl-5 text-slate-700 space-y-1 my-1" {...p} />,
  ol: (p: object) => <ol className="list-decimal pl-5 text-slate-700 space-y-1 my-1" {...p} />,
  strong: (p: object) => <strong className="font-semibold text-slate-900" {...p} />,
}

export function WidgetBlock({ id, lang }: { id: string; lang: Lang }) {
  const W = WIDGETS[id]
  if (!W) return <div className="text-sm text-red-500">Unbekanntes Widget: {id}</div>
  return (
    <Suspense fallback={<div className="rounded-xl border bg-white p-6 text-sm text-slate-400 animate-pulse">{t(lang, 'loading')}</div>}>
      <W lang={lang} />
    </Suspense>
  )
}

export function CheckBlock({ prompt, options, answer, lang }: {
  prompt: string; options: string[]; answer: number; lang: Lang
}) {
  const [picked, setPicked] = useState<number | null>(null)
  const correct = picked === answer
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{t(lang, 'quickCheck')}</p>
      <p className="font-medium text-slate-800 mb-2">{prompt}</p>
      <div className="flex flex-col gap-1.5">
        {options.map((opt, i) => (
          <button key={i} onClick={() => setPicked(i)} disabled={picked !== null}
            className={`text-left rounded-lg border px-3 py-1.5 text-sm transition-colors ${
              picked === null ? 'border-slate-200 text-slate-700 hover:bg-slate-50'
              : i === answer ? 'border-green-300 bg-green-50 text-green-800'
              : i === picked ? 'border-amber-300 bg-amber-50 text-amber-800'
              : 'border-slate-100 text-slate-400'}`}>
            {opt}
          </button>
        ))}
      </div>
      {picked !== null && (
        <div className="mt-2 flex items-center gap-3 text-sm">
          <span className={correct ? 'text-green-600 font-medium' : 'text-amber-600 font-medium'}>
            {correct ? `✓ ${t(lang, 'correct')}` : `✗ ${t(lang, 'incorrect')}`}
          </span>
          {!correct && (
            <button onClick={() => setPicked(null)} className="text-xs text-slate-500 underline hover:text-slate-700">
              {t(lang, 'tryAgainShort')}
            </button>
          )}
        </div>
      )}
    </div>
  )
}

export function RevealBlock({ teaser, value, lang }: { teaser: string; value: string; lang: Lang }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="font-medium text-slate-800">{teaser}</p>
      {open ? (
        <div className="mt-2 animate-fade-up"><Markdown components={MD_COMPONENTS}>{value}</Markdown></div>
      ) : (
        <button onClick={() => setOpen(true)}
          className="mt-2 rounded-lg border border-teal-200 text-teal-700 px-3 py-1.5 text-sm font-medium hover:bg-teal-50">
          {t(lang, 'reveal')}
        </button>
      )}
    </div>
  )
}

export function Blocks({
  blocks,
  lang = 'de',
  footer,
}: {
  blocks: Block[]
  lang?: Lang
  footer?: (block: Block, index: number) => ReactNode
}) {
  return (
    <div className="flex flex-col gap-6">
      {blocks.map((b, i) => (
        <div key={i} className="flex flex-col gap-1">
          {b.type === 'text' && <Markdown components={MD_COMPONENTS}>{b.value}</Markdown>}
          {b.type === 'image' && <img src={b.url} alt={b.alt ?? ''} className="rounded-lg border" />}
          {b.type === 'widget' && <WidgetBlock id={b.id} lang={lang} />}
          {b.type === 'check' && <CheckBlock prompt={b.prompt} options={b.options} answer={b.answer} lang={lang} />}
          {b.type === 'reveal' && <RevealBlock teaser={b.teaser} value={b.value} lang={lang} />}
          {footer?.(b, i)}
        </div>
      ))}
    </div>
  )
}
