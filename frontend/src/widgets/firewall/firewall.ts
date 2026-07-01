export type Action = 'allow' | 'deny'
export type Proto = 'TCP' | 'UDP'

export interface Rule {
  action: Action
  proto: Proto | 'any'
  port: number | 'any'
}

// Regeln werden von oben nach unten geprüft — die erste passende gewinnt.
export const RULES: Rule[] = [
  { action: 'allow', proto: 'TCP', port: 443 },
  { action: 'allow', proto: 'TCP', port: 22 },
  { action: 'deny', proto: 'TCP', port: 23 },
  { action: 'allow', proto: 'UDP', port: 53 },
]

export interface Packet {
  proto: Proto
  port: number
}

export interface Decision {
  action: Action
  ruleIndex: number | null // null = keine Regel, Default-Deny
}

function matches(rule: Rule, pkt: Packet): boolean {
  return (
    (rule.proto === 'any' || rule.proto === pkt.proto) &&
    (rule.port === 'any' || rule.port === pkt.port)
  )
}

/** First-Match-Wins, sonst Default-Deny. */
export function evaluate(rules: Rule[], pkt: Packet): Decision {
  for (let i = 0; i < rules.length; i++) {
    if (matches(rules[i], pkt)) {
      return { action: rules[i].action, ruleIndex: i }
    }
  }
  return { action: 'deny', ruleIndex: null }
}
