// @vitest-environment jsdom
//
// Sprachwechsel mitten im Modul: die Ansicht bleibt stehen (kein Lade-Skelett ->
// kein Sprung an den Seitenanfang), angeklickte Quizantworten bleiben, das Modul
// wird genau einmal neu geholt.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen, waitFor } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { useAuthStore } from '@/store/auth'
import { ModulePage } from '@/pages/ModulePage'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn().mockResolvedValue({ data: undefined }), put: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  authApi: {},
  errMsg: (_e: unknown, fallback = 'Fehler.') => fallback,
}))
import { api } from '@/lib/api'

window.scrollTo = vi.fn()
window.scrollBy = vi.fn()

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  useAuthStore.setState({ token: null, role: null, displayName: null })
  localStorage.clear()
})

describe('ModulePage: Sprachwechsel', () => {
  it('behält Ansicht und Quiz-Auswahl und lädt das Modul nur einmal nach', async () => {
    useAuthStore.setState({ token: 'demo', role: 'participant', displayName: 'Test' })
    let language: 'de' | 'en' = 'de'
    const moduleFor = (lang: 'de' | 'en') => ({
      key: 'm1', title: lang === 'de' ? 'Modul Eins' : 'Module One', order: 1, prerequisites: [],
      blocks: [{ uid: 't1', type: 'text', value: lang === 'de' ? 'Hallo Inhalt' : 'Hello content' }],
      quiz: { questions: [{ id: 'q1', type: 'single', prompt: lang === 'de' ? 'Frage?' : 'Question?', options: lang === 'de' ? ['ja', 'nein'] : ['yes', 'no'] }] },
    })
    let skeletons = 0
    vi.mocked(api.get).mockImplementation((url: string) => {
      if (url === '/me') return Promise.resolve({ data: { name: 'Test', participant_id: 1, course_id: 9, language, course: { id: 9, name: 'Kurs' }, workshop: null, progress: [] } })
      if (url === '/modules/m1') return Promise.resolve({ data: moduleFor(language) })
      if (url === '/modules') return Promise.resolve({ data: [] })
      if (url === '/features') return Promise.resolve({ data: { comments: false } })
      return Promise.reject(new Error(`kein Mock für ${url}`))
    })
    vi.mocked(api.patch).mockImplementation((_url: string, body?: unknown) => {
      language = (body as { language: 'de' | 'en' }).language
      return Promise.resolve({ data: { language } })
    })
    const moduleCalls = () => vi.mocked(api.get).mock.calls.filter(([url]) => url === '/modules/m1').length

    const { container } = renderWithProviders(<ModulePage />, { route: '/lernen/m1', path: '/lernen/:key' })
    const observer = new MutationObserver(() => { if (container.querySelector('[aria-busy="true"]')) skeletons++ })
    expect(await screen.findByText('Hallo Inhalt')).toBeTruthy()
    observer.observe(container, { childList: true, subtree: true })
    fireEvent.click(screen.getByLabelText('nein'))
    expect(moduleCalls()).toBe(1)

    fireEvent.click(screen.getAllByRole('button', { name: 'en' })[0])
    expect(await screen.findByText('Hello content')).toBeTruthy()
    observer.disconnect()

    expect(skeletons).toBe(0)
    expect((screen.getByLabelText('no') as HTMLInputElement).checked).toBe(true)
    await waitFor(() => expect(vi.mocked(api.get).mock.calls.filter(([url]) => url === '/me').length).toBe(2))
    expect(moduleCalls()).toBe(2)
  })
})
