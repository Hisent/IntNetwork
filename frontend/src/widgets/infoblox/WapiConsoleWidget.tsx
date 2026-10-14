import { useId, useRef, useState } from 'react'
import { Icon } from '@/components/Icon'
import type { Lang } from '@/lib/i18n'
import { BASE, execute, initialGrid, statusText, type Method, type WapiResponse } from './wapi'
import { TASKS, type Step } from './tasks'

const STR = {
  de: {
    kicker: 'WAPI-Konsole', sim: 'Simulation – ein kleiner Grid im Browser, kein echter Grid Master',
    intro: 'Objekttypen: record:host, record:a, network, fixedaddress. Zone nordwind-intern.de (mit Unterzone lab.), Netze 10.20.30.0/24 und 10.20.40.0/24. Änderungen bleiben bis zum Zurücksetzen erhalten.',
    tasks: 'Aufgaben', done: 'erledigt', open: 'offen', hint: 'Tipp', solution: 'Lösung', loadStart: 'Fehlerhafte Anfrage laden',
    load: 'In die Konsole laden', method: 'Methode', path: 'Pfad', body: 'JSON-Body', send: 'Senden', reset: 'Grid zurücksetzen',
    sendHint: 'Strg+Enter sendet', response: 'Antwort', none: 'Noch keine Anfrage gesendet.', solved: 'Aufgabe erledigt',
    simNote: 'Hinweis der Simulation', all: 'Alle Aufgaben erledigt.',
  },
  en: {
    kicker: 'WAPI console', sim: 'Simulation – a small Grid in your browser, no real Grid Master',
    intro: 'Object types: record:host, record:a, network, fixedaddress. Zone nordwind-intern.de (with subzone lab.), networks 10.20.30.0/24 and 10.20.40.0/24. Changes persist until you reset.',
    tasks: 'Tasks', done: 'done', open: 'open', hint: 'Hint', solution: 'Solution', loadStart: 'Load the failing request',
    load: 'Load into console', method: 'Method', path: 'Path', body: 'JSON body', send: 'Send', reset: 'Reset grid',
    sendHint: 'Ctrl+Enter sends', response: 'Response', none: 'No request sent yet.', solved: 'Task done',
    simNote: 'Simulation note', all: 'All tasks done.',
  },
} as const

const METHODS: Method[] = ['GET', 'POST', 'PUT', 'DELETE']
const BTN = 'wb-control inline-flex items-center rounded-lg border border-[var(--wb-border)] px-3 text-sm font-medium text-[var(--wb-ink)] hover:bg-[var(--wb-subtle)]'
const SMALL = 'rounded-md border border-[var(--wb-border)] px-2 py-1 text-xs font-medium text-[var(--wb-ink)] hover:bg-[var(--wb-subtle)]'

