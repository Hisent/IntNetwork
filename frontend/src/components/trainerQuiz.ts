import type { Question } from '@/types'

export function isCorrect(q: Question, opt: string): boolean {
  if (q.type === 'single') return q.answer === opt
  if (q.type === 'multi') return (q.answer ?? []).includes(opt)
  return false
}
