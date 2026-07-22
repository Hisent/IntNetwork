import { useEffect, useState } from 'react'
import { ChallengeBox } from '@/components/ChallengeBox'
import { useWidgetScope } from '@/lib/widgetScope'
import { labErrorMessage, runLab, type LabRunResult } from '@/lib/labApi'
import { LabDisabledBanner } from '@/widgets/lab/LabDisabledBanner'
import { LabOutputPanel } from '@/widgets/lab/LabOutputPanel'
import { readSnapshot } from '@/widgets/lab/snapshot'
import { useLabAvailability } from '@/widgets/lab/useLabAvailability'
import { compareIdempotency, parseRecap, type IdempotencyNote, type RecapTotals } from '@/widgets/ansiblelab/labOutput'
import { DEFAULT_EXERCISE, EXERCISES, exerciseById } from '@/widgets/ansiblelab/templates'
import type { Lang } from '@/lib/i18n'

const MAX_CHARS = 16_000
const WARN_CHARS = 15_000

interface Snapshot {
  exerciseId: string
  playbook: string
  extraVars: string
}

// Ungeprüfte Rohform, wie sie aus localStorage kommt: exerciseId/playbook
// müssen Strings sein, extraVars wird unten separat abgesichert (kann in
// einem alten/beschädigten Eintrag fehlen oder falsch typisiert sein, ohne
// dass deswegen der ganze Snapshot verworfen werden muss).
interface RawSnapshot {
  exerciseId: string
  playbook: string
  extraVars?: unknown
}

function isRawSnapshot(parsed: unknown): parsed is RawSnapshot {
  if (typeof parsed !== 'object' || parsed === null) return false
  const rec = parsed as Record<string, unknown>
  return typeof rec.exerciseId === 'string' && typeof rec.playbook === 'string'
}

// Pro Teilnehmer gespeichert (localStorage), exakt nach dem Muster der
// Live-CLI (ClaudeCliWidget.loadSnapshot): storageKey kommt aus dem
// Teilnehmer-/Kurs-Scope, ein beschädigter Eintrag fällt auf die Vorlage
// zurück statt die Seite zu zerlegen.
export function loadSnapshot(storageKey: string | null): Snapshot {
  const raw = readSnapshot(storageKey, isRawSnapshot, () => ({
    exerciseId: DEFAULT_EXERCISE.id, playbook: DEFAULT_EXERCISE.playbook, extraVars: '',
  }))
  return {
    exerciseId: raw.exerciseId,
    playbook: raw.playbook,
    extraVars: typeof raw.extraVars === 'string' ? raw.extraVars : '',
  }
}

const STR = {
  de: {
    title: 'Ansible-Lab', hint: 'Echtes Playbook, echte Ausführung — serverseitig in einem isolierten Container.',
    exercise: 'Übung', playbookLabel: 'Playbook', extraVarsLabel: 'Extra-Vars',
    extraVarsPlaceholder: 'z.B. umgebung=produktion',
    reset: 'Zurücksetzen', run: 'Ausführen', running: 'Läuft…',
    check: 'Nur prüfen (--check)', checking: 'Prüft…',
    chars: 'Zeichen', charWarning: 'Playbook wird groß — Grenze liegt bei 16.000 Zeichen.',
    disabledTitle: 'Lab auf diesem Server nicht aktiviert',
    disabledBody: 'Auf diesem Server ist das Lab nicht aktiviert; die Aufgabe lässt sich trotzdem lesen.',
    statusChecking: 'Prüfe Verfügbarkeit…',
    output: 'Ausgabe', noRunYet: 'Noch kein Lauf.', noRecap: 'Kein PLAY RECAP gefunden — vermutlich ein Syntax- oder Modulfehler (siehe Ausgabe unten).',
    ok: 'ok', changed: 'changed', failed: 'failed', skipped: 'skipped',
    rc: 'Rückgabewert', duration: 'Dauer', truncated: 'Ausgabe gekürzt', timedOut: 'Zeitüberschreitung',
    challenge: 'Lass dasselbe Playbook zweimal laufen und erkläre den Unterschied.',
  },
  en: {
    title: 'Ansible Lab', hint: 'A real playbook, really executed — server-side, in an isolated container.',
    exercise: 'Exercise', playbookLabel: 'Playbook', extraVarsLabel: 'Extra vars',
    extraVarsPlaceholder: 'e.g. umgebung=produktion',
    reset: 'Reset', run: 'Run', running: 'Running…',
    check: 'Check only (--check)', checking: 'Checking…',
    chars: 'characters', charWarning: 'Playbook is getting large — the limit is 16,000 characters.',
    disabledTitle: 'Lab not enabled on this server',
    disabledBody: 'The lab is not enabled on this server; the exercise can still be read.',
    statusChecking: 'Checking availability…',
    output: 'Output', noRunYet: 'No run yet.', noRecap: 'No PLAY RECAP found — likely a syntax or module error (see output below).',
    ok: 'ok', changed: 'changed', failed: 'failed', skipped: 'skipped',
    rc: 'Return code', duration: 'Duration', truncated: 'Output truncated', timedOut: 'Timed out',
    challenge: 'Run the same playbook twice and explain the difference.',
  },
} as const

