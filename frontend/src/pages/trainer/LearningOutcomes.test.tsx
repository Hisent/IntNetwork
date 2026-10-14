// @vitest-environment jsdom
//
// Lernerfolg im Kurs-Detail: Wissenstest steuern und auswerten, anonyme
// Kursbewertung, CSV-Export (Download mit Token über api.download).
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen, waitFor } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { LearningOutcomes } from '@/pages/trainer/LearningOutcomes'
import type { TrainerAssessment, TrainerEvaluation } from '@/lib/trainerApi'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn(), put: vi.fn(), patch: vi.fn(), delete: vi.fn(), download: vi.fn() },
  errMsg: (_e: unknown, fallback = 'Fehler.') => fallback,
}))
import { api } from '@/lib/api'

const ASSESSMENT: TrainerAssessment = {
  phase: 'post', fixed: true, answered: true,
  questions: [{ id: '11', module_key: 'm1', module_title: 'Modul Eins', prompt: 'Welcher Port?', type: 'single',
    pre_correct: 0, pre_attempts: 2, post_correct: 2, post_attempts: 2 }],
  participants: [{ id: 1, name: 'Ada', pre: 50, post: 100 }, { id: 2, name: 'Linus', pre: null, post: null }],
  summary: { pre_count: 1, post_count: 1, avg_pre: 50, avg_post: 100, avg_gain: 50, gain_count: 1 },
}
const scale = (mean: number | null, n: number, counts = [0, 0, 0, 0, 0]) => ({ mean, n, counts })
const EVALUATION: TrainerEvaluation = {
  open: true, count: 3, min_count: 3, hidden: false, overall: scale(4.5, 2, [0, 0, 0, 1, 1]), clarity: scale(null, 0), practice: scale(3, 1),
  trainer: scale(5, 1), pace: { slow: 0, ok: 1, fast: 1 }, good: ['Viele Übungen'], improve: ['Mehr Pausen'],
}

function mockGet(routes: Record<string, unknown>) {
  vi.mocked(api.get).mockImplementation((url: string) =>
    url in routes ? Promise.resolve({ data: routes[url] }) : Promise.reject(new Error(`kein Mock für ${url}`)))
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

describe('LearningOutcomes (Trainer)', () => {
  it('zeigt Vorher/Nachher je Teilnehmer und je Frage, Neuziehen ist nach Antworten gesperrt', async () => {
    mockGet({ '/trainer/courses/5/assessment': ASSESSMENT, '/trainer/courses/5/evaluation': EVALUATION })
    renderWithProviders(<LearningOutcomes cid={5} />)

    expect(await screen.findByText('Abschlusstest ist geöffnet')).toBeTruthy()
    const row = screen.getByRole('row', { name: /Ada/ })
    expect(row.textContent).toContain('50 %')
    expect(row.textContent).toContain('+50')
    expect(screen.queryByRole('row', { name: /Linus/ })).toBeNull()  // ohne Test keine Zeile
    expect(screen.getByRole('row', { name: /Welcher Port/ }).textContent).toContain('2 / 2')
    expect(screen.getByText(/Ø Zuwachs 50 Prozentpunkte/)).toBeTruthy()
    expect((screen.getByRole('button', { name: 'Fragen neu ziehen' }) as HTMLButtonElement).disabled).toBe(true)
    expect((screen.getByRole('button', { name: 'Abschlusstest öffnen' }) as HTMLButtonElement).disabled).toBe(true)

    vi.mocked(api.put).mockResolvedValue({ data: { ...ASSESSMENT, phase: null } })
    fireEvent.click(screen.getByRole('button', { name: 'Test schließen' }))
    await waitFor(() => expect(api.put).toHaveBeenCalledWith('/trainer/courses/5/assessment', { phase: null }))
    expect(await screen.findByText('Kein Test geöffnet')).toBeTruthy()
  })

  it('zeigt die anonyme Kursbewertung als Aggregat samt Freitexten', async () => {
    mockGet({ '/trainer/courses/5/assessment': ASSESSMENT, '/trainer/courses/5/evaluation': EVALUATION })
    renderWithProviders(<LearningOutcomes cid={5} />)

    expect(await screen.findByText('3 Abgaben')).toBeTruthy()
    expect(screen.getByRole('row', { name: /Gesamteindruck/ }).textContent).toContain('Ø 4,5 (n = 2)')
    expect(screen.getByText('Viele Übungen')).toBeTruthy()
    expect(screen.getByText('Mehr Pausen')).toBeTruthy()

    vi.mocked(api.put).mockResolvedValue({ data: { ...EVALUATION, open: false } })
    fireEvent.click(screen.getByRole('button', { name: 'Kursbewertung schließen' }))
    await waitFor(() => expect(api.put).toHaveBeenCalledWith('/trainer/courses/5/evaluation', { open: false }))
    expect(await screen.findByRole('button', { name: 'Kursbewertung öffnen' })).toBeTruthy()
  })

  it('unter der Mindestzahl nur die Zahl der Abgaben und ein Hinweis', async () => {
    mockGet({ '/trainer/courses/5/assessment': ASSESSMENT,
      '/trainer/courses/5/evaluation': { open: true, count: 2, min_count: 3, hidden: true } satisfies TrainerEvaluation })
    renderWithProviders(<LearningOutcomes cid={5} />)

    expect(await screen.findByText('2 Abgaben')).toBeTruthy()
    expect(screen.getByText(/Ergebnisse erscheinen ab 3 Abgaben/)).toBeTruthy()
    expect(screen.queryByRole('row', { name: /Gesamteindruck/ })).toBeNull()
  })

  it('lädt die CSV-Exporte mit Token herunter und meldet Fehler', async () => {
    mockGet({ '/trainer/courses/5/assessment': ASSESSMENT, '/trainer/courses/5/evaluation': EVALUATION })
    vi.mocked(api.download).mockResolvedValueOnce(undefined).mockRejectedValueOnce(new Error('HTTP 500'))
    renderWithProviders(<LearningOutcomes cid={5} />)

    fireEvent.click(await screen.findByRole('button', { name: 'Fortschritt (CSV)' }))
    await waitFor(() => expect(api.download).toHaveBeenCalledWith('/trainer/courses/5/export/dashboard?lang=de', 'intlab-kurs5-dashboard.csv'))
    fireEvent.click(screen.getByRole('button', { name: 'Kursbewertung (CSV)' }))
    expect(await screen.findByText('Export fehlgeschlagen.')).toBeTruthy()
  })
})
