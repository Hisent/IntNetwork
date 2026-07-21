import { describe, expect, it } from 'vitest'
import { modulePositions } from './modulePosition'
import type { ModuleMeta } from '@/types'

function mod(key: string, order: number): ModuleMeta {
  return { key, title: key, title_en: key, order, prerequisites: [] }
}

describe('modulePositions', () => {
  it('maps modules to 1-based positions in order', () => {
    const modules = [mod('a', 1), mod('b', 2), mod('c', 3)]
    const positions = modulePositions(modules)
    expect(positions.get('a')).toBe(1)
    expect(positions.get('b')).toBe(2)
    expect(positions.get('c')).toBe(3)
  })

  it('sorts by order regardless of input array order', () => {
    const modules = [mod('c', 3), mod('a', 1), mod('b', 2)]
    const positions = modulePositions(modules)
    expect(positions.get('a')).toBe(1)
    expect(positions.get('b')).toBe(2)
    expect(positions.get('c')).toBe(3)
  })

  it('ignores the absolute order value — only relative position counts', () => {
    // Claude-Code-Workshop: order 101..118 muss trotzdem als 1..18 erscheinen.
    const modules = [mod('m101', 101), mod('m102', 102), mod('m118', 118)]
    const positions = modulePositions(modules)
    expect(positions.get('m101')).toBe(1)
    expect(positions.get('m102')).toBe(2)
    expect(positions.get('m118')).toBe(3)
  })

  it('returns an empty map for an empty list', () => {
    expect(modulePositions([]).size).toBe(0)
  })
})
