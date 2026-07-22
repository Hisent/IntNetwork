import { describe, it, expect } from 'vitest'
import { CASES, scoreOf } from './errors'

describe('CASES', () => {
  it('jeder Fall hat genau 4 Optionen', () => {
    for (const c of CASES) {
      expect(c.options).toHaveLength(4)
    }
  })

  it('answer liegt im gültigen Bereich (0-3)', () => {
    for (const c of CASES) {
      expect(c.answer).toBeGreaterThanOrEqual(0)
      expect(c.answer).toBeLessThan(c.options.length)
    }
  })

  it('de- und en-Optionslisten sind gleich lang wie options', () => {
    for (const c of CASES) {
      expect(c.options.every((o) => typeof o.de === 'string' && o.de.length > 0)).toBe(true)
      expect(c.options.every((o) => typeof o.en === 'string' && o.en.length > 0)).toBe(true)
    }
  })

  it('jeder Fall hat eine echte Fehlermeldung, Erklärung und einen nächsten Schritt in beiden Sprachen', () => {
    for (const c of CASES) {
      expect(c.message.length).toBeGreaterThan(0)
      expect(c.explanation.de.length).toBeGreaterThan(0)
      expect(c.explanation.en.length).toBeGreaterThan(0)
      expect(c.nextStep.de.length).toBeGreaterThan(0)
      expect(c.nextStep.en.length).toBeGreaterThan(0)
    }
  })

  it('keine zwei Fälle teilen dieselbe Fehlermeldung', () => {
    const messages = CASES.map((c) => c.message)
    expect(new Set(messages).size).toBe(messages.length)
  })
})

describe('scoreOf', () => {
  it('zählt korrekt beantwortete Fälle', () => {
    const allCorrect = CASES.map((c) => c.answer)
    expect(scoreOf(allCorrect, CASES)).toBe(CASES.length)
  })

  it('zählt 0 bei komplett falschen Antworten', () => {
    const allWrong = CASES.map((c) => (c.answer + 1) % c.options.length)
    expect(scoreOf(allWrong, CASES)).toBe(0)
  })

  it('zählt unbeantwortete (null) Fälle nicht mit', () => {
    const partial: (number | null)[] = CASES.map((c) => c.answer)
    partial[0] = null
    expect(scoreOf(partial, CASES)).toBe(CASES.length - 1)
  })
})
