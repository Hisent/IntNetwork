// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { Quiz } from './Quiz'
import { learnApi } from '@/lib/learnApi'
import type { Question } from '@/types'

const questions: Question[] = [
  { id: '7', type: 'single', prompt: 'Frage A', options: ['x', 'y'] },
  { id: '8', type: 'number', prompt: 'Frage B' },
]

afterEach(cleanup)

describe('Quiz', () => {
  it('zeigt die Erklärung je Frage erst mit dem bewerteten Ergebnis', async () => {
    const submit = vi.spyOn(learnApi, 'submitQuiz').mockResolvedValue({
      data: { score: 1, total: 2, passed: false, best: 50, details: { '7': true, '8': false }, explanations: { '7': 'Weil x.' } },
    } as Awaited<ReturnType<typeof learnApi.submitQuiz>>)
    render(<Quiz moduleKey="m" questions={questions} lang="de" />)

    expect(screen.queryByText('Weil x.')).toBeNull()
    fireEvent.click(screen.getByLabelText('x'))
    fireEvent.change(screen.getByLabelText('Frage B'), { target: { value: '3' } })
    fireEvent.click(screen.getByRole('button', { name: 'Auswerten' }))

    await waitFor(() => expect(screen.getByText('Weil x.')).toBeTruthy())
    expect(submit).toHaveBeenCalledWith('m', { '7': 0, '8': '3' })
    expect(screen.getAllByText('Erklärung:', { exact: false })).toHaveLength(1)  // Frage B hat keine
  })

  it('bricht lange Wörter ohne Leerzeichen in Frage und Optionen um (kein Seitenüberlauf am Handy)', () => {
    render(<Quiz moduleKey="m" questions={[{ id: '9', type: 'single', prompt: 'TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384?', options: ['a', 'b'] }]} lang="de" />)
    expect(screen.getByText('TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384?', { exact: false }).closest('[class*="overflow-wrap:anywhere"]')).toBeTruthy()
  })

  it('Sprachwechsel mitten im Quiz: angeklickte Antworten und Optionsreihenfolge bleiben', () => {
    const de: Question[] = [{ id: '7', type: 'single', prompt: 'Frage A', options: ['eins', 'zwei', 'drei', 'vier', 'fünf', 'sechs'] }, { id: '8', type: 'multi', prompt: 'Frage B', options: ['ja', 'nein'] }]
    const en: Question[] = [{ id: '7', type: 'single', prompt: 'Question A', options: ['one', 'two', 'three', 'four', 'five', 'six'] }, { id: '8', type: 'multi', prompt: 'Question B', options: ['yes', 'no'] }]
    const { rerender } = render(<Quiz moduleKey="m" questions={de} lang="de" />)
    fireEvent.click(screen.getByLabelText('drei'))
    fireEvent.click(screen.getByLabelText('nein'))
    const order = (names: string[]) => screen.getAllByRole('radio').map((r) => names.indexOf(r.closest('label')!.textContent!))
    const before = order(de[0].type === 'single' ? de[0].options : [])

    rerender(<Quiz moduleKey="m" questions={en} lang="en" />)
    expect((screen.getByLabelText('three') as HTMLInputElement).checked).toBe(true)
    expect((screen.getByLabelText('no') as HTMLInputElement).checked).toBe(true)
    expect(order(en[0].type === 'single' ? en[0].options : [])).toEqual(before)
    expect(screen.getByText('2 / 2', { exact: false })).toBeTruthy()
  })
})
