import { useId, useMemo, useState, type KeyboardEvent, type ReactNode } from 'react'
import type { Lang } from '@/lib/i18n'
import { useExercise } from '@/lib/exerciseState'
import { usePrinting } from '@/lib/printMode'
import { FLOW, SEQ, diagramAlt, edgeKey, layoutFlow, layoutSequence, seqRoute, textWidth } from './diagramLayout'
import type { CompareDiagram, DiagramData, FlowDiagram, FlowShape, LayersDiagram, SequenceDiagram, SeqStyle } from './types'

// Farben: Linien/Text über slate-Utilities (kippen im Dark Mode über die
// Palette), Hervorhebung über text-teal-600 + currentColor — so folgt sie in
// jedem Lehrgang der Kursfarbe, ohne neue teal-Varianten in index.css.
const ACCENT = 'text-teal-600'
const BTN = 'rounded-lg border border-slate-200 px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-50 disabled:opacity-40'

const activate = (fn: () => void) => (e: KeyboardEvent) => {
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fn() }
}

function Stepper({ step, total, onStep, lang, all, onAll }: {
  step: number; total: number; onStep: (s: number) => void; lang: Lang; all?: boolean; onAll?: () => void
}) {
  const de = lang === 'de'
  return (
    <div className="mt-3 flex flex-wrap items-center gap-2 print:hidden">
      <button type="button" className={BTN} disabled={step === 0} onClick={() => onStep(step - 1)}>← {de ? 'Zurück' : 'Back'}</button>
      <button type="button" className={BTN} disabled={step === total - 1} onClick={() => onStep(step + 1)}>{de ? 'Weiter' : 'Next'} →</button>
      <span className="text-sm tabular-nums text-slate-500">{de ? 'Schritt' : 'Step'} {step + 1} / {total}</span>
      {onAll && (
        <button type="button" className={`${BTN} ml-auto`} aria-pressed={all} onClick={onAll}>
          {all ? (de ? 'Schrittweise' : 'Step by step') : (de ? 'Alles zeigen' : 'Show all')}
        </button>
      )}
    </div>
  )
}

/** Pfeiltasten gehören dem Diagramm, solange der Fokus darin liegt — sonst blättert der Beamer-Modus die Folie. */
function arrowKeys(step: number, total: number, onStep: (s: number) => void) {
  return (e: KeyboardEvent) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return
    if ((e.target as Element).closest('input, select, textarea')) return
    e.preventDefault()
    e.stopPropagation()
    onStep(Math.min(total - 1, Math.max(0, step + (e.key === 'ArrowRight' ? 1 : -1))))
  }
}

function Detail({ head, children }: { head?: string; children?: ReactNode }) {
  return (
    <div aria-live="polite" className="mt-3 min-h-[3.25rem] rounded-lg border border-teal-100 bg-teal-50 px-3 py-2 text-sm text-teal-900">
      {head && <p className="font-semibold">{head}</p>}
      {children && <p className="whitespace-pre-line">{children}</p>}
    </div>
  )
}

function Lines({ lines, x, y, lineH, size, className, weight }: {
  lines: string[]; x: number; y: number; lineH: number; size: number; className?: string; weight?: number
}) {
  return (
    <text x={x} y={y} textAnchor="middle" fontSize={size} fontWeight={weight} className={className}>
      {lines.map((l, i) => <tspan key={i} x={x} dy={i === 0 ? 0 : lineH}>{l}</tspan>)}
    </text>
  )
}

function Canvas({ width, height, label, describedBy, children }: {
  width: number; height: number; label: string; describedBy: string; children: ReactNode
}) {
  return (
    <div className="overflow-x-auto rounded-lg bg-slate-50 p-2">
      {/* minWidth: lieber waagerecht scrollen, als die Schrift unter ~10px zu skalieren */}
      <svg viewBox={`0 0 ${width} ${height}`} role="group" aria-label={label} aria-describedby={describedBy}
        className="mx-auto block h-auto w-full" style={{ minWidth: Math.min(width, 560), maxWidth: width * 1.35 }}>
        {children}
      </svg>
    </div>
  )
}

// --- sequence ----------------------------------------------------------------

