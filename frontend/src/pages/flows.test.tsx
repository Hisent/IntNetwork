// @vitest-environment jsdom
//
// Regressionstests zu Befunden aus dem Ende-zu-Ende-Test: sprachrichtiger
// Modultitel, 404 ≠ Verbindungsfehler, Hinweis nach erzwungenem Abmelden,
// gekennzeichnete Suchtreffer/Modulseite bei offener Voraussetzung, ehrliche
// Auswertung im Übungsmodus.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen, waitFor } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { useAuthStore } from '@/store/auth'
import { LandingPage } from '@/pages/LandingPage'
import { ModulePage } from '@/pages/ModulePage'
import { PracticePage } from '@/pages/PracticePage'
import { SearchBox } from '@/components/SearchBox'

vi.mock('@/lib/api', () => ({
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

const httpError = (status: number, detail?: unknown) => Object.assign(new Error(`HTTP ${status}`), { response: { status, data: { detail } } })

function mockGet(routes: Record<string, unknown>) {
  vi.mocked(api.get).mockImplementation((url: string) => {
    if (!(url in routes)) return Promise.reject(new Error(`kein Mock für ${url}`))
    const data = routes[url]
    return data instanceof Error ? Promise.reject(data) : Promise.resolve({ data })
  })
}

const me = (language: 'de' | 'en', progress: unknown[] = []) =>
  ({ name: 'Ada', participant_id: 1, course_id: 9, language, course: { id: 9, name: 'Kurs' }, workshop: null, progress })
const META = [
  { key: 'm1', title: 'Modul Eins', title_en: 'Module One', order: 1, prerequisites: [] },
  { key: 'm2', title: 'Modul Zwei', title_en: 'Module Two', order: 2, prerequisites: ['m1'] },
]
const detail = (extra: object = {}) => ({
  key: 'm2', title: 'Modul Zwei', title_en: 'Module Two', order: 2, prerequisites: ['m1'],
  blocks: [{ type: 'text', value: 'Blockinhalt' }], quiz: { questions: [] }, ...extra,
})

window.scrollTo = vi.fn()

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  useAuthStore.setState({ token: null, role: null, displayName: null, sessionLost: false })
  localStorage.clear()
  sessionStorage.clear()
})

const asParticipant = () => useAuthStore.setState({ token: 'demo', role: 'participant', displayName: 'Ada' })

describe('ModulePage — Titel in der Teilnehmersprache', () => {
  it('zeigt als EN-Teilnehmer title_en in Überschrift, Kopfzeile und Tab-Titel', async () => {
    asParticipant()
    mockGet({ '/me': me('en'), '/modules/m2': detail(), '/modules': META, '/features': { comments: false } })
    renderWithProviders(<ModulePage />, { route: '/lernen/m2', path: '/lernen/:key' })

    expect((await screen.findByRole('heading', { level: 1 })).textContent).toBe('Module Two')
    expect(screen.getByRole('banner').textContent).toContain('Module Two')
    expect(document.title).toBe('Module Two · IntLab')
  })

  it('bleibt ohne title_en beim gelieferten Titel', async () => {
    asParticipant()
    mockGet({ '/me': me('en'), '/modules/m2': detail({ title_en: undefined }), '/modules': META, '/features': { comments: false } })
    renderWithProviders(<ModulePage />, { route: '/lernen/m2', path: '/lernen/:key' })
    expect((await screen.findByRole('heading', { level: 1 })).textContent).toBe('Modul Zwei')
  })
})

describe('ModulePage — 404 ist kein Verbindungsfehler', () => {
  it.each([
    ['ohne maschinenlesbaren Grund', 'Modul nicht gefunden'],
    ['mit strukturiertem detail', { code: 'module_not_in_course', message: 'Modul nicht gefunden' }],
  ])('zeigt eine eigene Meldung mit Link zur Lernseite, ohne Retry und ohne Heartbeat (%s)', async (_name, body) => {
    asParticipant()
    mockGet({ '/me': me('de'), '/modules/weg': httpError(404, body), '/modules': META, '/features': { comments: false } })
    renderWithProviders(<ModulePage />, { route: '/lernen/weg', path: '/lernen/:key' })

    expect(await screen.findByText('Dieses Modul ist nicht verfügbar')).toBeTruthy()
    expect(screen.getByRole('link', { name: 'Zur Lernseite' }).getAttribute('href')).toBe('/lernen')
    expect(screen.queryByText('Konnte nicht geladen werden')).toBeNull()
    expect(screen.queryByRole('button', { name: 'Erneut versuchen' })).toBeNull()
    expect(api.post).not.toHaveBeenCalledWith('/modules/weg/heartbeat')
  })

  it.each([
    ['module_not_enabled', 'in deinem Kurs nicht freigeschaltet'],
    ['module_unknown', 'Dieses Modul gibt es nicht'],
    [undefined, 'nicht freigeschaltet oder existiert nicht'],
  ])('unterscheidet den Grund anhand des Felds code (%s)', async (code, text) => {
    asParticipant()
    const err = Object.assign(new Error('HTTP 404'), { response: { status: 404, data: { detail: 'x', code } } })
    mockGet({ '/me': me('de'), '/modules/weg': err, '/modules': META, '/features': { comments: false } })
    renderWithProviders(<ModulePage />, { route: '/lernen/weg', path: '/lernen/:key' })
    expect((await screen.findByText(new RegExp(text))).tagName).toBe('P')
  })

  it('zeigt bei einem echten Ladefehler weiterhin „Erneut versuchen“', async () => {
    asParticipant()
    mockGet({ '/me': me('de'), '/modules/m2': httpError(500), '/modules': META, '/features': { comments: false } })
    renderWithProviders(<ModulePage />, { route: '/lernen/m2', path: '/lernen/:key' })
    expect(await screen.findByRole('button', { name: 'Erneut versuchen' })).toBeTruthy()
  })
})

describe('Reihenfolge ist Führung, keine Sperre', () => {
  it('ModulePage nennt die offene Voraussetzung mit Link — und schweigt, sobald sie bestanden ist', async () => {
    asParticipant()
    mockGet({ '/me': me('de'), '/modules/m2': detail(), '/modules': META, '/features': { comments: false } })
    const first = renderWithProviders(<ModulePage />, { route: '/lernen/m2', path: '/lernen/:key' })
    const hint = await screen.findByText(/Dieses Modul baut auf/)
    expect(hint.querySelector('a')?.getAttribute('href')).toBe('/lernen/m1')
    first.unmount()

    mockGet({ '/me': me('de', [{ module_key: 'm1', done: true, best: 100 }]), '/modules/m2': detail(), '/modules': META, '/features': { comments: false } })
    renderWithProviders(<ModulePage />, { route: '/lernen/m2', path: '/lernen/:key' })
    await screen.findByText('Blockinhalt')
    expect(screen.queryByText(/Dieses Modul baut auf/)).toBeNull()
  })

  it('SearchBox kennzeichnet Treffer in Modulen mit offener Voraussetzung', async () => {
    mockGet({ '/search?q=vlan': { hits: [
      { module_key: 'm1', module_title: 'Modul Eins', kind: 'text', uid: 'u1', snippet: 'VLAN im ersten Modul' },
      { module_key: 'm2', module_title: 'Modul Zwei', kind: 'text', uid: 'u2', snippet: 'VLAN im zweiten Modul' },
    ], more: false } })
    renderWithProviders(<SearchBox lang="de" modules={META} progress={[]} />)
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'vlan' } })

    const locked = (await screen.findByText('VLAN im zweiten Modul')).closest('a')!
    expect(locked.textContent).toContain('Baut auf „Modul Eins“ auf')
    expect(locked.getAttribute('href')).toBe('/lernen/m2#b-u2')
    expect(screen.getByText('VLAN im ersten Modul').closest('a')!.textContent).not.toContain('Baut auf')
  })
})

