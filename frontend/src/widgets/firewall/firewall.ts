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

/** Gültiger TCP/UDP-Port: ganze Zahl 1–65535 (Port 0 ist reserviert). */
export function isValidPort(n: number): boolean {
  return Number.isInteger(n) && n >= 1 && n <= 65535
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

// Ziel-Traffic für den Regel-Baukasten: was soll durch, was nicht. NTP (UDP 123) sorgt dafür,
// dass ein zu breites „allow UDP/any" nicht als Lösung für „genau HTTPS und DNS" durchgeht.
export const SAMPLES: { label: string; pkt: Packet; expected: Action }[] = [
  { label: 'HTTPS (TCP 443)', pkt: { proto: 'TCP', port: 443 }, expected: 'allow' },
  { label: 'DNS (UDP 53)', pkt: { proto: 'UDP', port: 53 }, expected: 'allow' },
  { label: 'Telnet (TCP 23)', pkt: { proto: 'TCP', port: 23 }, expected: 'deny' },
  { label: 'RDP (TCP 3389)', pkt: { proto: 'TCP', port: 3389 }, expected: 'deny' },
  { label: 'HTTP (TCP 80)', pkt: { proto: 'TCP', port: 80 }, expected: 'deny' },
  { label: 'NTP (UDP 123)', pkt: { proto: 'UDP', port: 123 }, expected: 'deny' },
]

/** Baukasten-Aufgabe gelöst: jedes Muster-Paket wird wie gewünscht behandelt, mit 1–2 Regeln. */
export function labSolved(rules: Rule[]): boolean {
  return rules.length > 0 && rules.length <= 2
    && SAMPLES.every((s) => evaluate(rules, s.pkt).action === s.expected)
}
