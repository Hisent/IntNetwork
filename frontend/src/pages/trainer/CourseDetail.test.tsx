// @vitest-environment jsdom
//
// Deckt Teil B des Einladungslink-Features ab: die "Teilnehmer einladen"-
// Sektion zeigt den korrekten Link (Route + Kurs-Code) und rendert lokal
// einen QR-Code dazu (kein externer Dienst, siehe CSP in nginx.conf).
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, screen } from '@testing-library/react'
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
    expect(screen.queryByText(/müssen weiterhin von dir freigegeben werden/)).toBeNull()
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

    expect(await screen.findByText(/müssen weiterhin von dir freigegeben werden/)).toBeTruthy()
  })
})
