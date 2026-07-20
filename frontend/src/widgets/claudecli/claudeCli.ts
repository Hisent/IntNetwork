export type CliMode = 'default' | 'plan' | 'acceptEdits'

export interface CliResult {
  output: string
}

export interface TerminalState {
  files: Record<string, string>
}

export function createTerminalState(): TerminalState {
  return {
    files: {
      'README.md': '# Claude-Code-Workspace\n\nDies ist ein isolierter Browser-Prototyp.',
      'src/app.ts': 'export const answer = 42\n',
    },
  }
}

export function runTerminalCommand(
  state: TerminalState,
  input: string,
  lang: 'de' | 'en',
): { output: string; state: TerminalState } {
  const cmd = input.trim()
  const de = lang !== 'en'
  const [name, ...args] = cmd.split(/\s+/)
  if (cmd === '') return { output: '', state }

  switch (name) {
    case 'help':
      return {
        output: de
          ? 'Befehle: help · pwd · ls · cat <datei> · echo <text> > <datei> · touch <datei> · whoami · clear'
          : 'Commands: help · pwd · ls · cat <file> · echo <text> > <file> · touch <file> · whoami · clear',
        state,
      }
    case 'pwd':
      return { output: '/workspace', state }
    case 'ls':
      return { output: Object.keys(state.files).sort().join('  '), state }
    case 'cat': {
      const file = args[0]
      if (!file) return { output: de ? 'Nutzung: cat <datei>' : 'Usage: cat <file>', state }
      return {
        output: state.files[file] ?? (de ? 'Datei nicht gefunden: ' + file : 'File not found: ' + file),
        state,
      }
    }
    case 'touch': {
      const file = args[0]
      if (!file) return { output: de ? 'Nutzung: touch <datei>' : 'Usage: touch <file>', state }
      return { output: '', state: { files: { ...state.files, [file]: state.files[file] ?? '' } } }
    }
    case 'echo': {
      const redirect = cmd.match(/^echo\s+(.+?)\s*>\s*(\S+)$/)
      if (!redirect) return { output: args.join(' '), state }
      const [, value, file] = redirect
      return { output: '', state: { files: { ...state.files, [file]: value } } }
    }
    case 'whoami':
      return { output: 'participant (sandbox prototype)', state }
    case 'clear':
      return { output: '__CLEAR__', state }
    default:
      return {
        output: de ? name + ': Befehl nicht gefunden. Tippe help.' : name + ': command not found. Type help.',
        state,
      }
  }
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
