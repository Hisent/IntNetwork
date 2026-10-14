import { useState } from 'react'
import { t, type Lang } from '@/lib/i18n'
import type { LivePoll } from '@/types'

// Eingabe und Ergebnis der Abstimmungsarten Skala, Freitext und Wortwolke
// (Single/Multiple Choice: PollOptions in LivePoll.tsx). Teilnehmer-Dialog und
// Beamer nutzen dieselben Bausteine, der Beamer mit big. Braucht die --wb-*-Tokens.

// Grenzen wie im Backend (services/poll_tally.py) — die API prüft selbst.
const TEXT_MAX = 280
const WORD_MAX = 30
const WORD_SLOTS = 3

const scaleRange = (poll: LivePoll) => {
  const lo = poll.min ?? 1
  return Array.from({ length: (poll.max ?? 5) - lo + 1 }, (_v, i) => lo + i)
}

function ScaleLabels({ poll, big }: { poll: LivePoll; big?: boolean }) {
  if (!poll.label_min && !poll.label_max) return null
  return (
    <div aria-hidden="true" className={`mt-2 flex justify-between gap-4 text-[var(--wb-muted)] ${big ? 'text-xl' : 'text-xs'}`}>
      <span>{poll.label_min && `${poll.min ?? 1} = ${poll.label_min}`}</span>
      <span className="text-right">{poll.label_max && `${poll.max ?? 5} = ${poll.label_max}`}</span>
    </div>
  )
}

/** Werte als Knopfreihe; die Endpunkte tragen ihre Beschriftung auch für Screenreader. */
export function ScaleInput({ poll, lang, onVote }: { poll: LivePoll; lang: Lang; onVote: (value: number) => void }) {
  const values = scaleRange(poll)
  const label = (v: number) =>
    v === values[0] && poll.label_min ? `${v} – ${poll.label_min}`
      : v === values[values.length - 1] && poll.label_max ? `${v} – ${poll.label_max}` : String(v)
  return (
    <div role="group" aria-label={t(lang, 'pollScaleValue')}>
      <div className="flex flex-wrap gap-2">
        {values.map((v) => (
          <button key={v} type="button" aria-pressed={poll.my_choice === v} aria-label={label(v)} onClick={() => onVote(v)}
            className={`wb-control min-w-11 flex-1 rounded-xl border-2 bg-[var(--wb-surface)] text-lg font-semibold tabular-nums text-[var(--wb-ink)] hover:border-[var(--wb-accent)] ${poll.my_choice === v ? 'border-[var(--wb-accent)] bg-[var(--wb-accent-soft)]' : 'border-[var(--wb-border)]'}`}>
            {v}
          </button>
        ))}
      </div>
      <ScaleLabels poll={poll} />
    </div>
  )
}

/** Verteilung als Säulen je Wert plus Mittelwert. */
export function ScaleResult({ poll, lang, big }: { poll: LivePoll; lang: Lang; big?: boolean }) {
  const counts = poll.counts ?? []
  const top = Math.max(1, ...counts)
  const values = scaleRange(poll)
  return (
    <div>
      <ol className={`flex items-stretch gap-1 sm:gap-2 ${big ? 'h-72' : 'h-36'}`}>
        {values.map((v, i) => {
          const n = counts[i] ?? 0
          return (
            <li key={v} className="flex min-w-0 flex-1 flex-col items-center">
              <span className="sr-only">{t(lang, 'pollScaleValue')} {v}: {n}</span>
              <span aria-hidden="true" className={`font-semibold tabular-nums ${big ? 'text-2xl' : 'text-xs'}`}>{n}</span>
              <span aria-hidden="true" className="flex w-full flex-1 items-end border-b-2 border-[var(--wb-border)]">
                <span data-testid="poll-bar" className="w-full rounded-t-md bg-[var(--wb-accent)] transition-[height] duration-500 motion-reduce:transition-none"
                  style={{ height: `${Math.round((n / top) * 100)}%` }} />
              </span>
              <span aria-hidden="true" className={`mt-1 tabular-nums ${poll.my_choice === v ? 'font-bold text-[var(--wb-accent)]' : 'text-[var(--wb-muted)]'} ${big ? 'text-2xl' : 'text-xs'}`}>{v}</span>
            </li>
          )
        })}
      </ol>
      <ScaleLabels poll={poll} big={big} />
      {poll.mean != null && (
        <p data-testid="poll-mean" className={`mt-3 font-semibold ${big ? 'text-3xl' : 'text-sm'}`}>
          {t(lang, 'pollMean')}: <span className="tabular-nums">{poll.mean.toLocaleString(lang, { maximumFractionDigits: 2 })}</span>
        </p>
      )}
    </div>
  )
}

function SendButton({ lang, disabled }: { lang: Lang; disabled: boolean }) {
  return (
    <button type="submit" disabled={disabled}
      className="wb-control rounded-lg bg-[var(--wb-accent)] px-5 font-semibold text-white hover:bg-[var(--wb-accent-hover)] disabled:opacity-50">
      {t(lang, 'pollSend')}
    </button>
  )
}

const field = 'w-full rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-3 py-2 text-base text-[var(--wb-ink)]'

