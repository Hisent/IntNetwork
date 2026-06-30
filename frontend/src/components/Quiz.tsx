import { useState } from 'react'
import type { Question } from '@/types'
import { learnApi } from '@/lib/learnApi'

interface Result { score: number; total: number; passed: boolean; best: number }

export function Quiz({ moduleKey, questions }: { moduleKey: string; questions: Question[] }) {
  const [answers, setAnswers] = useState<Record<string, unknown>>({})
  const [result, setResult] = useState<Result | null>(null)
  const [best, setBest] = useState<number | null>(null)
  const [busy, setBusy] = useState(false)

  const set = (id: string, value: unknown) => setAnswers((a) => ({ ...a, [id]: value }))
  const toggleMulti = (id: string, opt: string) =>
    setAnswers((a) => {
      const cur = (a[id] as string[]) ?? []
      return { ...a, [id]: cur.includes(opt) ? cur.filter((o) => o !== opt) : [...cur, opt] }
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
        <h3 className="text-lg font-semibold text-slate-900">Quiz</h3>
        {best != null && <span className="text-sm text-slate-500">Bisher bester: <b>{best}%</b></span>}
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
                {q.options.map((opt) => (
                  <label key={opt} className={`flex items-center gap-2 ${locked ? 'text-slate-400' : 'text-slate-700'}`}>
                    <input
                      type={q.type === 'single' ? 'radio' : 'checkbox'}
                      name={q.id}
                      disabled={locked}
                      checked={q.type === 'single' ? answers[q.id] === opt : ((answers[q.id] as string[]) ?? []).includes(opt)}
                      onChange={() => (q.type === 'single' ? set(q.id, opt) : toggleMulti(q.id, opt))}
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
          {busy ? 'Werte aus…' : 'Auswerten'}
        </button>
      ) : (
        <div className="mt-5 flex items-center gap-4">
          <p className={`font-medium ${result.passed ? 'text-green-600' : 'text-amber-600'}`}>
            {result.score} / {result.total} richtig — {result.passed ? 'bestanden ✓' : 'noch nicht bestanden'}
          </p>
          <button onClick={retry} className="rounded-lg border border-slate-300 text-slate-700 px-4 py-2 font-medium hover:bg-slate-50">
            Erneut versuchen
          </button>
        </div>
      )}
    </div>
  )
}
