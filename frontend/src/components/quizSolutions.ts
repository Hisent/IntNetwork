import type { Question } from '@/types'

export function isCorrect(q: Question, optIndex: number): boolean {
  if (q.type === 'single') return q.answer === optIndex
  if (q.type === 'multi') return (q.answer ?? []).includes(optIndex)
  return false
}