const SEQ_STYLE: Record<SeqStyle, { dash?: string; width: number; open?: boolean; de: string; en: string }> = {
  request: { width: 1.8, de: 'Anfrage', en: 'Request' },
  reply: { dash: '7 5', width: 1.8, open: true, de: 'Antwort', en: 'Reply' },
  broadcast: { dash: '2 5', width: 3, de: 'Broadcast (an alle)', en: 'Broadcast (to all)' },
  multicast: { dash: '12 4 2 4', width: 3, de: 'Multicast (an eine Gruppe)', en: 'Multicast (to a group)' },
  encrypted: { width: 4, de: 'verschlüsselt', en: 'encrypted' },
}

function Sequence({ d, lang, altId }: { d: SequenceDiagram; lang: Lang; altId: string }) {
  const de = lang === 'de'
  const L = useMemo(() => layoutSequence(d), [d])
  const [step, setStep] = useExercise(0, () => false)  // Schritt wird gemerkt, zählt aber nicht als Übung
  const [showAll, setAll] = useState(false)
  const all = usePrinting() || showAll  // Druck: Endzustand mit allen Nachrichten
  const name = (id: string) => d.actors.find((a) => a.id === id)?.label ?? id
  const current = d.messages[step]
  const dividerX = (L.gutter + L.width) / 2
  const used = [...new Set(d.messages.filter((m) => m.from !== m.to).map((m) => m.style ?? 'request'))]

  return (
    <div onKeyDown={arrowKeys(step, d.messages.length, setStep)}>
      <Canvas width={L.width} height={L.height} label={d.title} describedBy={altId}>
        {L.actors.map((a) => (
          <g key={a.id} aria-hidden="true">
            <line x1={a.x} y1={L.headH} x2={a.x} y2={L.height - 4} strokeWidth={1.5} strokeDasharray="4 4" className="stroke-slate-300" />
            <rect x={a.x - a.w / 2} y={1} width={a.w} height={a.h - 2} rx={8} strokeWidth={1.5} className="fill-slate-100 stroke-slate-300" />
            <Lines lines={a.lines} x={a.x} y={(a.h - a.lines.length * SEQ.lineH) / 2 + SEQ.actorFont} lineH={SEQ.lineH} size={SEQ.actorFont} weight={600} className="fill-slate-900" />
          </g>
        ))}
        {L.messages.map((m) => {
          if (!all && m.index > step) return null
          const msg = d.messages[m.index]
          const on = m.index === step
          const st = SEQ_STYLE[msg.style ?? 'request']
          return (
            <g key={m.index} role="button" tabIndex={0} aria-current={on ? 'step' : undefined}
              aria-label={`${de ? 'Schritt' : 'Step'} ${m.index + 1}: ${seqRoute(msg, name)}: ${msg.label}`}
              onClick={() => setStep(m.index)} onKeyDown={activate(() => setStep(m.index))}
              className={`cursor-pointer outline-none ${on ? ACCENT : 'text-slate-500'}`}>
              {/* unsichtbare Trefferfläche über Beschriftung + Pfeil */}
              <rect x={m.cx - m.w / 2 - 8} y={m.top - 4} width={m.w + 16} height={m.y - m.top + 14} fill="transparent" />
              {m.self ? (
                <rect x={m.cx - m.w / 2} y={m.top} width={m.w} height={m.y - m.top} rx={6} strokeWidth={on ? 2.5 : 1.5} stroke="currentColor" className="fill-slate-50" />
              ) : (
                <>
                  {m.xs.map((x2, k) => {
                    const dir = x2 > m.x1 ? 1 : -1
                    const tip = x2 - dir * 2
                    return (
                      <g key={k}>
                        <line x1={m.x1} y1={m.y} x2={tip - dir * 8} y2={m.y} stroke="currentColor" strokeWidth={st.width + (on ? 0.8 : 0)} strokeDasharray={st.dash} />
                        <path d={`M${tip - dir * 11} ${m.y - 6}L${tip} ${m.y}L${tip - dir * 11} ${m.y + 6}${st.open ? '' : 'Z'}`}
                          stroke="currentColor" strokeWidth={1.8} fill={st.open ? 'none' : 'currentColor'} strokeLinejoin="round" />
                      </g>
                    )
                  })}
                  <circle cx={m.x1} cy={m.y} r={3.5} fill="currentColor" />
                </>
              )}
              <Lines lines={m.lines} x={m.cx} y={m.top + (m.self ? 6 : 0) + SEQ.labelFont - 1} lineH={SEQ.lineH}
                size={m.self ? SEQ.noteFont : SEQ.labelFont} weight={on ? 700 : 500} className={on ? 'fill-slate-950' : 'fill-slate-700'} />
              {msg.at && (
                <text x={6} y={(m.self ? (m.top + m.y) / 2 : m.y) + 4} fontSize={SEQ.atFont} fontWeight={on ? 700 : 500} className={`tabular-nums ${on ? 'fill-slate-950' : 'fill-slate-500'}`}>{msg.at}</text>
              )}
              {m.dividerY !== undefined && msg.divider && (
                <g className="text-slate-400">
                  <line x1={L.gutter + 6} y1={m.dividerY + 9} x2={L.width - 6} y2={m.dividerY + 9} stroke="currentColor" strokeWidth={1.2} strokeDasharray="1 4" strokeLinecap="round" />
                  <rect x={dividerX - textWidth(msg.divider, SEQ.noteFont) / 2 - 8} y={m.dividerY} width={textWidth(msg.divider, SEQ.noteFont) + 16} height={18} rx={9} className="fill-slate-50" stroke="currentColor" strokeWidth={1} />
                  <text x={dividerX} y={m.dividerY + 13.5} textAnchor="middle" fontSize={SEQ.noteFont} fontWeight={600} className="fill-slate-600">{msg.divider}</text>
                </g>
              )}
            </g>
          )
        })}
      </Canvas>
      {used.length > 1 && (
        <ul className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500" aria-label={de ? 'Legende' : 'Legend'}>
          {used.map((s) => (
            <li key={s} className="inline-flex items-center gap-1.5">
              <svg width="30" height="8" aria-hidden="true"><line x1="0" y1="4" x2="30" y2="4" stroke="currentColor" strokeWidth={SEQ_STYLE[s].width} strokeDasharray={SEQ_STYLE[s].dash} /></svg>
              {de ? SEQ_STYLE[s].de : SEQ_STYLE[s].en}
            </li>
          ))}
        </ul>
      )}
      <Stepper step={step} total={d.messages.length} onStep={setStep} lang={lang} all={all} onAll={() => setAll((a) => !a)} />
      <Detail head={`${step + 1}. ${seqRoute(current, name)}: ${current.label}`}>
        {current.detail}
      </Detail>
    </div>
  )
}

