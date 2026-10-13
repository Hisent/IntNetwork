// @vitest-environment jsdom
//
// Deckt Teil B des Einladungslink-Features ab: die "Teilnehmer einladen"-
// Sektion zeigt den korrekten Link (Route + Kurs-Code) und rendert lokal
// einen QR-Code dazu (kein externer Dienst, siehe CSP in nginx.conf).
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen, waitFor } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { CourseDetail } from '@/pages/trainer/CourseDetail'
import type { Course } from '@/lib/trainerApi'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn(), put: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))

import { api } from '@/lib/api'

function mockGet(routes: Record<string, unknown>) {
  vi.mocked(api.get).mockImplementation((url: string) => {
    for (const [pattern, data] of Object.entries(routes)) {
      if (url === pattern) return Promise.resolve({ data })
    }
    return Promise.reject(new Error(`kein Mock für ${url}`))
  })
}

const COURSE: Course = { id: 1, name: 'Testkurs', join_code: 'ABC123', workshop_key: 'network', participant_count: 0 }

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

describe('CourseDetail — Teilnehmer einladen', () => {
  it('zeigt den Einladungslink mit Workshop-Key und Kurs-Code sowie einen QR-Code dazu', async () => {
    mockGet({
      '/courses/1/modules': [],
      '/trainer/courses/1/presence': [],
      '/courses/1/dashboard': { course: COURSE, modules: [], participants: [] },
      '/features': { comments: false },
    })

    renderWithProviders(
      <CourseDetail
        course={COURSE}
        workshopTitle={() => 'Netzwerk-Grundlagen'}
        workshops={[]}
        portalContainer={null}
        onDeleted={() => {}}
      />,
    )

    const expectedLink = `${window.location.origin}/workshops/network?code=ABC123`
    expect(await screen.findByText(expectedLink)).toBeTruthy()

    const qr = (await screen.findByAltText('QR-Code zum Kursbeitritt')) as HTMLImageElement
    expect(qr.src.startsWith('data:image')).toBe(true)
  })

  it('zeigt keinen Freigabe-Hinweis, wenn require_approval aus ist', async () => {
    mockGet({
      '/courses/1/modules': [],
      '/trainer/courses/1/presence': [],
      '/courses/1/dashboard': { course: COURSE, modules: [], participants: [] },
      '/features': { comments: false },
    })

    renderWithProviders(
      <CourseDetail
        course={{ ...COURSE, require_approval: false }}
        workshopTitle={() => 'Netzwerk-Grundlagen'}
        workshops={[]}
        portalContainer={null}
        onDeleted={() => {}}
      />,
    )

    await screen.findByText(`${window.location.origin}/workshops/network?code=ABC123`)
    expect(screen.queryByText(/Teilnahmebestätigung gibt es weiterhin erst nach deiner Freigabe/)).toBeNull()
  })

  it('zeigt einen Freigabe-Hinweis, wenn require_approval an ist', async () => {
    mockGet({
      '/courses/1/modules': [],
      '/trainer/courses/1/presence': [],
      '/courses/1/dashboard': { course: { ...COURSE, require_approval: true }, modules: [], participants: [] },
      '/features': { comments: false },
    })

    renderWithProviders(
      <CourseDetail
        course={{ ...COURSE, require_approval: true }}
        workshopTitle={() => 'Netzwerk-Grundlagen'}
        workshops={[]}
        portalContainer={null}
        onDeleted={() => {}}
      />,
    )

    expect(await screen.findByText(/Teilnahmebestätigung gibt es weiterhin erst nach deiner Freigabe/)).toBeTruthy()
  })
})

describe('CourseDetail — laufende Live-Abstimmung', () => {
  const base = {
    '/courses/1/modules': [],
    '/trainer/courses/1/presence': [],
    '/courses/1/dashboard': { course: COURSE, modules: [], participants: [] },
  }
  const detail = <CourseDetail course={COURSE} workshopTitle={() => 'Netzwerk-Grundlagen'} workshops={[]} portalContainer={null} onDeleted={() => {}} />

  it('zeigt eine offene Abstimmung an und beendet sie auf Knopfdruck', async () => {
    mockGet({ ...base, '/features': { comments: false },
      '/trainer/courses/1/poll': { id: 7, status: 'open', prompt: 'Welche Schicht?', options: ['2', '3'], votes: 1 } })
    vi.mocked(api.delete).mockResolvedValue({ data: undefined })
    renderWithProviders(detail)

    expect(await screen.findByText('Welche Schicht?')).toBeTruthy()
    expect(screen.getByText(/Live-Abstimmung läuft · 1 Stimme$/)).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Abstimmung beenden' }))
    await waitFor(() => expect(screen.queryByText('Welche Schicht?')).toBeNull())
    expect(api.delete).toHaveBeenCalledWith('/trainer/courses/1/poll')
  })

  it('zeigt ohne Abstimmung nichts dazu', async () => {
    mockGet({ ...base, '/features': { comments: false }, '/trainer/courses/1/poll': null })
    renderWithProviders(detail)
    await screen.findByText(`${window.location.origin}/workshops/network?code=ABC123`)
    expect(screen.queryByText(/Live-Abstimmung läuft/)).toBeNull()
  })
})

describe('CourseDetail — Feedback beantworten und löschen', () => {
  const routes = {
    '/courses/1/modules': [],
    '/trainer/courses/1/presence': [],
    '/courses/1/dashboard': { course: COURSE, modules: [], participants: [] },
    '/features': { comments: true },
    '/trainer/courses/1/poll': null,
    '/trainer/courses/1/comments': [{ id: 5, module_key: 'm1', block_index: 0, body: 'Unklar', author_kind: 'participant', author_name: 'Ada', created_at: '2026-10-13T11:50:00' }],
    '/trainer/modules/m1': { key: 'm1', title: 'Modul Eins', order: 1, prerequisites: [], blocks: [{ type: 'text', value: 'Text' }], quiz: { questions: [] } },
  }
  const detail = <CourseDetail course={COURSE} workshopTitle={() => 'Netzwerk-Grundlagen'} workshops={[]} portalContainer={null} onDeleted={() => {}} />

  it('Enter sendet die Antwort, Umschalt+Enter nicht', async () => {
    mockGet(routes)
    vi.mocked(api.post).mockResolvedValue({ data: undefined })
    renderWithProviders(detail)

    const field = await screen.findByLabelText('Antwort zu Block 1')
    fireEvent.change(field, { target: { value: 'Schau in Abschnitt 2' } })
    fireEvent.keyDown(field, { key: 'Enter', shiftKey: true })
    expect(api.post).not.toHaveBeenCalled()
    fireEvent.keyDown(field, { key: 'Enter' })
    await waitFor(() => expect(api.post).toHaveBeenCalledTimes(1))
    expect(vi.mocked(api.post).mock.calls[0][1]).toMatchObject({ body: 'Schau in Abschnitt 2' })
  })

  it('löscht einen Kommentar erst nach Rückfrage', async () => {
    mockGet(routes)
    vi.mocked(api.delete).mockResolvedValue({ data: undefined })
    renderWithProviders(detail)

    fireEvent.click(await screen.findByRole('button', { name: 'Kommentar von Ada löschen' }))
    expect(api.delete).not.toHaveBeenCalled()
    fireEvent.click(await screen.findByRole('button', { name: 'Löschen' }))
    await waitFor(() => expect(api.delete).toHaveBeenCalledTimes(1))
  })
})
