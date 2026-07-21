import { describe, expect, it } from 'vitest'
import { groupModulesBySection } from './moduleGroups'
import type { ModuleMeta } from '@/types'

function mod(key: string, order: number): ModuleMeta {
  return { key, title: key, title_en: key, order, prerequisites: [] }
}

describe('groupModulesBySection', () => {
  it('splits modules into the given sections by order range', () => {
    const modules = [mod('a', 1), mod('b', 2), mod('c', 3)]
    const sections = [
      { key: 'day1', from: 1, to: 2, title_de: 'Tag 1', title_en: 'Day 1' },
      { key: 'day2', from: 3, to: 3, title_de: 'Tag 2', title_en: 'Day 2' },
    ]
    const groups = groupModulesBySection(modules, sections)
    expect(groups).toHaveLength(2)
    expect(groups[0].modules.map((m) => m.key)).toEqual(['a', 'b'])
    expect(groups[1].modules.map((m) => m.key)).toEqual(['c'])
  })

  it('drops sections that end up with no modules', () => {
    const modules = [mod('a', 1)]
    const sections = [
      { key: 'day1', from: 1, to: 1, title_de: 'Tag 1', title_en: 'Day 1' },
      { key: 'day2', from: 2, to: 5, title_de: 'Tag 2', title_en: 'Day 2' },
    ]
    const groups = groupModulesBySection(modules, sections)
    expect(groups.map((g) => g.key)).toEqual(['day1'])
  })

  it('falls back to a single "Module" group when no sections are given', () => {
    const modules = [mod('b', 2), mod('a', 1)]
    const groups = groupModulesBySection(modules)
    expect(groups).toHaveLength(1)
    expect(groups[0].modules.map((m) => m.key)).toEqual(['a', 'b'])
  })

  it('sorts modules by order within each group regardless of input order', () => {
    const modules = [mod('c', 3), mod('a', 1), mod('b', 2)]
    const groups = groupModulesBySection(modules, [{ key: 'all', from: 0, to: 10, title_de: 'Alle', title_en: 'All' }])
    expect(groups[0].modules.map((m) => m.key)).toEqual(['a', 'b', 'c'])
  })
})
