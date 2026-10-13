// @vitest-environment jsdom
//
// Deckt die Laufmechanik ab, die vitest lokal (ohne Runner) sonst nie sieht:
// Erfolg, deaktiviertes Lab (503/enabled:false), Rate-Limit (429) und
// Zeitüberschreitung (504) — jeweils über einen gemockten @/lib/api.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { AnsibleLab } from './AnsibleLabWidget'
import { EXERCISES, exerciseForModule } from './templates'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn() },
}))

import { api } from '@/lib/api'

function apiError(status: number, detail?: string) {
  const err = new Error(`HTTP ${status}`) as Error & { response: { status: number; data?: { detail?: string } } }
  err.response = { status, data: detail !== undefined ? { detail } : undefined }
  return err
}

// ok bewusst auf 9 fixiert und damit von changed verschieden — sonst kollidiert
// z.B. recapResult(9) mit sich selbst bei findByText (mehrdeutiger Treffer).
function recapResult(changed: number, ok = 9) {
  return {
    rc: 0, truncated: false, duration_ms: 1000, timed_out: false,
    output: `PLAY RECAP *********\nlabhost : ok=${ok} changed=${changed} unreachable=0 failed=0 skipped=0 rescued=0 ignored=0\n`,
  }
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

describe('AnsibleLab', () => {
  it('zeigt den freundlichen Hinweis statt eines toten Knopfes, wenn das Lab nicht aktiviert ist', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: false } })

    render(<AnsibleLab lang="de" />)

    expect(await screen.findByText('Lab auf diesem Server nicht aktiviert')).toBeTruthy()
    // Übungsvorlagen und Aufgabentext bleiben trotzdem sichtbar/lesbar.
    expect(screen.getByText('Idempotenz')).toBeTruthy()
    expect(screen.getByText(/erkläre, warum sie unterschiedlich ausfällt/)).toBeTruthy()

    const runButton = screen.getByRole('button', { name: 'Ausführen' }) as HTMLButtonElement
    expect(runButton.disabled).toBe(true)
  })

  it('führt einen Lauf aus und zeigt die Recap-Kennzahlen aus der echten Ausgabe', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true } })
    vi.mocked(api.post).mockResolvedValue({ data: recapResult(3) })

    render(<AnsibleLab lang="de" />)
    const runButton = await screen.findByRole('button', { name: 'Ausführen' }) as HTMLButtonElement
    expect(runButton.disabled).toBe(false)

    fireEvent.click(runButton)

    expect(await screen.findByText('3')).toBeTruthy()
    expect(api.post).toHaveBeenCalledWith('/lab/run', expect.objectContaining({ check: false }))
  })

  it('erkennt beim zweiten Lauf gesunkene Änderungen als Idempotenz', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true } })
    vi.mocked(api.post)
      .mockResolvedValueOnce({ data: recapResult(3) })
      .mockResolvedValueOnce({ data: recapResult(1) })

    render(<AnsibleLab lang="de" />)
    const runButton = await screen.findByRole('button', { name: 'Ausführen' })

    fireEvent.click(runButton)
    await screen.findByText('3')

    fireEvent.click(runButton)
    expect(await screen.findByText(/1 statt 3 Änderungen/)).toBeTruthy()
    expect(screen.getByText(/idempotent/)).toBeTruthy()
  })

  it('zeigt eine verständliche Meldung bei Rate-Limit (429)', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true } })
    vi.mocked(api.post).mockRejectedValue(apiError(429, 'Zu viele Versuche. Bitte kurz warten.'))

    render(<AnsibleLab lang="de" />)
    const runButton = await screen.findByRole('button', { name: 'Ausführen' })
    fireEvent.click(runButton)

    expect(await screen.findByText('Zu viele Versuche. Bitte kurz warten.')).toBeTruthy()
  })

  it('zeigt eine verständliche Meldung bei Zeitüberschreitung (504) ohne Detail-String', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true } })
    vi.mocked(api.post).mockRejectedValue(apiError(504))

    render(<AnsibleLab lang="de" />)
    const runButton = await screen.findByRole('button', { name: 'Ausführen' })
    fireEvent.click(runButton)

    expect(await screen.findByText(/Zeitüberschreitung/)).toBeTruthy()
  })

  it('nutzt --check für den Prüf-Lauf und aktualisiert die Idempotenz-Basislinie nicht', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true } })
    vi.mocked(api.post).mockResolvedValue({ data: recapResult(2) })

    render(<AnsibleLab lang="de" />)
    const checkButton = await screen.findByRole('button', { name: 'Nur prüfen (--check)' })
    fireEvent.click(checkButton)

    await screen.findByText('2')
    expect(api.post).toHaveBeenCalledWith('/lab/run', expect.objectContaining({ check: true }))
    // Kein Vergleichswert vorhanden -> keine Idempotenz-Aussage nach einem reinen Check-Lauf.
    expect(screen.queryByText(/Änderungen/)).toBeNull()
  })

  it('wählt die zum Modul passende Übung vor und zeigt deren eigene Challenge', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true } })

    render(
      <MemoryRouter initialEntries={['/lernen/templates-jinja2']}>
        <Routes><Route path="/lernen/:key" element={<AnsibleLab lang="de" />} /></Routes>
      </MemoryRouter>,
    )

    await screen.findByRole('button', { name: 'Ausführen' })
    const editor = screen.getByLabelText('Playbook') as HTMLTextAreaElement
    expect(editor.value).toContain('ansible.builtin.template')
    expect(screen.getByText(/Der Diff zeigt nur noch die geänderten Zeilen/)).toBeTruthy()
    // Die Idempotenz-Challenge gehört nicht mehr unter jede Übung.
    expect(screen.queryByText(/zweimal laufen und erkläre/)).toBeNull()
  })
})

