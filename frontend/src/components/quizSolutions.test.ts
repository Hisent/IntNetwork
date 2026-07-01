import { describe, it, expect } from 'vitest'
import { isCorrect } from './quizSolutions'
import type { Question } from '@/types'

const single: Question = { id: 's', type: 'single', prompt: '', options: ['a', 'b'], answer: 1 }
const multi: Question = { id: 'm', type: 'multi', prompt: '', options: ['a', 'b', 'c'], answer: [0, 2] }
const num: Question = { id: 'n', type: 'number', prompt: '', answer: 42 }

describe('isCorrect', () => {
  it('single: nur der Antwort-Index ist korrekt', () => {
    expect(isCorrect(single, 1)).toBe(true)
    expect(isCorrect(single, 0)).toBe(false)
  })
  it('multi: alle Antwort-Indizes korrekt', () => {
    expect(isCorrect(multi, 0)).toBe(true)
    expect(isCorrect(multi, 1)).toBe(false)
  })
  it('number: hat keine Options-Indizes -> false', () => {
    expect(isCorrect(num, 0)).toBe(false)
  })
})
