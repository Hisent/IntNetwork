import { describe, expect, it } from 'vitest'
import { MODULE_TEMPLATES, OPENSSL_TEMPLATES, templateById } from './templates'
import { validateLabRun, filesFromRecord, runMeetsExpectation } from '@/widgets/lab/limits'

describe('openssl-Vorlagen', () => {
  it('jede Modul-Vorwahl zeigt auf eine existierende Vorlage', () => {
    const ids = OPENSSL_TEMPLATES.map((t) => t.id)
    for (const list of Object.values(MODULE_TEMPLATES)) {
      expect(list.length).toBeGreaterThan(0)
      for (const id of list) expect(ids).toContain(id)
    }
  })

  it('jede Vorlage hält die Lab-Grenzen ein und ist zweisprachig beschrieben', () => {
    for (const t of OPENSSL_TEMPLATES) {
      expect(validateLabRun(filesFromRecord(t.files), t.commands)).toBeNull()
      expect(t.hint.de).not.toBe(t.hint.en)
    }
  })

  const run = (rc: number, output: string) => ({ rc, output, truncated: false, duration_ms: 1, timed_out: false })

  it('die Widerruf-Vorlage gilt als gelöst, wenn der letzte Befehl "certificate revoked" meldet (rc 2)', () => {
    const t = templateById('widerruf-pruefen')
    const revoked = '$ openssl verify gut.pem\ngut.pem: OK\n$ openssl verify gesperrt.pem\nerror 23 at 0 depth lookup: certificate revoked\n'
    expect(runMeetsExpectation(run(2, revoked), t.expect)).toBe(true)
    // rc 0 (letzter Befehl weggelassen) erfüllt die Aufgabe dieser Vorlage nicht mehr …
    expect(runMeetsExpectation(run(0, '$ openssl verify gut.pem\ngut.pem: OK\n'), t.expect)).toBe(false)
    // … ebenso wenig ein anderer Fehler mit rc 2 oder die Meldung an früherer Stelle.
    expect(runMeetsExpectation(run(2, '$ openssl verify x.pem\nerror 20: unable to get local issuer certificate\n'), t.expect)).toBe(false)
    expect(runMeetsExpectation(run(2, '$ openssl verify a\ncertificate revoked\n$ openssl verify b\nerror 20\n'), t.expect)).toBe(false)
    expect(t.expect?.task.de).toContain('certificate revoked')
    expect(t.expect?.task.en).toContain('certificate revoked')
    expect(t.hint.de).not.toContain('Rückgabewert 0')
  })

  it('ohne eigenes Kriterium zählt Rückgabewert 0; vor dem ersten Lauf ist nichts gelöst', () => {
    const t = templateById('kette-pruefen')
    expect(t.expect).toBeUndefined()
    expect(runMeetsExpectation(run(0, ''), t.expect)).toBe(true)
    expect(runMeetsExpectation(run(2, 'certificate revoked'), t.expect)).toBe(false)
    expect(runMeetsExpectation(null, t.expect)).toBe(false)
    expect(OPENSSL_TEMPLATES.filter((x) => x.expect).map((x) => x.id)).toEqual(['widerruf-pruefen'])
  })
})
