import { useEffect, useId, useRef, useState } from 'react'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'
import type { Dot1xLayer, Dot1xRole } from '@/widgets/nac/dot1x'
import {
  OPTION_LABEL, POLICY, QUESTIONS, QUESTION_KEYS, QUESTION_LABEL, SCENARIOS, SCENARIO_BY_ID, grade, isComplete,
  labStepName, portAt, type Answers, type QuestionKey, type ScenarioId,
} from '@/widgets/nac/radiusLab'

const STR = {
  de: {
    title: 'RADIUS-Labor: vorhersagen, dann nachsehen',
    subtitle: 'Wähle ein Endgerät, sag Methode, RADIUS-Antwort, Attribute und CoA voraus – dann zeigt der Paketablauf, was wirklich passiert.',
    device: 'Endgerät', policy: 'Nordwind-Regelwerk des Policy-Servers',
    check: 'Vorhersage prüfen', again: 'Neue Vorhersage', incomplete: 'Beantworte alle fünf Fragen.',
    score: (n: number, of: number) => `${n} von ${of} richtig`,
    yours: 'Deine Antwort', right: 'Richtig',
    trace: 'Paketablauf', prev: 'Zurück', next: 'Nächster Schritt', all: 'Alle zeigen',
    step: 'Schritt', of: 'von', port: 'Port',
    outcome: 'Ergebnis',
    roles: { supplicant: 'Endgerät', authenticator: 'Switch', server: 'Policy-Server' } as Record<Dot1xRole, string>,
    layers: { eapol: 'EAPOL', radius: 'RADIUS', data: 'Daten', local: 'intern' } as Record<Dot1xLayer, string>,
    challenge: 'Sag drei Endgeräte vollständig richtig voraus.',
    solved: '(gelöst)', okSr: 'richtig', badSr: 'falsch',
  },
  en: {
    title: 'RADIUS lab: predict, then look',
    subtitle: 'Pick an endpoint, predict method, RADIUS answer, attributes and CoA – then the packet flow shows what really happens.',
    device: 'Endpoint', policy: "Nordwind policy on the policy server",
    check: 'Check prediction', again: 'New prediction', incomplete: 'Answer all five questions.',
    score: (n: number, of: number) => `${n} of ${of} correct`,
    yours: 'Your answer', right: 'Correct',
    trace: 'Packet flow', prev: 'Back', next: 'Next step', all: 'Show all',
    step: 'Step', of: 'of', port: 'Port',
    outcome: 'Outcome',
    roles: { supplicant: 'Endpoint', authenticator: 'Switch', server: 'Policy server' } as Record<Dot1xRole, string>,
    layers: { eapol: 'EAPOL', radius: 'RADIUS', data: 'data', local: 'internal' } as Record<Dot1xLayer, string>,
    challenge: 'Predict three endpoints completely correctly.',
    solved: '(solved)', okSr: 'correct', badSr: 'wrong',
  },
} as const

const BTN = 'wb-control rounded-lg border px-3 py-1.5 text-sm font-medium aria-disabled:cursor-default aria-disabled:opacity-50'
const BTN_PLAIN = `${BTN} border-[var(--wb-border)] bg-[var(--wb-surface)] text-[var(--wb-ink)] hover:bg-[var(--wb-subtle)]`
const OK_BOX = 'border-green-200 bg-green-50 text-green-800'
const BAD_BOX = 'border-rose-300 bg-rose-50 text-rose-800'
const WAIT_BOX = 'border-amber-300 bg-amber-50 text-amber-800'

const label = (key: QuestionKey, option: string, lang: Lang) =>
  (OPTION_LABEL[key] as Record<string, { de: string; en: string }>)[option][lang]

