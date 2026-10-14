import { useEffect, useRef, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { learnApi } from '@/lib/learnApi'
import { clearInert, focusableElements, setInert, siblingsOf } from '@/lib/focusTrap'
import { t, type Lang } from '@/lib/i18n'
import { Icon } from '@/components/Icon'
import { ScaleInput, ScaleResult, TextAnswers, TextInput, WordCloud, WordsInput } from '@/components/PollKinds'
import type { LivePoll, PollChoice } from '@/types'

// Live-Abstimmung: Optionsliste (Beamer + Teilnehmer) und die Einblendung im
// offenen Modul. Braucht die --wb-*-Tokens, also eine ".workbench"-Wurzel.

const has = (value: LivePoll['my_choice'] | LivePoll['answer'], index: number) =>
  Array.isArray(value) ? (value as unknown[]).includes(index) : value === index

/** Gleiche Auswahl (Single: Zahl, Multiple: Menge)? */
function sameChoice(a: LivePoll['my_choice'] | LivePoll['answer'], b: LivePoll['my_choice'] | LivePoll['answer']) {
  const norm = (v: typeof a) => JSON.stringify(Array.isArray(v) ? [...v].sort() : v)
  return a != null && b != null && norm(a) === norm(b)
}

/** Optionen in der festen Server-Reihenfolge mit Buchstaben. Balken erscheinen,
 *  sobald `counts` da sind; die Lösung wird erst bei status "revealed" markiert
 *  (der Trainer kennt `answer` schon vorher — der Beamer darf sie nicht zeigen).
 *  Mehrfachauswahl: Prozent je Option bezogen auf die Teilnehmer, `full` sperrt
 *  weitere Optionen, sobald die Höchstzahl gewählt ist. */
export function PollOptions({ poll, lang, big, full, onVote }: { poll: LivePoll; lang: Lang; big?: boolean; full?: boolean; onVote?: (choice: number) => void }) {
  const total = poll.votes ?? 0
  const revealed = poll.status === 'revealed'
  return (
    <ol className={big ? 'space-y-3 text-2xl sm:text-3xl' : 'space-y-2 text-sm'}>
      {(poll.options ?? []).map((option, index) => {
        const count = poll.counts?.[index]
        const pct = count != null && total > 0 ? Math.round((count / total) * 100) : 0
        const correct = revealed && has(poll.answer, index)
        const mine = has(poll.my_choice, index)
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
              ? <button type="button" aria-pressed={mine} disabled={full && !mine} onClick={() => onVote(index)} className={`${row} wb-control hover:border-[var(--wb-accent)] disabled:opacity-50`}>{body}</button>
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
  const setMine = (choice: PollChoice) => qc.setQueryData<LivePoll | null>(queryKey, (old) => (old ? { ...old, my_choice: choice } : old))
  const vote = useMutation({
    mutationFn: (choice: PollChoice) => learnApi.pollVote(moduleKey, poll!.id, choice),
    // Sofort übernehmen: schnelles Umklicken bei Mehrfachauswahl rechnet sonst mit dem alten Stand.
    onMutate: setMine,
    onSuccess: (r, choice) => setMine(r.data?.my_choice ?? choice),  // Server normalisiert Text/Wörter
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
  const kind = poll.kind ?? 'single'
  const voted = poll.my_choice != null
  const graded = poll.answer != null  // nur Inhaltsfragen haben eine Lösung
  const correct = graded && sameChoice(poll.my_choice, poll.answer)
  const picked = Array.isArray(poll.my_choice) ? (poll.my_choice as number[]) : []
  const choose = kind === 'multi' && poll.max_selections
    ? t(lang, 'pollChooseMax').replace('{n}', String(poll.max_selections))
    : t(lang, ({ single: 'pollChoose', multi: 'pollChooseMulti', scale: 'pollChooseScale', text: 'pollChooseText', words: 'pollChooseWords' } as const)[kind])
  const status = revealed
    ? !voted ? t(lang, 'pollNoVote') : graded ? t(lang, correct ? 'pollCorrect' : 'pollWrong') : t(lang, 'pollThanks')
    : !voted ? choose : t(lang, kind === 'text' || kind === 'words' ? 'pollSaved' : 'pollVoted')
  const send = (choice: PollChoice) => vote.mutate(choice)
  const toggle = (index: number) => {
    const next = picked.includes(index) ? picked.filter((i) => i !== index) : [...picked, index].sort((a, b) => a - b)
    if (next.length) send(next)  // mindestens eine Antwort bleibt gewählt (wie bei Single Choice)
  }
  const body =
    kind === 'single' || kind === 'multi'
      ? <PollOptions poll={poll} lang={lang} full={kind === 'multi' && !!poll.max_selections && picked.length >= poll.max_selections}
          onVote={revealed ? undefined : kind === 'single' ? send : toggle} />
      : kind === 'scale'
        ? revealed ? <ScaleResult poll={poll} lang={lang} /> : <ScaleInput poll={poll} lang={lang} onVote={send} />
        : kind === 'text'
          ? revealed
            ? <>
                {typeof poll.my_choice === 'string' && <p className="mb-3 text-sm text-[var(--wb-muted)]">{t(lang, 'pollAnswerLabel')}: <span className="text-[var(--wb-ink)] [overflow-wrap:anywhere]">{poll.my_choice}</span></p>}
                <TextAnswers answers={poll.answers ?? []} lang={lang} />
              </>
            : <TextInput key={poll.id} poll={poll} lang={lang} pending={vote.isPending} onSend={send} />
          : revealed ? <WordCloud words={poll.words ?? []} lang={lang} /> : <WordsInput key={poll.id} poll={poll} lang={lang} pending={vote.isPending} onSend={send} />
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
        <div className="mt-4">{body}</div>
        <p role="status" className={`mt-4 text-sm font-medium ${revealed && correct ? 'text-[var(--wb-success)]' : 'text-[var(--wb-ink)]'}`}>
          {vote.isError ? t(lang, 'pollError') : status}
          {revealed && <span className="ml-2 font-normal text-[var(--wb-muted)]">{poll.votes} {t(lang, 'pollVotes')}</span>}
        </p>
        {revealed && poll.explanation && <p className="mt-3 border-l-2 border-[var(--wb-accent)] pl-3 text-sm leading-relaxed text-[var(--wb-muted)]">{poll.explanation}</p>}
      </div>
    </div>
  )
}
