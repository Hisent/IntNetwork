import type { WorkshopThemeName } from '@/lib/workshopTheme'
import type { ClozeData, DiagramData, MatchData, ScenarioData, TerminalData } from '@/components/blocks/types'

export type Block =
  | { type: 'text'; value: string; note?: string }
  | { type: 'widget'; id: string; note?: string }
  | { type: 'check'; kind?: 'choice' | 'number'; prompt: string; options: string[]; answer: number; note?: string }
  | { type: 'reveal'; teaser: string; value: string; note?: string }
  | { type: 'order'; prompt: string; items: string[]; note?: string }
  | { type: 'debug'; prompt: string; lines: string[]; wrong: number[]; explanation: string; note?: string }
  | { type: 'reflect'; prompt: string; note?: string }
  // deklarativer Baukasten (docs/content-authoring.md) — Payload flach im Block
  | ({ type: 'diagram'; note?: string } & DiagramData)
  | ({ type: 'terminal'; note?: string } & TerminalData)
  | ({ type: 'match'; note?: string } & MatchData)
  | ({ type: 'cloze'; note?: string } & ClozeData)
  | ({ type: 'scenario'; note?: string } & ScenarioData)

// answer und explanation kennt nur die Trainer-Ansicht; Teilnehmer bekommen die
// Erklärungen erst mit dem bewerteten Ergebnis (learnApi.submitQuiz).
export type Question = { id: string; prompt: string; explanation?: string } & (
  | { type: 'single'; options: string[]; answer?: number }
  | { type: 'multi'; options: string[]; answer?: number[] }
  | { type: 'number'; answer?: number })

export interface ModuleDetail {
  key: string
  workshop_key?: string | null
  title: string
  order: number
  scenario?: string
  prerequisites: string[]
  blocks: Block[]
  quiz: { questions: Question[] }
}

export interface TrainerModuleDetail extends ModuleDetail { goals?: string[] }

export interface ModuleMeta { key: string; title: string; title_en: string; order: number; prerequisites: string[]; workshop_key?: string }
export interface ProgressItem { module_key: string; done: boolean; best: number | null }
export interface Company { name: string; blurb: string; sites: string[]; devices: string[] }
export interface Workshop {
  key: string
  title: Record<'de' | 'en', string>
  summary?: Record<'de' | 'en', string>
  theme: WorkshopThemeName
  sections: { key: string; from: number; to: number; title_de: string; title_en: string }[]
  context?: { name: string; blurb_de: string; blurb_en: string } | null
}
export interface WorkshopDetail extends Workshop {
  modules: { key: string; title: Record<'de' | 'en', string>; order: number }[]
}
