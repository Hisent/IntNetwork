import { useState } from 'react'
import { electRoot, aggregateBandwidth, singleFlowBandwidth, type SwitchSpec } from '@/widgets/redundancy/redundancy'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const PRIORITY_STEPS = Array.from({ length: 16 }, (_, i) => i * 4096) // 0, 4096, ..., 61440

const INITIAL_SWITCHES: SwitchSpec[] = [
  { name: 'SW1', priority: 32768, mac: '00:11:22:33:44:01' },
  { name: 'SW2', priority: 32768, mac: '00:11:22:33:44:02' },
  { name: 'SW3', priority: 4096, mac: '00:11:22:33:44:03' },
  { name: 'SW4', priority: 49152, mac: '00:11:22:33:44:04' },
]

const LINK_MBIT = 1000

type Mode = 'parallel' | 'single'
type Tab = 'stp' | 'aggregation'

const STR = {
  de: {
    title: 'Redundanz — drei Mechanismen, drei Zwecke',
    tabStp: 'STP-Root-Wahl', tabAgg: 'Link-Aggregation',
    stpIntro: 'Jeder Switch hat eine Priorität (in 4096er-Schritten) und eine feste MAC-Adresse. '
      + 'Die niedrigste Priorität gewinnt die Root-Wahl; bei Gleichstand die niedrigste MAC-Adresse.',
    priority: 'Priorität', mac: 'MAC-Adresse',
    rootIs: (name: string) => `Root-Bridge: ${name}`,
    reasonPriority: 'Entschieden durch: niedrigste Priorität.',
    reasonMac: 'Entschieden durch: Priorität war gleich — niedrigste MAC-Adresse entscheidet.',
    blockedSimplified: (name: string) => `Vereinfacht: ${name} blockiert einen Port, um die Schleife zu brechen.`,
    blockedNote: 'Vereinfachung: In echten Netzen entscheiden Portkosten und Portrollen (Root-Port, '
      + 'designierter Port, Alternate-Port) je Segment — hier markieren wir nur, welcher Nicht-Root-Switch '
      + '(die schwächste Priorität/MAC) einen Port blockiert.',
    stpChallenge: 'Ändere die Priorität eines Switches so, dass sich die Root-Bridge ändert.',
    aggIntro: 'Ein Bündel aus mehreren 1-Gbit/s-Leitungen zwischen zwei Switches.',
    linkCount: 'Anzahl Leitungen', mode: 'Übertragungsart',
    modeParallel: 'Viele parallele Übertragungen', modeSingle: 'Eine einzelne große Übertragung',
    sumBandwidth: 'Summenbandbreite des Bündels', effective: 'Tatsächlich nutzbar für dieses Szenario',
    failLink: 'Leitung ausfallen lassen', restoreAll: 'Alle Leitungen wiederherstellen', link: 'Leitung',
    activeLinks: 'aktive Leitungen', stillUp: 'Verbindung bleibt bestehen, nur mit weniger Summenbandbreite.',
    singleFlowNote: 'Kernaussage: Der Verteilungs-Hash bindet einen einzelnen Datenfluss fest an EINE Leitung — '
      + 'mehr Leitungen im Bündel erhöhen die Summenbandbreite, helfen einem einzelnen Fluss aber nicht.',
    aggChallenge: 'Stelle mehrere Leitungen ein und wechsle zu „eine einzelne große Übertragung“ — beobachte, dass sie trotzdem bei 1 Gbit/s bleibt.',
    challenge: 'Kippe die Root-Wahl durch eine Prioritätsänderung UND beobachte den Einzelfluss-Effekt bei der Link-Aggregation.',
  },
  en: {
    title: 'Redundancy — Three Mechanisms, Three Purposes',
    tabStp: 'STP Root Election', tabAgg: 'Link Aggregation',
    stpIntro: 'Every switch has a priority (in steps of 4096) and a fixed MAC address. '
      + 'The lowest priority wins the root election; on a tie, the lowest MAC address decides.',
    priority: 'Priority', mac: 'MAC address',
    rootIs: (name: string) => `Root bridge: ${name}`,
    reasonPriority: 'Decided by: lowest priority.',
    reasonMac: 'Decided by: priority was tied — lowest MAC address decides.',
    blockedSimplified: (name: string) => `Simplified: ${name} blocks a port to break the loop.`,
    blockedNote: 'Simplification: real networks decide via port costs and port roles (root port, '
      + 'designated port, alternate port) per segment — here we only mark which non-root switch '
      + '(the weakest priority/MAC) blocks a port.',
    stpChallenge: 'Change a switch’s priority so the root bridge changes.',
    aggIntro: 'A bundle of several 1 Gbit/s links between two switches.',
    linkCount: 'Number of links', mode: 'Transfer type',
    modeParallel: 'Many parallel transfers', modeSingle: 'One single large transfer',
    sumBandwidth: 'Bundle total bandwidth', effective: 'Actually usable for this scenario',
    failLink: 'Fail a link', restoreAll: 'Restore all links', link: 'Link',
    activeLinks: 'active links', stillUp: 'Connection stays up, just with less total bandwidth.',
    singleFlowNote: 'Key point: the distribution hash binds a single data flow to ONE link — '
      + 'more links in the bundle raise the total bandwidth, but do not help a single flow.',
    aggChallenge: 'Set several links and switch to “one single large transfer” — watch it still stays at 1 Gbit/s.',
    challenge: 'Flip the root election via a priority change AND observe the single-flow effect in link aggregation.',
  },
} as const

