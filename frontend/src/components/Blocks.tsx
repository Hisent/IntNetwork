import { Suspense, useMemo, useState, type ReactNode } from 'react'
import Markdown from 'react-markdown'
import type { Block } from '@/types'
import { WIDGETS } from '@/widgets/registry'
import { shuffledIndices } from '@/components/Quiz'
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
    // Breakout: Widgets dürfen breiter sein als die schmale Textspalte
    // (auf großen Screens bis 60rem, zentriert; auf kleinen = Spaltenbreite).
    <div className="relative left-1/2 -translate-x-1/2 w-[min(60rem,100vw-3rem)]">
      <Suspense fallback={<div className="rounded-xl border bg-white p-6 text-sm text-slate-400 animate-pulse">{t(lang, 'loading')}</div>}>
        <W lang={lang} />
      </Suspense>
    </div>
  )
}

function NumberCheck({ answer, lang }: { answer: number; lang: Lang }) {
  const [val, setVal] = useState('')
  const [checked, setChecked] = useState(false)
  const correct = Number(val) === answer
  return (
    <div>
      <div className="flex items-center gap-2">
        <input type="number" value={val} disabled={checked}
          onChange={(e) => setVal(e.target.value)}
          className="w-32 border border-slate-200 rounded-lg px-3 py-1.5 text-sm font-mono" />
        <button onClick={() => setChecked(true)} disabled={checked || val === ''}
          className="rounded-lg border border-teal-200 text-teal-700 px-3 py-1.5 text-sm font-medium hover:bg-teal-50 disabled:opacity-50">
          {t(lang, 'checkIt')}
        </button>
      </div>
      {checked && (
        <div className="mt-2 flex items-center gap-3 text-sm">
          <span className={correct ? 'text-green-600 font-medium' : 'text-amber-600 font-medium'}>
            {correct ? `✓ ${t(lang, 'correct')}` : `✗ ${t(lang, 'incorrect')}`}
          </span>
          {!correct && (
            <button onClick={() => { setChecked(false); setVal('') }}
              className="text-xs text-slate-500 underline hover:text-slate-700">
              {t(lang, 'tryAgainShort')}
            </button>
          )}
        </div>
      )}
    </div>
  )
}

export function CheckBlock({ prompt, options, answer, kind, lang }: {
  prompt: string; options: string[]; answer: number; kind?: 'choice' | 'number'; lang: Lang
}) {
  const [picked, setPicked] = useState<number | null>(null)
  const correct = picked === answer
  if (kind === 'number') {
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{t(lang, 'quickCheck')}</p>
        <p className="font-medium text-slate-800 mb-2">{prompt}</p>
        <NumberCheck answer={answer} lang={lang} />
      </div>
    )
  }
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

export function OrderBlock({ prompt, items, lang }: { prompt: string; items: string[]; lang: Lang }) {
  const initial = useMemo(() => shuffledIndices(items.length), [items])
  const [pool, setPool] = useState<number[]>(initial)
  const [seq, setSeq] = useState<number[]>([])
  const [checked, setChecked] = useState(false)
  const allCorrect = checked && seq.every((idx, pos) => idx === pos)

  const reset = () => { setPool(shuffledIndices(items.length)); setSeq([]); setChecked(false) }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{t(lang, 'sequence')}</p>
      <p className="font-medium text-slate-800 mb-1">{prompt}</p>
      <p className="text-xs text-slate-400 mb-2">{t(lang, 'orderHint')}</p>
      {seq.length > 0 && (
        <ol className="flex flex-col gap-1.5 mb-2">
          {seq.map((idx, pos) => (
            <li key={idx}>
              <button onClick={() => { if (checked) return; setSeq((s) => s.filter((x) => x !== idx)); setPool((p) => [...p, idx]) }}
                disabled={checked}
                className={`w-full text-left rounded-lg border px-3 py-1.5 text-sm flex items-center gap-2 ${
                  !checked ? 'border-slate-200 text-slate-700 hover:bg-slate-50'
                  : idx === pos ? 'border-green-300 bg-green-50 text-green-800'
                  : 'border-amber-300 bg-amber-50 text-amber-800'}`}>
                <span className="font-mono text-xs text-slate-400">{pos + 1}.</span> {items[idx]}
                {checked && <span className="ml-auto">{idx === pos ? '✓' : '✗'}</span>}
              </button>
            </li>
          ))}
        </ol>
      )}
      {pool.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-2">
          {pool.map((idx) => (
            <button key={idx} onClick={() => { setSeq((s) => [...s, idx]); setPool((p) => p.filter((x) => x !== idx)) }}
              className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-100">
              {items[idx]}
            </button>
          ))}
        </div>
      )}
      {!checked && pool.length === 0 && (
        <button onClick={() => setChecked(true)}
          className="rounded-lg border border-teal-200 text-teal-700 px-3 py-1.5 text-sm font-medium hover:bg-teal-50">
          {t(lang, 'checkIt')}
        </button>
      )}
      {checked && (
        <div className="flex items-center gap-3 text-sm">
          <span className={allCorrect ? 'text-green-600 font-medium' : 'text-amber-600 font-medium'}>
            {allCorrect ? `✓ ${t(lang, 'correct')}` : `✗ ${t(lang, 'incorrect')}`}
          </span>
          {!allCorrect && (
            <button onClick={reset} className="text-xs text-slate-500 underline hover:text-slate-700">
              {t(lang, 'tryAgainShort')}
            </button>
          )}
        </div>
      )}
    </div>
  )
}

