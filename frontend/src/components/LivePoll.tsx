import { useEffect, useRef, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { learnApi } from '@/lib/learnApi'
import { clearInert, focusableElements, setInert, siblingsOf } from '@/lib/focusTrap'
import { t, type Lang } from '@/lib/i18n'
import { Icon } from '@/components/Icon'
import type { LivePoll } from '@/types'

// Live-Abstimmung: Optionsliste (Beamer + Teilnehmer) und die Einblendung im
// offenen Modul. Braucht die --wb-*-Tokens, also eine ".workbench"-Wurzel.

/** Optionen in der festen Server-Reihenfolge mit Buchstaben. Balken erscheinen,
 *  sobald `counts` da sind; die Lösung wird erst bei status "revealed" markiert
 *  (der Trainer kennt `answer` schon vorher — der Beamer darf sie nicht zeigen). */
export function PollOptions({ poll, lang, big, onVote }: { poll: LivePoll; lang: Lang; big?: boolean; onVote?: (choice: number) => void }) {
  const total = poll.votes ?? 0
  const revealed = poll.status === 'revealed'
  return (
    <ol className={big ? 'space-y-3 text-2xl sm:text-3xl' : 'space-y-2 text-sm'}>
      {poll.options.map((option, index) => {
        const count = poll.counts?.[index]
        const pct = count != null && total > 0 ? Math.round((count / total) * 100) : 0
        const correct = revealed && poll.answer === index
        const mine = poll.my_choice === index
        const row = `relative block w-full overflow-hidden rounded-xl border-2 bg-[var(--wb-surface)] text-left text-[var(--wb-ink)] ${big ? 'px-5 py-4' : 'px-3 py-2.5'} ${correct ? 'border-[var(--wb-success)]' : mine ? 'border-[var(--wb-accent)]' : 'border-[var(--wb-border)]'}`
        const body = (
          <>
            {count != null && <span aria-hidden="true" data-testid="poll-bar" className="absolute inset-y-0 left-0 bg-[var(--wb-accent)] opacity-25 transition-[width] duration-500 motion-reduce:transition-none" style={{ width: `${pct}%` }} />}
            <span className="relative flex items-center gap-3">
              <span aria-hidden="true" className={`grid shrink-0 place-items-center rounded-lg border border-current font-bold ${big ? 'h-12 w-12' : 'h-7 w-7 text-xs'}`}>{String.fromCharCode(65 + index)}</span>
              <span className="sr-only">{String.fromCharCode(65 + index)}:</span>
              <span className="min-w-0 flex-1 [overflow-wrap:anywhere]">{option}</span>
              {mine && <span className="shrink-0 rounded-full border border-current px-2 py-0.5 text-xs font-semibold">{t(lang, 'pollYours')}</span>}
              {correct && <span className="inline-flex shrink-0 items-center gap-1 font-semibold text-[var(--wb-success)]"><Icon name="check" className={big ? 'h-8 w-8' : 'h-4 w-4'} /><span className={big ? 'text-lg' : 'sr-only'}>{t(lang, 'pollRight')}</span></span>}
              {count != null && <span className="shrink-0 font-semibold tabular-nums">{count}<span className={`ml-2 font-normal text-[var(--wb-muted)] ${big ? 'text-xl' : 'text-xs'}`}>{pct} %</span></span>}
            </span>
          </>
        )
        return (
          <li key={index}>
            {onVote
              ? <button type="button" aria-pressed={mine} onClick={() => onVote(index)} className={`${row} wb-control hover:border-[var(--wb-accent)]`}>{body}</button>
              : <div className={row}>{body}</div>}
          </li>
        )
      })}
    </ol>
  )
}

/** Einblendung im offenen Modul: fragt alle 5 s nach einer Abstimmung des Kurses.
 *  Escape/Klick daneben minimiert zum Hinweis-Chip (statt die Frage zu verlieren);
 *  eine neue Abstimmung und die Auflösung blenden sich erneut ein. */
export function ParticipantPoll({ moduleKey, lang }: { moduleKey: string; lang: Lang }) {
  const qc = useQueryClient()
  const queryKey = ['poll', moduleKey]
  // refetchInterval ruht bei verstecktem Tab von selbst (react-query:
  // refetchIntervalInBackground=false) und holt beim Zurückkehren sofort nach.
  const { data: poll } = useQuery({
    queryKey, queryFn: () => learnApi.poll(moduleKey).then((r) => r.data), refetchInterval: 5_000, retry: false,
  })
  const vote = useMutation({
    mutationFn: (choice: number) => learnApi.pollVote(moduleKey, poll!.id, choice),
    onSuccess: (_r, choice) => qc.setQueryData<LivePoll | null>(queryKey, (old) => (old ? { ...old, my_choice: choice } : old)),
    onError: () => qc.invalidateQueries({ queryKey }),  // z. B. 409: inzwischen aufgelöst
  })
  const stage = poll ? `${poll.id}-${poll.status}` : ''
  const [minimized, setMinimized] = useState('')
  const open = !!poll && minimized !== stage
  const dialogRef = useRef<HTMLDivElement | null>(null)
  const panelRef = useRef<HTMLDivElement | null>(null)

  // Fokus-Handling wie ConfirmDialog/GlossaryPanel (lib/focusTrap.ts).
  useEffect(() => {
    if (!open) return
    const dialogNode = dialogRef.current
    const before = document.activeElement as HTMLElement | null
    const onKeydown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') { setMinimized(stage); return }
      if (event.key !== 'Tab' || !dialogNode) return
      const focusable = focusableElements(dialogNode)
      if (focusable.length === 0) return
      const first = focusable[0]
      const last = focusable[focusable.length - 1]
      const active = document.activeElement
      const outside = !dialogNode.contains(active)
      // Rückwärts von der (nur per Skript fokussierten) Karte ginge es sonst aus dem Dialog hinaus.
      if (event.shiftKey ? outside || active === first || active === panelRef.current : outside || active === last) {
        event.preventDefault()
        ;(event.shiftKey ? last : first).focus()
      }
    }
    document.addEventListener('keydown', onKeydown)
    document.body.classList.add('overflow-hidden')
    const background = dialogNode?.parentElement ? siblingsOf(dialogNode.parentElement, dialogNode) : []
    setInert(background)
    // Fokus auf die Karte, NICHT auf eine Option: wer gerade tippt (Reflexion,
    // Kommentar), gäbe sonst mit Leertaste/Enter versehentlich eine Stimme ab.
    panelRef.current?.focus()
    return () => {
      document.removeEventListener('keydown', onKeydown)
      document.body.classList.remove('overflow-hidden')
      clearInert(background)
      if (before?.isConnected) before.focus()
    }
  }, [open, stage])

  if (!poll) return null
  const revealed = poll.status === 'revealed'
  if (!open)
    return (
      <button type="button" onClick={() => setMinimized('')}
        className="wb-control fixed bottom-4 right-4 z-40 inline-flex items-center gap-2 rounded-full border-2 border-[var(--wb-accent)] bg-[var(--wb-surface)] px-4 text-sm font-semibold text-[var(--wb-ink)] shadow-lg print:hidden">
        <span aria-hidden="true" className="h-2.5 w-2.5 rounded-full bg-[var(--wb-accent)]" />
        {t(lang, revealed ? 'pollChipRevealed' : 'pollChipOpen')}
      </button>
    )
  const status = revealed
    ? poll.my_choice == null ? t(lang, 'pollNoVote') : t(lang, poll.my_choice === poll.answer ? 'pollCorrect' : 'pollWrong')
    : poll.my_choice == null ? t(lang, 'pollChoose') : t(lang, 'pollVoted')
  return (
    <div ref={dialogRef} role="dialog" aria-modal="true" aria-labelledby="poll-title" aria-describedby="poll-prompt"
      className="fixed inset-0 z-[100] flex items-end justify-center bg-slate-900/30 p-4 sm:items-center print:hidden"
      onMouseDown={(event) => { if (event.target === event.currentTarget) setMinimized(stage) }}>
      <div ref={panelRef} tabIndex={-1} className="wb-surface max-h-[calc(100dvh-2rem)] w-full max-w-lg overflow-y-auto p-5 shadow-xl">
        <div className="flex items-center justify-between gap-3">
          <p id="poll-title" className="text-xs font-semibold uppercase tracking-wide text-[var(--wb-accent)]">{t(lang, 'pollTitle')}</p>
          <button type="button" onClick={() => setMinimized(stage)} aria-label={t(lang, 'pollMinimize')} title={t(lang, 'pollMinimize')}
            className="wb-control -my-2 -mr-2 grid w-11 place-items-center rounded-lg text-[var(--wb-muted)] hover:text-[var(--wb-ink)]"><Icon name="close" className="h-5 w-5" /></button>
        </div>
        <h2 id="poll-prompt" className="mt-2 text-lg font-semibold leading-snug text-[var(--wb-ink)]">{poll.prompt}</h2>
        <div className="mt-4"><PollOptions poll={poll} lang={lang} onVote={revealed ? undefined : (choice) => vote.mutate(choice)} /></div>
        <p role="status" className={`mt-4 text-sm font-medium ${revealed && poll.my_choice === poll.answer ? 'text-[var(--wb-success)]' : 'text-[var(--wb-ink)]'}`}>
          {vote.isError ? t(lang, 'pollError') : status}
          {revealed && <span className="ml-2 font-normal text-[var(--wb-muted)]">{poll.votes} {t(lang, 'pollVotes')}</span>}
        </p>
        {revealed && poll.explanation && <p className="mt-3 border-l-2 border-[var(--wb-accent)] pl-3 text-sm leading-relaxed text-[var(--wb-muted)]">{poll.explanation}</p>}
      </div>
    </div>
  )
}
