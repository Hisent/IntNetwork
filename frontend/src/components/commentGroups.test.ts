import { describe, it, expect } from 'vitest'
import { groupByModuleBlock, blockSnippet, type TrainerComment } from './commentGroups'
import type { Block } from '@/types'

const mk = (id: number, module_key: string, block_index: number): TrainerComment => ({
  id, module_key, block_index, body: 'x', author_kind: 'participant', author_name: 'A',
  created_at: '2026-07-01T10:00:00', own: false,
})

describe('groupByModuleBlock', () => {
  it('gruppiert nach Modul + Block', () => {
    const g = groupByModuleBlock([mk(1, 'vlan', 0), mk(2, 'vlan', 0), mk(3, 'vlan', 2)])
    expect(g).toHaveLength(2)
    expect(g[0]).toMatchObject({ moduleKey: 'vlan', blockIndex: 0 })
    expect(g[0].items).toHaveLength(2)
    expect(g[1].blockIndex).toBe(2)
  })
})

describe('blockSnippet', () => {
  it('kürzt Text-Blöcke und entfernt Markdown-Zeichen', () => {
    const b: Block = { type: 'text', value: '## Titel\n\nEin **langer** Satz zum Thema Netzwerk und Switching hier.' }
    const s = blockSnippet(b, 20)
    expect(s.length).toBeLessThanOrEqual(21)
    expect(s).not.toContain('#')
    expect(s.endsWith('…')).toBe(true)
  })
  it('leer für Nicht-Text-Blöcke', () => {
    expect(blockSnippet({ type: 'widget', id: 'x' })).toBe('')
    expect(blockSnippet(undefined)).toBe('')
  })
})
