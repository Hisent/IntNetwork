import type { BlockPayload, EditorBlock, EditorQuestion } from '@/lib/trainerApi'

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

// --- deklarativer Baukasten: Payload wird als JSON bearbeitet --------------------

export const DECLARATIVE_TYPES = ['diagram', 'terminal', 'match', 'cloze', 'scenario'] as const
export type DeclarativeType = (typeof DECLARATIVE_TYPES)[number]

export function isDeclarativeType(type: string): type is DeclarativeType {
  return (DECLARATIVE_TYPES as readonly string[]).includes(type)
}

/** Kleinstes gültiges Gerüst je Typ — Startpunkt beim Typwechsel im Editor. */
export function declarativeTemplate(type: DeclarativeType): BlockPayload {
  switch (type) {
    case 'diagram':
      return {
        kind: 'sequence', title_de: 'Titel', title_en: 'Title',
        actors: [{ id: 'a', label: 'A' }, { id: 'b', label: 'B' }],
        messages: [{ from: 'a', to: 'b', label_de: 'Nachricht', label_en: 'Message' }],
      }
    case 'terminal':
      return { prompt: 'device>', commands: [{ cmd: 'show version', output: 'v1.0' }] }
    case 'match':
      return {
        prompt_de: 'Ordne zu.', prompt_en: 'Match the pairs.',
        pairs: [1, 2, 3].map((n) => ({ left: `Begriff ${n}`, right_de: `Beschreibung ${n}`, right_en: `Description ${n}` })),
      }
    case 'cloze':
      return {
        prompt_de: 'Fülle die Lücke.', prompt_en: 'Fill the gap.', mono: true,
        text: 'switchport mode [[mode]]', gaps: [{ id: 'mode', accept: ['access'] }],
      }
    case 'scenario':
      return {
        title_de: 'Titel', title_en: 'Title', start: 'start',
        nodes: [
          { id: 'start', text_de: 'Situation', text_en: 'Situation', options: [
            { label_de: 'Option A', label_en: 'Option A', to: 'gut' },
            { label_de: 'Option B', label_en: 'Option B', to: 'schlecht' },
          ] },
          { id: 'gut', outcome: 'good', text_de: 'Begründung', text_en: 'Reason' },
          { id: 'schlecht', outcome: 'bad', text_de: 'Begründung', text_en: 'Reason' },
        ],
      }
  }
}

/** JSON-Text des Editors -> Payload. Nur ein Objekt ist gültig (kein Array, keine Zahl). */
export function parsePayloadJson(text: string, notObject = 'Erwartet wird ein JSON-Objekt { … }', invalid = 'Ungültiges JSON'): { payload: BlockPayload } | { error: string } {
  try {
    const parsed: unknown = JSON.parse(text)
    if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) return { error: notObject }
    return { payload: parsed as BlockPayload }
  } catch (err) {
    return { error: err instanceof Error ? err.message : invalid }
  }
}

/** Auswahl für „Voraussetzungen“ im Editor: nur Module desselben Lehrgangs (ohne
 *  das Modul selbst). Bereits gesetzte Voraussetzungen bleiben sichtbar, auch
 *  wenn sie aus einem anderen Lehrgang stammen — sonst ließen sie sich nicht abwählen. */
export function prerequisiteChoices<T extends { key: string; workshop_key: string | null }>(
  all: T[], moduleKey: string, workshopKey: string | null | undefined, selected: string[],
): T[] {
  return all.filter((m) => m.key !== moduleKey
    && ((m.workshop_key ?? null) === (workshopKey ?? null) || selected.includes(m.key)))
}

/** Die 422-Meldung des Servers nennt bei Baukasten-Blöcken den Block:
 *  "<typ>-Block '<uid | #n>': <feldpfad>: <grund>" -> Index im Formular, sonst -1. */
export function blockIndexFromError(message: string, blocks: { uid?: string | null; widget_id?: string | null }[]): number {
  const label = message.match(/-Block '([^']+)'/)?.[1]
  if (!label) return -1
  const position = label.match(/^#(\d+)$/)
  if (position) return Number(position[1]) <= blocks.length ? Number(position[1]) - 1 : -1
  return blocks.findIndex((b) => b.uid === label || b.widget_id === label)
}
