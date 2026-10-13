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

function globToRe(glob: string): RegExp {
  const esc = glob.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*')
  return new RegExp('^' + esc + '$')
}

export function matches(rule: Rule, call: ToolCall): boolean {
  if (rule.tool !== call.tool) return false
  return globToRe(rule.glob).test(call.arg)
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
