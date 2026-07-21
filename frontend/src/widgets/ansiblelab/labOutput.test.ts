import { describe, expect, it } from 'vitest'
import { compareIdempotency, parseRecap } from './labOutput'

const SINGLE_HOST = `
PLAY [all] *********************************************************

TASK [Gathering Facts] **********************************************
ok: [labhost]

TASK [Verzeichnis anlegen] ******************************************
changed: [labhost]

PLAY RECAP ***********************************************************
labhost                    : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
`

const MULTI_HOST = `
PLAY RECAP ***********************************************************
host1                      : ok=2    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
host2                      : ok=3    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
`

const SYNTAX_ERROR = `ERROR! couldn't resolve module/action 'filee'. This often indicates a misspelling, missing collection, or incorrect module path.`

describe('parseRecap', () => {
  it('liest ok/changed/failed/skipped aus einem einzelnen Host', () => {
    const recap = parseRecap(SINGLE_HOST)
    expect(recap).toEqual({ ok: 2, changed: 1, failed: 0, skipped: 0, hosts: 1 })
  })

  it('summiert mehrere Hosts', () => {
    const recap = parseRecap(MULTI_HOST)
    expect(recap).toEqual({ ok: 5, changed: 1, failed: 1, skipped: 1, hosts: 2 })
  })

  it('gibt null zurück, wenn kein Recap vorhanden ist (Syntaxfehler)', () => {
    expect(parseRecap(SYNTAX_ERROR)).toBeNull()
  })

  it('gibt null zurück bei leerer Ausgabe', () => {
    expect(parseRecap('')).toBeNull()
  })
})

describe('compareIdempotency', () => {
  it('liefert keine Einordnung ohne vorherigen Lauf', () => {
    expect(compareIdempotency(null, { ok: 2, changed: 1, failed: 0, skipped: 0, hosts: 1 }, 'de')).toBeNull()
  })

  it('liefert keine Einordnung ohne aktuellen Lauf (z.B. Syntaxfehler)', () => {
    expect(compareIdempotency({ ok: 2, changed: 1, failed: 0, skipped: 0, hosts: 1 }, null, 'de')).toBeNull()
  })

  it('erkennt gesunkene Änderungen als Idempotenz (DE)', () => {
    const note = compareIdempotency(
      { ok: 2, changed: 3, failed: 0, skipped: 0, hosts: 1 },
      { ok: 2, changed: 1, failed: 0, skipped: 0, hosts: 1 },
      'de',
    )
    expect(note?.kind).toBe('improved')
    expect(note?.message).toContain('1 statt 3 Änderungen')
    expect(note?.message).toContain('idempotent')
  })

  it('erkennt gesunkene Änderungen als Idempotenz (EN)', () => {
    const note = compareIdempotency(
      { ok: 2, changed: 3, failed: 0, skipped: 0, hosts: 1 },
      { ok: 2, changed: 1, failed: 0, skipped: 0, hosts: 1 },
      'en',
    )
    expect(note?.kind).toBe('improved')
    expect(note?.message).toContain('1 instead of 3 changes')
  })

  it('ordnet gleichbleibende Änderungen als "typisch für command ohne creates" ein', () => {
    const note = compareIdempotency(
      { ok: 2, changed: 1, failed: 0, skipped: 0, hosts: 1 },
      { ok: 2, changed: 1, failed: 0, skipped: 0, hosts: 1 },
      'de',
    )
    expect(note?.kind).toBe('same')
    expect(note?.message).toContain('bleiben bei 1')
    expect(note?.message).toContain('creates')
  })

  it('meldet gestiegene Änderungen als Warnsignal', () => {
    const note = compareIdempotency(
      { ok: 2, changed: 0, failed: 0, skipped: 0, hosts: 1 },
      { ok: 2, changed: 2, failed: 0, skipped: 0, hosts: 1 },
      'de',
    )
    expect(note?.kind).toBe('worse')
    expect(note?.message).toContain('0 → 2')
  })
})