export function DebugBlock({ prompt, lines, wrong, explanation, lang }: {
  prompt: string; lines: string[]; wrong: number[]; explanation: string; lang: Lang
}) {
  const [sel, setSel] = useState<Set<number>>(new Set())
  const [checked, setChecked] = useState(false)
  const wrongSet = useMemo(() => new Set(wrong), [wrong])
  const solved = checked && sel.size === wrongSet.size && [...sel].every((i) => wrongSet.has(i))

  const toggle = (i: number) => {
    if (checked) return
    setSel((s) => { const n = new Set(s); if (n.has(i)) n.delete(i); else n.add(i); return n })
  }
  const lineStyle = (i: number) => {
    if (!checked) return sel.has(i) ? 'bg-amber-50 border-l-2 border-amber-400' : 'hover:bg-slate-50 border-l-2 border-transparent'
    if (wrongSet.has(i) && sel.has(i)) return 'bg-green-50 border-l-2 border-green-400'
    if (wrongSet.has(i)) return 'bg-amber-50 border-l-2 border-amber-400'
    if (sel.has(i)) return 'bg-rose-50 border-l-2 border-rose-300'
    return 'border-l-2 border-transparent'
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{t(lang, 'findError')}</p>
      <p className="font-medium text-slate-800 mb-1">{prompt}</p>
      <p className="text-xs text-slate-400 mb-2">{t(lang, 'debugHint')}</p>
      <div className="rounded-lg border border-slate-200 bg-slate-900 py-2 mb-2 font-mono text-xs">
        {lines.map((line, i) => (
          <button key={i} onClick={() => toggle(i)} disabled={checked}
            className={`block w-full text-left px-3 py-1 text-slate-100 ${lineStyle(i)}`}>
            {line}
          </button>
        ))}
      </div>
      {!checked ? (
        <button onClick={() => setChecked(true)} disabled={sel.size === 0}
          className="rounded-lg border border-teal-200 text-teal-700 px-3 py-1.5 text-sm font-medium hover:bg-teal-50 disabled:opacity-50">
          {t(lang, 'checkIt')}
        </button>
      ) : (
        <div className="text-sm">
          <div className="flex items-center gap-3 mb-1">
            <span className={solved ? 'text-green-600 font-medium' : 'text-amber-600 font-medium'}>
              {solved ? `✓ ${t(lang, 'correct')}` : `✗ ${t(lang, 'incorrect')}`}
            </span>
            {!solved && (
              <button onClick={() => { setSel(new Set()); setChecked(false) }}
                className="text-xs text-slate-500 underline hover:text-slate-700">
                {t(lang, 'tryAgainShort')}
              </button>
            )}
          </div>
          <p className="text-slate-600 animate-fade-up">{explanation}</p>
        </div>
      )}
    </div>
  )
}

export function ReflectBlock({ prompt, storageKey, lang }: { prompt: string; storageKey: string; lang: Lang }) {
  const [text, setText] = useState(() => localStorage.getItem(storageKey) ?? '')
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{t(lang, 'reflection')}</p>
      <p className="font-medium text-slate-800 mb-2">{prompt}</p>
      <textarea value={text} rows={3}
        onChange={(e) => { setText(e.target.value); localStorage.setItem(storageKey, e.target.value) }}
        className="w-full border border-slate-200 rounded-lg px-3 py-1.5 text-sm text-slate-700" />
      <p className="text-xs text-slate-400 mt-1">{t(lang, 'reflectHint')}</p>
    </div>
  )
}

export function Blocks({
  blocks,
  lang = 'de',
  moduleKey = '',
  footer,
}: {
  blocks: Block[]
  lang?: Lang
  moduleKey?: string
  footer?: (block: Block, index: number) => ReactNode
}) {
  const phaseOf = (type: Block['type']): 'understand' | 'practice' | 'reflect' => {
    if (type === 'widget' || type === 'check' || type === 'order' || type === 'debug') return 'practice'
    if (type === 'reflect') return 'reflect'
    return 'understand'
  }
  const phaseLabel = (phase: ReturnType<typeof phaseOf>) => {
    if (lang === 'en') return phase === 'understand' ? 'Understand' : phase === 'practice' ? 'Try it' : 'Reflect'
    return phase === 'understand' ? 'Verstehen' : phase === 'practice' ? 'Ausprobieren' : 'Reflektieren'
  }

  return (
    <div className="flex flex-col gap-6">
      {blocks.map((b, i) => (
        <div key={i} id={`block-${i}`} className="flex flex-col gap-1 scroll-mt-20">
          {(i === 0 || phaseOf(blocks[i - 1].type) !== phaseOf(b.type)) && (
            <div className="mb-1 flex items-center gap-3 pt-2">
              <span className="text-[11px] font-semibold uppercase tracking-[0.18em] text-teal-700">{phaseLabel(phaseOf(b.type))}</span>
              <div className="h-px flex-1 bg-teal-100" aria-hidden="true" />
            </div>
          )}
          {b.type === 'text' && <Markdown components={MD_COMPONENTS}>{b.value}</Markdown>}
          {b.type === 'widget' && <WidgetBlock id={b.id} lang={lang} />}
          {b.type === 'check' && <CheckBlock prompt={b.prompt} options={b.options} answer={b.answer} kind={b.kind} lang={lang} />}
          {b.type === 'reveal' && <RevealBlock teaser={b.teaser} value={b.value} lang={lang} />}
          {b.type === 'order' && <OrderBlock prompt={b.prompt} items={b.items} lang={lang} />}
          {b.type === 'debug' && <DebugBlock prompt={b.prompt} lines={b.lines} wrong={b.wrong} explanation={b.explanation} lang={lang} />}
          {b.type === 'reflect' && <ReflectBlock prompt={b.prompt} storageKey={`intnetwork-reflect-${moduleKey}-${i}`} lang={lang} />}
          {footer?.(b, i)}
        </div>
      ))}
    </div>
  )
}
