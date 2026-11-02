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

function setup(role: 'admin' | 'trainer', workshops: TrainerWorkshop[] = [DRAFT]) {
  vi.mocked(api.get).mockImplementation((url: string) => {
    if (url === '/trainer/accounts') return Promise.resolve({ data: [{ id: 1, name: 'Me', email: 'm@x.de', role, is_self: true }] })
    if (url === '/trainer/modules') return Promise.resolve({ data: [
      { key: 'm-ro', title: 'Fremd', title_en: 'x', order: 1, prerequisites: [], workshop_key: 'ro' },
      { key: 'm-rw', title: 'Eigen', title_en: 'y', order: 2, prerequisites: [], workshop_key: 'vpn' },
    ] })
    return Promise.resolve({ data: [] })
  })
  renderWithProviders(<ModuleAdmin workshops={workshops} />)
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

  it('blendet Bearbeiten-Link für nicht editierbare Workshops aus', async () => {
    setup('trainer', [DRAFT, { ...DRAFT, key: 'ro', title: { de: 'Fremd-WS', en: 'x' }, status: 'published', editable: false }])
    fireEvent.change(await screen.findByLabelText('Modul suchen'), { target: { value: 'e' } })
    await screen.findByText('Eigen')
    expect(screen.getAllByRole('link', { name: /bearbeiten|edit/i }).map((a) => a.getAttribute('href')))
      .toEqual(['/trainer/modul/m-rw/bearbeiten'])
  })
})
