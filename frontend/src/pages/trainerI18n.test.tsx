// @vitest-environment jsdom
//
// Trainer-Oberfläche zweisprachig: Key-Parität DE/EN, kein Deutsch im EN-Wörterbuch
// und ein Render von Login, Dashboard und Beamer-Modus in EN ohne deutsche Reste.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { useAuthStore } from '@/store/auth'
import { useLangStore } from '@/store/lang'
import { TRAINER_DE, TRAINER_EN } from '@/lib/i18nTrainer'
import { TrainerPage } from '@/pages/TrainerPage'
import { TrainerPresentPage } from '@/pages/TrainerPresentPage'

vi.mock('@/lib/api', async (original) => ({
  ...(await original<typeof import('@/lib/api')>()),
  api: { get: vi.fn(), post: vi.fn(), put: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))
import { api } from '@/lib/api'

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  useAuthStore.setState({ token: null, role: null, displayName: null })
  useLangStore.setState({ lang: 'de' })
  localStorage.clear()
})

// Gleichlautende Wörter/Symbole in beiden Sprachen (kein fehlender Key).
const SAME_IN_BOTH = new Set([
  'trTrainer', 'trWorkshop', 'trNameLabel', 'trFeedback', 'trPasskeys', 'trQuiz', 'trBlockN', 'trBackTrainer',
  'trTextDe', 'trTextEn', 'trOptionDe', 'trOptionEn', 'trAddOption', 'trEvalTrainer',
])

describe('Trainer-Wörterbuch', () => {
  it('EN hat exakt die Keys von DE', () => {
    expect(Object.keys(TRAINER_EN).sort()).toEqual(Object.keys(TRAINER_DE).sort())
  })

  it('EN enthält kein Deutsch (Umlaute, unübersetzte Werte)', () => {
    for (const [key, de] of Object.entries(TRAINER_DE)) {
      const en = TRAINER_EN[key as keyof typeof TRAINER_DE]
      expect(en, key).not.toMatch(/[äöüÄÖÜß]/)
      if (!SAME_IN_BOTH.has(key)) expect(en, `${key} ist unübersetzt`).not.toBe(de)
    }
  })
})

const GERMAN = /Kursübersicht|Verwaltung|Abmelden|Anmelden|Passwort|Trainer-Zugänge|Einstellungen|Änderungslog|Protokoll|Lädt|zurück|weiter →|Kurs für Live-Abstimmung|Nur für Trainer/

describe('Trainer-UI in EN', () => {
  it('Login ist englisch und der Umschalter wechselt zurück auf DE', async () => {
    useLangStore.setState({ lang: 'en' })
    renderWithProviders(<TrainerPage />)
    expect(screen.getByRole('heading', { name: 'Trainer login' })).toBeTruthy()
    expect(screen.getByLabelText('Password')).toBeTruthy()
    expect(document.body.textContent).not.toMatch(GERMAN)

    fireEvent.click(screen.getByRole('button', { name: 'de' }))
    expect(await screen.findByRole('heading', { name: 'Trainer-Login' })).toBeTruthy()
    expect(localStorage.getItem('intnetwork-lang')).toBe('de')
  })

  it('Dashboard: englisch ohne deutsche Reste', async () => {
    useLangStore.setState({ lang: 'en' })
    useAuthStore.setState({ token: 'demo', role: 'trainer', displayName: 'T' })
    vi.mocked(api.get).mockImplementation((url: string) => Promise.resolve({
      data: url === '/features' ? { comments: false } : [],
    }))
    renderWithProviders(<TrainerPage />)
    expect(await screen.findByText('Course overview')).toBeTruthy()
    expect(await screen.findByText('Administration')).toBeTruthy()
    expect(await screen.findByText('Trainer accounts')).toBeTruthy()
    expect(document.body.textContent).not.toMatch(GERMAN)
  })

  it('Beamer-Modus: Navigation und Abstimmungsleiste englisch', async () => {
    useLangStore.setState({ lang: 'en' })
    useAuthStore.setState({ token: 'demo', role: 'trainer', displayName: 'T' })
    vi.mocked(api.get).mockImplementation((url: string) => Promise.resolve({
      data: url === '/trainer/modules/m1'
        ? { key: 'm1', title: 'Module', order: 1, prerequisites: [], workshop_key: 'network', blocks: [{ uid: 'r1', type: 'reflect', prompt: 'Why?' }], quiz: { questions: [] } }
        : [],
    }))
    renderWithProviders(<TrainerPresentPage />, { route: '/trainer/modul/m1/praesentieren', path: '/trainer/modul/:key/praesentieren' })
    expect(await screen.findByRole('button', { name: 'next →' })).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'next →' }))
    expect(await screen.findByText('Reflection')).toBeTruthy()
    expect(screen.getByText('Arrow keys / space')).toBeTruthy()
    expect(document.body.textContent).not.toMatch(GERMAN)
  })
})
