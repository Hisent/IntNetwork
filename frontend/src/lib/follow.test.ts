// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { dismiss, followHref, followTarget, loadDismissed } from './follow'
import type { Follow, ModuleMeta } from '@/types'

const mod = (key: string, prerequisites: string[] = []): ModuleMeta => ({ key, title: key, title_en: key, order: 1, prerequisites })
const modules = [mod('a'), mod('b', ['a']), mod('c')]
const at = (module_key: string, block_uid: string | null = null): Follow => ({ module_key, block_uid, updated_at: '' })

afterEach(() => sessionStorage.clear())

describe('followTarget', () => {
  it('zeigt das Modul des Trainers, wenn es offen steht und der Teilnehmer woanders ist', () => {
    expect(followTarget(at('c'), 'a', modules, [], [])?.key).toBe('c')
    expect(followTarget(at('c'), null, modules, [], [])?.key).toBe('c')  // Kursübersicht
  })

  it('kein Hinweis: nichts geteilt, schon dort, weggeklickt', () => {
    expect(followTarget(null, 'a', modules, [], [])).toBeNull()
    expect(followTarget(undefined, 'a', modules, [], [])).toBeNull()
    expect(followTarget(at('a', 'x'), 'a', modules, [], [])).toBeNull()
    expect(followTarget(at('c'), 'a', modules, [], ['c'])).toBeNull()
  })

  it('kein Hinweis auf ein Modul, das (noch) nicht offen steht', () => {
    expect(followTarget(at('b'), 'c', modules, [], [])).toBeNull()  // Voraussetzung a offen
    expect(followTarget(at('b'), 'c', modules, [{ module_key: 'a', done: true, best: 100 }], [])?.key).toBe('b')
    expect(followTarget(at('fremd'), 'a', modules, [], [])).toBeNull()  // nicht im Kurs
  })
})

describe('followHref', () => {
  it('springt mit Block per #b-<uid> (wie ein Suchtreffer)', () => {
    expect(followHref(at('c'))).toBe('/lernen/c')
    expect(followHref(at('c', 'b 1'))).toBe('/lernen/c#b-b%201')
  })
})

describe('dismiss', () => {
  it('merkt weggeklickte Module je Tab, ohne Doppelte', () => {
    expect(loadDismissed()).toEqual([])
    expect(dismiss(dismiss([], 'c'), 'c')).toEqual(['c'])
    expect(loadDismissed()).toEqual(['c'])
    sessionStorage.setItem('intlab-follow-dismissed', '{kaputt')
    expect(loadDismissed()).toEqual([])
  })
})
