// @vitest-environment jsdom
//
// Modul-Editor: ungespeicherte Änderungen überleben einen Hintergrund-Refetch,
// Rückmeldungen (Erfolg, Fehler, Konflikt) stehen beim Speichern-Knopf, und jedes
// Speichern schickt die Version mit, auf der das Formular beruht.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { QueryClient, QueryClientProvider, focusManager } from '@tanstack/react-query'
import { useAuthStore } from '@/store/auth'
import { TrainerModuleEditPage } from '@/pages/TrainerModuleEditPage'
import type { EditorModule } from '@/lib/trainerApi'

vi.mock('@/lib/api', async (original) => ({
  ...(await original<typeof import('@/lib/api')>()),
  api: { get: vi.fn(), post: vi.fn(), put: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))
import { api } from '@/lib/api'

const URL = '/trainer/content/modules/m1'
const server = (over: Partial<EditorModule> = {}): EditorModule => ({
  key: 'm1', workshop_key: 'network', title_de: 'Server-Titel', title_en: 'Server title', order: 1, prerequisites: [],
  goals: [], scenario_de: '', scenario_en: '', quiz: [], has_snapshot: false, has_seed: true, version: 'v1',
  blocks: [
    { uid: 't1', type: 'text', value_de: 'Hallo', value_en: 'Hello' },
    { uid: 'dia-1', type: 'diagram', payload: { kind: 'sequence' } },
  ],
  ...over,
})
const apiError = (status: number, detail: string) => Object.assign(new Error(`HTTP ${status}`), { response: { status, data: { detail } } })

let current: EditorModule
let client: QueryClient
function open() {
  current = server()
  useAuthStore.setState({ token: 'demo', role: 'trainer', displayName: 'T' })
  vi.mocked(api.get).mockImplementation((url: string) =>
    Promise.resolve({ data: url === URL ? current : [] }))
  client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={['/trainer/modul/m1/bearbeiten']}>
        <Routes><Route path="/trainer/modul/:key/bearbeiten" element={<TrainerModuleEditPage />} /></Routes>
      </MemoryRouter>
    </QueryClientProvider>)
}
const title = () => screen.getByLabelText('Titel DE') as HTMLInputElement
const moduleLoads = () => vi.mocked(api.get).mock.calls.filter(([url]) => url === URL).length
const lastPutUrl = () => vi.mocked(api.put).mock.calls.at(-1)![0]

window.confirm = () => true
Element.prototype.scrollIntoView = vi.fn()

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  focusManager.setFocused(undefined)
  useAuthStore.setState({ token: null, role: null, displayName: null })
})

