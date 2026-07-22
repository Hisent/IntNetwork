// @vitest-environment jsdom
//
// Schlanke Render-Tests im Stil von pages.smoke.test.tsx: gemockter API-Layer,
// keine echten Requests. Deckt die beiden in diesem Review geänderten
// Verhalten ab — Busy-State beim Trainer-Login und Paginierung im Audit-Log.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, screen, waitFor } from '@testing-library/react'
import { renderWithProviders } from '@/test/renderWithProviders'
import { useAuthStore } from '@/store/auth'
import { TrainerPage } from '@/pages/TrainerPage'
import { TrainerModulePage } from '@/pages/TrainerModulePage'
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

function mockPost(routes: Record<string, unknown>) {
  vi.mocked(api.post).mockImplementation((url: string) => {
    for (const [pattern, data] of Object.entries(routes)) {
      if (url === pattern) return Promise.resolve({ data })
    }
    return Promise.reject(new Error(`kein Mock für POST ${url}`))
  })
}

// isPasskeySupported() (lib/passkey.ts) prüft window.PublicKeyCredential UND
// window.isSecureContext — beides existiert in jsdom standardmäßig nicht.
// Das jsdom-window selbst lebt aber über die gesamte Testdatei hinweg (nicht
// pro Test neu), ein defineProperty in einem Test würde also ohne Aufräumen
// in allen folgenden Tests dieser Datei weiterwirken — siehe afterEach unten.
function stubPasskeySupport() {
  Object.defineProperty(window, 'PublicKeyCredential', { value: function PublicKeyCredential() {}, configurable: true })
  Object.defineProperty(window, 'isSecureContext', { value: true, configurable: true })
}

function stubCredentials(overrides: { create?: () => Promise<unknown>; get?: () => Promise<unknown> }) {
  Object.defineProperty(navigator, 'credentials', {
    value: { create: vi.fn(), get: vi.fn(), ...overrides },
    configurable: true,
  })
}

function fakeAssertionCredential() {
  return {
    id: 'cred-1',
    rawId: new Uint8Array([1, 2, 3]).buffer,
    type: 'public-key',
    response: {
      clientDataJSON: new Uint8Array([4, 5, 6]).buffer,
      authenticatorData: new Uint8Array([7, 8, 9]).buffer,
      signature: new Uint8Array([10, 11, 12]).buffer,
      userHandle: null,
    },
    getClientExtensionResults: () => ({}),
  }
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  useAuthStore.setState({ token: null, role: null, displayName: null })
  // Rückbau der Passkey-Stubs — jsdoms window/navigator überleben (anders als
  // die DOM-Baum-Bereinigung durch cleanup()) über die ganze Testdatei hinweg.
  delete (window as { PublicKeyCredential?: unknown }).PublicKeyCredential
  delete (window as { isSecureContext?: unknown }).isSecureContext
  delete (navigator as { credentials?: unknown }).credentials
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
    // Skiplink-Ziel (App.tsx springt zu #main-content) muss auf Trainer-Seiten existieren.
    expect(document.getElementById('main-content')).toBeTruthy()
    expect(screen.getByText('50+ Aktionen anzeigen')).toBeTruthy()
    expect(screen.queryByText('Aktion 51')).toBeNull()

    fireEvent.click(screen.getByRole('button', { name: 'Weitere laden' }))

    expect(await screen.findByText('Aktion 51')).toBeTruthy()
    // Zweite Seite hat nur 1 Eintrag (< Seitengröße) — kein weiterer Knopf.
    expect(screen.queryByRole('button', { name: 'Weitere laden' })).toBeNull()
  })
})

