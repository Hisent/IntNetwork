export type CliMode = 'normal' | 'plan' | 'accept'

export interface CliResult {
  output: string
}

// Stark vereinfachte Nachbildung der Claude-Code-Prompt-Zeile — nur zur
// Veranschaulichung der eingebauten Slash-Commands. "__CLEAR__" signalisiert
// der UI, den Verlauf zu leeren.
export function runCommand(input: string, mode: CliMode, lang: 'de' | 'en'): CliResult {
  const cmd = input.trim()
  const de = lang !== 'en'
  if (cmd === '') return { output: '' }
  if (!cmd.startsWith('/')) {
    return {
      output: de
        ? `» Aufgabe an Claude Code übergeben (Modus: ${mode}). In dieser Demo laufen nur Slash-Commands.`
        : `» Task handed to Claude Code (mode: ${mode}). This demo only runs slash commands.`,
    }
  }
  const name = cmd.split(/\s+/)[0]
  switch (name) {
    case '/help':
      return { output: '/help /context /compact /clear /status /model /init /memory' }
    case '/context':
      return {
        output: de
          ? 'Kontextfenster: 42% belegt — System 8%, CLAUDE.md 6%, Verlauf 21%, Tools 7%.'
          : 'Context window: 42% used — system 8%, CLAUDE.md 6%, history 21%, tools 7%.',
      }
    case '/compact':
      return {
        output: de
          ? 'Verlauf verdichtet. Kontext wieder frei (~14% belegt).'
          : 'History compacted. Context freed up (~14% used).',
      }
    case '/clear':
      return { output: '__CLEAR__' }
    case '/status':
      return { output: de ? `Angemeldet · Modell: sonnet · Modus: ${mode}` : `Signed in · model: sonnet · mode: ${mode}` }
    case '/model':
      return { output: de ? 'Modell wechseln (Demo): sonnet ⇄ opus ⇄ haiku' : 'Switch model (demo): sonnet ⇄ opus ⇄ haiku' }
    case '/init':
      return {
        output: de
          ? 'Analysiere Repo … CLAUDE.md erzeugt (Build-/Test-Befehle, Konventionen).'
          : 'Analyzing repo … generated CLAUDE.md (build/test commands, conventions).',
      }
    case '/memory':
      return {
        output: de
          ? 'Memory: CLAUDE.md (Projekt), ~/.claude/CLAUDE.md (User).'
          : 'Memory: CLAUDE.md (project), ~/.claude/CLAUDE.md (user).',
      }
    default:
      return { output: de ? `Unbekannter Befehl: ${name}. Tippe /help.` : `Unknown command: ${name}. Type /help.` }
  }
}
