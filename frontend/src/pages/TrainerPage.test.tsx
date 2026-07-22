// @vitest-environment jsdom
//
// Schlanke Render-Tests im Stil von pages.smoke.test.tsx: gemockter API-Layer,
// keine echten Requests. Deckt die beiden in diesem Review geänderten
// Verhalten ab — Busy-State beim Trainer-Login und Paginierung im Audit-Log.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { useAuthStore } from '@/store/auth'
import { TrainerPage } from '@/pages/TrainerPage'
import type { AuditLogEntry } from '@/lib/trainerApi'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn(), put: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  authApi: { trainerLogin: vi.fn(), join: vi.fn() },
  errMsg: (_e: unknown, fallback = 'Fehler.') => fallback,
}))

import { api, authApi } from '@/lib/api'

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
  useAuthStore.setState({ token: null, role: null, displayName: null })
})

describe('TrainerPage — Login', () => {
  it('deaktiviert den Anmelden-Knopf während des Requests und wieder danach bei einem Fehler', async () => {
    let rejectLogin: (reason: unknown) => void = () => {}
    vi.mocked(authApi.trainerLogin).mockImplementation(() => new Promise((_resolve, reject) => { rejectLogin = reject }))

    renderWithProviders(<TrainerPage />)

    fireEvent.change(screen.getByLabelText('E-Mail'), { target: { value: 'trainer@beispiel.de' } })
    fireEvent.change(screen.getByLabelText('Passwort'), { target: { value: 'geheim123' } })
    fireEvent.click(screen.getByRole('button', { name: 'Anmelden' }))

    const busyButton = await screen.findByRole('button', { name: 'Meldet an…' })
    expect((busyButton as HTMLButtonElement).disabled).toBe(true)

    rejectLogin(new Error('Login fehlgeschlagen'))

    expect(await screen.findByText('Login fehlgeschlagen.')).toBeTruthy()
    expect(((await screen.findByRole('button', { name: 'Anmelden' })) as HTMLButtonElement).disabled).toBe(false)
  })
})

describe('TrainerPage — Audit-Log', () => {
  it('lädt die erste Seite und hängt weitere Seiten per Knopf an', async () => {
    useAuthStore.setState({ token: 'demo', role: 'trainer', displayName: 'Trainer' })

    const firstPage: AuditLogEntry[] = Array.from({ length: 50 }, (_, i) => ({
      id: i + 1, created_at: '2026-01-01T00:00:00Z', trainer_email: 't@example.com',
      action: `Aktion ${i + 1}`, target: null, detail: null,
    }))
    const secondPage: AuditLogEntry[] = [
      { id: 51, created_at: '2026-01-02T00:00:00Z', trainer_email: 't@example.com', action: 'Aktion 51', target: null, detail: null },
    ]

    mockGet({
      '/courses': [],
      '/workshops': [],
      '/trainer/modules': [],
      '/trainer/accounts': [],
      '/features': { comments: false },
      '/changelog': [],
      '/trainer/audit?limit=50&offset=0': firstPage,
      '/trainer/audit?limit=50&offset=50': secondPage,
    })

    renderWithProviders(<TrainerPage />)

    expect(await screen.findByText('Aktion 1')).toBeTruthy()
    expect(screen.getByText('50+ Aktionen anzeigen')).toBeTruthy()
    expect(screen.queryByText('Aktion 51')).toBeNull()

    fireEvent.click(screen.getByRole('button', { name: 'Weitere laden' }))

    expect(await screen.findByText('Aktion 51')).toBeTruthy()
    // Zweite Seite hat nur 1 Eintrag (< Seitengröße) — kein weiterer Knopf.
    expect(screen.queryByRole('button', { name: 'Weitere laden' })).toBeNull()
  })
})
