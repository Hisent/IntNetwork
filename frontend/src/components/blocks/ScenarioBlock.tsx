import { useEffect, useRef } from 'react'
import { useExercise } from '@/lib/exerciseState'
import type { Lang } from '@/lib/i18n'
import { walkScenario } from './exerciseLogic'
import type { ScenarioData } from './types'

const OUTCOME = {
  good: { box: 'border-green-300 bg-green-50 text-green-800', de: 'Gute Entscheidung', en: 'Good call' },
  ok: { box: 'border-amber-300 bg-amber-50 text-amber-800', de: 'Vertretbar — es geht besser', en: 'Acceptable — there is a better way' },
  bad: { box: 'border-rose-300 bg-rose-50 text-rose-800', de: 'Riskante Entscheidung', en: 'Risky call' },
} as const

const START: number[] = []

export default function ScenarioBlock({ data, lang }: { data: ScenarioData; lang: Lang }) {
  const de = lang === 'de'
  // erledigt = ein Ausgang erreicht (gleich welcher — das Szenario bewertet nicht)
  const [saved, setChoices] = useExercise<number[]>([], (c) => {
    const path = walkScenario(data, c)
    return !!path[path.length - 1]?.outcome
  })
  // Gemerkter Pfad, den es im aktuellen Szenario nicht (mehr) gibt -> zurück an den Start.
  const walked = walkScenario(data, Array.isArray(saved) ? saved : [])
  const choices = Array.isArray(saved) && walked.length === saved.length + 1 ? saved : START
  const visited = choices === saved ? walked : walked.slice(0, 1)
  const node = visited[visited.length - 1]
  // Nach einer Wahl verschwindet der geklickte Knopf — Fokus auf die neue Situation setzen,
  // sonst landet die Tastatur wieder am Seitenanfang.
  const currentRef = useRef<HTMLDivElement>(null)
  const moved = useRef(false)
  useEffect(() => {
    if (moved.current) currentRef.current?.focus()
  }, [choices])
  const go = (next: number[]) => { moved.current = true; setChoices(next) }

  if (!node) return <div className="text-sm text-red-500">{de ? 'Szenario ohne Startknoten' : 'Scenario without start node'}</div>
  const outcome = node.outcome ? OUTCOME[node.outcome] : null

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">{de ? 'Szenario' : 'Scenario'}</p>
      <p className="font-medium text-slate-800 mb-2">{data.title}</p>
      {choices.length > 0 && (
        <ol className="mb-3 flex flex-col gap-1 border-l-2 border-teal-200 pl-3 text-sm text-slate-500" aria-label={de ? 'Bisherige Entscheidungen' : 'Decisions so far'}>
          {visited.slice(0, -1).map((v, i) => <li key={i}>{i + 1}. {v.options?.[choices[i]]?.label}</li>)}
        </ol>
      )}
      <div ref={currentRef} tabIndex={-1} aria-live="polite" className="outline-none">
        {outcome ? (
          <div className={`rounded-lg border px-3 py-2 ${outcome.box}`}>
            <p className="text-sm font-semibold">{de ? outcome.de : outcome.en}</p>
            <p className="mt-1 whitespace-pre-line text-sm">{node.text}</p>
          </div>
        ) : (
          <p className="whitespace-pre-line text-slate-700">{node.text}</p>
        )}
      </div>
      {node.options && (
        <div className="mt-3 flex flex-col gap-1.5">
          {node.options.map((o, i) => (
            <button key={`${node.id}-${i}`} type="button" onClick={() => go([...choices, i])}
              className="rounded-lg border border-slate-200 px-3 py-1.5 text-left text-sm text-slate-700 hover:bg-slate-50">
              {o.label}
            </button>
          ))}
        </div>
      )}
      {choices.length > 0 && (
        <div className="mt-3 flex flex-wrap items-center gap-3">
          {outcome && (
            <button type="button" onClick={() => go([])}
              className="rounded-lg border border-teal-200 text-teal-700 px-3 py-1.5 text-sm font-medium hover:bg-teal-50">
              {de ? 'Nochmal' : 'Try again'}
            </button>
          )}
          <button type="button" onClick={() => go(choices.slice(0, -1))} className="text-xs text-slate-500 underline hover:text-slate-700">
            {de ? 'Einen Schritt zurück' : 'One step back'}
          </button>
        </div>
      )}
    </div>
  )
}
