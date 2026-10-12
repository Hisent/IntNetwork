// @vitest-environment jsdom
//
// Schlanke Render-Smoke-Suite: die wichtigsten Teilnehmer-Seiten mit
// gemocktem API-Layer (@/lib/api) rendern und je eine zentrale Aussage
// prüfen. Kein E2E, kein echter Server — nur "rendert es überhaupt sinnvoll".
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen } from '@testing-library/react'
import { Link } from 'react-router-dom'
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

import { api, authApi } from '@/lib/api'

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

// jsdom kennt scrollTo nicht (ModulePage scrollt beim Modulwechsel nach oben).
window.scrollTo = vi.fn()

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

  it('ModulePage trägt Modul-Zustand (Reflexion) nicht in ein anderes, bereits geladenes Modul', async () => {
    useAuthStore.setState({ token: 'demo', role: 'participant', displayName: 'Test' })
    const module = (key: string) => ({
      key, title: `Modul ${key}`, order: 1, prerequisites: [],
      blocks: [{ type: 'reflect', prompt: `Frage ${key}` }], quiz: { questions: [] },
    })
    mockGet({
      '/me': { name: 'Test', participant_id: 1, course_id: 9, language: 'de', course: { id: 9, name: 'Kurs' }, workshop: null, progress: [] },
      '/modules/m1': module('m1'),
      '/modules/m2': module('m2'),
      '/modules': [],
      '/features': { comments: false },
    })

    renderWithProviders(
      <><ModulePage /><Link to="/lernen/m1">zu-m1</Link><Link to="/lernen/m2">zu-m2</Link></>,
      { route: '/lernen/m1', path: '/lernen/:key' })

    fireEvent.change(await screen.findByLabelText('Frage m1'), { target: { value: 'Notiz A' } })
    fireEvent.click(screen.getByText('zu-m2'))
    fireEvent.change(await screen.findByLabelText('Frage m2'), { target: { value: 'Notiz B' } })
    // m1 liegt jetzt im Query-Cache -> kein Skeleton dazwischen, der den Zustand zufällig räumt.
    fireEvent.click(screen.getByText('zu-m1'))

    expect((await screen.findByLabelText<HTMLTextAreaElement>('Frage m1')).value).toBe('Notiz A')
    expect(localStorage.getItem('intnetwork-reflect-1-9-m2-0')).toBe('Notiz B')
  })

  it('ModulePage meldet Präsenz nur im sichtbaren Tab und sofort bei Rückkehr', async () => {
    useAuthStore.setState({ token: 'demo', role: 'participant', displayName: 'Ada' })
    mockGet({})
    const hidden = vi.spyOn(document, 'hidden', 'get').mockReturnValue(true)
    renderWithProviders(<ModulePage />, { route: '/lernen/m1', path: '/lernen/:key' })
    expect(api.post).not.toHaveBeenCalledWith('/modules/m1/heartbeat')

    hidden.mockReturnValue(false)
    document.dispatchEvent(new Event('visibilitychange'))
    expect(api.post).toHaveBeenCalledWith('/modules/m1/heartbeat')
    hidden.mockRestore()
  })

  it('ModulePage leitet ohne Teilnehmer-Sitzung zur Startseite um', () => {
    renderWithProviders(<ModulePage />, { route: '/lernen/m1', path: '/lernen/:key' })
    expect(screen.queryByText('Konnte nicht geladen werden')).toBeNull()
    expect(api.get).not.toHaveBeenCalled()
  })

  it('zeigt bei einem Ladefehler LoadError statt eines Dauerskeletons', async () => {
    mockGetError('/workshops/network')

    renderWithProviders(<WorkshopPage />, { route: '/workshops/network', path: '/workshops/:key' })

    expect(await screen.findByText('Konnte nicht geladen werden')).toBeTruthy()
  })

  it('WorkshopPage deaktiviert den Beitreten-Button während des Requests', async () => {
    mockGet({
      '/workshops/network': {
        key: 'network', title: { de: 'Netzwerk-Grundlagen', en: 'Networking Basics' }, theme: 'network',
        sections: [], modules: [{ key: 'm1', title: { de: 'Modul Eins', en: 'Module One' }, order: 1 }],
      },
    })
    let resolveJoin: (value: { data: { access_token: string; course_name: string; name: string; resume_code: string | null } }) => void = () => {}
    vi.mocked(authApi.join).mockImplementation(() => new Promise((resolve) => { resolveJoin = resolve }))

    renderWithProviders(<WorkshopPage />, { route: '/workshops/network', path: '/workshops/:key' })

    fireEvent.change(await screen.findByLabelText(/Kurs-Code/), { target: { value: 'ABC123' } })
    fireEvent.change(screen.getByLabelText(/Dein Name/), { target: { value: 'Test' } })
    fireEvent.click(screen.getByRole('button', { name: /Workshop starten/ }))

    const busyButton = await screen.findByRole('button', { name: /Wird gestartet/ })
    expect((busyButton as HTMLButtonElement).disabled).toBe(true)

    resolveJoin({ data: { access_token: 'tok', course_name: 'Kurs', name: 'Test', resume_code: null } })
  })
})
