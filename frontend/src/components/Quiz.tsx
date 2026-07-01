import { useState } from 'react'
import type { Question } from '@/types'
import { learnApi } from '@/lib/learnApi'
import { t, type Lang } from '@/lib/i18n'

interface Result { score: number; total: number; passed: boolean; best: number }

export function Quiz({ moduleKey, questions, lang }: { moduleKey: string; questions: Question[]; lang: Lang }) {
  const [answers, setAnswers] = useState<Record<string, unknown>>({})
  const [result, setResult] = useState<Result | null>(null)
  const [best, setBest] = useState<number | null>(null)
  const [busy, setBusy] = useState(false)

  const set = (id: string, value: unknown) => setAnswers((a) => ({ ...a, [id]: value }))
  const toggleMulti = (id: string, optIndex: number) =>
    setAnswers((a) => {
      const cur = (a[id] as number[]) ?? []
      return { ...a, [id]: cur.includes(optIndex) ? cur.filter((o) => o !== optIndex) : [...cur, optIndex] }
    })

  async function submit() {
    setBusy(true)
    try {
      const r = await learnApi.submitQuiz(moduleKey, answers)
      setResult(r.data)
      setBest(r.data.best)
    } finally {
      setBusy(false)
    }
  }

  function retry() {
    setAnswers({})
    setResult(null)
  }

  const locked = result !== null

  return (
    <div className="mt-8 rounded-2xl border bg-white p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-slate-900">{t(lang, 'quiz')}</h3>
        {best != null && <span className="text-sm text-slate-500">{t(lang, 'bestSoFar')}: <b>{best}%</b></span>}
      </div>
      <div className="flex flex-col gap-5">
        {questions.map((q) => (
          <div key={q.id}>
            <p className="font-medium text-slate-800 mb-2">{q.prompt}</p>
            {q.type === 'number' ? (
              <input type="number" disabled={locked} className="border rounded-lg px-3 py-1.5 w-32 disabled:bg-slate-100"
                value={(answers[q.id] as number) ?? ''}
                onChange={(e) => set(q.id, Number(e.target.value))} />
            ) : (
              <div className="flex flex-col gap-1.5">
                {q.options.map((opt, i) => (
                  <label key={opt} className={`flex items-center gap-2 ${locked ? 'text-slate-400' : 'text-slate-700'}`}>
                    <input
                      type={q.type === 'single' ? 'radio' : 'checkbox'}
                      name={q.id}
                      disabled={locked}
                      checked={q.type === 'single' ? answers[q.id] === i : ((answers[q.id] as number[]) ?? []).includes(i)}
                      onChange={() => (q.type === 'single' ? set(q.id, i) : toggleMulti(q.id, i))}
                    />
                    {opt}
                  </label>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {!locked ? (
        <button onClick={submit} disabled={busy}
          className="mt-5 rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 font-medium disabled:opacity-60">
          {busy ? t(lang, 'evaluating') : t(lang, 'submit')}
        </button>
      ) : (
        <div className="mt-5 flex items-center gap-4">
          <p className={`font-medium ${result.passed ? 'text-green-600' : 'text-amber-600'}`}>
            {result.score} / {result.total} {result.passed ? `✓ ${t(lang, 'passed')}` : t(lang, 'notPassedYet')}
          </p>
          <button onClick={retry} className="rounded-lg border border-slate-300 text-slate-700 px-4 py-2 font-medium hover:bg-slate-50">
            {t(lang, 'retry')}
          </button>
        </div>
      )}
    </div>
  )
}
