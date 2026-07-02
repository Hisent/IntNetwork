export type Block =
  | { type: 'text'; value: string; note?: string }
  | { type: 'widget'; id: string; note?: string }
  | { type: 'check'; kind?: 'choice' | 'number'; prompt: string; options: string[]; answer: number; note?: string }
  | { type: 'reveal'; teaser: string; value: string; note?: string }
  | { type: 'order'; prompt: string; items: string[]; note?: string }
  | { type: 'debug'; prompt: string; lines: string[]; wrong: number[]; explanation: string; note?: string }
  | { type: 'reflect'; prompt: string; note?: string }

export type Question =
  | { id: string; type: 'single'; prompt: string; options: string[]; answer?: number }
  | { id: string; type: 'multi'; prompt: string; options: string[]; answer?: number[] }
  | { id: string; type: 'number'; prompt: string; answer?: number }

export interface ModuleDetail {
  key: string
  title: string
  order: number
  scenario?: string
  prerequisites: string[]
  blocks: Block[]
  quiz: { questions: Question[] }
}

export interface TrainerModuleDetail extends ModuleDetail { goals?: string[] }

export interface ModuleMeta { key: string; title: string; title_en: string; order: number; prerequisites: string[] }
export interface ProgressItem { module_key: string; done: boolean; best: number | null }
export interface Company { name: string; blurb: string; sites: string[]; devices: string[] }
