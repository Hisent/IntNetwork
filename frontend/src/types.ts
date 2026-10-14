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
// das Ergebnis (counts/votes/mean/answers/words, bei Inhaltsfragen answer/explanation);
// der Trainer sieht es immer, bei Freitext samt ausgeblendeter Antworten und deren id.
export type PollKind = 'single' | 'multi' | 'scale' | 'text' | 'words'
export type PollChoice = number | number[] | string | string[]
export interface LivePoll {
  id: number
  kind?: PollKind  // fehlt = single
  status: 'open' | 'revealed'
  prompt: string
  options?: string[]  // single/multi; feste Reihenfolge — Beamer und Teilnehmer sehen dieselben Buchstaben
  max_selections?: number  // multi
  min?: number; max?: number; label_min?: string; label_max?: string  // scale
  my_choice?: PollChoice | null
  counts?: number[]  // single/multi je Option, scale je Wert ab min
  votes?: number
  mean?: number | null
  answers?: { id?: number; text: string; hidden?: boolean }[]  // text
  words?: { word: string; count: number }[]  // words, häufigste zuerst
  answer?: number | number[]
  explanation?: string | null
}
export interface AdhocPoll {
  kind: Exclude<PollKind, 'single'>
  prompt: string
  options?: string[]
  max_selections?: number | null
  min?: number; max?: number; label_min?: string; label_max?: string
}
