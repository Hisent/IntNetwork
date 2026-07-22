import { useMemo, useState } from 'react'
import {
  buildGraph, shortestPath, fewestHopsPath, withoutLink, TOPOLOGY, type LinkSpec,
} from '@/widgets/ospf/ospf'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const LABEL: Record<string, { de: string; en: string }> = {
  Zentrale: { de: 'Zentrale', en: 'Headquarters' },
  Lager: { de: 'Lager', en: 'Warehouse' },
  FilialeNord: { de: 'Filiale Nord', en: 'North branch' },
  FilialeSued: { de: 'Filiale Süd', en: 'South branch' },
  Rechenzentrum: { de: 'Rechenzentrum', en: 'Data center' },
}

const REFERENCE_OPTIONS = [10, 100, 1000, 100_000] as const

function linkKey(a: string, b: string): string {
  return [a, b].sort().join('|')
}

function edgeOnPath(path: string[], a: string, b: string): boolean {
  for (let i = 0; i < path.length - 1; i++) {
    if ((path[i] === a && path[i + 1] === b) || (path[i] === b && path[i + 1] === a)) return true
  }
  return false
}

const STR = {
  de: {
    title: 'OSPF — Kostenpfad statt Hop-Count',
    subtitle: 'Nordwind-Standorte, verbunden über Leitungen mit je eigener Bandbreite. '
      + 'OSPF wählt nicht den Weg mit den wenigsten Sprüngen, sondern den mit der niedrigsten Kostensumme.',
    reference: 'Referenzbandbreite', referenceHint: (mbit: number) =>
      mbit <= 100
        ? 'Klassischer Standardwert: Alle Leitungen ab 100 Mbit/s bekommen die Kosten 1 — sie sind dann nicht mehr unterscheidbar.'
        : 'Höher gesetzt: schnelle Leitungen bekommen wieder unterschiedliche Kosten, statt alle auf 1 zu fallen.',
    from: 'Von', to: 'Nach',
    linksTitle: 'Leitungen', bandwidth: 'Bandbreite', cost: 'Kosten', down: 'ausfallen lassen', restore: 'wiederherstellen',
    bestPath: 'Kostengünstigster Pfad (OSPF)', fewestHops: 'Pfad mit den wenigsten Sprüngen (RIP-artig)',
    sameAsCost: 'entspricht dem kostengünstigsten Pfad',
    costSum: 'Kostensumme', hopCount: 'Sprünge', hops: 'Sprünge',
    unreachable: 'Ziel nicht erreichbar — kein funktionierender Pfad mehr vorhanden.',
    challenge: 'Lass eine Leitung auf dem aktuellen besten Pfad ausfallen und beobachte, wie sich der Pfad ändert.',
  },
  en: {
    title: 'OSPF — Cost Path, Not Hop Count',
    subtitle: 'Nordwind sites connected by links, each with its own bandwidth. '
      + 'OSPF does not choose the path with fewest hops, but the one with the lowest total cost.',
    reference: 'Reference bandwidth', referenceHint: (mbit: number) =>
      mbit <= 100
        ? 'Classic default: every link at 100 Mbit/s or above gets cost 1 — they become indistinguishable.'
        : 'Raised: fast links get distinguishable costs again instead of all collapsing to 1.',
    from: 'From', to: 'To',
    linksTitle: 'Links', bandwidth: 'Bandwidth', cost: 'Cost', down: 'fail link', restore: 'restore',
    bestPath: 'Lowest-cost path (OSPF)', fewestHops: 'Fewest-hops path (RIP-like)',
    sameAsCost: 'matches the lowest-cost path',
    costSum: 'Total cost', hopCount: 'Hops', hops: 'hops',
    unreachable: 'Destination unreachable — no working path remains.',
    challenge: 'Fail a link on the current best path and watch how the path changes.',
  },
} as const

