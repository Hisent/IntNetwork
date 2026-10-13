// @vitest-environment jsdom
import { describe, expect, it, vi } from 'vitest'

vi.mock('@/lib/api', () => ({ api: { get: vi.fn(), post: vi.fn() } }))

import { isSnapshot } from './useFileCommandLab'
import { validateLabRun } from './limits'

describe('isSnapshot (strenge Prüfung des gespeicherten Stands)', () => {
  const ok = { templateId: 't', files: [{ name: 'a.txt', content: 'x' }], commands: ['init'] }

  it('akzeptiert einen vollständigen Stand, auch mit leeren Listen', () => {
    expect(isSnapshot(ok)).toBe(true)
    expect(isSnapshot({ templateId: 't', files: [], commands: [] })).toBe(true)
  })

  it('lehnt Stände mit falsch geformten Elementen ab', () => {
    for (const bad of [
      null, 'x', [],
      { ...ok, templateId: 1 },
      { ...ok, files: 'a.txt' },
      { ...ok, files: [null] },
      { ...ok, files: ['a.txt'] },
      { ...ok, files: [{ name: 'a.txt' }] },
      { ...ok, files: [{ name: 1, content: 'x' }] },
      { ...ok, files: [{ name: 'a.txt', content: null }] },
      { ...ok, commands: [42] },
      { ...ok, commands: ['init', null] },
    ]) expect(isSnapshot(bad)).toBe(false)
  })
})

describe('validateLabRun: doppelte Dateinamen', () => {
  it('meldet einen doppelten Namen zweisprachig, statt ihn still zu überschreiben', () => {
    const v = validateLabRun([{ name: 'a.txt', content: '1' }, { name: 'b.txt', content: '' }, { name: 'a.txt', content: '2' }], ['init'])
    expect(v?.de).toContain('"a.txt" kommt mehrfach vor')
    expect(v?.en).toContain('"a.txt" is used more than once')
  })

  it('lässt unterschiedliche Namen durch', () => {
    expect(validateLabRun([{ name: 'a.txt', content: '1' }, { name: 'A.txt', content: '2' }], ['init'])).toBeNull()
  })
})
