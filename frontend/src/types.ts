import type { WorkshopThemeName } from '@/lib/workshopTheme'
import type { ClozeData, DiagramData, MatchData, ScenarioData, TerminalData } from '@/components/blocks/types'

// uid: stabile Kennung des Blocks im Modul (Sprungziel der Suche, Schlüssel des Übungsstands)
export type Block = { uid?: string | null } & (
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
  | ({ type: 'scenario'; note?: string } & ScenarioData))

// answer und explanation kennt nur die Trainer-Ansicht; Teilnehmer bekommen die
// Erklärungen erst mit dem bewerteten Ergebnis (learnApi.submitQuiz).
export type Question = { id: string; prompt: string; explanation?: string } & (
  | { type: 'single'; options: string[]; answer?: number }
  | { type: 'multi'; options: string[]; answer?: number[] }
  | { type: 'number'; answer?: number })

export interface ModuleDetail {
  key: string
  workshop_key?: string | null
  title: string  // deutsch; Anzeige über localTitle() (lib/i18n.ts)
  title_en?: string
  order: number
  scenario?: string
  goals?: string[]  // in der Teilnehmersprache (Fallback Deutsch)
  prerequisites: string[]
  blocks: Block[]
  quiz: { questions: Question[] }
}

export type TrainerModuleDetail = ModuleDetail

export interface ModuleMeta { key: string; title: string; title_en: string; order: number; prerequisites: string[]; workshop_key?: string; minutes?: number }
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

// Live-Abstimmung. Teilnehmer bekommen my_choice und erst bei status "revealed"
// counts/votes/answer/explanation; der Trainer sieht diese Felder immer.
export interface LivePoll {
  id: number
  status: 'open' | 'revealed'
  prompt: string
  options: string[]  // feste Reihenfolge — Beamer und Teilnehmer sehen dieselben Buchstaben
  my_choice?: number | null
  counts?: number[]
  votes?: number
  answer?: number
  explanation?: string | null
}
