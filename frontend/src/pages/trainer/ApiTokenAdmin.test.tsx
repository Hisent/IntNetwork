// @vitest-environment jsdom
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen, waitFor } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { ApiTokenAdmin } from './ApiTokenAdmin'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn(), put: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  errMsg: (_e: unknown, fallback = 'Fehler.') => fallback,
}))
import { api } from '@/lib/api'

const ROW = { id: 7, name: 'Laptop', prefix: 'lgt_abcd', created_at: '2026-11-01T10:00:00Z', last_used_at: null }

afterEach(() => { cleanup(); vi.clearAllMocks() })

describe('ApiTokenAdmin', () => {
  it('zeigt Token und Befehl genau einmal und entfernt sie beim Schließen', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: [] })
    vi.mocked(api.post).mockResolvedValue({ data: { ...ROW, token: 'lgt_SECRET123' } })
    renderWithProviders(<ApiTokenAdmin />)
    fireEvent.change(await screen.findByLabelText(/Name/), { target: { value: 'Laptop' } })
    fireEvent.click(screen.getByRole('button', { name: /Token erstellen/ }))
    const cmd = `claude mcp add --transport http lehrgang ${window.location.origin}/api/mcp --header "Authorization: Bearer lgt_SECRET123"`
    await waitFor(() => expect(screen.getAllByText(cmd)).toHaveLength(1))
    expect(api.post).toHaveBeenCalledWith('/trainer/api-tokens', { name: 'Laptop' })
    expect(screen.getAllByDisplayValue('lgt_SECRET123')).toHaveLength(1)
    fireEvent.click(screen.getByRole('button', { name: /Schließen/ }))
    expect(screen.queryByText(cmd)).toBeNull()
    expect(screen.queryByDisplayValue('lgt_SECRET123')).toBeNull()
  })

  it('löscht einen Token', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: [ROW] })
    vi.mocked(api.delete).mockResolvedValue({ data: { ok: true } })
    renderWithProviders(<ApiTokenAdmin />)
    fireEvent.click(await screen.findByRole('button', { name: /Laptop.*widerrufen/ }))
    await waitFor(() => expect(api.delete).toHaveBeenCalledWith('/trainer/api-tokens/7'))
  })
})