export function WapiConsole({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const uid = useId()
  const pathRef = useRef<HTMLInputElement>(null)
  const [grid, setGrid] = useState(initialGrid)
  const [method, setMethod] = useState<Method>('GET')
  const [path, setPath] = useState('record:host')
  const [body, setBody] = useState('')
  const [last, setLast] = useState<{ line: string; res: WapiResponse } | null>(null)
  const [solved, setSolved] = useState<string[]>([])
  const [open, setOpen] = useState<Record<string, 'hint' | 'solution' | undefined>>({})
  const [announce, setAnnounce] = useState('')
  const hasBody = method === 'POST' || method === 'PUT'

  const send = (e?: { preventDefault: () => void }) => {
    e?.preventDefault()
    const req = { method, path, body: hasBody ? body : '' }
    const out = execute(grid, req)
    setGrid(out.grid)
    setLast({ line: `${method} ${path.trim()}`, res: out.res })
    const fresh = TASKS.filter((t) => !solved.includes(t.id) && t.done(req, out.res, out.grid))
    if (fresh.length) setSolved([...solved, ...fresh.map((t) => t.id)])
    const status = out.res.status ? `HTTP ${out.res.status} ${statusText(out.res.status)}` : s.simNote
    setAnnounce([status, ...fresh.map((t) => `${s.solved}: ${t.text[lang]}`)].join('. '))
  }
  const load = (step: Step) => {
    setMethod(step.method)
    setPath(step.path)
    setBody(step.body ?? '')
    pathRef.current?.focus()
  }
  const reset = () => {
    setGrid(initialGrid())
    setSolved([])
    setLast(null)
    setOpen({})
    setAnnounce('')
  }
  const toggle = (id: string, what: 'hint' | 'solution') => setOpen({ ...open, [id]: open[id] === what ? undefined : what })

  const res = last?.res
  return (
    <div className="rounded-xl border border-[var(--wb-border)] bg-[var(--wb-surface)] p-4 text-[var(--wb-ink)]">
      <p className="text-xs font-semibold uppercase tracking-wide text-[var(--wb-accent)]">
        {s.kicker}
        <span className="ml-2 font-normal normal-case tracking-normal text-[var(--wb-muted)]">{s.sim}</span>
      </p>
      <p className="mt-1 text-sm text-[var(--wb-muted)]">{s.intro}</p>

      <h3 className="mt-4 text-sm font-semibold">{s.tasks} ({solved.length}/{TASKS.length})</h3>
      <ol className="mt-2 flex flex-col gap-3">
        {TASKS.map((task) => {
          const done = solved.includes(task.id)
          const panel = open[task.id]
          const panelId = `${uid}-${task.id}`
          return (
            <li key={task.id} className="flex items-start gap-2 text-sm">
              <span className={`mt-0.5 inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-full border ${done ? 'border-[var(--wb-success)] text-[var(--wb-success)]' : 'border-[var(--wb-border)]'}`}>
                {done && <Icon name="check" className="h-3.5 w-3.5" />}
              </span>
              <div className="min-w-0 flex-1">
                <p>{task.text[lang]} <span className="sr-only">({done ? s.done : s.open})</span></p>
                {task.start && (
                  <pre className="mt-1 overflow-x-auto rounded-md bg-[var(--wb-subtle)] p-2 font-mono text-xs">{`${task.start.method} ${task.start.path}\n${task.start.body ?? ''}`}</pre>
                )}
                <div className="mt-1.5 flex flex-wrap gap-1.5">
                  {task.start && <button type="button" className={SMALL} onClick={() => load(task.start!)}>{s.loadStart}</button>}
                  {(['hint', 'solution'] as const).map((what) => (
                    <button key={what} type="button" className={SMALL} aria-expanded={panel === what} aria-controls={panelId}
                      onClick={() => toggle(task.id, what)}>{s[what]}</button>
                  ))}
                </div>
                <div id={panelId}>
                  {panel === 'hint' && <p className="mt-1.5 text-[var(--wb-muted)]">{task.hint[lang]}</p>}
                  {panel === 'solution' && task.solution(grid).map((step, i) => (
                    <div key={i} className="mt-1.5">
                      <pre className="overflow-x-auto whitespace-pre-wrap break-all rounded-md bg-[var(--wb-subtle)] p-2 font-mono text-xs">{`${step.method} ${step.path}${step.body ? `\n${step.body}` : ''}`}</pre>
                      <button type="button" className={`${SMALL} mt-1`} onClick={() => load(step)}>{s.load}</button>
                    </div>
                  ))}
                </div>
              </div>
            </li>
          )
        })}
      </ol>
      {solved.length === TASKS.length && <p className="mt-2 text-sm font-semibold text-[var(--wb-success)]">{s.all}</p>}

      <form onSubmit={send} className="mt-4 border-t border-[var(--wb-border)] pt-4">
        <p className="break-all font-mono text-xs text-[var(--wb-muted)]">{BASE}</p>
        <div className="mt-1 flex flex-wrap gap-2">
          <label className="sr-only" htmlFor={`${uid}-m`}>{s.method}</label>
          <select id={`${uid}-m`} value={method} onChange={(e) => setMethod(e.target.value as Method)}
            className="wb-control rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-2 font-mono text-sm text-[var(--wb-ink)]">
            {METHODS.map((m) => <option key={m}>{m}</option>)}
          </select>
          <label className="sr-only" htmlFor={`${uid}-p`}>{s.path}</label>
          <input id={`${uid}-p`} ref={pathRef} value={path} onChange={(e) => setPath(e.target.value)}
            spellCheck={false} autoComplete="off" autoCapitalize="off"
            className="wb-control min-w-0 flex-1 basis-48 rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-2 font-mono text-sm text-[var(--wb-ink)]" />
        </div>
        {hasBody && (
          <>
            <label className="mt-2 block text-xs text-[var(--wb-muted)]" htmlFor={`${uid}-b`}>{s.body} · {s.sendHint}</label>
            <textarea id={`${uid}-b`} value={body} rows={5} onChange={(e) => setBody(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) send(e) }}
              spellCheck={false} autoComplete="off" autoCapitalize="off"
              className="mt-1 w-full rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] p-2 font-mono text-sm text-[var(--wb-ink)]" />
          </>
        )}
        <div className="mt-2 flex flex-wrap gap-2">
          <button type="submit" className="wb-control rounded-lg bg-[var(--wb-accent)] px-4 text-sm font-semibold text-white hover:bg-[var(--wb-accent-hover)]">{s.send}</button>
          <button type="button" className={BTN} onClick={reset}>{s.reset}</button>
        </div>
      </form>

      <h3 className="mt-4 text-sm font-semibold">{s.response}</h3>
      <p className="sr-only" aria-live="polite">{announce}</p>
      {!res ? <p className="mt-1 text-sm text-[var(--wb-muted)]">{s.none}</p> : (
        <div className="mt-1">
          <p className="break-all font-mono text-xs text-[var(--wb-muted)]">{last?.line}</p>
          {res.status ? (
            <>
              <p className={`mt-1 font-mono text-sm font-semibold ${res.status < 300 ? 'text-[var(--wb-success)]' : 'text-[var(--wb-warning)]'}`}>
                HTTP {res.status} {statusText(res.status)}
              </p>
              <pre className="mt-1 max-h-80 overflow-auto whitespace-pre-wrap break-all rounded-lg bg-[var(--wb-subtle)] p-3 font-mono text-xs">{JSON.stringify(res.body, null, 2)}</pre>
            </>
          ) : (
            <p className="mt-1 text-sm"><span className="font-semibold">{s.simNote}:</span> {res.note?.[lang]}</p>
          )}
        </div>
      )}
    </div>
  )
}
