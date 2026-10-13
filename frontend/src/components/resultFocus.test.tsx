// @vitest-environment jsdom
//
// Tastaturfokus nach „Prüfen“: der ausgelöste Knopf wird disabled bzw. verschwindet —
// der Fokus muss auf dem Ergebnis landen (nicht auf <body>), nach „Nochmal“ wieder
// im Block. Beim bloßen Laden eines gemerkten Stands wird kein Fokus gesetzt.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { Blocks } from '@/components/Blocks'
import { Quiz } from '@/components/Quiz'
import { PracticePage } from '@/pages/PracticePage'
import { renderWithProviders } from '@/test/renderWithProviders'
import { useAuthStore } from '@/store/auth'
import type { Block } from '@/types'

vi.mock('@/lib/learnApi', () => ({
  learnApi: {
    submitQuiz: vi.fn().mockResolvedValue({ data: { score: 0, total: 1, passed: false, best: 0, details: { q1: false } } }),
    me: vi.fn().mockResolvedValue({ data: { name: 'T', participant_id: 1, course_id: 9, language: 'de', course: { id: 9, name: 'K' }, workshop: null, progress: [] } }),
    practice: vi.fn().mockResolvedValue({ data: { wrong_total: 1, questions: [
      { id: 'p1', type: 'single', prompt: 'Übungsfrage?', options: ['a', 'b'], module_key: 'm1', module_title: 'Modul' },
      { id: 'p2', type: 'single', prompt: 'Zweite?', options: ['c', 'd'], module_key: 'm1', module_title: 'Modul' },
    ] } }),
    practiceCheck: vi.fn().mockResolvedValue({ data: { correct: false, explanation: 'weil' } }),
  },
}))

const show = (blocks: Block[]) => render(<Blocks blocks={blocks} moduleKey="arp" keyScope="1-9" />)
const focused = () => document.activeElement as HTMLElement
const checkIn = (uid: string) => within(document.querySelector<HTMLElement>(`[data-uid="${uid}"]`)!).getByRole('button', { name: 'Prüfen' })

beforeEach(() => localStorage.clear())
afterEach(cleanup)

