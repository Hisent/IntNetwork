// @vitest-environment jsdom
//
// Lernerfolg, Teilnehmerseite: Hinweiskarten auf /lernen, Wissenstest (vorher ohne
// Auflösung, nachher mit Erklärungen) und anonyme Kursbewertung.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen, waitFor } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { useAuthStore } from '@/store/auth'
import { LearnPage } from '@/pages/LearnPage'
import { AssessmentPage, EvaluationPage } from '@/pages/OutcomePages'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn(), put: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  errMsg: (_e: unknown, fallback = 'Fehler.') => fallback,
}))
import { api } from '@/lib/api'

const ME = { name: 'Test', participant_id: 1, course_id: 9, language: 'de', course: { id: 9, name: 'Kurs' }, workshop: null, progress: [] }
const QUESTIONS = [
  { id: '11', type: 'single', module_key: 'm1', prompt: 'Welcher Port?', options: ['22', '80'] },
  { id: '12', type: 'number', module_key: 'm1', prompt: 'Wie viele Bits?' },
]

function mockGet(routes: Record<string, unknown>) {
  vi.mocked(api.get).mockImplementation((url: string) =>
    url in routes ? Promise.resolve({ data: routes[url] }) : Promise.reject(new Error(`kein Mock für ${url}`)))
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  useAuthStore.setState({ token: null, role: null, displayName: null })
})

describe('Lernerfolg (Teilnehmer)', () => {
  it('zeigt offene Aufgaben als Karten auf der Kursseite', async () => {
    useAuthStore.setState({ token: 't', role: 'participant', displayName: 'Test' })
    mockGet({ '/me': { ...ME, tasks: { assessment: 'post', evaluation: true } }, '/modules': [] })
    renderWithProviders(<LearnPage />)
    expect(await screen.findByRole('heading', { name: 'Abschlusstest' })).toBeTruthy()
    expect(screen.getByRole('link', { name: /Test starten/ }).getAttribute('href')).toBe('/lernen/wissenstest')
    expect(screen.getByRole('link', { name: /Kurs bewerten/ }).getAttribute('href')).toBe('/lernen/bewertung')
  })

  it('Eingangstest: Abgabe erst wenn alles beantwortet, danach nur die Punktzahl', async () => {
    useAuthStore.setState({ token: 't', role: 'participant', displayName: 'Test' })
    mockGet({ '/me': ME, '/assessment': { phase: 'pre', questions: QUESTIONS, result: null } })
    vi.mocked(api.post).mockResolvedValue({ data: { score: 1, total: 2 } })
    renderWithProviders(<AssessmentPage />)

    const submit = await screen.findByRole('button', { name: 'Test abgeben' })
    expect((submit as HTMLButtonElement).disabled).toBe(true)
    fireEvent.click(screen.getByRole('radio', { name: '80' }))
    fireEvent.change(screen.getByRole('spinbutton', { name: 'Wie viele Bits?' }), { target: { value: '32' } })
    fireEvent.click(submit)

    expect(await screen.findByText('1 von 2 richtig')).toBeTruthy()
    expect(api.post).toHaveBeenCalledWith('/assessment', { phase: 'pre', answers: { '11': 1, '12': '32' } })
    expect(screen.getByText('Danke! Die Auflösung gibt es nach dem Abschlusstest.')).toBeTruthy()
    expect(screen.queryByText('Welcher Port?')).toBeNull()
  })

  it('Abschlusstest: Ergebnis mit richtig/falsch und Erklärungen', async () => {
    useAuthStore.setState({ token: 't', role: 'participant', displayName: 'Test' })
    mockGet({ '/me': ME, '/assessment': { phase: 'post', questions: QUESTIONS, result: {
      score: 1, total: 2, details: { '11': true, '12': false }, explanations: { '12': 'IPv4 hat 32 Bit.' } } } })
    renderWithProviders(<AssessmentPage />)
    expect(await screen.findByText('IPv4 hat 32 Bit.')).toBeTruthy()
    expect(screen.getByText('Richtig')).toBeTruthy()
    expect(screen.queryByRole('button', { name: 'Test abgeben' })).toBeNull()
  })

  it('Kursbewertung: Gesamteindruck ist Pflicht, Rest optional; danach Dank', async () => {
    useAuthStore.setState({ token: 't', role: 'participant', displayName: 'Test' })
    mockGet({ '/me': { ...ME, tasks: { assessment: null, evaluation: true } } })
    vi.mocked(api.post).mockResolvedValue({ data: { ok: true } })
    renderWithProviders(<EvaluationPage />)

    const send = await screen.findByRole('button', { name: 'Bewertung absenden' })
    expect((send as HTMLButtonElement).disabled).toBe(true)
    const overall = screen.getByRole('group', { name: /Gesamteindruck/ })
    fireEvent.click(overall.querySelector('input[value="4"]')!)
    fireEvent.click(screen.getByRole('radio', { name: 'zu schnell' }))
    fireEvent.change(screen.getByLabelText(/Was war gut/), { target: { value: 'Labs' } })
    fireEvent.click(send)

    expect(await screen.findByText('Danke für deine Bewertung!')).toBeTruthy()
    await waitFor(() => expect(api.post).toHaveBeenCalledWith('/evaluation', {
      overall: 4, clarity: null, practice: null, pace: 'fast', trainer: null, good: 'Labs', improve: '' }))
  })

  it('Kursbewertung geschlossen: Hinweis statt Formular', async () => {
    useAuthStore.setState({ token: 't', role: 'participant', displayName: 'Test' })
    mockGet({ '/me': { ...ME, tasks: { assessment: null, evaluation: false } } })
    renderWithProviders(<EvaluationPage />)
    expect(await screen.findByText(/nicht geöffnet/)).toBeTruthy()
    expect(screen.queryByRole('button', { name: 'Bewertung absenden' })).toBeNull()
  })
})
