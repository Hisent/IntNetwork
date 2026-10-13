import { Children, createContext, isValidElement, lazy, Suspense, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import Markdown from 'react-markdown'
import type { Block } from '@/types'
import { isDeclarative, type DeclarativeBlockData } from '@/components/blocks/types'
import { WIDGETS } from '@/widgets/registry'
import { shuffledIndices } from '@/components/Quiz'
import { t, type Lang } from '@/lib/i18n'
import { WidgetScopeContext } from '@/lib/widgetScope'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { Icon } from '@/components/Icon'
import { doneExercises, ExerciseSlotContext, exerciseStorageKey, fingerprint, legacyFingerprint, useExercise } from '@/lib/exerciseState'
import { usePrinting } from '@/lib/printMode'
import { useResultFocus } from '@/components/blocks/useResultFocus'

function InlineCode({ className, children }: {
  className?: string
  children?: ReactNode
}) {
  // overflow-wrap: lange URLs/Cipher-Suiten ohne Leerzeichen dürfen die Seite auf dem Handy nicht sprengen
  return <code className={`rounded bg-slate-100 px-1 py-0.5 font-mono text-[0.9em] text-teal-800 [overflow-wrap:anywhere] ${className ?? ''}`}>{children}</code>
}

// MD_COMPONENTS wird von react-markdown ohne Zusatz-Props aufgerufen — CodeBlock
// braucht die aktive Sprache trotzdem für den Kopieren-Button. Statt MD_COMPONENTS
// für alle Aufrufer (auch Trainer-Seiten außerhalb dieser Datei) auf eine Fabrik
// umzustellen, holt sich CodeBlock die Sprache implizit aus dem Kontext — analog
// zu WidgetScopeContext oben. Ohne Provider (z.B. Trainer-Ansichten) bleibt es bei 'de'.
const CodeLangContext = createContext<Lang>('de')

function CodeBlock({ children }: { children?: ReactNode }) {
  const lang = useContext(CodeLangContext)
  const [copied, setCopied] = useState(false)
  const child = Children.toArray(children)[0]
  const childProps = isValidElement<{ children?: ReactNode; className?: string }>(child) ? child.props : {}
  const source = String(childProps.children ?? '').replace(/\n$/, '')
  const language = childProps.className?.match(/language-([\w-]+)/)?.[1]

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(source)
      setCopied(true)
    } catch {
      setCopied(false)
    }
  }

  return (
    <div className="wb-code group relative my-3 overflow-hidden rounded-xl border border-slate-800 bg-slate-950 shadow-sm">
      <div className="flex items-center justify-between border-b border-slate-800 px-3 py-2 print:hidden">
        <span className="font-mono text-[11px] uppercase tracking-[0.14em] text-slate-500">{language ?? 'code'}</span>
        <button type="button" onClick={() => void copy()} aria-label="Code kopieren / Copy code" className="rounded-md px-2 py-1 text-xs font-medium text-teal-300 hover:bg-slate-800 hover:text-teal-100 focus-visible:outline-teal-300">
          {copied ? t(lang, 'copiedCode') : t(lang, 'copyCode')}
        </button>
      </div>
      <pre className="overflow-x-auto p-4 text-sm leading-relaxed text-slate-100"><code className="font-mono">{childProps.children}</code></pre>
    </div>
  )
}

// react-markdown reicht jedem Element zusätzlich `node` (den hast-Knoten) durch — ungefiltert
// gespreadet landete er als Attribut node="[object Object]" im DOM.
type MdProps = { node?: unknown; children?: ReactNode }

export const MD_COMPONENTS = {
  h2: ({ node: _node, ...p }: MdProps) => <h2 className="text-xl font-bold text-slate-900 mt-2 mb-1" {...p} />,
  h3: ({ node: _node, ...p }: MdProps) => <h3 className="text-base font-semibold text-slate-800 mt-2 mb-1" {...p} />,
  p: ({ node: _node, ...p }: MdProps) => <p className="text-slate-700 leading-relaxed" {...p} />,
  ul: ({ node: _node, ...p }: MdProps) => <ul className="list-disc pl-5 text-slate-700 space-y-1 my-1" {...p} />,
  ol: ({ node: _node, ...p }: MdProps) => <ol className="list-decimal pl-5 text-slate-700 space-y-1 my-1" {...p} />,
  strong: ({ node: _node, ...p }: MdProps) => <strong className="font-semibold text-slate-900" {...p} />,
  pre: CodeBlock,
  code: InlineCode,
}