describe('Hinweis nach erzwungenem Abmelden', () => {
  it('erscheint einmal auf der Startseite und lässt sich schließen', async () => {
    mockGet({ '/workshops': [] })
    useAuthStore.setState({ sessionLost: true })
    renderWithProviders(<LandingPage />)
    expect(screen.getByText(/Deine Sitzung ist nicht mehr gültig/)).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Hinweis schließen' }))
    expect(screen.queryByText(/Deine Sitzung ist nicht mehr gültig/)).toBeNull()
  })

  it('erscheint nicht ohne erzwungenes Abmelden', () => {
    mockGet({ '/workshops': [] })
    renderWithProviders(<LandingPage />)
    expect(screen.queryByText(/Deine Sitzung ist nicht mehr gültig/)).toBeNull()
  })
})

describe('PracticePage — nur der erste Versuch zählt', () => {
  it('wertet eine erst im zweiten Versuch richtige Antwort nicht als richtig', async () => {
    asParticipant()
    const question = { id: 'q1', type: 'number', prompt: 'Wie viele Bits hat IPv4?', module_key: 'm1', module_title: 'Modul Eins' }
    mockGet({ '/me': me('de'), '/practice?mode=mixed': { questions: [question], wrong_total: 0 } })
    vi.mocked(api.post)
      .mockResolvedValueOnce({ data: { correct: false, explanation: null } })
      .mockResolvedValueOnce({ data: { correct: true, explanation: null } })
    renderWithProviders(<PracticePage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Gemischtes Üben' }))
    const answer = async (value: string) => {
      fireEvent.change(await screen.findByRole('spinbutton'), { target: { value } })
      fireEvent.click(screen.getByRole('button', { name: 'Prüfen' }))
    }
    await answer('16')
    fireEvent.click(await screen.findByRole('button', { name: 'Nochmal' }))
    await answer('32')
    fireEvent.click(await screen.findByRole('button', { name: /Auswertung/ }))

    await waitFor(() => expect(screen.getByText(/0 von 1 im ersten Versuch richtig/)).toBeTruthy())
    // Der „Auswertung“-Knopf verschwindet — der Fokus gehört der Auswertung, nicht <body>.
    expect(document.activeElement).toBe(screen.getByText(/0 von 1 im ersten Versuch richtig/))
  })
})