/** Kurze Antwort; vorbelegt mit der eigenen, solange die Abstimmung offen ist. */
export function TextInput({ poll, lang, pending, onSend }: { poll: LivePoll; lang: Lang; pending: boolean; onSend: (text: string) => void }) {
  const [text, setText] = useState(typeof poll.my_choice === 'string' ? poll.my_choice : '')
  return (
    <form onSubmit={(e) => { e.preventDefault(); if (text.trim()) onSend(text.trim()) }}>
      <label htmlFor="poll-text" className="text-sm font-medium text-[var(--wb-ink)]">{t(lang, 'pollAnswerLabel')}</label>
      <textarea id="poll-text" value={text} rows={3} maxLength={TEXT_MAX} aria-describedby="poll-text-count"
        onChange={(e) => setText(e.target.value)} className={`mt-1 ${field}`} />
      <div className="mt-2 flex items-center justify-between gap-3">
        <span id="poll-text-count" className="text-xs tabular-nums text-[var(--wb-muted)]">{text.length} / {TEXT_MAX}</span>
        <SendButton lang={lang} disabled={pending || !text.trim()} />
      </div>
    </form>
  )
}

/** Freitexte als Karten (die API liefert nur sichtbare); onHide nur in der Trainer-Ansicht. */
export function TextAnswers({ answers, lang, big, onHide }: {
  answers: NonNullable<LivePoll['answers']>; lang: Lang; big?: boolean; onHide?: (id: number) => void
}) {
  if (answers.length === 0) return <p className={`text-[var(--wb-muted)] ${big ? 'text-2xl' : 'text-sm'}`}>{t(lang, 'pollNoAnswers')}</p>
  return (
    <ul className={big ? 'grid gap-3 text-2xl sm:grid-cols-2' : 'space-y-2 text-sm'}>
      {answers.map((a, i) => (
        <li key={a.id ?? i} className={`wb-surface flex items-start gap-3 ${big ? 'px-5 py-4' : 'px-3 py-2'}`}>
          <span className="min-w-0 flex-1 [overflow-wrap:anywhere]">{a.text}</span>
          {onHide && a.id != null && (
            <button type="button" onClick={() => onHide(a.id!)} aria-label={`Ausblenden: ${a.text}`}
              className="wb-control shrink-0 rounded-lg px-2 text-sm text-[var(--wb-muted)] hover:text-[var(--wb-ink)]">
              Ausblenden
            </button>
          )}
        </li>
      ))}
    </ul>
  )
}

/** Bis zu drei Wörter; die API normalisiert Groß/klein und Leerraum. */
export function WordsInput({ poll, lang, pending, onSend }: { poll: LivePoll; lang: Lang; pending: boolean; onSend: (words: string[]) => void }) {
  const mine = Array.isArray(poll.my_choice) ? poll.my_choice.map(String) : []
  const [words, setWords] = useState(() => Array.from({ length: WORD_SLOTS }, (_v, i) => mine[i] ?? ''))
  const filled = words.map((w) => w.trim()).filter(Boolean)
  return (
    <form onSubmit={(e) => { e.preventDefault(); if (filled.length) onSend(filled) }}>
      <div className="grid gap-2 sm:grid-cols-3">
        {words.map((w, i) => (
          <label key={i} className="text-xs font-medium text-[var(--wb-muted)]">
            {t(lang, 'pollWord')} {i + 1}
            <input value={w} maxLength={WORD_MAX} autoComplete="off"
              onChange={(e) => setWords(words.map((x, j) => (j === i ? e.target.value : x)))}
              className={`wb-control mt-1 ${field}`} />
          </label>
        ))}
      </div>
      <div className="mt-3 flex justify-end"><SendButton lang={lang} disabled={pending || filled.length === 0} /></div>
    </form>
  )
}

/** Wortwolke aus reinem CSS: Schriftgröße nach Häufigkeit (Wurzel, damit ein
 *  Ausreißer nicht alles andere winzig macht), das häufigste Wort in der Mitte.
 *  Screenreader bekommen stattdessen die sortierte Liste mit Zahlen. */
export function WordCloud({ words, lang, big }: { words: NonNullable<LivePoll['words']>; lang: Lang; big?: boolean }) {
  if (words.length === 0) return <p className={`text-[var(--wb-muted)] ${big ? 'text-2xl' : 'text-sm'}`}>{t(lang, 'pollNoAnswers')}</p>
  const top = words[0].count
  const centered = words.reduce<typeof words>((acc, w, i) => (i % 2 ? [w, ...acc] : [...acc, w]), [])
  return (
    <figure>
      <ul aria-hidden="true" data-testid="word-cloud"
        className="flex flex-wrap items-center justify-center gap-x-5 gap-y-1 leading-tight">
        {centered.map((w) => {
          const weight = Math.sqrt(w.count / top)
          return (
            <li key={w.word} title={`${w.count}×`}
              style={{ fontSize: `${((big ? 1.5 : 0.875) + (big ? 3.5 : 1.25) * weight).toFixed(2)}rem` }}
              className={`max-w-full font-semibold [overflow-wrap:anywhere] ${weight > 0.7 ? 'text-[var(--wb-accent)]' : 'text-[var(--wb-ink)]'}`}>
              {w.word}
            </li>
          )
        })}
      </ul>
      <figcaption className="sr-only">
        {t(lang, 'pollWordCloud')}
        <ol>{words.map((w) => <li key={w.word}>{w.word}: {w.count}</li>)}</ol>
      </figcaption>
    </figure>
  )
}

