// @vitest-environment jsdom
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen, waitFor } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { ModuleAdmin } from './ModuleAdmin'
import type { TrainerWorkshop } from '@/types'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn(), put: vi.fn(), patch: vi.fn(), delete: vi.fn() },
  errMsg: (_e: unknown, fallback = 'Fehler.') => fallback,
}))
import { api } from '@/lib/api'

const DRAFT: TrainerWorkshop = {
  key: 'vpn', title: { de: 'VPN-Kurs', en: 'VPN course' }, theme: 'network', sections: [],
  status: 'draft', owner_name: 'Anna', editable: true,
}

function setup(role: 'admin' | 'trainer') {
  vi.mocked(api.get).mockImplementation((url: string) => {
    if (url === '/trainer/accounts') return Promise.resolve({ data: [{ id: 1, name: 'Me', email: 'm@x.de', role, is_self: true }] })
    return Promise.resolve({ data: [] })
  })
  renderWithProviders(<ModuleAdmin workshops={[DRAFT]} />)
}

afterEach(() => { cleanup(); vi.clearAllMocks() })

describe('ModuleAdmin Entwürfe', () => {
  it('zeigt Badge und Besitzer; Veröffentlichen nur für Admins', async () => {
    setup('admin')
    expect(await screen.findByText('Entwurf')).toBeTruthy()
    expect(screen.getByText(/Anna/)).toBeTruthy()
    vi.mocked(api.post).mockResolvedValue({ data: { ...DRAFT, status: 'published' } })
    fireEvent.click(await screen.findByRole('button', { name: /Veröffentlichen/ }))
    await waitFor(() => expect(api.post).toHaveBeenCalledWith('/trainer/workshops/vpn/publish'))
  })

  it('versteckt Veröffentlichen für Trainer', async () => {
    setup('trainer')
    await screen.findByText('Entwurf')
    await waitFor(() => expect(api.get).toHaveBeenCalledWith('/trainer/accounts'))
    expect(screen.queryByRole('button', { name: /Veröffentlichen/ })).toBeNull()
  })
})
