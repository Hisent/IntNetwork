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
})
