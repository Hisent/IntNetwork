export type Block =
  | { type: 'text'; value: string }
  | { type: 'image'; url: string; alt?: string }
  | { type: 'widget'; id: string }

export type Question =
  | { id: string; type: 'single'; prompt: string; options: string[] }
  | { id: string; type: 'multi'; prompt: string; options: string[] }
  | { id: string; type: 'number'; prompt: string }

export interface ModuleDetail {
  key: string
  title: string
  blocks: Block[]
  quiz: { questions: Question[] }
}

export interface ModuleMeta { key: string; title: string; order: number }
export interface ProgressItem { module_key: string; done: boolean; best: number | null }
