// @vitest-environment jsdom
//
// Beamer-Modus: jede Folie zeigt ihren Block in derselben Komponenteninstanz —
// der Zustand der vorigen Folie (Schritt eines Diagramms) darf nicht mitwandern.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { useAuthStore } from '@/store/auth'
import { TrainerPresentPage } from '@/pages/TrainerPresentPage'

vi.mock('@/lib/api', async (original) => ({
  ...(await original<typeof import('@/lib/api')>()),
  api: { get: vi.fn(), post: vi.fn(), put: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))
import { api } from '@/lib/api'

const seq = (uid: string, title: string, n: number) => ({
  uid, type: 'diagram', kind: 'sequence', title,
  actors: [{ id: 'a', label: 'A' }, { id: 'b', label: 'B' }],
  messages: Array.from({ length: n }, (_, i) => ({ from: 'a', to: 'b', label: `${title}-${i + 1}` })),
})

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  useAuthStore.setState({ token: null, role: null, displayName: null })
})

describe('TrainerPresentPage', () => {
  it('Folienwechsel zwischen zwei Sequenzdiagrammen: das zweite startet bei Schritt 1 und stürzt nicht ab', async () => {
    useAuthStore.setState({ token: 'demo', role: 'trainer', displayName: 'T' })
    vi.spyOn(console, 'error').mockImplementation(() => {})
    vi.mocked(api.get).mockImplementation((url: string) => Promise.resolve({
      data: url === '/trainer/modules/m1'
        ? { key: 'm1', title: 'Modul', order: 1, prerequisites: [], workshop_key: 'network', blocks: [seq('d1', 'Lang', 6), seq('d2', 'Kurz', 2)], quiz: { questions: [] } }
        : [],
    }))
    renderWithProviders(<TrainerPresentPage />, { route: '/trainer/modul/m1/praesentation', path: '/trainer/modul/:key/praesentation' })

    fireEvent.click(await screen.findByRole('button', { name: 'weiter →' }))
    const step = await screen.findByRole('button', { name: 'Weiter →' })
    for (let i = 0; i < 5; i++) fireEvent.click(step)
    expect(screen.getByText('Schritt 6 / 6')).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: 'weiter →' }))
    expect(await screen.findByText('Schritt 1 / 2')).toBeTruthy()
    expect(screen.queryByText('Dieses interaktive Element konnte nicht geladen werden.')).toBeNull()

    // zurück: auch die erste Folie beginnt wieder frisch
    fireEvent.click(screen.getByRole('button', { name: '← zurück' }))
    expect(await screen.findByText('Schritt 1 / 6')).toBeTruthy()
    vi.restoreAllMocks()
  })
})