export function WidgetBlock({ id, lang }: { id: string; lang: Lang }) {
  const W = WIDGETS[id]
  if (!W) return <div className="text-sm text-red-500">{lang === 'de' ? 'Unbekanntes Widget' : 'Unknown widget'}: {id}</div>
  return (
    // Widgets bleiben innerhalb der aktuellen Inhalts-/Navigationsspalte.
    // Tabellen und lange Inhalte müssen sich darin selbst scrollbar machen.
    <div className="w-full min-w-0">
      {/* key: ein anderes Widget an derselben Stelle (Folienwechsel) setzt auch die Fehlergrenze zurück */}
      <ErrorBoundary key={id} fallback={<div className="rounded-xl border bg-white p-6 text-sm text-slate-500">{lang === 'de' ? 'Dieses interaktive Element konnte nicht geladen werden.' : 'This interactive element could not be loaded.'}</div>}>
        <Suspense fallback={<div className="rounded-xl border bg-white p-6 text-sm text-slate-500 animate-pulse">{t(lang, 'loading')}</div>}>
          <W lang={lang} />
        </Suspense>
      </ErrorBoundary>
    </div>
  )
}

// Deklarativer Baukasten: jeder Typ ist ein eigener Lazy-Chunk (wie die Widgets),
// damit der Haupt-Chunk nicht mit SVG-Layout und Übungslogik wächst.
const DiagramBlock = lazy(() => import('@/components/blocks/DiagramBlock'))
const TerminalBlock = lazy(() => import('@/components/blocks/TerminalBlock'))
const MatchBlock = lazy(() => import('@/components/blocks/MatchBlock'))
const ClozeBlock = lazy(() => import('@/components/blocks/ClozeBlock'))
const ScenarioBlock = lazy(() => import('@/components/blocks/ScenarioBlock'))

export function DeclarativeBlock({ block: b, lang }: { block: DeclarativeBlockData; lang: Lang }) {
  // Der Zustand eines Blocks (Schritt, Zuordnung, Pfad …) gehört zu genau dieser Struktur.
  // Zeigt dieselbe Komponenteninstanz einen anderen Block (Folienwechsel im Beamer-Modus,
  // Content-Update bei offenem Modul), beginnt er neu — samt Fehlergrenze. Reine
  // Textänderungen (Sprachwechsel) ändern den Fingerabdruck nicht.
  const version = useMemo(() => fingerprint(b), [b])
  return (
    // contain: die Mindestbreite von SVG/Tabelle/Terminal darf die Seite nicht aufziehen —
    // der Block scrollt in sich (am Handy sonst waagerechter Seiten-Overflow).
    <div className="w-full min-w-0 [contain:inline-size]">
      <ErrorBoundary key={version} fallback={<div className="rounded-xl border bg-white p-6 text-sm text-slate-500">{lang === 'de' ? 'Dieses interaktive Element konnte nicht geladen werden.' : 'This interactive element could not be loaded.'}</div>}>
        <Suspense fallback={<div className="rounded-xl border bg-white p-6 text-sm text-slate-500 animate-pulse">{t(lang, 'loading')}</div>}>
          {b.type === 'diagram' && <DiagramBlock data={b} lang={lang} />}
          {b.type === 'terminal' && <TerminalBlock data={b} lang={lang} />}
          {b.type === 'match' && <MatchBlock data={b} lang={lang} />}
          {b.type === 'cloze' && <ClozeBlock data={b} lang={lang} />}
          {b.type === 'scenario' && <ScenarioBlock data={b} lang={lang} />}
        </Suspense>
      </ErrorBoundary>
    </div>
  )
}

