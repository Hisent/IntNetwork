// @vitest-environment jsdom
//
// Abstimmungsarten: Mehrfachauswahl, Skala, Freitext, Wortwolke — Teilnehmer-Dialog
// (beide Sprachen) und Beamer (eigene Abstimmung anlegen, Freitext moderieren).
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen, waitFor, within } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { ParticipantPoll } from '@/components/LivePoll'
import { TrainerPresentPage } from '@/pages/TrainerPresentPage'
import { useAuthStore } from '@/store/auth'
import type { LivePoll } from '@/types'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn(), put: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  errMsg: (_e: unknown, fallback: string) => fallback,
}))

import { api } from '@/lib/api'

function mockGet(routes: Record<string, unknown>) {
  vi.mocked(api.get).mockImplementation((url: string) =>
    url in routes ? Promise.resolve({ data: routes[url] }) : Promise.reject(new Error(`kein Mock für ${url}`)))
}
const echoVote = () => vi.mocked(api.post).mockImplementation((_url: string, body?: unknown) =>
  Promise.resolve({ data: { ok: true, my_choice: (body as { choice: unknown }).choice } }))

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  useAuthStore.setState({ token: null, role: null, displayName: null })
})

const renderPoll = (poll: LivePoll, lang: 'de' | 'en' = 'de') => {
  mockGet({ '/modules/m1/poll': poll })
  return renderWithProviders(<div className="workbench"><ParticipantPoll moduleKey="m1" lang={lang} /></div>)
}
const base = { id: 9, status: 'open' as const, prompt: 'Frage?', my_choice: null }

