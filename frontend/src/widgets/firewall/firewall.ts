export type Action = 'allow' | 'deny'
export type Proto = 'TCP' | 'UDP'

export interface Rule {
  action: Action
  proto: Proto | 'any'
  port: number | 'any'
  desc: string
}

// Regeln werden von oben nach unten geprüft — die erste passende gewinnt.
export const RULES: Rule[] = [
  { action: 'allow', proto: 'TCP', port: 443, desc: 'HTTPS zum Webserver' },
  { action: 'allow', proto: 'TCP', port: 22, desc: 'SSH nur für Admins' },
  { action: 'deny', proto: 'TCP', port: 23, desc: 'Telnet verboten (unverschlüsselt)' },
  { action: 'allow', proto: 'UDP', port: 53, desc: 'DNS-Anfragen' },
]

export interface Packet {
  proto: Proto
  port: number
}

export interface Decision {
  action: Action
  ruleIndex: number | null // null = keine Regel, Default-Deny
  reason: string
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
      return { action: rules[i].action, ruleIndex: i, reason: rules[i].desc }
    }
  }
  return { action: 'deny', ruleIndex: null, reason: 'Keine Regel trifft zu → Default-Deny' }
}
