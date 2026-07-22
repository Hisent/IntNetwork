// @vitest-environment jsdom
//
// Deckt die vier vom Auftrag geforderten Fälle ab: deaktiviertes Lab (bzw.
// "git" nicht in status.kinds), eine Vorlage setzt die Befehle, ein
// erfolgreicher Lauf zeigt die echte Ausgabe, und eine Grenzverletzung
// (7. Befehl) wird clientseitig abgelehnt. Mock von @/lib/api nach demselben
// Muster wie AnsibleLabWidget.test.tsx, kein echter Server.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { GitLab } from './GitLabWidget'

vi.mock('@/lib/api', () => ({
  api: { get: vi.fn(), post: vi.fn() },
}))

import { api } from '@/lib/api'

function runResult() {
  return {
    rc: 0, truncated: false, duration_ms: 17, timed_out: false,
    output: '$ git init\nInitialized empty Git repository\n$ git commit -m start\n[main (root-commit)] start\n',
  }
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

describe('GitLab', () => {
  it('zeigt den freundlichen Hinweis statt eines toten Knopfes, wenn das Lab (oder die Art) nicht aktiviert ist', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: false, kinds: [] } })

    render(<GitLab lang="de" />)

    expect(await screen.findByText('Lab auf diesem Server nicht aktiviert')).toBeTruthy()
    const runButton = screen.getByRole('button', { name: 'Ausführen' }) as HTMLButtonElement
    expect(runButton.disabled).toBe(true)
  })

  it('zeigt den Hinweis auch, wenn das Lab aktiviert ist, aber "git" nicht in status.kinds steht', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true, kinds: ['openssl'] } })

    render(<GitLab lang="de" />)

    expect(await screen.findByText('Lab auf diesem Server nicht aktiviert')).toBeTruthy()
    const runButton = screen.getByRole('button', { name: 'Ausführen' }) as HTMLButtonElement
    expect(runButton.disabled).toBe(true)
  })

  it('zeigt immer den Hinweis, dass clone/fetch/push/pull mangels Netzwerk fehlschlagen', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true, kinds: ['git'] } })

    render(<GitLab lang="de" />)

    expect(await screen.findByText('Kein Netzwerk im Runner')).toBeTruthy()
  })

  it('setzt Dateien und Befehle aus einer Vorlage', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true, kinds: ['git'] } })

    render(<GitLab lang="de" />)
    await screen.findByRole('button', { name: 'Ausführen' })

    fireEvent.click(screen.getByRole('button', { name: 'Worktree anlegen und auflisten' }))

    expect(screen.getByDisplayValue('worktree list')).toBeTruthy()
  })

  it('führt einen Lauf aus und zeigt die echte Ausgabe', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true, kinds: ['git'] } })
    vi.mocked(api.post).mockResolvedValue({ data: runResult() })

    render(<GitLab lang="de" />)
    const runButton = await screen.findByRole('button', { name: 'Ausführen' }) as HTMLButtonElement
    expect(runButton.disabled).toBe(false)

    fireEvent.click(runButton)

    expect(await screen.findByText(/Initialized empty Git repository/)).toBeTruthy()
    expect(api.post).toHaveBeenCalledWith('/lab/run', expect.objectContaining({ kind: 'git' }))
  })

  it('lehnt einen 7. Befehl clientseitig ab (Grenze: höchstens 6 Befehle)', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true, kinds: ['git'] } })

    render(<GitLab lang="de" />)
    const addCommandButton = await screen.findByRole('button', { name: '+ Befehl' })

    // Vorlage "Repository anlegen + erster Commit" (Standard) hat 3 Befehle -> 4 weitere ergeben 7.
    fireEvent.click(addCommandButton)
    fireEvent.click(addCommandButton)
    fireEvent.click(addCommandButton)
    fireEvent.click(addCommandButton)

    expect(await screen.findByText('Höchstens 6 Befehle pro Lauf.')).toBeTruthy()
    const runButton = screen.getByRole('button', { name: 'Ausführen' }) as HTMLButtonElement
    expect(runButton.disabled).toBe(true)
    expect(api.post).not.toHaveBeenCalled()
  })
})
