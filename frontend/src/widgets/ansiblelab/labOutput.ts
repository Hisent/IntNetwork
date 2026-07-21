// Reine Logik rund um die Ausgabe von `ansible-playbook` — keine React-, keine
// Netzwerk-Abhängigkeiten. Zwei Dinge stecken hier drin, die beide leicht mit
// vitest zu testen sind, aber in der Komponente nur Rauschen wären:
//
// 1. parseRecap: liest die "PLAY RECAP"-Zeile(n) am Ende der Ausgabe und
//    summiert ok/changed/failed/skipped über alle Hosts.
// 2. compareIdempotency: vergleicht zwei Recaps (voriger vs. aktueller Lauf)
//    und formuliert die didaktische Einordnung ("zweiter Lauf: weniger
//    Änderungen -> idempotent" bzw. "gleich viele -> typisch für command
//    ohne Prüfung").
import type { Lang } from '@/lib/i18n'

export interface RecapTotals {
  ok: number
  changed: number
  failed: number
  skipped: number
  /** Anzahl Hosts, über die summiert wurde (für "mehrere Hosts"-Fälle). */
  hosts: number
}

const RECAP_HEADER = /^PLAY RECAP\b/m
// Host-Zeile im Recap: "hostname : ok=2  changed=1  unreachable=0 ...".
// Der Hostname selbst darf (fast) alles enthalten, entscheidend ist der
// Doppelpunkt gefolgt von mindestens einem "schlüssel=zahl"-Paar.
const KV_PAIR = /(\w+)=(\d+)/g

/**
 * Liest die PLAY-RECAP-Zahlen aus einer `ansible-playbook`-Ausgabe.
 * Gibt `null` zurück, wenn kein Recap vorhanden ist — das passiert bei
 * Syntaxfehlern oder falschen Modulnamen: Ansible bricht ab, bevor es
 * überhaupt einen Host abgearbeitet hat.
 */
export function parseRecap(output: string): RecapTotals | null {
  const header = RECAP_HEADER.exec(output)
  if (!header) return null

  const totals: RecapTotals = { ok: 0, changed: 0, failed: 0, skipped: 0, hosts: 0 }
  const rest = output.slice(header.index + header[0].length)

  for (const rawLine of rest.split('\n')) {
    const line = rawLine.trim()
    if (line === '') continue
    if (/^\*+$/.test(line)) continue // Unterstreichung der Kopfzeile ("****")

    const colon = line.indexOf(':')
    if (colon < 0) break // erste Zeile ohne ":" beendet den Recap-Block

    const pairs = [...line.slice(colon + 1).matchAll(KV_PAIR)]
    if (pairs.length === 0) break

    totals.hosts += 1
    for (const [, key, value] of pairs) {
      const n = Number(value)
      if (key === 'ok') totals.ok += n
      else if (key === 'changed') totals.changed += n
      else if (key === 'failed') totals.failed += n
      else if (key === 'skipped') totals.skipped += n
    }
  }

  return totals.hosts > 0 ? totals : null
}

export interface IdempotencyNote {
  kind: 'improved' | 'same' | 'worse'
  message: string
}

/**
 * Ordnet den Unterschied zwischen zwei Läufen desselben Playbooks didaktisch
 * ein. `prev` ist das Recap des vorherigen *echten* Laufs (kein --check),
 * `curr` das des aktuellen. Ohne beide Werte (erster Lauf oder ein Lauf ohne
 * Recap, z.B. nach einem Syntaxfehler) gibt es nichts zu vergleichen.
 */
export function compareIdempotency(prev: RecapTotals | null, curr: RecapTotals | null, lang: Lang): IdempotencyNote | null {
  if (!prev || !curr) return null

  if (curr.changed < prev.changed) {
    // Singular/Plural ausformulieren statt „Task(s)" — der Satz steht im
    // Lernmaterial und wird gelesen, nicht überflogen.
    const rest = curr.changed > 0
      ? (lang === 'de'
          ? (curr.changed === 1
              ? ' — bis auf einen Task, der weiterhin changed meldet'
              : ` — bis auf ${curr.changed} Tasks, die weiterhin changed melden`)
          : (curr.changed === 1
              ? ' — except for one task that still reports changed'
              : ` — except for ${curr.changed} tasks that still report changed`))
      : ''
    return {
      kind: 'improved',
      message: lang === 'de'
        ? `Zweiter Lauf: ${curr.changed} statt ${prev.changed} Änderungen — die Tasks sind idempotent${rest}.`
        : `Second run: ${curr.changed} instead of ${prev.changed} changes — the tasks are idempotent${rest}.`,

    }
  }

  if (curr.changed === prev.changed) {
    return {
      kind: 'same',
      message: lang === 'de'
        ? `Änderungen bleiben bei ${curr.changed} — typisch für Module wie \`command\`/\`shell\` ohne Zustandsprüfung (z.B. fehlendes \`creates\`).`
        : `Changes stay at ${curr.changed} — typical for modules like \`command\`/\`shell\` without a state check (e.g. a missing \`creates\`).`,
    }
  }

  return {
    kind: 'worse',
    message: lang === 'de'
      ? `Änderungen sind gestiegen (${prev.changed} → ${curr.changed}) — das Playbook ist nicht idempotent, oder der Zustand hat sich zwischenzeitlich geändert.`
      : `Changes increased (${prev.changed} → ${curr.changed}) — the playbook isn't idempotent, or the state changed in between.`,
  }
}