export function Ospf({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const nodeIds = useMemo(() => {
    const set = new Set<string>()
    for (const l of TOPOLOGY) { set.add(l.a); set.add(l.b) }
    return [...set]
  }, [])

  const [reference, setReference] = useState<number>(100)
  const [from, setFrom] = useState('Zentrale')
  const [to, setTo] = useState('Rechenzentrum')
  const [downLinks, setDownLinks] = useState<Set<string>>(new Set())
  const [changedPathOnce, setChangedPathOnce] = useState(false)

  const fullGraph = useMemo(() => buildGraph(reference), [reference])
  const graph = useMemo(() => {
    let g = buildGraph(reference)
    for (const l of TOPOLOGY) {
      if (downLinks.has(linkKey(l.a, l.b))) g = withoutLink(g, l.a, l.b)
    }
    return g
  }, [reference, downLinks])

  const best = shortestPath(graph, from, to)
  const baseline = shortestPath(fullGraph, from, to)
  const hopPath = fewestHopsPath(graph, from, to)
  const hopsDiffer = best && hopPath && best.path.join('>') !== hopPath.path.join('>')

  function toggleLink(l: LinkSpec) {
    const key = linkKey(l.a, l.b)
    setDownLinks((prev) => {
      const next = new Set(prev)
      if (next.has(key)) next.delete(key)
      else next.add(key)
      return next
    })
    // Erfolgskriterium: der Ausfall hat den tatsächlich genutzten Pfad verändert.
    const wasOnBestPath = best ? edgeOnPath(best.path, l.a, l.b) : false
    if (wasOnBestPath) setChangedPathOnce(true)
  }

  const currentPathChanged = !!baseline && (!best || best.path.join('>') !== baseline.path.join('>'))

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <div className="flex flex-wrap items-end gap-3 mb-2">
        <label className="text-xs text-slate-600" htmlFor="ospf-reference">
          {s.reference}
          <select
            id="ospf-reference"
            value={reference}
            onChange={(e) => setReference(Number(e.target.value))}
            className="ml-1 border rounded px-1 py-0.5"
          >
            {REFERENCE_OPTIONS.map((m) => (
              <option key={m} value={m}>{m.toLocaleString(lang)} Mbit/s</option>
            ))}
          </select>
        </label>
        <label className="text-xs text-slate-600" htmlFor="ospf-from">
          {s.from}
          <select id="ospf-from" value={from} onChange={(e) => setFrom(e.target.value)} className="ml-1 border rounded px-1 py-0.5">
            {nodeIds.map((n) => <option key={n} value={n}>{LABEL[n][lang]}</option>)}
          </select>
        </label>
        <label className="text-xs text-slate-600" htmlFor="ospf-to">
          {s.to}
          <select id="ospf-to" value={to} onChange={(e) => setTo(e.target.value)} className="ml-1 border rounded px-1 py-0.5">
            {nodeIds.map((n) => <option key={n} value={n}>{LABEL[n][lang]}</option>)}
          </select>
        </label>
      </div>
      <p className="text-xs text-amber-700 mb-4">{s.referenceHint(reference)}</p>

      <p className="text-xs font-semibold text-slate-500 mb-1">{s.linksTitle}</p>
      <div className="rounded-lg border divide-y text-xs mb-4">
        {TOPOLOGY.map((l) => {
          const key = linkKey(l.a, l.b)
          const isDown = downLinks.has(key)
          const edge = graph.edges.find((e) => linkKey(e.a, e.b) === key) ?? fullGraph.edges.find((e) => linkKey(e.a, e.b) === key)!
          const onBestPath = !isDown && best ? edgeOnPath(best.path, l.a, l.b) : false
          return (
            <div key={key} className={`flex flex-wrap items-center justify-between gap-2 px-3 py-1.5 ${
              isDown ? 'bg-rose-50' : onBestPath ? 'bg-teal-50' : ''}`}
            >
              <span className={isDown ? 'text-rose-400 line-through' : 'text-slate-700'}>
                {LABEL[l.a][lang]} ↔ {LABEL[l.b][lang]}
              </span>
              <span className="text-slate-500">{s.bandwidth}: {l.mbit.toLocaleString(lang)} Mbit/s</span>
              <span className="text-slate-500">{s.cost}: {isDown ? '—' : edge.cost}</span>
              <button
                onClick={() => toggleLink(l)}
                className="rounded border px-2 py-0.5 text-[11px] font-medium text-slate-700 hover:bg-slate-50"
              >
                {isDown ? s.restore : s.down}
              </button>
            </div>
          )
        })}
      </div>

      <div className="rounded-lg border-2 border-teal-300 bg-teal-50/60 p-3 text-xs mb-3" aria-live="polite">
        <p className="font-semibold text-teal-800 mb-1">{s.bestPath}</p>
        {best ? (
          <>
            <p className="text-slate-700">{best.path.map((n) => LABEL[n][lang]).join(' → ')}</p>
            <p className="text-slate-600 mt-1">{s.costSum}: {best.cost}</p>
          </>
        ) : (
          <p className="text-rose-700">{s.unreachable}</p>
        )}
      </div>

      {hopsDiffer && hopPath && (
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-xs mb-1" aria-live="polite">
          <p className="font-semibold text-slate-600 mb-1">{s.fewestHops}</p>
          <p className="text-slate-700">{hopPath.path.map((n) => LABEL[n][lang]).join(' → ')}</p>
          <p className="text-slate-500 mt-1">{s.hopCount}: {hopPath.hops} {s.hops}</p>
        </div>
      )}
      {!hopsDiffer && hopPath && best && (
        <p className="text-[11px] text-slate-400 mb-1">{s.fewestHops} {s.sameAsCost}.</p>
      )}

      <ChallengeBox lang={lang} task={s.challenge} done={changedPathOnce && currentPathChanged} />
    </div>
  )
}
