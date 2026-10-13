// Ausgelieferte (bereits sprachaufgelöste) Form der deklarativen Blocktypen.
// Quelle der Wahrheit für Felder und Grenzen: docs/content-authoring.md und
// backend/app/services/block_validation.py.

import type { Block } from '@/types'

export type DeclarativeBlockData = Extract<Block, { type: 'diagram' | 'terminal' | 'match' | 'cloze' | 'scenario' }>

export function isDeclarative(b: Block): b is DeclarativeBlockData {
  return b.type === 'diagram' || b.type === 'terminal' || b.type === 'match' || b.type === 'cloze' || b.type === 'scenario'
}

export type SeqStyle = 'request' | 'reply' | 'broadcast' | 'multicast' | 'encrypted'
export type FlowShape = 'host' | 'switch' | 'router' | 'firewall' | 'server' | 'cloud' | 'database' | 'user' | 'process' | 'decision'

export interface SequenceDiagram {
  kind: 'sequence'; title: string; caption?: string
  actors: { id: string; label: string }[]
  /** `to` als Liste = dieselbe Nachricht parallel an mehrere Empfänger */
  messages: { from: string; to: string | string[]; label: string; detail?: string; style?: SeqStyle; at?: string; divider?: string }[]
}
export interface LayersDiagram {
  kind: 'layers'; title: string; caption?: string
  layers: { name: string; content?: string; pdu?: string; detail?: string }[]
}
export interface FlowNode { id: string; label: string; shape?: FlowShape; row: number; col: number; detail?: string }
export interface FlowEdge { id?: string; from: string; to: string; label?: string; detail?: string; style?: 'solid' | 'dashed'; arrow?: 'end' | 'both' | 'none' }
export interface FlowDiagram {
  kind: 'flow'; title: string; caption?: string
  nodes: FlowNode[]
  edges?: FlowEdge[]
  steps?: { highlight: string[]; text: string }[]
}
export interface CompareDiagram {
  kind: 'compare'; title: string; caption?: string
  columns: { title: string }[]
  rows: { label: string; values: string[]; mono?: boolean; detail?: string }[]
}
export type DiagramData = SequenceDiagram | LayersDiagram | FlowDiagram | CompareDiagram

export interface TerminalCommand {
  cmd: string; aliases?: string[]; output: string; desc?: string; prompt?: string; chip?: boolean; label?: string
  sets?: string[]; clears?: string[]; variants?: { when: string; output: string }[]
}
export interface TerminalTask { text: string; command?: string; answers?: string[]; explanation?: string }
export interface TerminalData {
  title?: string; prompt: string; intro?: string; unknown?: string
  abbreviations?: boolean; case_sensitive?: boolean; wrap?: boolean
  commands: TerminalCommand[]
  tasks?: TerminalTask[]
}

export interface MatchData { prompt: string; pairs: { left: string; right: string }[]; explanation?: string }

export interface ClozeGap { id: string; options?: string[]; answer?: number | number[]; accept?: string[]; case_sensitive?: boolean; strict_whitespace?: boolean }
export interface ClozeData { prompt: string; text: string; mono?: boolean; options?: string[]; gaps: ClozeGap[]; explanation?: string }

export interface ScenarioNode { id: string; text: string; options?: { label: string; to: string }[]; outcome?: 'good' | 'ok' | 'bad' }
export interface ScenarioData { title: string; start: string; nodes: ScenarioNode[] }
