import { createTerminalState, type CliMode, type TerminalState } from '@/widgets/claudecli/claudeCli'

export interface CliSnapshot { mode: CliMode; lines: string[]; terminal: TerminalState; solved: boolean; sessionId: string }

export const newSessionId = () => Math.random().toString(36).slice(2, 8)

// Startmodus einer frischen Session: laut code.claude.com/docs/en/permission-modes
// ist Auto ab Claude Code v2.1.283 der eingebaute Startmodus interaktiver
// Terminal-Sessions (vorher nur Pro/Max/Team; HIPAA-Organisationen: Manual).
export const START_MODE: CliMode = 'auto'

// Pro Teilnehmer gespeichert (localStorage, wie Lese-Merker/Reflexionen) — die
// Session überlebt Reload und gehört dem eingeloggten Teilnehmer, nicht dem Browser.
export function loadSnapshot(storageKey: string | null, intro: string): CliSnapshot {
  if (storageKey) {
    try {
      const raw = localStorage.getItem(storageKey)
      if (raw) {
        const p = JSON.parse(raw)
        if (p && p.terminal?.files && Array.isArray(p.lines)) {
          return { mode: p.mode ?? START_MODE, lines: p.lines, terminal: p.terminal,
            solved: !!p.solved, sessionId: p.sessionId ?? newSessionId() }
        }
      }
    } catch {
      // beschädigter Eintrag -> frische Session
    }
  }
  return { mode: START_MODE, lines: [intro], terminal: createTerminalState(), solved: false, sessionId: newSessionId() }
}