// --- flow --------------------------------------------------------------------

// 24×24-Linien-Icons, bewusst schlicht (ein Pfad je Gerätetyp).
const SHAPE_PATH: Partial<Record<FlowShape, string>> = {
  host: 'M3 4h18v12H3zM9 20h6M12 16v4',
  server: 'M4 3h16v7H4zM4 14h16v7H4zM7.5 6.5h.01M7.5 17.5h.01',
  switch: 'M2 7h20v10H2zM6 10.5h7m-2-2 2 2-2 2M18 14.5h-7m2-2-2 2 2 2',
  router: 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 6v12M6 12h12M10 8l2-2 2 2M10 16l2 2 2-2M8 10l-2 2 2 2M16 10l2 2-2 2',
  firewall: 'M3 4h18v16H3zM3 9.3h18M3 14.7h18M9 4v5.3M15 4v5.3M12 9.3v5.4M9 14.7V20M15 14.7V20',
  cloud: 'M7 19a5 5 0 0 1-.6-9.96A6.5 6.5 0 0 1 19 11.5 3.75 3.75 0 0 1 18.25 19z',
  database: 'M4 6c0-1.66 3.58-3 8-3s8 1.34 8 3-3.58 3-8 3-8-1.34-8-3zM4 6v12c0 1.66 3.58 3 8 3s8-1.34 8-3V6M4 12c0 1.66 3.58 3 8 3s8-1.34 8-3',
  user: 'M12 3.5a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM4 21c0-4.4 3.6-7.5 8-7.5s8 3.1 8 7.5',
}

