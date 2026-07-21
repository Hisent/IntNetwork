// @vitest-environment jsdom
//
// Schlanke Render-Smoke-Suite: die wichtigsten Teilnehmer-Seiten mit
// gemocktem API-Layer (@/lib/api) rendern und je eine zentrale Aussage
// prüfen. Kein E2E, kein echter Server — nur "rendert es überhaupt sinnvoll".
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, screen } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { useAuthStore } from '@/store/auth'
import { LandingPage } from '@/pages/LandingPage'
import { WorkshopPage } from '@/pages/WorkshopPage'
import { LearnPage } from '@/pages/LearnPage'
import { ModulePage } from '@/pages/ModulePage'

vi.mock('@/lib/api', () => ({
  // post/put/patch/delete lösen im Ruhezustand auf (z.B. das Heartbeat-
  // Intervall der ModulePage) — nur .get wird pro Test gezielt belegt.
  api: {
    get: vi.fn(),
    post: vi.fn().mockResolvedValue({ data: undefined }),
    put: vi.fn().mockResolvedValue({ data: undefined }),
    patch: vi.fn().mockResolvedValue({ data: undefined }),
    delete: vi.fn().mockResolvedValue({ data: undefined }),
  },
  authApi: { trainerLogin: vi.fn(), join: vi.fn() },
  errMsg: (_e: unknown, fallback = 'Fehler.') => fallback,
}))

import { api } from '@/lib/api'

// Kleiner Router für api.get: Tests registrieren nur, was die jeweilige Seite
// wirklich lädt (fetch-Wrapper antwortet immer mit { data }).
function mockGet(routes: Record<string, unknown>) {
  vi.mocked(api.get).mockImplementation((url: string) => {
    for (const [pattern, data] of Object.entries(routes)) {
      if (url === pattern) return Promise.resolve({ data })
    }
    return Promise.reject(new Error(`kein Mock für ${url}`))
  })
}

function mockGetError(url: string) {
  vi.mocked(api.get).mockImplementation((requested: string) =>
    requested === url ? Promise.reject(new Error('Netzwerkfehler')) : Promise.reject(new Error(`kein Mock für ${requested}`)))
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  useAuthStore.setState({ token: null, role: null, displayName: null })
  localStorage.clear()
  sessionStorage.clear()
})

describe('Seiten-Smoke-Tests', () => {
  it('LandingPage rendert den Workshop-Katalog aus Fake-Daten', async () => {
    mockGet({
      '/workshops': [
        { key: 'network', title: { de: 'Netzwerk-Grundlagen', en: 'Networking Basics' }, theme: 'network', sections: [] },
      ],
    })

    renderWithProviders(<LandingPage />)

    expect(await screen.findByText('Netzwerk-Grundlagen')).toBeTruthy()
  })

  it('WorkshopPage rendert das Beitritts-Formular', async () => {
    mockGet({
      '/workshops/network': {
        key: 'network', title: { de: 'Netzwerk-Grundlagen', en: 'Networking Basics' }, theme: 'network',
        sections: [], modules: [{ key: 'm1', title: { de: 'Modul Eins', en: 'Module One' }, order: 1 }],
      },
    })

    renderWithProviders(<WorkshopPage />, { route: '/workshops/network', path: '/workshops/:key' })

    expect(await screen.findByLabelText(/Kurs-Code/)).toBeTruthy()
    expect(screen.getByLabelText(/Dein Name/)).toBeTruthy()
  })

  it('LearnPage rendert die Modulliste aus Fake-Daten', async () => {
    useAuthStore.setState({ token: 'demo', role: 'participant', displayName: 'Test' })
    mockGet({
      '/me': { name: 'Test', participant_id: 1, course_id: 9, language: 'de', course: { id: 9, name: 'Kurs' }, workshop: null, progress: [] },
      '/modules': [{ key: 'm1', title: 'Modul Eins', title_en: 'Module One', order: 1, prerequisites: [] }],
    })

    renderWithProviders(<LearnPage />)

    // Der Modultitel taucht sowohl in der "Hier weitermachen"-Kachel als auch
    // in der Modulliste auf — deshalb auf mindestens ein Vorkommen prüfen.
    expect((await screen.findAllByText('Modul Eins')).length).toBeGreaterThan(0)
  })

  it('ModulePage rendert die Blöcke des Moduls', async () => {
    useAuthStore.setState({ token: 'demo', role: 'participant', displayName: 'Test' })
    mockGet({
      '/me': { name: 'Test', participant_id: 1, course_id: 9, language: 'de', course: { id: 9, name: 'Kurs' }, workshop: null, progress: [] },
      '/modules/m1': {
        key: 'm1', title: 'Modul Eins', order: 1, prerequisites: [],
        blocks: [{ type: 'text', value: 'Hallo Blockinhalt' }], quiz: { questions: [] },
      },
      '/modules': [{ key: 'm1', title: 'Modul Eins', title_en: 'Module One', order: 1, prerequisites: [] }],
      '/features': { comments: false },
    })

    renderWithProviders(<ModulePage />, { route: '/lernen/m1', path: '/lernen/:key' })

    expect(await screen.findByText('Hallo Blockinhalt')).toBeTruthy()
  })

  it('zeigt bei einem Ladefehler LoadError statt eines Dauerskeletons', async () => {
    mockGetError('/workshops/network')

    renderWithProviders(<WorkshopPage />, { route: '/workshops/network', path: '/workshops/:key' })

    expect(await screen.findByText('Konnte nicht geladen werden')).toBeTruthy()
  })
})