function NumberCheck({ answer, lang }: { answer: number; lang: Lang }) {
  const [{ val, checked }, setState] = useExercise({ val: '', checked: false }, (s) => s.checked && Number(s.val) === answer)
  const setVal = (next: string) => setState((s) => ({ ...s, val: next }))
  const setChecked = (next: boolean) => setState((s) => ({ ...s, checked: next }))
  const correct = Number(val) === answer
  const root = useResultFocus(checked)
  return (
    <div ref={root}>
      <div className="flex items-center gap-2">
        <input type="number" value={val} disabled={checked}
          onChange={(e) => setVal(e.target.value)}
          aria-label={t(lang, 'quickCheck')}
          className="w-32 border border-slate-200 rounded-lg px-3 py-1.5 text-sm font-mono" />
        <button onClick={() => setChecked(true)} disabled={checked || val === ''}
          className="rounded-lg border border-teal-200 text-teal-700 px-3 py-1.5 text-sm font-medium hover:bg-teal-50 disabled:opacity-50">
          {t(lang, 'checkIt')}
        </button>
      </div>
      {checked && (
        <div className="mt-2 flex items-center gap-3 text-sm">
          <span role="status" tabIndex={-1} className={`inline-flex items-center gap-1 ${correct ? 'text-green-600 font-medium' : 'text-amber-600 font-medium'}`}>
            <Icon name={correct ? 'check' : 'close'} className="h-4 w-4" />{correct ? t(lang, 'correct') : t(lang, 'incorrect')}
          </span>
          {!correct && (
            <button onClick={() => setState({ val: '', checked: false })}
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
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{t(lang, 'quickCheck')}</p>
      <p className="font-medium text-slate-800 mb-2">{prompt}</p>
      {kind === 'number' ? <NumberCheck answer={answer} lang={lang} /> : <ChoiceCheck options={options} answer={answer} lang={lang} />}
    </div>
  )
}

function ChoiceCheck({ options, answer, lang }: { options: string[]; answer: number; lang: Lang }) {
  const [picked, setPicked] = useExercise<number | null>(null, (p) => p === answer)
  const correct = picked === answer
  const root = useResultFocus(picked !== null)
  return (
    <div ref={root}>
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
          <span role="status" tabIndex={-1} className={`inline-flex items-center gap-1 ${correct ? 'text-green-600 font-medium' : 'text-amber-600 font-medium'}`}>
            <Icon name={correct ? 'check' : 'close'} className="h-4 w-4" />{correct ? t(lang, 'correct') : t(lang, 'incorrect')}
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
  const [open, setOpen] = useExercise<boolean>(false, Boolean)
  const printing = usePrinting()  // Spickzettel: der verdeckte Inhalt ist Lernstoff
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="font-medium text-slate-800">{teaser}</p>
      {open || printing ? (
        <div className="wb-reveal-content mt-2 animate-fade-up">
          <CodeLangContext.Provider value={lang}><Markdown components={MD_COMPONENTS}>{value}</Markdown></CodeLangContext.Provider>
        </div>
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
  const fresh = () => ({ pool: shuffledIndices(items.length), seq: [] as number[], checked: false })
  const [{ pool, seq, checked }, setState] = useExercise(fresh,
    (s) => s.checked && s.pool.length === 0 && s.seq.every((idx, pos) => idx === pos))
  const allCorrect = checked && seq.every((idx, pos) => idx === pos)
  const move = (idx: number, toSeq: boolean) => setState((s) => (toSeq
    ? { ...s, seq: [...s.seq, idx], pool: s.pool.filter((x) => x !== idx) }
    : { ...s, seq: s.seq.filter((x) => x !== idx), pool: [...s.pool, idx] }))
  const setChecked = (next: boolean) => setState((s) => ({ ...s, checked: next }))
  const reset = () => setState(fresh())
  const root = useResultFocus(checked)

  return (
    <div ref={root} className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{t(lang, 'sequence')}</p>
      <p className="font-medium text-slate-800 mb-1">{prompt}</p>
      <p className="text-xs text-slate-500 mb-2">{t(lang, 'orderHint')}</p>
      {seq.length > 0 && (
        <ol className="flex flex-col gap-1.5 mb-2">
          {seq.map((idx, pos) => (
            <li key={idx}>
              <button onClick={() => { if (!checked) move(idx, false) }}
                disabled={checked}
                className={`w-full text-left rounded-lg border px-3 py-1.5 text-sm flex items-center gap-2 ${
                  !checked ? 'border-slate-200 text-slate-700 hover:bg-slate-50'
                  : idx === pos ? 'border-green-300 bg-green-50 text-green-800'
                  : 'border-amber-300 bg-amber-50 text-amber-800'}`}>
                <span className="font-mono text-xs text-slate-500">{pos + 1}.</span> {items[idx]}
                {checked && (
                  <span className="ml-auto inline-flex items-center gap-1">
                    <Icon name={idx === pos ? 'check' : 'close'} className="h-4 w-4" />
                    <span className="sr-only">{idx === pos ? t(lang, 'correct') : t(lang, 'incorrect')}</span>
                  </span>
                )}
              </button>
            </li>
          ))}
        </ol>
      )}
      {pool.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-2">
          {pool.map((idx) => (
            <button key={idx} onClick={() => move(idx, true)}
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
          <span role="status" tabIndex={-1} className={`inline-flex items-center gap-1 ${allCorrect ? 'text-green-600 font-medium' : 'text-amber-600 font-medium'}`}>
            <Icon name={allCorrect ? 'check' : 'close'} className="h-4 w-4" />{allCorrect ? t(lang, 'correct') : t(lang, 'incorrect')}
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
  const wrongSet = useMemo(() => new Set(wrong), [wrong])
  const hits = (picked: number[]) => picked.length === wrongSet.size && picked.every((i) => wrongSet.has(i))
  const [state, setState] = useExercise({ sel: [] as number[], checked: false }, (s) => s.checked && hits(s.sel))
  const sel = new Set(state.sel)
  const checked = state.checked
  const solved = checked && hits(state.sel)
  const setChecked = (next: boolean) => setState((s) => ({ ...s, checked: next }))
  const root = useResultFocus(checked)

  const toggle = (i: number) => {
    if (checked) return
    setState((s) => ({ ...s, sel: s.sel.includes(i) ? s.sel.filter((x) => x !== i) : [...s.sel, i] }))
  }
  const lineStyle = (i: number) => {
    if (!checked) return sel.has(i) ? 'bg-amber-50 border-l-2 border-amber-400' : 'hover:bg-slate-50 border-l-2 border-transparent'
    if (wrongSet.has(i) && sel.has(i)) return 'bg-green-50 border-l-2 border-green-400'
    if (wrongSet.has(i)) return 'bg-amber-50 border-l-2 border-amber-400'
    if (sel.has(i)) return 'bg-rose-50 border-l-2 border-rose-300'
    return 'border-l-2 border-transparent'
  }

  return (
    <div ref={root} className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{t(lang, 'findError')}</p>
      <p className="font-medium text-slate-800 mb-1">{prompt}</p>
      <p className="text-xs text-slate-500 mb-2">{t(lang, 'debugHint')}</p>
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
            <span role="status" tabIndex={-1} className={`inline-flex items-center gap-1 ${solved ? 'text-green-600 font-medium' : 'text-amber-600 font-medium'}`}>
              <Icon name={solved ? 'check' : 'close'} className="h-4 w-4" />{solved ? t(lang, 'correct') : t(lang, 'incorrect')}
            </span>
            {!solved && (
              <button onClick={() => setState({ sel: [], checked: false })}
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
  // Speicherzugriffe abgesichert: blockiertes/volles localStorage darf nicht die ganze Modulseite reißen.
  const [text, setText] = useState(() => { try { return localStorage.getItem(storageKey) ?? '' } catch { return '' } })
  const printing = usePrinting()
  if (printing) {
    // Spickzettel: die eigene Notiz als Fließtext (ein <textarea> druckt nur seinen sichtbaren Ausschnitt).
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{t(lang, 'reflection')}</p>
        <p className="font-medium text-slate-800 mb-2">{prompt}</p>
        <p className="whitespace-pre-wrap text-sm text-slate-700">{text.trim() || '—'}</p>
      </div>
    )
  }
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{t(lang, 'reflection')}</p>
      <p className="font-medium text-slate-800 mb-2">{prompt}</p>
      <textarea value={text} rows={3}
        onChange={(e) => { setText(e.target.value); try { localStorage.setItem(storageKey, e.target.value) } catch { /* nur für diese Sitzung */ } }}
        aria-label={prompt}
        className="w-full border border-slate-200 rounded-lg px-3 py-1.5 text-sm text-slate-700" />
      <p className="text-xs text-slate-500 mt-1">{t(lang, 'reflectHint')}</p>
    </div>
  )
}

export function Blocks({
  blocks,
  lang = 'de',
  moduleKey = '',
  keyScope = '',
  footer,
}: {
  blocks: Block[]
  lang?: Lang
  moduleKey?: string
  // Teilnehmer-/Kurs-Präfix, damit Reflexionen am geteilten Browser nicht durchsickern.
  keyScope?: string
  footer?: (block: Block, index: number) => ReactNode
}) {
  const phaseOf = (type: Block['type']): 'understand' | 'practice' | 'reflect' => {
    if (type === 'widget' || type === 'check' || type === 'order' || type === 'debug'
      || type === 'terminal' || type === 'match' || type === 'cloze' || type === 'scenario') return 'practice'
    if (type === 'reflect') return 'reflect'
    return 'understand'
  }
  const phaseLabel = (phase: ReturnType<typeof phaseOf>) => {
    if (lang === 'en') return phase === 'understand' ? 'Understand' : phase === 'practice' ? 'Try it' : 'Reflect'
    return phase === 'understand' ? 'Verstehen' : phase === 'practice' ? 'Ausprobieren' : 'Reflektieren'
  }
  // Die Marke ("VERSTEHEN" etc.) soll nur beim ersten echten Auftreten einer
  // Phase im Modul erscheinen, nicht bei jedem Rückwechsel — sonst inflationiert
  // sie bei Modulen, die zwischen den Phasen hin- und herspringen (z.B.
  // Verstehen -> Ausprobieren -> Verstehen -> ...). Die Trennlinie bleibt bei
  // jedem Phasenwechsel bestehen, sie trägt den optischen Rhythmus.
  const firstPhaseOccurrence = useMemo(() => {
    const seen = new Set<ReturnType<typeof phaseOf>>()
    const firsts = new Set<number>()
    blocks.forEach((b, i) => {
      const phase = phaseOf(b.type)
      if (!seen.has(phase)) { seen.add(phase); firsts.add(i) }
    })
    return firsts
  }, [blocks])

  // Übungsstand: je Block ein Slot (Kennung + Fingerabdruck), siehe lib/exerciseState.ts.
  // Ohne Teilnehmerkontext (Trainer-Vorschau) bleibt storageKey leer -> nichts wird gemerkt.
  const storageKey = exerciseStorageKey(keyScope, moduleKey)
  const uidOf = (b: Block, i: number) => b.uid || `${b.type}-${i}`
  const versions = useMemo(
    () => Object.fromEntries(blocks.map((b, i) => [b.uid || `${b.type}-${i}`, fingerprint(b)])),
    [blocks])
  const legacy = useMemo(
    () => Object.fromEntries(blocks.map((b, i) => [b.uid || `${b.type}-${i}`, legacyFingerprint(b)])),
    [blocks])
  const exerciseUids = useMemo(
    () => blocks.flatMap((b, i) => (isExercise(b) ? [b.uid || `${b.type}-${i}`] : [])),
    [blocks])
  const [done, setDone] = useState<ReadonlySet<string>>(new Set())
  useEffect(() => setDone(doneExercises(storageKey, versions, legacy)), [storageKey, versions, legacy])
  const onDone = useCallback((uid: string, isDone: boolean) => setDone((prev) => {
    if (prev.has(uid) === isDone) return prev
    const next = new Set(prev)
    if (isDone) next.add(uid); else next.delete(uid)
    return next
  }), [])
  const doneCount = exerciseUids.filter((uid) => done.has(uid)).length
  // Im Druck (Spickzettel) bleiben Theorie, Diagramme, aufgedeckte Inhalte und die
  // eigenen Notizen; Übungen und Widgets sind Interaktions-UI.
  const printable = (type: Block['type']) => type === 'text' || type === 'reveal' || type === 'diagram' || type === 'reflect'

  return (
    <WidgetScopeContext.Provider value={keyScope}>
    <CodeLangContext.Provider value={lang}>
    <div className="content-blocks flex flex-col gap-6">
      {storageKey && exerciseUids.length > 0 && (
        <div className="flex items-center gap-3 text-xs text-slate-600 print:hidden" data-testid="exercise-summary">
          <span aria-live="polite">
            {lang === 'de' ? `${doneCount} von ${exerciseUids.length} Übungen erledigt` : `${doneCount} of ${exerciseUids.length} exercises done`}
          </span>
          <span className="h-1 w-24 overflow-hidden rounded-full bg-slate-200" aria-hidden="true">
            <span className="block h-full rounded-full bg-teal-500 transition-[width]" style={{ width: `${Math.round((doneCount / exerciseUids.length) * 100)}%` }} />
          </span>
          <span>{lang === 'de' ? 'nur in diesem Browser gemerkt' : 'remembered in this browser only'}</span>
        </div>
      )}
      {blocks.map((b, i) => (
        // key: die stabile Kennung, nicht die Position — sonst erbt ein eingefügter/verschobener Block den Zustand seines Vorgängers
        <div key={uidOf(b, i)} id={`block-${i}`} data-uid={b.uid ?? undefined} className={`flex flex-col gap-1 scroll-mt-20 ${printable(b.type) ? '' : 'print:hidden'}`}>
          {(i === 0 || phaseOf(blocks[i - 1].type) !== phaseOf(b.type)) && (
            <div className="mb-1 flex items-center gap-3 pt-2 print:hidden">
              {firstPhaseOccurrence.has(i) && (
                <span className="text-[11px] font-semibold uppercase tracking-[0.18em] text-teal-700">{phaseLabel(phaseOf(b.type))}</span>
              )}
              <div className="h-px flex-1 bg-teal-100" aria-hidden="true" />
            </div>
          )}
          {/* key: der Teilnehmer-Scope steht erst nach /me fest — der Remount lädt dann den gemerkten Stand.
              Mit dem Fingerabdruck im key beginnt ein strukturell geänderter Block (Content-Update bei
              offenem Modul) neu, statt den alten Zustand unter dem neuen Fingerabdruck zu speichern. */}
          <ExerciseSlotContext.Provider key={`${storageKey}|${versions[uidOf(b, i)]}`} value={storageKey ? { storageKey, uid: uidOf(b, i), v: versions[uidOf(b, i)], legacy: legacy[uidOf(b, i)], onDone } : null}>
          {b.type === 'text' && <Markdown components={MD_COMPONENTS}>{b.value}</Markdown>}
          {b.type === 'widget' && <WidgetBlock id={b.id} lang={lang} />}
          {b.type === 'check' && <CheckBlock prompt={b.prompt} options={b.options} answer={b.answer} kind={b.kind} lang={lang} />}
          {b.type === 'reveal' && <RevealBlock teaser={b.teaser} value={b.value} lang={lang} />}
          {b.type === 'order' && <OrderBlock prompt={b.prompt} items={b.items} lang={lang} />}
          {b.type === 'debug' && <DebugBlock prompt={b.prompt} lines={b.lines} wrong={b.wrong} explanation={b.explanation} lang={lang} />}
          {/* key: der Teilnehmer-Scope steht erst nach /me fest — ohne Remount bliebe das Feld leer und überschriebe die gespeicherte Notiz. */}
          {b.type === 'reflect' && <ReflectBlock key={`${keyScope}-${moduleKey}-${i}`} prompt={b.prompt} storageKey={`intnetwork-reflect-${keyScope}-${moduleKey}-${i}`} lang={lang} />}
          {isDeclarative(b) && <DeclarativeBlock block={b} lang={lang} />}
          </ExerciseSlotContext.Provider>
          {footer?.(b, i)}
        </div>
      ))}
    </div>
    </CodeLangContext.Provider>
    </WidgetScopeContext.Provider>
  )
}

// Zählt für „x von y Übungen erledigt“: alles mit einem prüfbaren Ende. Ein Terminal
// ohne Aufgaben und Diagramme merken sich zwar ihren Stand, sind aber keine Übung.
function isExercise(b: Block): boolean {
  return b.type === 'check' || b.type === 'order' || b.type === 'debug' || b.type === 'reveal'
    || b.type === 'match' || b.type === 'cloze' || b.type === 'scenario'
    || (b.type === 'terminal' && (b.tasks?.length ?? 0) > 0)
}