export function AnsibleLab({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const scope = useWidgetScope()
  const storageKey = scope ? `intnetwork-ansiblelab-${scope}` : null

  const [snap] = useState(() => loadSnapshot(storageKey))
  const [exerciseId, setExerciseId] = useState(snap.exerciseId)
  const [playbook, setPlaybook] = useState(snap.playbook)
  const [extraVars, setExtraVars] = useState(snap.extraVars)
  const exercise = exerciseById(exerciseId)

  useEffect(() => {
    if (!storageKey) return
    try {
      localStorage.setItem(storageKey, JSON.stringify({ exerciseId, playbook, extraVars }))
    } catch {
      // Speicher voll/blockiert — die Sitzung läuft für die Seite trotzdem weiter.
    }
  }, [storageKey, exerciseId, playbook, extraVars])

  const { labEnabled } = useLabAvailability()

  const [running, setRunning] = useState<'run' | 'check' | null>(null)
  const [result, setResult] = useState<LabRunResult | null>(null)
  const [runError, setRunError] = useState<string | null>(null)
  const [prevRecap, setPrevRecap] = useState<RecapTotals | null>(null)
  const [note, setNote] = useState<IdempotencyNote | null>(null)

  function pickExercise(id: string) {
    const ex = exerciseById(id)
    setExerciseId(ex.id)
    setPlaybook(ex.playbook)
    setExtraVars('')
    setResult(null)
    setRunError(null)
    setPrevRecap(null)
    setNote(null)
  }

  function resetToTemplate() {
    setPlaybook(exercise.playbook)
    setExtraVars('')
    setResult(null)
    setRunError(null)
    setPrevRecap(null)
    setNote(null)
  }

  async function handleRun(check: boolean) {
    setRunning(check ? 'check' : 'run')
    setRunError(null)
    try {
      const res = await runLab({ playbook, extra_vars: extraVars.trim() || undefined, check })
      setResult(res)
      const recap = parseRecap(res.output)
      if (check) {
        // --check verändert nichts am Zielzustand — als Idempotenz-Basislinie
        // ungeeignet, deshalb hier keine Einordnung und kein neues prevRecap.
        setNote(null)
      } else {
        setNote(compareIdempotency(prevRecap, recap, lang))
        setPrevRecap(recap)
      }
    } catch (e) {
      setRunError(labErrorMessage(e, lang))
      setResult(null)
    } finally {
      setRunning(null)
    }
  }

  const recap = result ? parseRecap(result.output) : null
  const charCount = playbook.length
  const tooLong = charCount > MAX_CHARS
  const disabled = labEnabled !== true || running !== null || tooLong

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-3">{s.hint}</p>

      <div className="flex flex-wrap gap-1 mb-3">
        {EXERCISES.map((ex) => (
          <button key={ex.id} type="button" onClick={() => pickExercise(ex.id)}
            className={`rounded-lg border px-2 py-1 text-xs ${
              exerciseId === ex.id ? 'border-teal-300 bg-teal-50 text-teal-800' : 'hover:bg-slate-50'}`}>
            {lang === 'de' ? ex.title.de : ex.title.en}
          </button>
        ))}
      </div>

      <p className="mb-3 text-sm text-slate-700">{lang === 'de' ? exercise.task.de : exercise.task.en}</p>

      {labEnabled === false && <LabDisabledBanner title={s.disabledTitle} body={s.disabledBody} />}

      <label className="mb-1 block text-xs font-medium text-slate-600" htmlFor="ansiblelab-playbook">
        {s.playbookLabel}
      </label>
      <textarea
        id="ansiblelab-playbook" value={playbook} onChange={(e) => setPlaybook(e.target.value)}
        spellCheck={false} rows={14}
        className="w-full rounded-lg border px-2 py-1.5 font-mono text-xs text-slate-800 mb-1"
      />
      <p className={`mb-3 text-[11px] ${charCount >= WARN_CHARS ? 'text-amber-700' : 'text-slate-400'}`}>
        {charCount.toLocaleString(lang === 'de' ? 'de-DE' : 'en-US')} / {MAX_CHARS.toLocaleString(lang === 'de' ? 'de-DE' : 'en-US')} {s.chars}
        {charCount >= WARN_CHARS && <> — {s.charWarning}</>}
      </p>

      <label className="mb-1 block text-xs font-medium text-slate-600" htmlFor="ansiblelab-extravars">
        {s.extraVarsLabel}
      </label>
      <input
        id="ansiblelab-extravars" value={extraVars} onChange={(e) => setExtraVars(e.target.value)}
        placeholder={s.extraVarsPlaceholder} spellCheck={false}
        className="mb-3 w-full rounded-lg border px-2 py-1.5 font-mono text-xs text-slate-800"
      />

      <div className="mb-3 flex flex-wrap items-center gap-2">
        <button type="button" onClick={() => handleRun(false)} disabled={disabled}
          className="rounded-lg border border-teal-300 bg-teal-50 px-3 py-1.5 text-xs font-medium text-teal-800 hover:bg-teal-100 disabled:cursor-not-allowed disabled:opacity-50">
          {running === 'run' ? s.running : s.run}
        </button>
        <button type="button" onClick={() => handleRun(true)} disabled={disabled}
          className="rounded-lg border px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50">
          {running === 'check' ? s.checking : s.check}
        </button>
        <button type="button" onClick={resetToTemplate}
          className="rounded-lg border px-3 py-1.5 text-xs text-slate-500 hover:bg-slate-50">
          {s.reset}
        </button>
        {labEnabled === null && <span className="text-[11px] text-slate-400">{s.statusChecking}</span>}
        {running !== null && <span className="text-[11px] text-slate-400" role="status">{running === 'run' ? s.running : s.checking}</span>}
      </div>

      <LabOutputPanel
        outputLabel={s.output}
        runError={runError}
        errorClassName="text-red-300"
        result={result}
        noRunYetLabel={s.noRunYet}
        rcLabel={s.rc}
        durationLabel={s.duration}
        truncatedLabel={s.truncated}
        timedOutLabel={s.timedOut}
      >
        {/* text-slate-100 an den Kacheln ist Absicht: sie sind immer dunkel, ohne
            eigene Textfarbe erben die Beschriftungen die dunkle Seitenfarbe und
            waren im Hellmodus unlesbar. slate-100 ist in index.css fuer den Dark
            Mode fest hell gepinnt und passt damit in beiden Modi. */}
        {recap && (
          <div className="mb-2 grid grid-cols-4 gap-2 text-center text-xs">
            <div className="rounded bg-slate-800 py-1 text-slate-100"><span className="block text-green-400 font-mono">{recap.ok}</span>{s.ok}</div>
            <div className="rounded bg-slate-800 py-1 text-slate-100"><span className="block text-amber-400 font-mono">{recap.changed}</span>{s.changed}</div>
            <div className="rounded bg-slate-800 py-1 text-slate-100"><span className="block text-red-400 font-mono">{recap.failed}</span>{s.failed}</div>
            <div className="rounded bg-slate-800 py-1 text-slate-100"><span className="block text-slate-400 font-mono">{recap.skipped}</span>{s.skipped}</div>
          </div>
        )}
        {result && !recap && <p className="mb-2 text-xs text-amber-300">{s.noRecap}</p>}

        {note && (
          <p className={`mb-2 rounded px-2 py-1 text-xs ${
            note.kind === 'improved' ? 'bg-green-900/40 text-green-300'
            : note.kind === 'worse' ? 'bg-red-900/40 text-red-300'
            : 'bg-slate-800 text-slate-300'}`}>
            {note.message}
          </p>
        )}
      </LabOutputPanel>

      <ChallengeBox lang={lang} task={s.challenge} done={note !== null} />
    </div>
  )
}
