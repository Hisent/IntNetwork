import { describe, expect, it } from 'vitest'
import { GIT_TEMPLATES, templateById } from './templates'
import { validateLabRun, filesFromRecord, runMeetsExpectation } from '@/widgets/lab/limits'

// Hintergrund (mit echtem git über runner/worker.py nachgestellt, Review 2026-10):
// Das Arbeitsverzeichnis bleibt erhalten, und der Runner schreibt die Dateien
// einer Vorlage bei JEDEM Lauf neu.
describe('git-Vorlagen', () => {
  it('jede Vorlage hält die Lab-Grenzen ein', () => {
    for (const t of GIT_TEMPLATES) expect(validateLabRun(filesFromRecord(t.files), t.commands)).toBeNull()
  })

  it('keine Vorlage legt einen Zweig mit "checkout -b" an (scheitert beim zweiten Lauf)', () => {
    for (const t of GIT_TEMPLATES) for (const c of t.commands) expect(c).not.toMatch(/^checkout -b\b/)
  })

  it('der Konflikt-Folgeschritt bringt keine Dateien mit und endet mit dem Merge', () => {
    const t = templateById('merge-konflikt-2')
    expect(t.id).toBe('merge-konflikt-2')
    expect(t.files).toEqual({})
    expect(t.commands[0]).toBe('checkout -')
    expect(t.commands[t.commands.length - 1]).toBe('merge feature')
    // Ein Befehl nach dem fehlschlagenden Merge liefe nie (Abbruch beim ersten rc != 0).
    expect(templateById('merge-konflikt').hint.de).toContain('Schritt 2')
  })

  it('der Konflikt-Folgeschritt gilt als gelöst, wenn der Merge "CONFLICT" meldet (rc 1), nicht bei rc 0', () => {
    const t = templateById('merge-konflikt-2')
    const run = (rc: number, output: string) => ({ rc, output, truncated: false, duration_ms: 1, timed_out: false })
    const conflict = '$ git commit -m main-edit\n[main 1a2b3c4] main-edit\n$ git merge feature\nCONFLICT (content): Merge conflict in shared.txt\n'
    expect(runMeetsExpectation(run(1, conflict), t.expect)).toBe(true)
    expect(runMeetsExpectation(run(0, '$ git merge feature\nAlready up to date.\n'), t.expect)).toBe(false)
    expect(runMeetsExpectation(run(1, '$ git commit -m main-edit\nnothing to commit\n'), t.expect)).toBe(false)
    expect(GIT_TEMPLATES.filter((x) => x.expect).map((x) => x.id)).toEqual(['merge-konflikt-2'])
  })
})
