export type ActionId = 'session' | 'prompt' | 'edit' | 'bash'

export interface TimelineStep {
  event: string
  fires: boolean
  detail: string
}

interface Ev {
  event: string
  fires: boolean
  de: string
  en: string
}

// Beispiel-Hook-Setup: SessionStart legt Kontext bei, PostToolUse(Write|Edit)
// formatiert, PreToolUse(Bash) prüft/blockt riskante Kommandos.
const CHAINS: Record<ActionId, Ev[]> = {
  session: [
    { event: 'SessionStart', fires: true, de: 'Beispiel-Hook legt Branch/Issues bei.', en: 'example hook injects branch/issues.' },
  ],
  prompt: [
    { event: 'UserPromptSubmit', fires: false, de: 'vor der Verarbeitung des Prompts', en: 'before the prompt is processed' },
    { event: 'Stop', fires: false, de: 'Claude ist mit der Antwort fertig', en: 'Claude finished responding' },
  ],
  edit: [
    { event: 'UserPromptSubmit', fires: false, de: 'Aufgabe kommt an', en: 'task arrives' },
    { event: 'PreToolUse', fires: false, de: 'vor dem Edit (kein Matcher trifft)', en: 'before the edit (no matcher hits)' },
    { event: 'PostToolUse', fires: true, de: 'matcher Write|Edit → Formatter läuft', en: 'matcher Write|Edit → formatter runs' },
    { event: 'Stop', fires: false, de: 'Turn endet', en: 'turn ends' },
  ],
  bash: [
    { event: 'UserPromptSubmit', fires: false, de: 'Aufgabe kommt an', en: 'task arrives' },
    { event: 'PreToolUse', fires: true, de: 'matcher Bash → riskante Kommandos werden geprüft/geblockt', en: 'matcher Bash → risky commands are checked/blocked' },
    { event: 'PostToolUse', fires: false, de: 'nach der Ausführung', en: 'after execution' },
    { event: 'Stop', fires: false, de: 'Turn endet', en: 'turn ends' },
  ],
}

export function timeline(action: ActionId, lang: 'de' | 'en'): TimelineStep[] {
  return CHAINS[action].map((e) => ({
    event: e.event,
    fires: e.fires,
    detail: lang === 'en' ? e.en : e.de,
  }))
}