function Flow({ d, lang, altId }: { d: FlowDiagram; lang: Lang; altId: string }) {
  const de = lang === 'de'
  const L = useMemo(() => layoutFlow(d), [d])
  const edges = d.edges ?? []
  const steps = d.steps
  const [step, setStep] = useExercise(0, () => false)
  const [sel, setSel] = useState<string | null>(null)
  const printing = usePrinting()  // Druck: alle Elemente gleich sichtbar statt eines hervorgehobenen Schritts
  const lit = steps && !printing ? new Set(steps[step].highlight) : null
  const state = (key: string) => (sel === key || lit?.has(key) ? 'on' : lit ? 'dim' : 'idle')
  const cls = (key: string) => (state(key) === 'on' ? ACCENT : state(key) === 'dim' ? 'text-slate-400 opacity-45' : 'text-slate-500')
  const selNode = d.nodes.find((n) => n.id === sel)
  const selEdge = edges.find((e, i) => edgeKey(e, i) === sel)
  const name = (id: string) => d.nodes.find((n) => n.id === id)?.label ?? id
  const hasDetails = d.nodes.some((n) => n.detail) || edges.some((e) => e.detail)
  const interactive = (key: string, label: string, detail?: string) => (detail ? {
    role: 'button', tabIndex: 0, 'aria-pressed': sel === key, 'aria-label': label,
    onClick: () => setSel(sel === key ? null : key), onKeyDown: activate(() => setSel(sel === key ? null : key)),
  } : { 'aria-hidden': true })

  return (
    <div onKeyDown={steps ? arrowKeys(step, steps.length, setStep) : undefined}>
      <Canvas width={L.width} height={L.height} label={d.title} describedBy={altId}>
        {L.edges.map((b, i) => {
          const e = edges[i]
          const on = state(b.key) === 'on'
          // Pfeilspitzen von Hand statt <marker>: marker erben currentColor nicht in allen Browsern
          // Spitze (x,y), Pfeil zeigt aus Richtung (fx,fy); bei Bögen ist das der vorletzte Stützpunkt
          const pts = b.points
          const head = (x: number, y: number, fx: number, fy: number) => {
            const len = Math.hypot(x - fx, y - fy) || 1
            const ux = (x - fx) / len
            const uy = (y - fy) / len
            return `M${x} ${y}L${x - (ux * 10 - uy * 5)} ${y - (uy * 10 + ux * 5)}L${x - (ux * 10 + uy * 5)} ${y - (uy * 10 - ux * 5)}Z`
          }
          const [ex, ey] = pts ? pts[pts.length - 3] ?? pts[0] : [b.x1, b.y1]
          const [sx, sy] = pts ? pts[2] ?? pts[pts.length - 1] : [b.x2, b.y2]
          const path = pts ? `M${pts.map(([x, y]) => `${x.toFixed(1)} ${y.toFixed(1)}`).join('L')}` : `M${b.x1} ${b.y1}L${b.x2} ${b.y2}`
          return (
            <g key={b.key} {...interactive(b.key, `${name(e.from)} → ${name(e.to)}${e.label ? `: ${e.label}` : ''}`, e.detail)}
              className={`outline-none ${e.detail ? 'cursor-pointer' : ''} ${cls(b.key)}`}>
              <path d={path} fill="none" stroke="currentColor" strokeWidth={on ? 3 : 1.8} strokeLinejoin="round"
                strokeDasharray={e.style === 'dashed' ? '6 5' : undefined} />
              {e.arrow !== 'none' && <path d={head(b.x2, b.y2, ex, ey)} fill="currentColor" />}
              {e.arrow === 'both' && <path d={head(b.x1, b.y1, sx, sy)} fill="currentColor" />}
              {e.detail && <path d={path} fill="none" stroke="transparent" strokeWidth={18} />}
              {b.label && (
                <>
                  <rect x={b.label.cx - b.label.w / 2} y={b.label.cy - b.label.h / 2} width={b.label.w} height={b.label.h} rx={4}
                    className="fill-slate-50" stroke={e.detail ? 'currentColor' : 'none'} strokeWidth={1} />
                  <Lines lines={b.label.lines} x={b.label.cx} y={b.label.cy - b.label.h / 2 + 3 + FLOW.edgeFont} lineH={FLOW.lineH}
                    size={FLOW.edgeFont} weight={on ? 700 : 500} className={on ? 'fill-slate-950' : 'fill-slate-600'} />
                </>
              )}
            </g>
          )
        })}
        {L.nodes.map((b, i) => {
          const n = d.nodes[i]
          const on = state(b.id) === 'on'
          const x = b.cx - b.w / 2
          const y = b.cy - b.h / 2
          const icon = b.icon ? SHAPE_PATH[n.shape as FlowShape] : undefined
          const textTop = b.cy - (b.lines.length * FLOW.lineH) / 2 + (icon ? FLOW.iconH / 2 : 0)
          return (
            <g key={b.id} {...interactive(b.id, n.label, n.detail)}
              className={`outline-none ${n.detail ? 'cursor-pointer' : ''} ${cls(b.id)}`}>
              {n.shape === 'decision' ? (
                <path d={`M${b.cx} ${y}L${x + b.w} ${b.cy}L${b.cx} ${y + b.h}L${x} ${b.cy}Z`} stroke="currentColor" strokeWidth={on ? 3 : 1.6} strokeLinejoin="round" className="fill-slate-100" />
              ) : (
                <rect x={x} y={y} width={b.w} height={b.h} rx={n.shape === 'process' || !n.shape ? 18 : 8} stroke="currentColor" strokeWidth={on ? 3 : 1.6} className="fill-slate-100" />
              )}
              {icon && (
                <path d={icon} transform={`translate(${b.cx - 12} ${y + 7})`} fill="none" stroke="currentColor" strokeWidth={1.6} strokeLinecap="round" strokeLinejoin="round" />
              )}
              <Lines lines={b.lines} x={b.cx} y={textTop + FLOW.font - 1} lineH={FLOW.lineH} size={FLOW.font} weight={600} className="fill-slate-900" />
              {n.detail && <circle cx={x + b.w - 9} cy={y + 9} r={3} fill="currentColor" />}
            </g>
          )
        })}
      </Canvas>
      {steps && <Stepper step={step} total={steps.length} onStep={setStep} lang={lang} />}
      {(steps || hasDetails) && (
        <>
          {steps && <Detail head={`${de ? 'Schritt' : 'Step'} ${step + 1}`}>{steps[step].text}</Detail>}
          {selNode?.detail && <Detail head={selNode.label}>{selNode.detail}</Detail>}
          {selEdge?.detail && <Detail head={`${name(selEdge.from)} → ${name(selEdge.to)}${selEdge.label ? `: ${selEdge.label}` : ''}`}>{selEdge.detail}</Detail>}
          {!steps && !selNode && !selEdge && (
            <p className="mt-3 text-xs text-slate-500">{de ? 'Elemente mit Punkt anklicken (oder Tab + Enter) für Details.' : 'Click elements with a dot (or Tab + Enter) for details.'}</p>
          )}
        </>
      )}
    </div>
  )
}

