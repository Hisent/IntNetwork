import type { Block } from '@/types'

export interface TrainerComment {
  id: number
  module_key: string
  block_index: number
  body: string
  author_kind: string
  author_name: string
  created_at: string
  own: boolean
}

export interface CommentGroup {
  moduleKey: string
  blockIndex: number
  items: TrainerComment[]
}

export function groupByModuleBlock(comments: TrainerComment[]): CommentGroup[] {
  const map = new Map<string, CommentGroup>()
  for (const c of comments) {
    const k = `${c.module_key}#${c.block_index}`
    let g = map.get(k)
    if (!g) {
      g = { moduleKey: c.module_key, blockIndex: c.block_index, items: [] }
      map.set(k, g)
    }
    g.items.push(c)
  }
  return [...map.values()]
}

export function blockSnippet(block: Block | undefined, maxLen = 60): string {
  if (!block || block.type !== 'text') return ''
  const text = block.value.replace(/[#*`]/g, ' ').replace(/\s+/g, ' ').trim()
  return text.length > maxLen ? text.slice(0, maxLen) + '…' : text
}
