import { useState } from 'react'
import type { Question } from '@/types'
import { learnApi } from '@/lib/learnApi'

export function Quiz({ moduleKey, questions }: { moduleKey: string; questions: Question[] }) {
  const [answers, setAnswers] = useState<Record<string, unknown>>({})
  const [result, setResult] = useState<{ score: number; total: number; passed: boolean } | null>(null)

  const set = (id: string, value: unknown) => setAnswers((a) => ({ ...a, [id]: value }))
  const toggleMulti = (id: string, opt: string) =>
    setAnswers((a) => {
      const cur = (a[id] as string[]) ?? []
      return { ...a, [id]: cur.includes(opt) ? cur.filter((o) => o !== opt) : [...cur, opt] }
    })

  async function submit() {
    const r = await learnApi.submitQuiz(moduleKey, answers)
    setResult(r.data)
  }

  return (
    <div className="mt-8 rounded-2xl border bg-white p-6">
      <h3 className="text-lg font-semibold text-slate-900 mb-4">Quiz</h3>
      <div className="flex flex-col gap-5">
        {questions.map((q) => (
          <div key={q.id}>
            <p className="font-medium text-slate-800 mb-2">{q.prompt}</p>
            {q.type === 'number' ? (
              <input type="number" className="border rounded-lg px-3 py-1.5 w-32"
                onChange={(e) => set(q.id, Number(e.target.value))} />
            ) : (
              <div className="flex flex-col gap-1.5">
                {q.options.map((opt) => (
                  <label key={opt} className="flex items-center gap-2 text-slate-700">
                    <input
                      type={q.type === 'single' ? 'radio' : 'checkbox'}
                      name={q.id}
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
      <button onClick={submit} className="mt-5 rounded-lg bg-indigo-600 text-white px-4 py-2 font-medium">
        Auswerten
      </button>
      {result && (
        <p className={`mt-4 font-medium ${result.passed ? 'text-green-600' : 'text-amber-600'}`}>
          {result.score} / {result.total} richtig — {result.passed ? 'bestanden ✓' : 'noch nicht bestanden'}
        </p>
      )}
    </div>
  )
}
