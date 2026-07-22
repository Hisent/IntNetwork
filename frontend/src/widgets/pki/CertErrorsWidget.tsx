import { useState } from 'react'
import { CASES, scoreOf } from '@/widgets/pki/errors'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'Fehlerbilder aus der Praxis — welche Ursache steckt dahinter?',
    subtitle: 'Echte Fehlermeldungen aus Browser, openssl und curl. Ordne jeweils die wahrscheinlichste Ursache zu.',
    progress: (i: number, n: number) => `Fall ${i} von ${n}`,
    caseLabel: 'Situation',
    optionsLabel: 'Was ist die wahrscheinlichste Ursache?',
    submit: 'Antwort prüfen',
    next: 'Nächster Fall',
    correct: '✓ Richtig',
    incorrect: '✗ Nicht ganz',
    explanationLabel: 'Erklärung',
    nextStepLabel: 'Nächster Diagnoseschritt',
    doneTitle: 'Auswertung',
    doneText: (score: number, n: number) => `Du hast ${score} von ${n} Fällen richtig zugeordnet.`,
    restart: 'Nochmal von vorn',
    challenge: 'Beantworte alle Fälle.',
  },
  en: {
    title: 'Real-world error patterns — what is actually causing this?',
    subtitle: 'Genuine error messages from browsers, openssl and curl. Match each one to its most likely cause.',
    progress: (i: number, n: number) => `Case ${i} of ${n}`,
    caseLabel: 'Situation',
    optionsLabel: 'What is the most likely cause?',
    submit: 'Check answer',
    next: 'Next case',
    correct: '✓ Correct',
    incorrect: '✗ Not quite',
    explanationLabel: 'Explanation',
    nextStepLabel: 'Next diagnostic step',
    doneTitle: 'Results',
    doneText: (score: number, n: number) => `You matched ${score} of ${n} cases correctly.`,
    restart: 'Start over',
    challenge: 'Answer every case.',
  },
} as const

export function CertErrors({ lang }: { lang: Lang }) {
  const n = CASES.length
  const [index, setIndex] = useState(0)
  const [answers, setAnswers] = useState<(number | null)[]>(() => Array(n).fill(null))
  const [revealed, setRevealed] = useState<boolean[]>(() => Array(n).fill(false))
  const s = STR[lang]

  const done = revealed.every(Boolean)
  const current = CASES[index]
  const answer = answers[index]
  const isRevealed = revealed[index]

  const choose = (i: number) => {
    if (isRevealed) return
    setAnswers((prev) => prev.map((a, idx) => (idx === index ? i : a)))
  }
  const submit = () => {
    if (answer === null) return
    setRevealed((prev) => prev.map((r, idx) => (idx === index ? true : r)))
  }
  const next = () => setIndex((i) => Math.min(i + 1, n - 1))
  const restart = () => {
    setIndex(0)
    setAnswers(Array(n).fill(null))
    setRevealed(Array(n).fill(false))
  }

  const score = scoreOf(answers, CASES)

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-3">{s.subtitle}</p>

      <div className="mb-4">
        <p className="mb-1 text-xs font-semibold text-slate-500">{s.progress(index + 1, n)}</p>
        <div className="flex gap-1.5" aria-label={s.progress(index + 1, n)}>
          {CASES.map((_, i) => (
            <div
              key={i}
              className={`h-1.5 flex-1 rounded ${
                revealed[i] ? 'bg-teal-600' : i === index ? 'bg-teal-300' : 'bg-slate-200'
              }`}
            />
          ))}
        </div>
      </div>

      {!done ? (
        <div>
          <p className="mb-1 text-xs font-semibold text-slate-500">{s.caseLabel}</p>
          <p className="mb-2 text-sm text-slate-700">{current.context[lang]}</p>
          <div className="rounded-lg bg-slate-900 p-3 font-mono text-xs text-amber-300 mb-3 break-all">
            {current.message}
          </div>

          <p className="mb-1.5 text-xs font-semibold text-slate-500">{s.optionsLabel}</p>
          <div className="flex flex-col gap-1.5 mb-3" role="radiogroup" aria-label={s.optionsLabel}>
            {current.options.map((opt, i) => {
              const isCorrect = i === current.answer
              const style = isRevealed
                ? isCorrect
                  ? 'border-green-300 bg-green-50'
                  : answer === i
                    ? 'border-rose-300 bg-rose-50'
                    : 'border-slate-200'
                : answer === i
                  ? 'border-teal-300 bg-teal-50/60'
                  : 'border-slate-200 hover:bg-slate-50'
              return (
                <label key={i} className={`flex items-start gap-2 rounded-lg border px-3 py-2 text-sm cursor-pointer transition-colors ${style}`}>
                  <input
                    type="radio"
                    name={`case-${current.id}`}
                    checked={answer === i}
                    disabled={isRevealed}
                    onChange={() => choose(i)}
                    className="mt-0.5 accent-teal-600"
                  />
                  <span className="text-slate-700">{opt[lang]}</span>
                </label>
              )
            })}
          </div>

          {!isRevealed ? (
            <button
              onClick={submit}
              disabled={answer === null}
              className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium disabled:opacity-40"
            >
              {s.submit}
            </button>
          ) : (
            <div aria-live="polite">
              <p className={`text-sm font-semibold mb-2 ${answer === current.answer ? 'text-green-700' : 'text-rose-700'}`}>
                {answer === current.answer ? s.correct : s.incorrect}
              </p>
              <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700 mb-2">
                <p className="mb-2"><span className="font-semibold text-slate-800">{s.explanationLabel}:</span> {current.explanation[lang]}</p>
                <p className="font-mono text-xs bg-white border border-slate-200 rounded p-2 break-all">
                  <span className="font-sans font-semibold text-slate-600">{s.nextStepLabel}:</span><br />
                  {current.nextStep[lang]}
                </p>
              </div>
              {index < n - 1 && (
                <button
                  onClick={next}
                  className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium"
                >
                  {s.next}
                </button>
              )}
            </div>
          )}
        </div>
      ) : (
        <div className="rounded-lg border border-teal-200 bg-teal-50/60 p-4" aria-live="polite">
          <p className="font-semibold text-teal-900 mb-1">{s.doneTitle}</p>
          <p className="text-sm text-teal-800 mb-3">{s.doneText(score, n)}</p>
          <button
            onClick={restart}
            className="rounded-lg border border-teal-300 bg-white px-3 py-1.5 text-sm font-medium text-teal-800 hover:bg-teal-50"
          >
            {s.restart}
          </button>
        </div>
      )}

      <ChallengeBox lang={lang} task={s.challenge} done={done} />
    </div>
  )
}