describe('TrainerModuleEditPage', () => {
  it('setzt einen eigenen Tab-Titel mit dem Modultitel', async () => {
    open()
    await screen.findByDisplayValue('Server-Titel')
    expect(document.title).toBe('Server-Titel · Editor · IntLab')
  })

  it('ein Refetch ersetzt ungespeicherte Änderungen nicht; ohne Änderungen wird der Serverstand übernommen', async () => {
    open()
    await screen.findByDisplayValue('Server-Titel')
    current = server({ title_de: 'Von nebenan', version: 'v2' })
    await act(() => client.invalidateQueries({ queryKey: ['content-module', 'm1'] }))
    await waitFor(() => expect(title().value).toBe('Von nebenan'))  // nicht dirty -> übernommen

    fireEvent.change(title(), { target: { value: 'Meine Änderung' } })
    current = server({ title_de: 'Noch neuer', version: 'v3' })
    const loads = moduleLoads()
    await act(() => client.invalidateQueries({ queryKey: ['content-module', 'm1'] }))
    expect(moduleLoads()).toBe(loads + 1)
    await act(() => new Promise((resolve) => setTimeout(resolve, 20)))
    expect(title().value).toBe('Meine Änderung')
  })

  it('lädt bei Rückkehr in den Tab nicht neu, solange ungespeicherte Änderungen bestehen', async () => {
    open()
    await screen.findByDisplayValue('Server-Titel')
    fireEvent.change(title(), { target: { value: 'Meine Änderung' } })
    const before = moduleLoads()
    await act(async () => { focusManager.setFocused(false); focusManager.setFocused(true) })
    expect(moduleLoads()).toBe(before)
    expect(title().value).toBe('Meine Änderung')
  })

  it('meldet den Erfolg beim Speichern-Knopf und speichert danach mit der neuen Version', async () => {
    open()
    await screen.findByDisplayValue('Server-Titel')
    vi.mocked(api.put).mockResolvedValue({ data: { version: 'v2' } })
    fireEvent.change(title(), { target: { value: 'Neu' } })
    fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
    const status = await screen.findByRole('status')
    expect(status.textContent).toContain('Gespeichert')
    expect(status.closest('[data-testid="save-bar"]')!.contains(screen.getByRole('button', { name: 'Speichern' }))).toBe(true)
    expect(lastPutUrl()).toBe(`${URL}?base_version=v1`)

    current = server({ title_de: 'Neu', version: 'v2' })
    fireEvent.change(title(), { target: { value: 'Neu 2' } })
    expect(screen.queryByRole('status')).toBeNull()  // „Gespeichert“ gilt nicht mehr
    fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
    await waitFor(() => expect(lastPutUrl()).toBe(`${URL}?base_version=v2`))
  })

  it('409: Meldung als alert beim Knopf, Formular bleibt, ausdrücklicher Knopf lädt den Serverstand', async () => {
    open()
    await screen.findByDisplayValue('Server-Titel')
    vi.mocked(api.put).mockRejectedValue(apiError(409, 'Inzwischen hat jemand anderes gespeichert.'))
    fireEvent.change(title(), { target: { value: 'Meine Änderung' } })
    current = server({ title_de: 'Von nebenan', version: 'v2' })
    fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
    const alert = await screen.findByRole('alert')
    expect(alert.textContent).toContain('Inzwischen hat jemand anderes gespeichert.')
    expect(title().value).toBe('Meine Änderung')

    fireEvent.click(screen.getByRole('button', { name: 'Serverstand laden (eigene Änderungen verwerfen)' }))
    await waitFor(() => expect(title().value).toBe('Von nebenan'))
    expect(screen.queryByRole('alert')).toBeNull()
    vi.mocked(api.put).mockResolvedValue({ data: { version: 'v3' } })
    fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
    await waitFor(() => expect(lastPutUrl()).toBe(`${URL}?base_version=v2`))
  })

  it('422 mit Block-id: öffnet den genannten Block und setzt den Fokus hinein', async () => {
    const { container } = open()
    await screen.findByDisplayValue('Server-Titel')
    vi.mocked(api.put).mockRejectedValue(apiError(422, "diagram-Block 'dia-1': messages: fehlt"))
    fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
    expect((await screen.findByRole('alert')).textContent).toContain("diagram-Block 'dia-1'")
    const blocks = container.querySelectorAll('details')
    expect(blocks[1].open).toBe(true)
    expect(blocks[0].open).toBe(false)
    expect(blocks[1].contains(document.activeElement)).toBe(true)
    expect(Element.prototype.scrollIntoView).toHaveBeenCalled()
  })

  it('nach „Auslieferungszustand laden“ ersetzt der Serverstand das Formular, gespeichert wird mit dessen Version', async () => {
    open()
    await screen.findByDisplayValue('Server-Titel')
    fireEvent.change(title(), { target: { value: 'Meine Änderung' } })
    vi.mocked(api.post).mockImplementation(() => { current = server({ title_de: 'Auslieferung', version: 'v9' }); return Promise.resolve({ data: {} }) })
    fireEvent.click(screen.getByRole('button', { name: 'Auslieferungszustand laden' }))
    await waitFor(() => expect(title().value).toBe('Auslieferung'))
    vi.mocked(api.put).mockResolvedValue({ data: { version: 'v10' } })
    fireEvent.click(screen.getByRole('button', { name: 'Speichern' }))
    await waitFor(() => expect(lastPutUrl()).toBe(`${URL}?base_version=v9`))
  })
})
