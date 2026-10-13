export type Effect = 'allow' | 'ask' | 'deny'

export interface Rule {
  effect: Effect
  tool: string
  glob: string
}

export interface ToolCall {
  tool: string
  arg: string
}

const esc = (text: string) => text.replace(/[.+^${}()|[\]\\]/g, '\\$&')

// Bash-Regeln (code.claude.com/docs/en/permissions, "Wildcard patterns"): `*` steht
// für beliebigen Text; ein abschließendes " *" (oder ":*") als einziger Wildcard
// trifft auch den nackten Befehl — `Bash(ls *)` passt auf `ls` und `ls -la`,
// nicht auf `lsof`.
function bashRe(glob: string): RegExp {
  const g = glob.endsWith(':*') ? glob.slice(0, -2) + ' *' : glob
  if (g.endsWith(' *') && g.indexOf('*') === g.length - 1) return new RegExp('^' + esc(g.slice(0, -2)) + '( .*)?$')
  return new RegExp('^' + esc(g).replace(/\*/g, '.*') + '$')
}

// Read/Edit-Regeln folgen der gitignore-Syntax: `*` bleibt in einem Pfadsegment,
// `**` reicht über Verzeichnisse, ein nackter Dateiname passt in jeder Tiefe.
// ponytail: nur Pfade relativ zum Arbeitsverzeichnis (`pfad`, `./pfad`); die Anker
// `//`, `~/`, `/` und die Tiefenregel für deny/ask bei `dir/**` fehlen.
const relPath = (path: string) => path.replace(/^\.\//, '')
function pathRe(glob: string): RegExp {
  const g = relPath(glob)
  const body = esc(g).replace(/\*\*\/?|\*/g, (m) => (m === '*' ? '[^/]*' : m.endsWith('/') ? '(.*/)?' : '.*'))
  return new RegExp('^' + (g.includes('/') ? '' : '(.*/)?') + body + '$')
}

// Zusammengesetzte Befehle: Claude Code kennt die Shell-Operatoren und prüft
// jeden Teilbefehl einzeln.
const subcommands = (cmd: string) => cmd.split(/&&|\|\||[;|&\n]/).map((c) => c.trim()).filter(Boolean)

export function matches(rule: Rule, call: ToolCall): boolean {
  if (rule.tool !== call.tool) return false
  if (call.tool === 'Read' || call.tool === 'Edit' || call.tool === 'Write') return pathRe(rule.glob).test(relPath(call.arg))
  if (call.tool !== 'Bash') return bashRe(rule.glob).test(call.arg)
  const parts = subcommands(call.arg)
  const hit = (part: string) => bashRe(rule.glob).test(part)
  // deny/ask greifen, sobald EIN Teilbefehl passt; allow nur, wenn JEDER passt —
  // `Bash(npm run *)` erlaubt also nicht `npm run test && rm -rf x`.
  return rule.effect === 'allow' ? parts.length > 0 && parts.every(hit) : parts.some(hit)
}

// Woher die Entscheidung kommt: aus einer Regel, aus dem eingebauten Verhalten
// für lesende Zugriffe oder aus dem Standard des Manual-Modus (Rückfrage).
export type Reason = 'rule' | 'readonly' | 'default'

// Eingebaute Read-only-Befehle laut code.claude.com/docs/en/permissions
// ("Read-only commands"). ponytail: ohne die read-only-Formen von git und ohne
// Sonderfälle – alles mit Shell-Operatoren/Umleitung fällt auf Rückfrage zurück.
const READONLY_BASH = new Set([
  'ls', 'cat', 'echo', 'pwd', 'head', 'tail', 'grep', 'find', 'wc', 'which', 'diff', 'stat', 'du', 'cd',
])

function isReadOnly(call: ToolCall): boolean {
  if (call.tool === 'Read') return !/^(\/|~|\.\.(\/|$))|\/\.\.(\/|$)/.test(call.arg) // im Arbeitsverzeichnis
  if (call.tool === 'Bash') {
    return !/[;&|<>`$]/.test(call.arg) && READONLY_BASH.has(call.arg.trim().split(/\s+/)[0])
  }
  return false
}

// Vereinfachte Claude-Code-Präzedenz im Manual-Modus: deny überstimmt alles,
// dann ask, dann allow. Ohne Treffer entscheidet das Werkzeug: Lesen im
// Arbeitsverzeichnis und Read-only-Bash laufen ohne Rückfrage, alles andere fragt.
export function explain(rules: Rule[], call: ToolCall): { effect: Effect; reason: Reason } {
  for (const effect of ['deny', 'ask', 'allow'] as const) {
    if (rules.some((r) => r.effect === effect && matches(r, call))) return { effect, reason: 'rule' }
  }
  return isReadOnly(call) ? { effect: 'allow', reason: 'readonly' } : { effect: 'ask', reason: 'default' }
}

export function evaluate(rules: Rule[], call: ToolCall): Effect {
  return explain(rules, call).effect
}