describe('ParticipantPoll — Abstimmungsarten', () => {
  it('Mehrfachauswahl: schaltet Antworten um und sperrt ab der Höchstzahl', async () => {
    echoVote()
    renderPoll({ ...base, kind: 'multi', options: ['TCP', 'UDP', 'ICMP'], max_selections: 2 })
    expect((await screen.findByRole('status')).textContent).toBe('Wähle bis zu 2 Antworten.')
    fireEvent.click(screen.getByRole('button', { name: /UDP/ }))
    await waitFor(() => expect(api.post).toHaveBeenLastCalledWith('/modules/m1/poll/vote', { poll_id: 9, choice: [1] }))
    fireEvent.click(screen.getByRole('button', { name: /TCP/ }))
    await waitFor(() => expect(api.post).toHaveBeenLastCalledWith('/modules/m1/poll/vote', { poll_id: 9, choice: [0, 1] }))
    await waitFor(() => expect((screen.getByRole('button', { name: /ICMP/ }) as HTMLButtonElement).disabled).toBe(true))
    expect(screen.getAllByRole('button', { pressed: true })).toHaveLength(2)
    fireEvent.click(screen.getByRole('button', { name: /TCP/ }))  // abwählen gibt wieder frei
    await waitFor(() => expect(api.post).toHaveBeenLastCalledWith('/modules/m1/poll/vote', { poll_id: 9, choice: [1] }))
    fireEvent.click(screen.getByRole('button', { name: /UDP/ }))  // die letzte bleibt
    expect(api.post).toHaveBeenCalledTimes(3)
  })

  it('Mehrfachauswahl-Quizfrage: richtig nur bei genau der Lösungsmenge', async () => {
    renderPoll({ ...base, kind: 'multi', status: 'revealed', options: ['a', 'b', 'c'], my_choice: [2, 0], answer: [0, 2], counts: [1, 0, 1], votes: 1 })
    expect((await screen.findByRole('status')).textContent).toContain('Richtig!')
    expect(screen.getAllByText('Richtige Antwort')).toHaveLength(2)
  })

  it('Skala: Werte mit Endbeschriftung, danach Verteilung und Mittelwert', async () => {
    echoVote()
    const scale = { ...base, kind: 'scale' as const, min: 1, max: 5, label_min: 'gar nicht', label_max: 'sehr' }
    renderPoll(scale)
    fireEvent.click(await screen.findByRole('button', { name: '5 – sehr' }))
    await waitFor(() => expect(api.post).toHaveBeenCalledWith('/modules/m1/poll/vote', { poll_id: 9, choice: 5 }))
    expect(screen.getAllByRole('button', { name: /^[1-5]/ })).toHaveLength(5)
    cleanup()
    renderPoll({ ...scale, status: 'revealed', my_choice: 4, counts: [0, 1, 0, 2, 1], votes: 4, mean: 3.75 })
    expect((await screen.findByTestId('poll-mean')).textContent).toBe('Mittelwert: 3,75')
    expect(screen.getAllByTestId('poll-bar').map((b) => b.style.height)).toEqual(['0%', '50%', '0%', '100%', '50%'])
    expect(screen.getByText('Wert 4: 2')).toBeTruthy()
    expect(screen.getByRole('status').textContent).toContain('Danke fürs Mitmachen!')
  })

  it('Freitext: Zeichenzähler, Senden, danach nur sichtbare Antworten', async () => {
    echoVote()
    renderPoll({ ...base, kind: 'text' })
    const box = await screen.findByLabelText('Deine Antwort')
    expect(box.getAttribute('maxLength')).toBe('280')
    expect((screen.getByRole('button', { name: 'Senden' }) as HTMLButtonElement).disabled).toBe(true)
    fireEvent.change(box, { target: { value: '  Trunks verstehen ' } })
    expect(screen.getByText('19 / 280')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Senden' }))
    await waitFor(() => expect(api.post).toHaveBeenCalledWith('/modules/m1/poll/vote', { poll_id: 9, choice: 'Trunks verstehen' }))
    expect((await screen.findByRole('status')).textContent).toContain('Gespeichert.')
    cleanup()
    renderPoll({ ...base, kind: 'text', status: 'revealed', my_choice: 'Meins', answers: [{ text: 'Meins' }, { text: 'Anderes' }], votes: 3 })
    const list = await screen.findByRole('list')
    expect(within(list).getAllByRole('listitem').map((li) => li.textContent)).toEqual(['Meins', 'Anderes'])
    expect(screen.queryByRole('button', { name: /Ausblenden/ })).toBeNull()
  })

  it('Wortwolke (englisch): bis zu drei Wörter, Wolke mit Textliste für Screenreader', async () => {
    echoVote()
    renderPoll({ ...base, kind: 'words' }, 'en')
    expect((await screen.findByRole('status')).textContent).toBe('Name one to three words.')
    fireEvent.change(screen.getByLabelText('Word 1'), { target: { value: 'VLAN' } })
    fireEvent.change(screen.getByLabelText('Word 3'), { target: { value: ' trunk ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send' }))
    await waitFor(() => expect(api.post).toHaveBeenCalledWith('/modules/m1/poll/vote', { poll_id: 9, choice: ['VLAN', 'trunk'] }))
    cleanup()
    const words = [{ word: 'trunk', count: 4 }, { word: 'tag', count: 2 }, { word: 'acl', count: 1 }]
    renderPoll({ ...base, kind: 'words', status: 'revealed', words, votes: 5 }, 'en')
    const cloud = await screen.findByTestId('word-cloud')
    expect(cloud.getAttribute('aria-hidden')).toBe('true')
    const items = [...cloud.querySelectorAll('li')]
    expect(items.map((li) => li.textContent)).toEqual(['tag', 'trunk', 'acl'])  // häufigstes in der Mitte
    const size = (w: string) => parseFloat(items.find((li) => li.textContent === w)!.style.fontSize)
    expect(size('trunk')).toBeGreaterThan(size('tag'))
    expect(size('tag')).toBeGreaterThan(size('acl'))
    expect(screen.getByText('trunk: 4')).toBeTruthy()
    expect(screen.getByText('Word cloud')).toBeTruthy()
  })
})

describe('TrainerPresentPage — eigene Abstimmung', () => {
  const MODULE = {
    key: 'm1', title: 'Modul Eins', order: 1, prerequisites: [], workshop_key: 'network',
    blocks: [{ type: 'text', value: 'Hallo' }],
    quiz: { questions: [{ id: '21', type: 'multi', prompt: 'Mehrere', options: ['x', 'y'], answer: [0, 1] }] },
  }
  const renderPage = (poll: LivePoll | null = null) => {
    useAuthStore.setState({ token: 'demo', role: 'trainer', displayName: 'T' })
    mockGet({
      '/trainer/modules/m1': MODULE,
      '/trainer/modules': [{ key: 'm1', title: 'Modul Eins', title_en: 'One', order: 1, prerequisites: [], workshop_key: 'network' }],
      '/courses': [{ id: 7, name: 'Kurs Sieben', join_code: 'ABC', workshop_key: 'network' }],
      '/trainer/courses/7/poll': poll,
    })
    return renderWithProviders(<TrainerPresentPage />, { route: '/trainer/modul/m1/praesentieren?kurs=7', path: '/trainer/modul/:key/praesentieren' })
  }

  it('legt eine Skala an; Esc schließt nur das Formular; Multi-Quizfragen stehen zur Wahl', async () => {
    vi.mocked(api.post).mockResolvedValue({ data: { ...base, kind: 'scale', min: 0, max: 10, counts: Array(11).fill(0), votes: 0, mean: null } })
    renderPage()
    const quiz = await screen.findByLabelText('Quizfrage zur Abstimmung stellen')
    expect([...quiz.querySelectorAll('option')].map((o) => o.textContent)).toContain('1. Mehrere (Mehrfachauswahl)')

    fireEvent.click(screen.getByRole('button', { name: 'Eigene Abstimmung …' }))
    fireEvent.keyDown(window, { key: 'Escape' })
    expect(screen.queryByRole('form')).toBeNull()
    expect(screen.getByText('1 / 2')).toBeTruthy()  // Präsentation läuft weiter

    fireEvent.click(screen.getByRole('button', { name: 'Eigene Abstimmung …' }))
    const form = screen.getByRole('form', { name: 'Eigene Abstimmung' })
    expect((within(form).getByRole('button', { name: 'Abstimmung starten' }) as HTMLButtonElement).disabled).toBe(true)
    fireEvent.click(within(form).getByLabelText('Skala'))
    fireEvent.change(within(form).getByLabelText('Frage'), { target: { value: ' Wie sicher? ' } })
    fireEvent.change(within(form).getByLabelText('Von'), { target: { value: '0' } })
    fireEvent.change(within(form).getByLabelText('Bis'), { target: { value: '10' } })
    fireEvent.change(within(form).getByLabelText('Beschriftung oben (optional)'), { target: { value: 'sehr' } })
    fireEvent.click(within(form).getByRole('button', { name: 'Abstimmung starten' }))
    await waitFor(() => expect(api.post).toHaveBeenCalledWith('/trainer/courses/7/poll', {
      module_key: 'm1', source: 'adhoc', kind: 'scale', prompt: 'Wie sicher?', min: 0, max: 10, label_min: '', label_max: 'sehr' }))
    expect(await screen.findByRole('heading', { name: 'Frage?' })).toBeTruthy()
    expect(screen.getAllByTestId('poll-bar')).toHaveLength(11)
  })

  it('Mehrfachauswahl braucht zwei Antworten; Höchstzahl ist optional', async () => {
    vi.mocked(api.post).mockResolvedValue({ data: { ...base, kind: 'multi', options: ['a', 'b'], counts: [0, 0], votes: 0 } })
    renderPage()
    fireEvent.click(await screen.findByRole('button', { name: 'Eigene Abstimmung …' }))
    const form = screen.getByRole('form', { name: 'Eigene Abstimmung' })
    fireEvent.change(within(form).getByLabelText('Frage'), { target: { value: 'Welche?' } })
    const options = within(form).getByLabelText('Antworten (eine je Zeile, 2 bis 10)')
    fireEvent.change(options, { target: { value: 'a\n\n' } })
    expect((within(form).getByRole('button', { name: 'Abstimmung starten' }) as HTMLButtonElement).disabled).toBe(true)
    fireEvent.change(options, { target: { value: 'a\n b \n' } })
    fireEvent.click(within(form).getByRole('button', { name: 'Abstimmung starten' }))
    await waitFor(() => expect(api.post).toHaveBeenCalledWith('/trainer/courses/7/poll', {
      module_key: 'm1', source: 'adhoc', kind: 'multi', prompt: 'Welche?', options: ['a', 'b'], max_selections: null }))
  })

  it('Freitext: vor dem Auflösen nur hinter Klick, Ausblenden; ausgeblendete nie groß', async () => {
    const answers = [{ id: 1, text: 'Gut', hidden: false }, { id: 2, text: 'Unpassend', hidden: false }]
    const open: LivePoll = { ...base, kind: 'text', answers, votes: 2 }
    vi.mocked(api.patch).mockResolvedValue({ data: { ...open, answers: [answers[0], { ...answers[1], hidden: true }] } })
    vi.mocked(api.post).mockResolvedValue({ data: { ...open, status: 'revealed', answers: [answers[0], { ...answers[1], hidden: true }] } })
    renderPage(open)

    const details = (await screen.findByText(/Antworten prüfen \(2\)/)).closest('details')!
    expect(details.open).toBe(false)
    fireEvent.click(within(details).getByRole('button', { name: 'Ausblenden: Unpassend' }))
    await waitFor(() => expect(api.patch).toHaveBeenCalledWith('/trainer/courses/7/poll/answers/2', { hidden: true }))

    fireEvent.click(screen.getByRole('button', { name: 'Auflösen' }))
    const hiddenBox = (await screen.findByText('Ausgeblendete Antworten (1)')).closest('details')!
    expect(screen.getByText('Gut')).toBeTruthy()
    expect(within(hiddenBox).getByRole('button', { name: 'Einblenden: Unpassend' })).toBeTruthy()
    // „Unpassend“ steht nur in der eingeklappten Liste
    expect(screen.getAllByText('Unpassend').every((el) => hiddenBox.contains(el))).toBe(true)
  })
})