// --- layers / compare (HTML statt SVG: Text bricht hier beliebig um) -----------

function Layers({ d, lang }: { d: LayersDiagram; lang: Lang }) {
  const de = lang === 'de'
  const [sel, setSel] = useState<number | null>(null)
  const clickable = d.layers.some((l) => l.detail)
  const current = sel === null ? null : d.layers[sel]
  return (
    <div>
      <ol className="flex flex-col gap-1.5">
        {d.layers.map((l, i) => {
          const body = (
            <>
              <span className="min-w-0 font-semibold sm:w-2/5 sm:shrink-0">{l.name}</span>
              <span className="min-w-0 flex-1 text-sm">{l.content}</span>
              {l.pdu && <span className="shrink-0 self-start rounded-md border border-current px-1.5 py-0.5 font-mono text-xs sm:self-center">{l.pdu}</span>}
            </>
          )
          const box = `flex w-full flex-col gap-x-3 gap-y-0.5 rounded-lg border px-3 py-2 text-left sm:flex-row sm:items-center ${
            sel === i ? 'border-teal-600 bg-teal-50 text-teal-900' : 'border-slate-200 bg-slate-50 text-slate-700'}`
          return (
            <li key={i}>
              {l.detail
                ? <button type="button" aria-pressed={sel === i} onClick={() => setSel(sel === i ? null : i)} className={`${box} hover:bg-slate-100`}>{body}</button>
                : <div className={box}>{body}</div>}
            </li>
          )
        })}
      </ol>
      {clickable && (current?.detail
        ? <Detail head={current.name}>{current.detail}</Detail>
        : <p className="mt-3 text-xs text-slate-500">{de ? 'Schicht anklicken für Details.' : 'Click a layer for details.'}</p>)}
    </div>
  )
}