function Stp({ lang, onRootChanged }: { lang: Lang; onRootChanged: () => void }) {
  const s = STR[lang]
  const [initialSwitches] = useState(INITIAL_SWITCHES)
  const [switches, setSwitches] = useState(INITIAL_SWITCHES)
  const initialRoot = electRoot(initialSwitches).root
  const election = electRoot(switches)

  function setPriority(name: string, priority: number) {
    const next = switches.map((sw) => (sw.name === name ? { ...sw, priority } : sw))
    setSwitches(next)
    if (electRoot(next).root !== initialRoot) onRootChanged()
  }

  const nonRoot = switches.filter((sw) => sw.name !== election.root)
  const blocking = nonRoot.length > 0
    ? nonRoot.reduce((worst, cur) => (
      cur.priority !== worst.priority ? (cur.priority > worst.priority ? cur : worst) : (cur.mac > worst.mac ? cur : worst)
    ))
    : null

  return (
    <div>
      <p className="text-xs text-slate-500 mb-3">{s.stpIntro}</p>
      <div className="rounded-lg border divide-y text-xs mb-3">
        {switches.map((sw) => (
          <div key={sw.name} className={`flex flex-wrap items-center justify-between gap-2 px-3 py-1.5 ${
            sw.name === election.root ? 'bg-teal-50' : ''}`}
          >
            <span className="font-semibold text-slate-700 w-12">{sw.name}</span>
            <label className="text-slate-600" htmlFor={`prio-${sw.name}`}>
              {s.priority}
              <select
                id={`prio-${sw.name}`}
                value={sw.priority}
                onChange={(e) => setPriority(sw.name, Number(e.target.value))}
                className="ml-1 border rounded px-1 py-0.5 font-mono"
              >
                {PRIORITY_STEPS.map((p) => <option key={p} value={p}>{p}</option>)}
              </select>
            </label>
            <span className="font-mono text-slate-500">{s.mac}: {sw.mac}</span>
            {sw.name === election.root && <span className="rounded bg-teal-200 px-1.5 py-0.5 text-[10px] font-semibold text-teal-800">ROOT</span>}
          </div>
        ))}
      </div>

      <div className="rounded-lg border-2 border-teal-300 bg-teal-50/60 p-3 text-xs mb-2" aria-live="polite">
        <p className="font-semibold text-teal-800">{s.rootIs(election.root)}</p>
        <p className="text-slate-600 mt-1">{election.reason === 'priority' ? s.reasonPriority : s.reasonMac}</p>
      </div>

      {blocking && (
        <div className="rounded-lg border border-amber-200 bg-amber-50 p-3 text-xs mb-1">
          <p className="font-medium text-amber-800">{s.blockedSimplified(blocking.name)}</p>
          <p className="text-amber-700 mt-1">{s.blockedNote}</p>
        </div>
      )}
    </div>
  )
}

