import type { Question } from '@/types'
import { isCorrect } from '@/components/quizSolutions'

export function TrainerQuiz({ questions }: { questions: Question[] }) {
  return (
    <div className="mt-8 rounded-2xl border bg-white p-6">
      <h3 className="text-lg font-semibold text-slate-900 mb-4">Quiz — mit Lösungen</h3>
      <div className="flex flex-col gap-5">
        {questions.map((q) => (
          <div key={q.id}>
            <p className="font-medium text-slate-800 mb-2">{q.prompt}</p>
            {q.type === 'number' ? (
              <p className="text-sm">
                <span className="text-slate-500">Antwort: </span>
                <span className="font-mono font-semibold text-teal-700">{q.answer}</span>
              </p>
            ) : (
              <div className="flex flex-col gap-1.5">
                {q.options.map((opt, i) => {
                  const ok = isCorrect(q, i)
                  return (
                    <div
                      key={opt}
                      className={`flex items-center gap-2 text-sm ${ok ? 'text-teal-700 font-medium' : 'text-slate-600'}`}
                    >
                      <span>{ok ? '✓' : '○'}</span>
                      {opt}
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