function Compare({ d, lang }: { d: CompareDiagram; lang: Lang }) {
  const [sel, setSel] = useState<number | null>(null)
  const current = sel === null ? null : d.rows[sel]
  return (
    <>
    <div className="overflow-x-auto">
      <table className="w-full border-separate border-spacing-x-2 border-spacing-y-0 text-left text-sm" style={{ minWidth: 140 + d.columns.length * 150 }}>
        <thead>
          <tr>
            <td />
            {d.columns.map((c, i) => (
              <th key={i} scope="col" className="rounded-t-lg border border-b-0 border-teal-200 bg-teal-50 px-3 py-2 text-base font-semibold text-teal-900">{c.title}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {d.rows.map((r, ri) => (
            <tr key={ri}>
              <th scope="row" className="border-t border-slate-200 py-2 pr-2 align-top text-xs font-semibold uppercase tracking-wide text-slate-500">
                {r.detail ? (
                  <button type="button" aria-pressed={sel === ri} onClick={() => setSel(sel === ri ? null : ri)}
                    className={`text-left font-semibold uppercase tracking-wide underline decoration-dotted underline-offset-4 ${sel === ri ? ACCENT : 'hover:text-slate-700'}`}>
                    {r.label}
                  </button>
                ) : r.label}
              </th>
              {r.values.map((v, ci) => (
                <td key={ci} className={`border-x border-t border-slate-200 bg-slate-50 px-3 py-2 align-top text-slate-700 ${r.mono ? 'whitespace-pre-wrap break-words font-mono text-[0.8125rem]' : ''} ${ri === d.rows.length - 1 ? 'rounded-b-lg border-b' : ''}`}>{v}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    {d.rows.some((r) => r.detail) && (current?.detail
      ? <Detail head={current.label}>{current.detail}</Detail>
      : <p className="mt-3 text-xs text-slate-500">{lang === 'de' ? 'Unterstrichene Zeile anklicken für Details.' : 'Click an underlined row for details.'}</p>)}
    </>
  )
}

export default function DiagramBlock({ data, lang }: { data: DiagramData; lang: Lang }) {
  const uid = useId().replace(/[^a-zA-Z0-9_-]/g, '')
  const altId = `${uid}-alt`
  const svg = data.kind === 'sequence' || data.kind === 'flow'
  return (
    <figure className="rounded-xl border border-slate-200 bg-white p-4">
      {/* overflow-wrap: ein Titel wie TLS_ECDHE_RSA_WITH_… hat keine Leerzeichen und sprengte sonst die Handy-Seite */}
      <figcaption className="mb-3 [overflow-wrap:anywhere]">
        <p className="font-semibold text-slate-800">{data.title}</p>
        {data.caption && <p className="text-sm text-slate-500">{data.caption}</p>}
      </figcaption>
      {data.kind === 'sequence' && <Sequence d={data} lang={lang} altId={altId} />}
      {data.kind === 'flow' && <Flow d={data} lang={lang} altId={altId} />}
      {data.kind === 'layers' && <Layers d={data} lang={lang} />}
      {data.kind === 'compare' && <Compare d={data} lang={lang} />}
      {/* Textalternative der Grafik für Screenreader; layers/compare sind bereits echtes HTML */}
      {svg && <ol id={altId} className="sr-only">{diagramAlt(data).map((line, i) => <li key={i}>{line}</li>)}</ol>}
    </figure>
  )
}