function Aggregation({ lang, onSingleFlowSeen }: { lang: Lang; onSingleFlowSeen: () => void }) {
  const s = STR[lang]
  const [linkCount, setLinkCount] = useState(2)
  const [downLinks, setDownLinks] = useState(0)
  const [mode, setMode] = useState<Mode>('parallel')
  const activeLinks = Math.max(1, linkCount - downLinks)
  const sum = aggregateBandwidth(activeLinks, LINK_MBIT)
  const effective = mode === 'single' ? singleFlowBandwidth(LINK_MBIT) : sum

  function changeLinkCount(n: number) {
    setLinkCount(n)
    setDownLinks(0)
  }

  function setModeAndTrack(m: Mode) {
    setMode(m)
    if (m === 'single') onSingleFlowSeen()
  }

  return (
    <div>
      <p className="text-xs text-slate-500 mb-3">{s.aggIntro}</p>

      <div className="flex flex-wrap items-end gap-3 mb-3">
        <label className="text-xs text-slate-600" htmlFor="link-count">
          {s.linkCount}
          <select
            id="link-count"
            value={linkCount}
            onChange={(e) => changeLinkCount(Number(e.target.value))}
            className="ml-1 border rounded px-1 py-0.5"
          >
            {[2, 3, 4].map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
        </label>

        <fieldset className="text-xs text-slate-600">
          <legend className="mb-1">{s.mode}</legend>
          <div className="flex gap-2">
            <button
              onClick={() => setModeAndTrack('parallel')}
              aria-pressed={mode === 'parallel'}
              className={`rounded-lg border px-2 py-1 ${mode === 'parallel' ? 'border-teal-500 bg-teal-50 text-teal-700 font-medium' : 'hover:bg-slate-50'}`}
            >
              {s.modeParallel}
            </button>
            <button
              onClick={() => setModeAndTrack('single')}
              aria-pressed={mode === 'single'}
              className={`rounded-lg border px-2 py-1 ${mode === 'single' ? 'border-teal-500 bg-teal-50 text-teal-700 font-medium' : 'hover:bg-slate-50'}`}
            >
              {s.modeSingle}
            </button>
          </div>
        </fieldset>
      </div>

      <div className="rounded-lg border divide-y text-xs mb-3">
        {Array.from({ length: linkCount }, (_, i) => i).map((i) => {
          const isDown = i >= activeLinks
          return (
            <div key={i} className={`flex items-center justify-between px-3 py-1.5 ${isDown ? 'bg-rose-50' : 'bg-teal-50/40'}`}>
              <span className={isDown ? 'text-rose-400 line-through' : 'text-slate-700'}>
                {s.link} {i + 1} · {LINK_MBIT.toLocaleString(lang)} Mbit/s
              </span>
            </div>
          )
        })}
      </div>

      <div className="flex flex-wrap gap-2 mb-3">
        <button
          onClick={() => setDownLinks((d) => Math.min(linkCount - 1, d + 1))}
          disabled={activeLinks <= 1}
          className="rounded-lg border px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
        >
          {s.failLink}
        </button>
        {downLinks > 0 && (
          <button
            onClick={() => setDownLinks(0)}
            className="rounded-lg border px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50"
          >
            {s.restoreAll}
          </button>
        )}
      </div>

      <div className="rounded-lg border-2 border-teal-300 bg-teal-50/60 p-3 text-xs mb-2" aria-live="polite">
        <p className="text-slate-700">{s.sumBandwidth}: <span className="font-semibold text-teal-800">{sum.toLocaleString(lang)} Mbit/s</span> ({activeLinks} {s.activeLinks})</p>
        <p className="text-slate-700 mt-1">{s.effective}: <span className={`font-semibold ${mode === 'single' ? 'text-rose-700' : 'text-teal-800'}`}>{effective.toLocaleString(lang)} Mbit/s</span></p>
        {downLinks > 0 && <p className="text-slate-500 mt-1">{s.stillUp}</p>}
      </div>

      {mode === 'single' && (
        <p className="text-xs text-amber-700">{s.singleFlowNote}</p>
      )}
    </div>
  )
}

export function Redundancy({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const [tab, setTab] = useState<Tab>('stp')
  const [rootChanged, setRootChanged] = useState(false)
  const [singleFlowSeen, setSingleFlowSeen] = useState(false)

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>

      <div className="flex gap-2 mb-4" role="tablist">
        <button
          role="tab"
          aria-selected={tab === 'stp'}
          onClick={() => setTab('stp')}
          className={`rounded-lg border px-3 py-1.5 text-sm font-medium ${tab === 'stp' ? 'border-teal-500 bg-teal-50 text-teal-700' : 'hover:bg-slate-50'}`}
        >
          {s.tabStp}
        </button>
        <button
          role="tab"
          aria-selected={tab === 'aggregation'}
          onClick={() => setTab('aggregation')}
          className={`rounded-lg border px-3 py-1.5 text-sm font-medium ${tab === 'aggregation' ? 'border-teal-500 bg-teal-50 text-teal-700' : 'hover:bg-slate-50'}`}
        >
          {s.tabAgg}
        </button>
      </div>

      {tab === 'stp'
        ? <Stp lang={lang} onRootChanged={() => setRootChanged(true)} />
        : <Aggregation lang={lang} onSingleFlowSeen={() => setSingleFlowSeen(true)} />}

      <ChallengeBox lang={lang} task={s.challenge} done={rootChanged && singleFlowSeen} />
    </div>
  )
}
