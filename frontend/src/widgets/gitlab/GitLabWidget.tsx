import { useEffect, useId, useState } from 'react'
import { ChallengeBox } from '@/components/ChallengeBox'
import { useWidgetScope } from '@/lib/widgetScope'
import { fetchLabStatus, labErrorMessage, runLabKind, type LabRunResult } from '@/lib/labApi'
import { validateLabRun, type LabFile } from '@/widgets/lab/limits'
import { DEFAULT_TEMPLATE, GIT_TEMPLATES, templateById } from '@/widgets/gitlab/templates'
import type { Lang } from '@/lib/i18n'

interface Snapshot {
  templateId: string
  files: LabFile[]
  commands: string[]
}

function filesFromRecord(rec: Record<string, string>): LabFile[] {
  return Object.entries(rec).map(([name, content]) => ({ name, content }))
}

// Pro Teilnehmer gespeichert (localStorage), nach demselben Muster wie
// AnsibleLabWidget.loadSnapshot: storageKey kommt aus dem Teilnehmer-/
// Kurs-Scope, ein beschädigter Eintrag fällt auf die Vorlage zurück statt die
// Seite zu zerlegen.
export function loadSnapshot(storageKey: string | null): Snapshot {
  if (storageKey) {
    try {
      const raw = localStorage.getItem(storageKey)
      if (raw) {
        const p = JSON.parse(raw)
        if (p && typeof p.templateId === 'string' && Array.isArray(p.files) && Array.isArray(p.commands)) {
          return { templateId: p.templateId, files: p.files, commands: p.commands }
        }
      }
    } catch {
      // beschädigter Eintrag -> frische Vorlage
    }
  }
  return {
    templateId: DEFAULT_TEMPLATE.id,
    files: filesFromRecord(DEFAULT_TEMPLATE.files),
    commands: [...DEFAULT_TEMPLATE.commands],
  }
}

const STR = {
  de: {
    title: 'Git-Lab',
    hint: 'Echte git-Befehle tippen und die echte Ausgabe lesen — serverseitig in einem isolierten Container.',
    workspaceHint: 'Das Arbeitsverzeichnis bleibt zwischen Läufen erhalten — ein Repository aus Schritt 1 ist in Schritt 2 noch da.',
    noNetworkTitle: 'Kein Netzwerk im Runner',
    noNetworkBody: 'clone, fetch, push und pull schlagen hier absichtlich fehl — der Runner hat keine Netzwerkverbindung. '
      + 'Das ist kein Defekt: die Übungen sind lokal (init, branch, merge, Konflikt, worktree, reflog).',
    disabledTitle: 'Lab auf diesem Server nicht aktiviert',
    disabledBody: 'Auf diesem Server ist das Git-Lab nicht aktiviert; die Aufgaben lassen sich trotzdem als Denkaufgaben lösen.',
    statusChecking: 'Prüfe Verfügbarkeit…',
    templates: 'Vorlagen',
    filesLabel: 'Dateien',
    fileName: 'Dateiname',
    fileContent: 'Inhalt',
    addFile: '+ Datei', removeFile: 'Entfernen',
    commandsLabel: 'Befehle (ohne führendes „git“)',
    command: 'Befehl', addCommand: '+ Befehl', removeCommand: 'Entfernen',
    run: 'Ausführen', running: 'Läuft…',
    output: 'Ausgabe', noRunYet: 'Noch kein Lauf.',
    rc: 'Rückgabewert', duration: 'Dauer', truncated: 'Ausgabe gekürzt', timedOut: 'Zeitüberschreitung',
    challenge: 'Führe einen Lauf mit Rückgabewert 0 aus.',
  },
  en: {
    title: 'Git Lab',
    hint: 'Type real git commands and read the real output — server-side, in an isolated container.',
    workspaceHint: 'The workspace persists between runs — a repository from step 1 is still there in step 2.',
    noNetworkTitle: 'No network in the runner',
    noNetworkBody: 'clone, fetch, push and pull fail here on purpose — the runner has no network connection. '
      + 'This is not a defect: the exercises are local (init, branch, merge, conflict, worktree, reflog).',
    disabledTitle: 'Lab not enabled on this server',
    disabledBody: 'The git lab is not enabled on this server; the exercises can still be solved as thought exercises.',
    statusChecking: 'Checking availability…',
    templates: 'Templates',
    filesLabel: 'Files',
    fileName: 'File name',
    fileContent: 'Content',
    addFile: '+ File', removeFile: 'Remove',
    commandsLabel: 'Commands (without a leading "git")',
    command: 'Command', addCommand: '+ Command', removeCommand: 'Remove',
    run: 'Run', running: 'Running…',
    output: 'Output', noRunYet: 'No run yet.',
    rc: 'Return code', duration: 'Duration', truncated: 'Output truncated', timedOut: 'Timed out',
    challenge: 'Run a command batch that returns 0.',
  },
} as const

