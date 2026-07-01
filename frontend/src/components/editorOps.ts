import type { EditorBlock, EditorQuestion } from '@/lib/trainerApi'

export function moveItem<T>(items: T[], index: number, dir: -1 | 1): T[] {
  const target = index + dir
  if (target < 0 || target >= items.length) return items
  const copy = [...items]
  ;[copy[index], copy[target]] = [copy[target], copy[index]]
  return copy
}

export function removeAt<T>(items: T[], index: number): T[] {
  return items.filter((_, i) => i !== index)
}

export function addOption(de: string[], en: string[]): [string[], string[]] {
  return [[...de, ''], [...en, '']]
}

export function removeOption(de: string[], en: string[], index: number): [string[], string[]] {
  return [removeAt(de, index), removeAt(en, index)]
}

export const emptyBlock = (): EditorBlock => ({ type: 'text', value_de: '', value_en: '', note: '' })
export const emptyQuestion = (): EditorQuestion => ({
  qtype: 'single', prompt_de: '', prompt_en: '', options_de: [''], options_en: [''], answer: 0,
})
