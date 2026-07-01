import { describe, it, expect } from 'vitest'
import { isCorrect } from './trainerQuiz'
import type { Question } from '@/types'

const single: Question = { id: 's', type: 'single', prompt: '', options: ['a', 'b'], answer: 'b' }
const multi: Question = { id: 'm', type: 'multi', prompt: '', options: ['a', 'b', 'c'], answer: ['a', 'c'] }
const num: Question = { id: 'n', type: 'number', prompt: '', answer: 42 }

describe('isCorrect', () => {
  it('single: nur die Antwort ist korrekt', () => {
    expect(isCorrect(single, 'b')).toBe(true)
    expect(isCorrect(single, 'a')).toBe(false)
  })
  it('multi: alle Antwort-Optionen korrekt', () => {
    expect(isCorrect(multi, 'a')).toBe(true)
    expect(isCorrect(multi, 'b')).toBe(false)
  })
  it('number: Optionen gibt es nicht -> false', () => {
    expect(isCorrect(num, '42')).toBe(false)
  })
})