describe('Übungsvorlagen', () => {
  const recap = (over: Partial<{ ok: number; changed: number; failed: number; skipped: number }>) =>
    ({ ok: 3, changed: 0, failed: 0, skipped: 0, hosts: 1, ...over })
  const byId = (id: string) => EXERCISES.find((e) => e.id === id)!

  it('hat je Modul höchstens eine Übung und nutzt nur FQCN-Module aus ansible.builtin', () => {
    const modules = EXERCISES.map((e) => e.module)
    expect(new Set(modules).size).toBe(modules.length)
    expect(exerciseForModule('fakten-bedingungen')?.id).toBe('fakten')
    expect(exerciseForModule('rollen')).toBeUndefined()
    for (const ex of EXERCISES) {
      const moduleLines = ex.playbook.split('\n').filter((l) => /^ {6}[a-z_.]+:( |$)/.test(l))
        .filter((l) => !/^ {6}(when|loop|notify|register|changed_when|check_mode|diff|vars):/.test(l))
      expect(moduleLines.length).toBeGreaterThan(0)
      for (const line of moduleLines) expect(line.trim().startsWith('ansible.builtin.')).toBe(true)
    }
  })

  it('wertet die Challenge je Übung aus dem letzten Lauf aus', () => {
    const none = { recap: null, output: '', rerun: false }
    for (const ex of EXERCISES) expect(ex.done(none)).toBe(false)

    expect(byId('idempotenz').done({ recap: recap({ changed: 1 }), output: 'x', rerun: true })).toBe(true)
    expect(byId('fehler-lesen').done({ recap: recap({ failed: 1 }), output: 'x', rerun: false })).toBe(false)
    expect(byId('fehler-lesen').done({ recap: recap({}), output: 'x', rerun: false })).toBe(true)
    expect(byId('kontrollfluss').done({ recap: recap({ changed: 0 }), output: 'x', rerun: true })).toBe(false)
    expect(byId('kontrollfluss').done({ recap: recap({ changed: 2 }), output: 'x', rerun: true })).toBe(true)
    expect(byId('variablen-vorrang').done({ recap: recap({}), output: 'Aktive Umgebung: staging', rerun: false })).toBe(false)
    expect(byId('variablen-vorrang').done({ recap: recap({}), output: 'Aktive Umgebung: produktion', rerun: false })).toBe(true)
    expect(byId('templates').done({ recap: recap({ changed: 0 }), output: 'x', rerun: true })).toBe(false)
    expect(byId('templates').done({ recap: recap({ changed: 1 }), output: 'x', rerun: true })).toBe(true)
    expect(byId('fakten').done({ recap: recap({ skipped: 1 }), output: 'x', rerun: false })).toBe(false)
    expect(byId('fakten').done({ recap: recap({ skipped: 2 }), output: 'x', rerun: false })).toBe(true)
  })
})
