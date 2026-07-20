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

// Vereinfachte Claude-Code-Präzedenz: deny überstimmt alles, dann ask, dann
// allow; ohne Treffer greift der Standard (ask/Rückfrage).
export function evaluate(rules: Rule[], call: ToolCall): Effect {
  if (rules.some((r) => r.effect === 'deny' && matches(r, call))) return 'deny'
  if (rules.some((r) => r.effect === 'ask' && matches(r, call))) return 'ask'
  if (rules.some((r) => r.effect === 'allow' && matches(r, call))) return 'allow'
  return 'ask'
}
