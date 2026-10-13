import type { Lang } from '@/lib/i18n'

/** Zeitstempel der API. Ohne Zonenangabe ist UTC gemeint (das Backend speichert
 *  UTC; SQLite liefert naive Werte) — `new Date()` läse sie sonst als Ortszeit
 *  und die Anzeige läge um den UTC-Versatz daneben. */
export function parseApiTime(value: string): Date {
  return new Date(/(Z|[+-]\d\d:?\d\d)$/.test(value) ? value : `${value}Z`)
}

/** Datum und Uhrzeit in der Ortszeit des Browsers; unlesbare Werte unverändert. */
export function formatApiTime(value: string, lang: Lang, timeZone?: string): string {
  const date = parseApiTime(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString(lang === 'de' ? 'de-DE' : 'en-GB', { dateStyle: 'short', timeStyle: 'short', timeZone })
}
