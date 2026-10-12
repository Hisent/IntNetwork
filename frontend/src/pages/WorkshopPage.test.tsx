// @vitest-environment jsdom
//
// Deckt Teil A des Einladungslink-Features ab: der Kurs-Code kommt aus dem
// Query-Param ?code=..., der Name bleibt Pflicht und muss weiterhin getippt
// werden. Ohne Query-Param bleibt das Verhalten exakt wie zuvor (leeres Feld,
// kein Hinweistext).
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen, waitFor } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { WorkshopPage } from '@/pages/WorkshopPage'
import type { WorkshopDetail } from '@/types'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn(), put: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  authApi: { join: vi.fn() },
  errMsg: (_e: unknown, fallback = 'Fehler.') => fallback,
}))

import { api, authApi } from '@/lib/api'

const WORKSHOP: WorkshopDetail = {
  key: 'network',
  title: { de: 'Netzwerk-Grundlagen', en: 'Networking fundamentals' },
  summary: { de: 'Kurzbeschreibung', en: 'Summary' },
  theme: 'network',
  sections: [],
  modules: [{ key: 'm1', title: { de: 'Modul 1', en: 'Module 1' }, order: 1 }],
}

function mockGet(routes: Record<string, unknown>) {
  vi.mocked(api.get).mockImplementation((url: string) => {
    for (const [pattern, data] of Object.entries(routes)) {
      if (url === pattern) return Promise.resolve({ data })
    }
    return Promise.reject(new Error(`kein Mock für ${url}`))
  })
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  localStorage.clear()
})

describe('WorkshopPage — Kurs-Code aus dem Einladungslink', () => {
  it('befüllt das Kurs-Code-Feld aus ?code=... und zeigt den Übernahme-Hinweis', async () => {
    mockGet({ '/workshops/network': WORKSHOP })

    renderWithProviders(<WorkshopPage />, { route: '/workshops/network?code=abc123', path: '/workshops/:key' })

    const codeInput = (await screen.findByLabelText('Kurs-Code')) as HTMLInputElement
    expect(codeInput.value).toBe('ABC123')
    expect(screen.getByText(/aus deinem Einladungslink übernommen/)).toBeTruthy()
  })

  it('lässt das Kurs-Code-Feld ohne Query-Param leer und zeigt keinen Hinweis', async () => {
    mockGet({ '/workshops/network': WORKSHOP })

    renderWithProviders(<WorkshopPage />, { route: '/workshops/network', path: '/workshops/:key' })

    const codeInput = (await screen.findByLabelText('Kurs-Code')) as HTMLInputElement
    expect(codeInput.value).toBe('')
    expect(screen.queryByText(/aus deinem Einladungslink übernommen/)).toBeNull()
  })

  it('setzt bei vorausgefülltem Code den Fokus initial aufs Namensfeld', async () => {
    mockGet({ '/workshops/network': WORKSHOP })

    renderWithProviders(<WorkshopPage />, { route: '/workshops/network?code=abc123', path: '/workshops/:key' })

    const nameInput = await screen.findByLabelText('Dein Name')
    expect(document.activeElement).toBe(nameInput)
  })
})

describe('WorkshopPage — Sprachwahl', () => {
  it('merkt sich die Wahl über Seiten hinweg und nimmt sie beim Beitritt in den Kurs mit', async () => {
    mockGet({ '/workshops/network': WORKSHOP })
    vi.mocked(authApi.join).mockResolvedValue({ data: { access_token: 'tok', course_name: 'Kurs', name: 'Ada', resume_code: null } })
    vi.mocked(api.patch).mockResolvedValue({ data: { language: 'en' } })

    renderWithProviders(<WorkshopPage />, { route: '/workshops/network', path: '/workshops/:key' })
    fireEvent.click(await screen.findByRole('button', { name: 'en' }))
    cleanup()

    // „Neue Seite“: die Wahl kommt aus dem Browser-Speicher, nicht aus dem alten State.
    renderWithProviders(<WorkshopPage />, { route: '/workshops/network?code=abc123', path: '/workshops/:key' })
    fireEvent.change(await screen.findByLabelText('Your name'), { target: { value: 'Ada' } })
    fireEvent.click(screen.getByRole('button', { name: /Start workshop/ }))

    await waitFor(() => expect(api.patch).toHaveBeenCalledWith('/me/language', { language: 'en' }))
  })

  it('lässt die gespeicherte Teilnehmer-Sprache ohne ausdrückliche Wahl unangetastet', async () => {
    mockGet({ '/workshops/network': WORKSHOP })
    vi.mocked(authApi.join).mockResolvedValue({ data: { access_token: 'tok', course_name: 'Kurs', name: 'Ada', resume_code: null } })

    renderWithProviders(<WorkshopPage />, { route: '/workshops/network?code=abc123', path: '/workshops/:key' })
    fireEvent.change(await screen.findByLabelText('Dein Name'), { target: { value: 'Ada' } })
    fireEvent.click(screen.getByRole('button', { name: /Workshop starten/ }))

    await waitFor(() => expect(authApi.join).toHaveBeenCalled())
    expect(api.patch).not.toHaveBeenCalled()
  })
})
