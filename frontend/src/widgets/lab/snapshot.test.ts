// @vitest-environment jsdom
//
// Reine Logik rund um den Pro-Teilnehmer-Snapshot, den alle drei
// Lab-Widgets aus localStorage lesen (readSnapshot). Deckt genau die Fälle
// ab, die die einzelnen loadSnapshot()-Funktionen (Ansible/Openssl/Git)
// bisher inline getestet haben: kein Key, kein Eintrag, beschädigtes JSON,
// ein Eintrag, der den Type-Guard nicht besteht, und der Erfolgsfall.
import { afterEach, describe, expect, it } from 'vitest'
import { readSnapshot } from './snapshot'

interface Sample {
  id: string
}

function isSample(parsed: unknown): parsed is Sample {
  return typeof parsed === 'object' && parsed !== null && typeof (parsed as Record<string, unknown>).id === 'string'
}

afterEach(() => {
  localStorage.clear()
})

describe('readSnapshot', () => {
  it('liefert die Vorlage, wenn kein storageKey vorhanden ist', () => {
    expect(readSnapshot(null, isSample, () => ({ id: 'fallback' }))).toEqual({ id: 'fallback' })
  })

  it('liefert die Vorlage, wenn noch kein Eintrag existiert', () => {
    expect(readSnapshot('missing-key', isSample, () => ({ id: 'fallback' }))).toEqual({ id: 'fallback' })
  })

  it('liefert die Vorlage bei beschädigtem JSON statt zu werfen', () => {
    localStorage.setItem('broken-key', '{not json')
    expect(readSnapshot('broken-key', isSample, () => ({ id: 'fallback' }))).toEqual({ id: 'fallback' })
  })

  it('liefert die Vorlage, wenn der gespeicherte Eintrag den Type-Guard nicht besteht', () => {
    localStorage.setItem('wrong-shape', JSON.stringify({ id: 42 }))
    expect(readSnapshot('wrong-shape', isSample, () => ({ id: 'fallback' }))).toEqual({ id: 'fallback' })
  })

  it('liefert den gespeicherten Eintrag, wenn er den Type-Guard besteht', () => {
    localStorage.setItem('good-key', JSON.stringify({ id: 'stored' }))
    expect(readSnapshot('good-key', isSample, () => ({ id: 'fallback' }))).toEqual({ id: 'stored' })
  })
})