export function NacRadiusLab({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const uid = useId()
  const [scenarioId, setScenarioId] = useState<ScenarioId>(SCENARIOS[0].id)
  const [answers, setAnswers] = useState<Partial<Answers>>({})
  const [checked, setChecked] = useState(false)
  const [idx, setIdx] = useState(0)
  const [solved, setSolved] = useState<Set<ScenarioId>>(new Set())
  const sc = SCENARIO_BY_ID[scenarioId]
  const complete = isComplete(answers)
  const graded = checked && complete ? grade(sc, answers) : null
  const last = sc.trace.length - 1
  const port = portAt(sc.trace, idx)
  const step = sc.trace[idx]

  // Prüfen/Nochmal: der auslösende Knopf verschwindet – Fokus gezielt setzen,
  // statt ihn auf <body> fallen zu lassen. Ein Szenariowechsel bewegt ihn nicht.
  const resultRef = useRef<HTMLDivElement>(null)
  const formRef = useRef<HTMLDivElement>(null)
  const focusTo = useRef<'result' | 'form' | null>(null)
  useEffect(() => {
    if (focusTo.current === 'result') resultRef.current?.focus()
    if (focusTo.current === 'form') formRef.current?.querySelector('input')?.focus()
    focusTo.current = null
  }, [checked])

  const pick = (id: ScenarioId) => { setScenarioId(id); setAnswers({}); setChecked(false); setIdx(0) }
  const check = () => {
    if (!complete) return
    if (grade(sc, answers).every((g) => g.ok)) setSolved((prev) => new Set(prev).add(sc.id))
    focusTo.current = 'result'
    setIdx(0)
    setChecked(true)
  }
  const retry = () => { focusTo.current = 'form'; setAnswers({}); setChecked(false); setIdx(0) }

  return (
    <div className="rounded-2xl border border-[var(--wb-border)] bg-[var(--wb-surface)] p-4 text-[var(--wb-ink)] sm:p-5">
      <p className="text-sm font-semibold">{s.title}</p>
      <p className="mb-4 text-xs text-[var(--wb-muted)]">{s.subtitle}</p>

      <fieldset className="mb-3">
        <legend className="mb-1 text-xs font-semibold text-[var(--wb-muted)]">{s.device}</legend>
        <div className="flex flex-wrap gap-2">
          {SCENARIOS.map((x) => (
            <button key={x.id} type="button" aria-pressed={x.id === scenarioId} onClick={() => pick(x.id)}
              className={`${BTN} ${x.id === scenarioId
                ? 'border-[var(--wb-accent)] bg-[var(--wb-accent-soft)] text-[var(--wb-ink)]'
                : 'border-[var(--wb-border)] bg-[var(--wb-surface)] text-[var(--wb-ink)] hover:bg-[var(--wb-subtle)]'}`}>
              {x.title[lang]}
              {solved.has(x.id) && <><span aria-hidden="true"> ✓</span><span className="sr-only">{s.solved}</span></>}
            </button>
          ))}
        </div>
      </fieldset>

      <p className="mb-3 rounded-lg border-l-2 border-[var(--wb-accent)] bg-[var(--wb-subtle)] px-3 py-2 text-sm text-[var(--wb-ink)]">
        {sc.situation[lang]}
      </p>

      <details className="mb-4 text-sm">
        <summary className="cursor-pointer font-medium text-[var(--wb-ink)]">{s.policy}</summary>
        <ul className="mt-2 list-disc space-y-1 pl-5 text-[var(--wb-muted)]">
          {POLICY.map((rule) => <li key={rule.en}>{rule[lang]}</li>)}
        </ul>
      </details>

      <div ref={formRef} className="mb-3 grid gap-3">
        {QUESTION_KEYS.map((key) => (
          <fieldset key={key} disabled={checked} className="min-w-0">
            <legend className="mb-1 text-xs font-semibold text-[var(--wb-muted)]">{QUESTION_LABEL[key][lang]}</legend>
            <div className="flex flex-wrap gap-2">
              {QUESTIONS[key].map((option) => {
                const on = answers[key] === option
                return (
                  <label key={option} className={`flex min-h-[44px] cursor-pointer items-center gap-2 rounded-lg border px-3 py-1.5 text-sm ${
                    on ? 'border-[var(--wb-accent)] bg-[var(--wb-accent-soft)] text-[var(--wb-ink)]' : 'border-[var(--wb-border)] text-[var(--wb-ink)]'}`}>
                    <input type="radio" name={`${uid}-${key}`} checked={on}
                      onChange={() => setAnswers((a) => ({ ...a, [key]: option }))} />
                    {label(key, option, lang)}
                  </label>
                )
              })}
            </div>
          </fieldset>
        ))}
      </div>

      {!checked && (
        <div className="mb-2 flex flex-wrap items-center gap-3">
          <button type="button" onClick={check} aria-disabled={!complete}
            className={`${BTN} border-transparent bg-[var(--wb-accent)] text-white hover:bg-[var(--wb-accent-hover)]`}>
            {s.check}
          </button>
          {!complete && <span className="text-xs text-[var(--wb-muted)]">{s.incomplete}</span>}
        </div>
      )}

      {graded && (
        <>
          <div ref={resultRef} role="status" tabIndex={-1} className="mb-4 outline-none">
            <p className="mb-2 text-sm font-semibold">{s.score(graded.filter((g) => g.ok).length, graded.length)}</p>
            <ul className="grid gap-2">
              {graded.map((g) => (
                <li key={g.key} className={`rounded-lg border px-3 py-2 text-sm ${g.ok ? OK_BOX : BAD_BOX}`}>
                  <p className="font-semibold"><span aria-hidden="true">{g.ok ? '✓' : '✗'} </span><span className="sr-only">{g.ok ? s.okSr : s.badSr}: </span>{QUESTION_LABEL[g.key][lang]}</p>
                  {!g.ok && (
                    <p className="text-xs">
                      {s.yours}: {label(g.key, answers[g.key] as string, lang)} · {s.right}: <strong>{label(g.key, g.correct, lang)}</strong>
                    </p>
                  )}
                  {g.notes.map((n) => <p key={n.en} className="mt-1">{n[lang]}</p>)}
                </li>
              ))}
            </ul>
          </div>

          <section aria-label={s.trace} className="mb-2">
            <p className="mb-2 text-sm font-semibold">{s.trace}</p>
            <div className={`mb-3 rounded-lg border px-3 py-2 text-sm ${port.open ? OK_BOX : WAIT_BOX}`} aria-live="polite">
              <p className="font-semibold">{s.step} {idx + 1} {s.of} {sc.trace.length}: {labStepName(step, lang)}</p>
              <p>{s.port}: {port.text[lang]}</p>
              {idx === last && <p className="mt-1">{s.outcome}: {sc.outcome[lang]}</p>}
            </div>
            <div className="mb-3 flex flex-wrap gap-2">
              <button type="button" className={BTN_PLAIN} aria-disabled={idx === 0}
                onClick={() => setIdx((i) => Math.max(i - 1, 0))}>{s.prev}</button>
              <button type="button" className={`${BTN} border-transparent bg-[var(--wb-accent)] text-white hover:bg-[var(--wb-accent-hover)]`}
                aria-disabled={idx === last} onClick={() => setIdx((i) => Math.min(i + 1, last))}>{s.next}</button>
              <button type="button" className={BTN_PLAIN} aria-disabled={idx === last}
                onClick={() => setIdx(last)}>{s.all}</button>
              <button type="button" className={BTN_PLAIN} onClick={retry}>{s.again}</button>
            </div>
            <ol className="grid gap-2">
              {sc.trace.slice(0, idx + 1).map((st, i) => (
                <li key={i} aria-current={i === idx ? 'step' : undefined}
                  className={`min-w-0 rounded-lg border px-3 py-2 text-sm ${i === idx
                    ? 'border-[var(--wb-accent)] bg-[var(--wb-accent-soft)] text-[var(--wb-ink)]'
                    : 'border-[var(--wb-border)] bg-[var(--wb-surface)] text-[var(--wb-ink)]'}`}>
                  <p className="text-xs text-[var(--wb-muted)]">
                    {i + 1}. {st.from === st.to ? s.roles[st.from] : `${s.roles[st.from]} → ${s.roles[st.to]}`} · {s.layers[st.layer]}
                  </p>
                  <p className="font-mono font-semibold [overflow-wrap:anywhere]">{labStepName(st, lang)}</p>
                  <p className="mt-0.5">{st.detail[lang]}</p>
                  {st.attrs && (
                    <ul className="mt-1 font-mono text-xs [overflow-wrap:anywhere]" aria-label={lang === 'de' ? 'RADIUS-Attribute' : 'RADIUS attributes'}>
                      {st.attrs.map((a) => <li key={a}>{a}</li>)}
                    </ul>
                  )}
                </li>
              ))}
            </ol>
          </section>
        </>
      )}

      <ChallengeBox lang={lang} task={s.challenge} done={solved.size >= 3} />
    </div>
  )
}
