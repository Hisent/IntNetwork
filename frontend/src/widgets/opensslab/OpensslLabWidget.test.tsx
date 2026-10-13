// @vitest-environment jsdom
//
// Deckt die vier vom Auftrag geforderten Fälle ab: deaktiviertes Lab (bzw.
// "openssl" nicht in status.kinds), eine Vorlage setzt die Befehle, ein
// erfolgreicher Lauf zeigt die echte Ausgabe, und eine Grenzverletzung
// (7. Befehl) wird clientseitig abgelehnt. Mock von @/lib/api nach demselben
// Muster wie AnsibleLabWidget.test.tsx, kein echter Server.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { WidgetScopeContext } from '@/lib/widgetScope'
import { OpensslLab } from './OpensslLabWidget'
import { MODULE_TEMPLATES, OPENSSL_TEMPLATES } from './templates'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn() },
}))

import { api } from '@/lib/api'

function runResult() {
  return {
    rc: 0, truncated: false, duration_ms: 42, timed_out: false,
    output: '$ openssl genrsa -out server.key 2048\nGenerating RSA private key, 2048 bit long modulus\n',
  }
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  localStorage.clear()
})

function renderInModule(moduleKey: string) {
  return render(
    <WidgetScopeContext.Provider value="7-3">
      <MemoryRouter initialEntries={[`/lernen/${moduleKey}`]}>
        <Routes><Route path="/lernen/:key" element={<OpensslLab lang="de" />} /></Routes>
      </MemoryRouter>
    </WidgetScopeContext.Provider>,
  )
}

describe('OpensslLab', () => {
  it('zeigt den freundlichen Hinweis statt eines toten Knopfes, wenn das Lab (oder die Art) nicht aktiviert ist', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: false, kinds: [] } })

    render(<OpensslLab lang="de" />)

    expect(await screen.findByText('Lab auf diesem Server nicht aktiviert')).toBeTruthy()
    const runButton = screen.getByRole('button', { name: 'Ausführen' }) as HTMLButtonElement
    expect(runButton.disabled).toBe(true)
  })

  it('zeigt den Hinweis auch, wenn das Lab aktiviert ist, aber "openssl" nicht in status.kinds steht', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true, kinds: ['ansible'] } })

    render(<OpensslLab lang="de" />)

    expect(await screen.findByText('Lab auf diesem Server nicht aktiviert')).toBeTruthy()
    const runButton = screen.getByRole('button', { name: 'Ausführen' }) as HTMLButtonElement
    expect(runButton.disabled).toBe(true)
  })

  it('setzt Dateien und Befehle aus einer Vorlage', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true, kinds: ['openssl'] } })

    render(<OpensslLab lang="de" />)
    await screen.findByRole('button', { name: 'Ausführen' })

    fireEvent.click(screen.getByRole('button', { name: 'Kette prüfen' }))

    expect(screen.getByDisplayValue('verify -CAfile ca.pem server.pem')).toBeTruthy()
  })

  it('führt einen Lauf aus und zeigt die echte Ausgabe', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true, kinds: ['openssl'] } })
    vi.mocked(api.post).mockResolvedValue({ data: runResult() })

    render(<OpensslLab lang="de" />)
    const runButton = await screen.findByRole('button', { name: 'Ausführen' }) as HTMLButtonElement
    expect(runButton.disabled).toBe(false)

    fireEvent.click(runButton)

    expect(await screen.findByText(/Generating RSA private key/)).toBeTruthy()
    expect(api.post).toHaveBeenCalledWith('/lab/run', expect.objectContaining({ kind: 'openssl' }))
  })

  it('lehnt einen 7. Befehl clientseitig ab (Grenze: höchstens 6 Befehle)', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true, kinds: ['openssl'] } })

    render(<OpensslLab lang="de" />)
    const addCommandButton = await screen.findByRole('button', { name: '+ Befehl' })

    // Vorlage "Schlüssel + CSR erzeugen" (Standard) hat 3 Befehle -> 4 weitere ergeben 7.
    fireEvent.click(addCommandButton)
    fireEvent.click(addCommandButton)
    fireEvent.click(addCommandButton)
    fireEvent.click(addCommandButton)

    expect(await screen.findByText('Höchstens 6 Befehle pro Lauf.')).toBeTruthy()
    const runButton = screen.getByRole('button', { name: 'Ausführen' }) as HTMLButtonElement
    expect(runButton.disabled).toBe(true)
    expect(api.post).not.toHaveBeenCalled()
  })

  it('wählt die zum Modul passende Vorlage vor', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true, kinds: ['openssl'] } })

    renderInModule('post-quantum-kryptografie')
    await screen.findByRole('button', { name: 'Ausführen' })

    expect(screen.getByDisplayValue('genpkey -algorithm ML-KEM-768 -out mlkem.key')).toBeTruthy()
    expect(screen.queryByDisplayValue('genrsa -out server.key 2048')).toBeNull()
  })

  it('behält den gespeicherten Stand nur, wenn seine Vorlage zum Modul gehört', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true, kinds: ['openssl'] } })
    const stored = (templateId: string) => localStorage.setItem('intnetwork-opensslab-7-3',
      JSON.stringify({ templateId, files: [], commands: ['version -a'] }))

    // Stand aus einem anderen Modul (Widerruf) -> im Signatur-Modul startet dessen erste Vorlage
    stored('widerruf-pruefen')
    renderInModule('digitale-signaturen')
    await screen.findByRole('button', { name: 'Ausführen' })
    expect(screen.getByDisplayValue('dgst -sha256 -hmac nordwind-geheim lieferschein.txt')).toBeTruthy()
    expect(screen.queryByDisplayValue('version -a')).toBeNull()
    cleanup()

    // eigene Änderungen an der zweiten Vorlage desselben Moduls bleiben erhalten
    stored('signieren-pruefen')
    renderInModule('digitale-signaturen')
    await screen.findByRole('button', { name: 'Ausführen' })
    expect(screen.getByDisplayValue('version -a')).toBeTruthy()
    cleanup()

    // Modul ohne eigene Zuordnung: der gespeicherte Stand gilt weiter
    renderInModule('tls-pruefen')
    await screen.findByRole('button', { name: 'Ausführen' })
    expect(screen.getByDisplayValue('version -a')).toBeTruthy()
  })

  it('verweist je Modul nur auf vorhandene Vorlagen', () => {
    const ids = new Set(OPENSSL_TEMPLATES.map((t) => t.id))
    for (const [moduleKey, templates] of Object.entries(MODULE_TEMPLATES)) {
      expect(templates.length, moduleKey).toBeGreaterThan(0)
      for (const id of templates) expect(ids.has(id), `${moduleKey}: ${id}`).toBe(true)
    }
  })
})
