// @vitest-environment jsdom
//
// Live-Abstimmung: Teilnehmer-Einblendung (Dialog, Abstimmen, Minimieren,
// Auflösung) und die Trainer-Anzeige im Beamer-Modus.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen, waitFor } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { ParticipantPoll } from '@/components/LivePoll'
import { TrainerPresentPage } from '@/pages/TrainerPresentPage'
import { useAuthStore } from '@/store/auth'
import type { LivePoll } from '@/types'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn(), put: vi.fn(() => Promise.resolve({ data: null })), patch: vi.fn(), delete: vi.fn() },
  errMsg: (_e: unknown, fallback: string) => fallback,
}))

import { api } from '@/lib/api'

function mockGet(routes: Record<string, unknown>) {
  vi.mocked(api.get).mockImplementation((url: string) =>
    url in routes ? Promise.resolve({ data: routes[url] }) : Promise.reject(new Error(`kein Mock für ${url}`)))
}

const OPEN: LivePoll = { id: 5, status: 'open', prompt: 'Welches Gerät trennt VLANs?', options: ['Hub', 'Switch', 'Repeater'], my_choice: null }
const REVEALED: LivePoll = { ...OPEN, status: 'revealed', my_choice: 0, counts: [1, 3, 0], votes: 4, answer: 1, explanation: 'Der Switch taggt die Frames.' }

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  useAuthStore.setState({ token: null, role: null, displayName: null })
})

describe('ParticipantPoll', () => {
  const renderPoll = () => renderWithProviders(
    <div className="workbench"><div data-testid="hintergrund"><button>Modulinhalt</button></div><ParticipantPoll moduleKey="m1" lang="de" /></div>)

  it('blendet die Frage als Dialog ein, stimmt ab und lässt sich minimieren und wieder aufrufen', async () => {
    mockGet({ '/modules/m1/poll': OPEN })
    vi.mocked(api.post).mockResolvedValue({ data: { ok: true, my_choice: 1 } })
    renderPoll()

    const dialog = await screen.findByRole('dialog')
    expect(dialog.getAttribute('aria-modal')).toBe('true')
    expect(screen.getByRole('heading', { name: OPEN.prompt })).toBeTruthy()
    // feste Reihenfolge mit Buchstaben, vor der Auflösung weder Balken noch Lösung
    expect(screen.getAllByRole('button', { pressed: false }).map((b) => b.textContent)).toEqual(['AA:Hub', 'BB:Switch', 'CC:Repeater'])
    expect(screen.queryByTestId('poll-bar')).toBeNull()
    expect(screen.queryByText('Richtige Antwort')).toBeNull()
    // Hintergrund gesperrt, Fokus liegt auf der Karte (nicht auf einer Option)
    expect(screen.getByTestId('hintergrund').hasAttribute('inert')).toBe(true)
    expect(dialog.contains(document.activeElement)).toBe(true)
    expect(document.activeElement?.tagName).toBe('DIV')

    fireEvent.click(screen.getByRole('button', { name: /Switch/ }))
    await waitFor(() => expect(api.post).toHaveBeenCalledWith('/modules/m1/poll/vote', { poll_id: 5, choice: 1 }))
    await waitFor(() => expect(screen.getByRole('button', { name: /Switch/ }).getAttribute('aria-pressed')).toBe('true'))
    expect(screen.getByRole('status').textContent).toContain('Stimme gezählt')

    // Escape minimiert zum Chip statt die Frage zu verlieren
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(screen.queryByRole('dialog')).toBeNull()
    expect(screen.getByTestId('hintergrund').hasAttribute('inert')).toBe(false)
    fireEvent.click(screen.getByRole('button', { name: 'Live-Abstimmung läuft' }))
    expect(screen.getByRole('dialog')).toBeTruthy()
  })

  it('zeigt nach der Auflösung richtig/falsch, Erklärung und Verteilung — ohne Abstimm-Knöpfe', async () => {
    mockGet({ '/modules/m1/poll': REVEALED })
    renderPoll()

    expect((await screen.findByRole('status')).textContent).toContain('Leider falsch.')
    expect(screen.getByRole('status').textContent).toContain('4 Stimmen')
    expect(screen.getByText('Der Switch taggt die Frames.')).toBeTruthy()
    expect(screen.getByText('Richtige Antwort')).toBeTruthy()
    expect(screen.getByText('Deine Wahl')).toBeTruthy()
    expect(screen.getAllByTestId('poll-bar').map((bar) => bar.style.width)).toEqual(['25%', '75%', '0%'])
    expect(screen.queryByRole('button', { name: /Switch/ })).toBeNull()
  })

  it('rendert nichts, solange keine Abstimmung läuft', async () => {
    mockGet({ '/modules/m1/poll': null })
    renderPoll()
    await waitFor(() => expect(api.get).toHaveBeenCalledWith('/modules/m1/poll'))
    expect(screen.queryByRole('dialog')).toBeNull()
    expect(screen.getByTestId('hintergrund').hasAttribute('inert')).toBe(false)
  })
})

