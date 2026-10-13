import { describe, expect, it } from 'vitest'
import { MODULE_TEMPLATES, OPENSSL_TEMPLATES, templateById } from './templates'
import { validateLabRun, filesFromRecord } from '@/widgets/lab/limits'

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

  it('die Widerruf-Vorlage sagt, wie die Aufgabe "Rückgabewert 0" trotz erwartetem Fehler erfüllbar ist', () => {
    const t = templateById('widerruf-pruefen')
    expect(t.hint.de).toContain('Rückgabewert 0')
    expect(t.hint.en).toContain('return 0')
  })
})