describe('Fokus nach dem Prüfen', () => {
  it('Kurz-Check: Ergebnis erhält den Fokus, „Nochmal“ führt zurück zu den Optionen, Laden stiehlt keinen Fokus', () => {
    const check: Block = { uid: 'c', type: 'check', prompt: '2+2?', options: ['3', '4'], answer: 1 }
    show([check])
    fireEvent.click(screen.getByRole('button', { name: '3' }))
    expect(focused().getAttribute('role')).toBe('status')
    expect(focused().textContent).toContain('Falsch')
    fireEvent.click(screen.getByRole('button', { name: 'Nochmal' }))
    expect(focused()).toBe(screen.getByRole('button', { name: '3' }))

    fireEvent.click(screen.getByRole('button', { name: '4' }))
    cleanup()
    show([check])  // „Neuladen“ mit gemerktem Stand
    expect(screen.getByText('Richtig')).toBeTruthy()
    expect(focused()).toBe(document.body)
  })

  it('Zahl-Check, Reihenfolge und Fehlersuche', () => {
    show([
      { uid: 'n', type: 'check', kind: 'number', prompt: 'Bits?', options: [], answer: 8 },
      { uid: 'o', type: 'order', prompt: 'Sortiere', items: ['eins'] },
      { uid: 'd', type: 'debug', prompt: 'Fehler?', lines: ['a', 'b'], wrong: [1], explanation: 'weil' },
    ])
    fireEvent.change(screen.getByRole('spinbutton'), { target: { value: '8' } })
    fireEvent.click(checkIn('n'))
    expect(focused().getAttribute('role')).toBe('status')
    expect(focused().closest('[data-uid]')!.getAttribute('data-uid')).toBe('n')

    fireEvent.click(screen.getByRole('button', { name: 'eins' }))
    fireEvent.click(checkIn('o'))
    expect(focused().closest('[data-uid]')!.getAttribute('data-uid')).toBe('o')

    fireEvent.click(screen.getByRole('button', { name: 'a' }))
    fireEvent.click(checkIn('d'))
    expect(focused().closest('[data-uid]')!.getAttribute('data-uid')).toBe('d')
    expect(focused().getAttribute('role')).toBe('status')
  })

  it('Zuordnung und Lückentext', async () => {
    show([
      { uid: 'm', type: 'match', prompt: 'Ordne zu', pairs: [{ left: 'L0', right: 'R0' }, { left: 'L1', right: 'R1' }] },
      { uid: 'z', type: 'cloze', prompt: 'Fülle', text: 'mode [[m]]', gaps: [{ id: 'm', accept: ['access'] }] },
    ])
    fireEvent.click(await screen.findByRole('button', { name: /R0/ }))
    fireEvent.click(screen.getByRole('button', { name: /R1/ }))
    fireEvent.click(checkIn('m'))
    expect(focused().getAttribute('role')).toBe('status')
    expect(focused().closest('[data-uid]')!.getAttribute('data-uid')).toBe('m')
    fireEvent.click(screen.getByRole('button', { name: 'Zurücksetzen' }))
    expect(focused()).toBe(screen.getByRole('button', { name: /^L0/ }))

    fireEvent.change(await screen.findByLabelText('Lücke 1'), { target: { value: 'trunk' } })
    fireEvent.click(checkIn('z'))
    expect(focused().closest('[data-uid]')!.getAttribute('data-uid')).toBe('z')
    fireEvent.click(screen.getByRole('button', { name: 'Nochmal' }))
    expect(focused()).toBe(screen.getByLabelText('Lücke 1'))
  })

  it('Wissenscheck: nach der Abgabe liegt der Fokus auf dem Ergebnis, nach „Nochmal“ auf der ersten Frage', async () => {
    render(<Quiz moduleKey="m1" lang="de" questions={[{ id: 'q1', type: 'single', prompt: 'Frage?', options: ['a', 'b'] }]} />)
    fireEvent.click(screen.getByLabelText('a'))
    fireEvent.click(screen.getByRole('button', { name: 'Auswerten' }))
    await waitFor(() => expect(focused().getAttribute('role')).toBe('status'))
    expect(focused().textContent).toContain('0 / 1')
    fireEvent.click(screen.getByRole('button', { name: 'Erneut versuchen' }))
    expect(focused().tagName).toBe('INPUT')
  })

  it('Übungsmodus: nach „Prüfen“ liegt der Fokus auf der Rückmeldung, nach „Nochmal“/„Nächste Frage“ auf der Frage', async () => {
    useAuthStore.setState({ token: 'demo', role: 'participant', displayName: 'T' })
    renderWithProviders(<PracticePage />)
    fireEvent.click(await screen.findByRole('button', { name: 'Gemischtes Üben' }))
    fireEvent.click(await screen.findByLabelText('a'))
    fireEvent.click(screen.getByRole('button', { name: 'Prüfen' }))
    await waitFor(() => expect(focused().getAttribute('role')).toBe('status'))
    expect(focused().textContent).toContain('Falsch')
    fireEvent.click(screen.getByRole('button', { name: 'Nochmal' }))
    expect(focused().tagName).toBe('INPUT')

    fireEvent.click(screen.getByLabelText('b'))
    fireEvent.click(screen.getByRole('button', { name: 'Prüfen' }))
    await waitFor(() => expect(focused().getAttribute('role')).toBe('status'))
    fireEvent.click(screen.getByRole('button', { name: /Nächste Frage/ }))
    expect(focused()).toBe(screen.getAllByRole('radio')[0])
    expect(screen.getByText('Zweite?')).toBeTruthy()
    useAuthStore.setState({ token: null, role: null, displayName: null })
  })
})