describe('TrainerPresentPage — Live-Abstimmung', () => {
  const MODULE = {
    key: 'm1', title: 'Modul Eins', order: 1, prerequisites: [], workshop_key: 'network',
    blocks: [{ type: 'check', uid: 'check-1', prompt: OPEN.prompt, options: OPEN.options, answer: 1 }],
    quiz: { questions: [
      { id: '11', type: 'single', prompt: 'Quizfrage Eins', options: ['x', 'y'], answer: 0 },
      { id: '12', type: 'number', prompt: 'Zahlenfrage', answer: 4 },
    ] },
  }
  const TRAINER_POLL: LivePoll = { ...OPEN, my_choice: undefined, counts: [1, 2, 0], votes: 3, answer: 1, explanation: 'Der Switch taggt die Frames.' }
  const routes = {
    '/trainer/modules/m1': MODULE,
    '/trainer/modules': [{ key: 'm1', title: 'Modul Eins', title_en: 'One', order: 1, prerequisites: [], workshop_key: 'network' }],
    '/courses': [{ id: 7, name: 'Kurs Sieben', join_code: 'ABC', workshop_key: 'network' }],
    '/trainer/courses/7/poll': null,
  }
  const renderPage = (query = '') => {
    useAuthStore.setState({ token: 'demo', role: 'trainer', displayName: 'T' })
    mockGet(routes)
    return renderWithProviders(<TrainerPresentPage />, { route: `/trainer/modul/m1/praesentieren${query}`, path: '/trainer/modul/:key/praesentieren' })
  }

  it('ohne Kurs: Präsentation wie bisher, kein Abstimmungs-Knopf', async () => {
    renderPage()
    fireEvent.click(await screen.findByRole('button', { name: /weiter/ }))
    expect(screen.getByText('2 / 2')).toBeTruthy()
    expect(screen.queryByRole('button', { name: 'Abstimmung starten' })).toBeNull()
    expect(screen.queryByLabelText('Quizfrage zur Abstimmung stellen')).toBeNull()
    expect(screen.getByLabelText('Kurs für Live-Abstimmung')).toBeTruthy()
    expect(api.get).not.toHaveBeenCalledWith('/trainer/courses/7/poll')
  })

  it('mit Kurs: startet zur check-Folie, zeigt Balken, löst auf und beendet; Tasten blättern währenddessen nicht', async () => {
    vi.mocked(api.post).mockImplementation((url: string) =>
      Promise.resolve({ data: url.endsWith('/reveal') ? { ...TRAINER_POLL, status: 'revealed' } : TRAINER_POLL }))
    vi.mocked(api.delete).mockResolvedValue({ data: { ok: true } })
    renderPage('?kurs=7')

    fireEvent.click(await screen.findByRole('button', { name: /weiter/ }))
    // nur Single-Choice-Quizfragen stehen zur Wahl
    const quiz = screen.getByLabelText('Quizfrage zur Abstimmung stellen')
    expect([...quiz.querySelectorAll('option')].map((o) => o.textContent)).toEqual(['Quizfrage abstimmen …', '1. Quizfrage Eins'])

    fireEvent.click(screen.getByRole('button', { name: 'Abstimmung starten' }))
    await waitFor(() => expect(api.post).toHaveBeenCalledWith('/trainer/courses/7/poll', { module_key: 'm1', source: 'check', ref: 'check-1' }))
    expect(await screen.findByRole('heading', { name: OPEN.prompt })).toBeTruthy()
    expect(screen.getByTestId('poll-votes').textContent).toBe('3 Stimmen')
    expect(screen.getAllByTestId('poll-bar').map((bar) => bar.style.width)).toEqual(['33%', '67%', '0%'])
    expect(screen.getByText(/Kurs Sieben/)).toBeTruthy()
    // Lösung und Erklärung bleiben bis zum Auflösen vom Beamer fern
    expect(screen.queryByText('Richtige Antwort')).toBeNull()
    expect(screen.queryByText('Der Switch taggt die Frames.')).toBeNull()

    // Folien-Tasten kollidieren nicht: Abstimmung bleibt stehen
    fireEvent.keyDown(window, { key: 'ArrowLeft' })
    fireEvent.keyDown(window, { key: 'Escape' })
    expect(screen.getByRole('heading', { name: OPEN.prompt })).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: 'Auflösen' }))
    expect(await screen.findByText('Richtige Antwort')).toBeTruthy()
    expect(api.post).toHaveBeenCalledWith('/trainer/courses/7/poll/reveal')
    expect(screen.getByText('Der Switch taggt die Frames.')).toBeTruthy()
    expect(screen.queryByRole('button', { name: 'Auflösen' })).toBeNull()

    fireEvent.click(screen.getByRole('button', { name: 'Abstimmung beenden' }))
    expect(await screen.findByText('2 / 2')).toBeTruthy()  // zurück auf derselben Folie
    expect(api.delete).toHaveBeenCalledWith('/trainer/courses/7/poll')
  })

  it('mit Kurs: „Folgt mir“ teilt Modul und Block je Folie; abschalten löscht den Stand', async () => {
    vi.mocked(api.delete).mockResolvedValue({ data: { ok: true } })
    renderPage('?kurs=7')
    await waitFor(() => expect(api.put).toHaveBeenCalledWith('/trainer/courses/7/follow', { module_key: 'm1', block_uid: null }))
    fireEvent.click(await screen.findByRole('button', { name: /weiter/ }))
    await waitFor(() => expect(api.put).toHaveBeenCalledWith('/trainer/courses/7/follow', { module_key: 'm1', block_uid: 'check-1' }))

    fireEvent.click(screen.getByRole('checkbox', { name: 'Meine Position teilen („Folgt mir“)' }))
    await waitFor(() => expect(api.delete).toHaveBeenCalledWith('/trainer/courses/7/follow'))
    vi.mocked(api.put).mockClear()
    fireEvent.click(screen.getByRole('button', { name: /zurück/ }))
    expect(screen.getByText('1 / 2')).toBeTruthy()
    expect(api.put).not.toHaveBeenCalled()  // abgeschaltet: Folienwechsel teilt nichts mehr
  })

  it('mit Kurs: eine Quizfrage lässt sich über die Auswahl zur Abstimmung stellen', async () => {
    vi.mocked(api.post).mockResolvedValue({ data: TRAINER_POLL })
    renderPage('?kurs=7')
    fireEvent.change(await screen.findByLabelText('Quizfrage zur Abstimmung stellen'), { target: { value: '11' } })
    await waitFor(() => expect(api.post).toHaveBeenCalledWith('/trainer/courses/7/poll', { module_key: 'm1', source: 'quiz', ref: '11' }))
  })
})