describe('TrainerPage — Passkey-Login', () => {
  it('zeigt den Passkey-Knopf nicht, wenn der Server enabled: false meldet', async () => {
    stubPasskeySupport()
    mockGet({ '/trainer/passkey/status': { enabled: false } })

    renderWithProviders(<TrainerPage />)

    await screen.findByRole('button', { name: 'Anmelden' })
    await waitFor(() => expect(vi.mocked(api.get)).toHaveBeenCalledWith('/trainer/passkey/status'))
    expect(screen.queryByRole('button', { name: 'Mit Passkey anmelden' })).toBeNull()
  })

  it('zeigt den Passkey-Knopf nicht, wenn der Browser WebAuthn nicht unterstützt (isPasskeySupported() falsch)', async () => {
    // Bewusst KEIN stubPasskeySupport() — window.PublicKeyCredential/isSecureContext
    // fehlen in jsdom von Haus aus, entspricht also einer nackten HTTP-Instanz.
    mockGet({ '/trainer/passkey/status': { enabled: true } })

    renderWithProviders(<TrainerPage />)

    await screen.findByRole('button', { name: 'Anmelden' })
    expect(screen.queryByRole('button', { name: 'Mit Passkey anmelden' })).toBeNull()
    // Ohne Unterstützung wird /status gar nicht erst abgefragt (useQuery enabled: false).
    expect(vi.mocked(api.get)).not.toHaveBeenCalledWith('/trainer/passkey/status')
  })

  it('meldet per Passkey an und setzt danach dasselbe Token wie beim Passwort-Login', async () => {
    stubPasskeySupport()
    stubCredentials({ get: vi.fn().mockResolvedValue(fakeAssertionCredential()) })
    mockGet({
      '/courses': [], '/workshops': [], '/trainer/modules': [], '/trainer/accounts': [],
      '/features': { comments: false }, '/changelog': [],
      '/trainer/passkey/status': { enabled: true }, '/trainer/passkey': [],
    })
    mockPost({
      '/trainer/passkey/login/options': { publicKey: { challenge: 'AAEC', timeout: 60000 } },
      '/trainer/passkey/login/verify': { access_token: 'passkey-token' },
    })

    renderWithProviders(<TrainerPage />)

    const passkeyButton = await screen.findByRole('button', { name: 'Mit Passkey anmelden' })
    fireEvent.click(passkeyButton)

    await waitFor(() => expect(useAuthStore.getState().token).toBe('passkey-token'))
    expect(useAuthStore.getState().role).toBe('trainer')
  })

  it('zeigt bei Abbruch des Systemdialogs (NotAllowedError) keine Fehlermeldung', async () => {
    stubPasskeySupport()
    stubCredentials({ get: vi.fn().mockRejectedValue(new DOMException('Der Nutzer hat abgebrochen.', 'NotAllowedError')) })
    mockGet({ '/trainer/passkey/status': { enabled: true } })
    mockPost({ '/trainer/passkey/login/options': { publicKey: { challenge: 'AAEC', timeout: 60000 } } })

    renderWithProviders(<TrainerPage />)

    const passkeyButton = await screen.findByRole('button', { name: 'Mit Passkey anmelden' })
    fireEvent.click(passkeyButton)

    await waitFor(() => expect((screen.getByRole('button', { name: 'Mit Passkey anmelden' }) as HTMLButtonElement).disabled).toBe(false))
    expect(screen.queryByText('Passkey-Anmeldung fehlgeschlagen.')).toBeNull()
    expect(useAuthStore.getState().token).toBeNull()
  })
})

describe('TrainerModulePage — Skiplink-Ziel', () => {
  it('rendert #main-content (Skiplink-Ziel), auch für Nicht-Netzwerk-Themes', async () => {
    useAuthStore.setState({ token: 'demo', role: 'trainer', displayName: 'Trainer' })
    mockGet({
      '/trainer/modules/m1': {
        key: 'm1', workshop_key: 'pki', title: 'Modul Eins', order: 1, prerequisites: [],
        blocks: [], quiz: { questions: [] },
      },
      '/courses': [],
      '/trainer/modules/m1/quiz-stats': { submissions: 0, questions: [] },
    })

    renderWithProviders(<TrainerModulePage />, { route: '/trainer/modul/m1', path: '/trainer/modul/:key' })

    expect(await screen.findByText('Modul Eins', { exact: false })).toBeTruthy()
    expect(document.getElementById('main-content')).toBeTruthy()
  })
})

describe('TrainerPage — Passkeys (Verwaltung)', () => {
  it('zeigt „noch nicht genutzt“ für einen Passkey ohne last_used_at', async () => {
    useAuthStore.setState({ token: 'demo', role: 'trainer', displayName: 'Trainer' })
    mockGet({
      '/courses': [], '/workshops': [], '/trainer/modules': [], '/trainer/accounts': [],
      '/features': { comments: false }, '/changelog': [],
      '/trainer/passkey/status': { enabled: true },
      '/trainer/passkey': [{ id: 'pk1', label: 'Notebook', created_at: '2026-01-01T00:00:00Z', last_used_at: null }],
    })

    renderWithProviders(<TrainerPage />)

    expect(await screen.findByText(/noch nicht genutzt/)).toBeTruthy()
  })
})