export function GitLab({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const uid = useId()
  const scope = useWidgetScope()
  const storageKey = scope ? `intnetwork-gitlab-${scope}` : null

  const [snap] = useState(() => loadSnapshot(storageKey))
  const [templateId, setTemplateId] = useState(snap.templateId)
  const [files, setFiles] = useState<LabFile[]>(snap.files)
  const [commands, setCommands] = useState<string[]>(snap.commands)

  useEffect(() => {
    if (!storageKey) return
    try {
      localStorage.setItem(storageKey, JSON.stringify({ templateId, files, commands }))
    } catch {
      // Speicher voll/blockiert — die Sitzung läuft für die Seite trotzdem weiter.
    }
  }, [storageKey, templateId, files, commands])

  // Verfügbarkeit einmal beim Laden abfragen — lokal ohne konfigurierten
  // Runner ist "nicht aktiviert" der Normalfall, nicht der Fehlerfall.
  const [labEnabled, setLabEnabled] = useState<boolean | null>(null)
  const [kinds, setKinds] = useState<string[]>([])
  useEffect(() => {
    let live = true
    fetchLabStatus()
      .then((st) => { if (live) { setLabEnabled(st.enabled); setKinds(st.kinds) } })
      .catch(() => { if (live) { setLabEnabled(false); setKinds([]) } })
    return () => { live = false }
  }, [])

  const [running, setRunning] = useState(false)
  const [result, setResult] = useState<LabRunResult | null>(null)
  const [runError, setRunError] = useState<string | null>(null)

  function pickTemplate(id: string) {
    const tpl = templateById(id)
    setTemplateId(tpl.id)
    setFiles(filesFromRecord(tpl.files))
    setCommands([...tpl.commands])
    setResult(null)
    setRunError(null)
  }

  function addFile() {
    setFiles((prev) => [...prev, { name: '', content: '' }])
  }
  function removeFile(idx: number) {
    setFiles((prev) => prev.filter((_, i) => i !== idx))
  }
  function updateFile(idx: number, patch: Partial<LabFile>) {
    setFiles((prev) => prev.map((f, i) => (i === idx ? { ...f, ...patch } : f)))
  }

  function addCommand() {
    setCommands((prev) => [...prev, ''])
  }
  function removeCommand(idx: number) {
    setCommands((prev) => prev.filter((_, i) => i !== idx))
  }
  function updateCommand(idx: number, value: string) {
    setCommands((prev) => prev.map((c, i) => (i === idx ? value : c)))
  }

  const violation = validateLabRun(files, commands)
  const kindEnabled = labEnabled === true && kinds.includes('git')
  const disabled = !kindEnabled || running || violation !== null

  async function handleRun() {
    if (violation !== null) return
    setRunning(true)
    setRunError(null)
    try {
      const filesRecord: Record<string, string> = {}
      for (const f of files) filesRecord[f.name] = f.content
      const res = await runLabKind({ kind: 'git', files: filesRecord, commands })
      setResult(res)
    } catch (e) {
      setRunError(labErrorMessage(e, lang))
      setResult(null)
    } finally {
      setRunning(false)
    }
  }

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-1">{s.hint}</p>
      <p className="text-xs text-slate-500 mb-3">{s.workspaceHint}</p>

      <div className="mb-3 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-600">
        <p className="font-semibold">{s.noNetworkTitle}</p>
        <p>{s.noNetworkBody}</p>
      </div>

      {labEnabled !== null && !kindEnabled && (
        <div className="mb-3 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-xs text-amber-800">
          <p className="font-semibold">{s.disabledTitle}</p>
          <p>{s.disabledBody}</p>
        </div>
      )}

      <p className="mb-1 text-xs font-medium text-slate-600">{s.templates}</p>
      <div className="flex flex-wrap gap-1 mb-3">
        {GIT_TEMPLATES.map((tpl) => (
          <button key={tpl.id} type="button" onClick={() => pickTemplate(tpl.id)}
            title={lang === 'de' ? tpl.hint.de : tpl.hint.en}
            className={`rounded-lg border px-2 py-1 text-xs ${
              templateId === tpl.id ? 'border-teal-300 bg-teal-50 text-teal-800' : 'hover:bg-slate-50'}`}>
            {lang === 'de' ? tpl.title.de : tpl.title.en}
          </button>
        ))}
      </div>
      <p className="mb-3 text-xs text-slate-600">
        {lang === 'de' ? templateById(templateId).hint.de : templateById(templateId).hint.en}
      </p>

      <p className="mb-1 text-xs font-medium text-slate-600">{s.filesLabel}</p>
      <div className="mb-2 flex flex-col gap-2">
        {files.map((f, idx) => (
          <div key={`${uid}-file-${idx}`} className="flex flex-wrap items-start gap-2 rounded-lg border p-2">
            <div className="min-w-0 flex-1">
              <label className="mb-1 block text-[11px] font-medium text-slate-600" htmlFor={`${uid}-file-name-${idx}`}>
                {s.fileName}
              </label>
              <input
                id={`${uid}-file-name-${idx}`} value={f.name} spellCheck={false}
                onChange={(e) => updateFile(idx, { name: e.target.value })}
                className="w-full rounded-lg border px-2 py-1 font-mono text-xs text-slate-800"
              />
            </div>
            <div className="min-w-0 flex-[2]">
              <label className="mb-1 block text-[11px] font-medium text-slate-600" htmlFor={`${uid}-file-content-${idx}`}>
                {s.fileContent}
              </label>
              <textarea
                id={`${uid}-file-content-${idx}`} value={f.content} spellCheck={false} rows={2}
                onChange={(e) => updateFile(idx, { content: e.target.value })}
                className="w-full rounded-lg border px-2 py-1 font-mono text-xs text-slate-800"
              />
            </div>
            <button type="button" onClick={() => removeFile(idx)}
              className="mt-5 rounded-lg border px-2 py-1 text-[11px] text-slate-500 hover:bg-slate-50">
              {s.removeFile}
            </button>
          </div>
        ))}
      </div>
      <button type="button" onClick={addFile}
        className="mb-3 rounded-lg border px-2 py-1 text-xs text-slate-600 hover:bg-slate-50">
        {s.addFile}
      </button>

      <p className="mb-1 text-xs font-medium text-slate-600">{s.commandsLabel}</p>
      <div className="mb-2 flex flex-col gap-2">
        {commands.map((c, idx) => (
          <div key={`${uid}-cmd-${idx}`} className="flex items-center gap-2">
            <label className="sr-only" htmlFor={`${uid}-cmd-${idx}`}>
              {`${s.command} ${idx + 1}`}
            </label>
            <input
              id={`${uid}-cmd-${idx}`} value={c} spellCheck={false}
              onChange={(e) => updateCommand(idx, e.target.value)}
              className="w-full rounded-lg border px-2 py-1 font-mono text-xs text-slate-800"
            />
            <button type="button" onClick={() => removeCommand(idx)}
              className="shrink-0 rounded-lg border px-2 py-1 text-[11px] text-slate-500 hover:bg-slate-50">
              {s.removeCommand}
            </button>
          </div>
        ))}
      </div>
      <button type="button" onClick={addCommand}
        className="mb-3 rounded-lg border px-2 py-1 text-xs text-slate-600 hover:bg-slate-50">
        {s.addCommand}
      </button>

      {violation && (
        <p className="mb-3 rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-xs text-rose-800">
          {lang === 'de' ? violation.de : violation.en}
        </p>
      )}

      <div className="mb-3 flex flex-wrap items-center gap-2">
        <button type="button" onClick={handleRun} disabled={disabled}
          className="rounded-lg border border-teal-300 bg-teal-50 px-3 py-1.5 text-xs font-medium text-teal-800 hover:bg-teal-100 disabled:cursor-not-allowed disabled:opacity-50">
          {running ? s.running : s.run}
        </button>
        {labEnabled === null && <span className="text-[11px] text-slate-400">{s.statusChecking}</span>}
        {running && <span className="text-[11px] text-slate-400" role="status">{s.running}</span>}
      </div>

      <p className="mb-2 text-xs font-medium text-slate-600">{s.output}</p>
      <div aria-live="polite" className="rounded-lg bg-slate-900 p-3">
        {runError && <p className="mb-2 text-xs text-rose-300">{runError}</p>}

        {result ? (
          <>
            <pre className="max-h-72 overflow-y-auto whitespace-pre-wrap font-mono text-xs text-slate-100">{result.output}</pre>
            <p className="mt-2 text-[11px] text-slate-500">
              {s.rc}: {result.rc} · {s.duration}: {result.duration_ms} ms
              {result.truncated && <> · {s.truncated}</>}
              {result.timed_out && <> · {s.timedOut}</>}
            </p>
          </>
        ) : (
          <p className="font-mono text-xs text-slate-500">{s.noRunYet}</p>
        )}
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={result !== null && result.rc === 0} />
    </div>
  )
}
