import { useId, type ReactNode } from 'react'
import { ChallengeBox } from '@/components/ChallengeBox'
import { LabDisabledBanner } from '@/widgets/lab/LabDisabledBanner'
import { LabOutputPanel } from '@/widgets/lab/LabOutputPanel'
import type { FileCommandLabState } from '@/widgets/lab/useFileCommandLab'
import type { Lang } from '@/lib/i18n'

export interface FileCommandLabStrings {
  title: string
  hint: string
  workspaceHint: string
  disabledTitle: string
  disabledBody: string
  statusChecking: string
  templates: string
  filesLabel: string
  fileName: string
  fileContent: string
  addFile: string
  removeFile: string
  commandsLabel: string
  command: string
  addCommand: string
  removeCommand: string
  run: string
  running: string
  output: string
  noRunYet: string
  rc: string
  duration: string
  truncated: string
  timedOut: string
  challenge: string
}

// Nur das, was die Vorlagen-Buttons + der Hinweistext brauchen — Dateien und
// Befehle einer Vorlage laufen ausschließlich durch useFileCommandLab.
export interface FileCommandTemplateMeta {
  id: string
  title: { de: string; en: string }
  hint: { de: string; en: string }
}

interface FileCommandLabConsoleProps {
  lang: Lang
  s: FileCommandLabStrings
  templates: FileCommandTemplateMeta[]
  /** Bereits aufgelöster (bilingualer) Hinweistext der aktiven Vorlage. */
  activeHint: string
  /** Zusatzhinweis vor dem "nicht aktiviert"-Banner, z.B. Git-Labs Netzwerkhinweis. */
  banner?: ReactNode
  state: FileCommandLabState
}

// Präsentationskomponente für OpensslLabWidget und GitLabWidget: Vorlagen,
// Datei-Editor, Befehlsliste, Grenzverletzung, Run-Button und Ausgabe. Beide
// Widgets liefern nur ihre Strings, ihre Vorlagenliste und den Zustand aus
// useFileCommandLab — Layout und Verhalten sind hier identisch.
export function FileCommandLabConsole({ lang, s, templates, activeHint, banner, state }: FileCommandLabConsoleProps) {
  const uid = useId()
  const {
    templateId, files, commands, labEnabled, kindEnabled, running, result, runError, violation, disabled,
    pickTemplate, addFile, removeFile, updateFile, addCommand, removeCommand, updateCommand, handleRun,
  } = state

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-1">{s.hint}</p>
      <p className="text-xs text-slate-500 mb-3">{s.workspaceHint}</p>

      {banner}

      {labEnabled !== null && !kindEnabled && (
        <LabDisabledBanner title={s.disabledTitle} body={s.disabledBody} />
      )}

      <p className="mb-1 text-xs font-medium text-slate-600">{s.templates}</p>
      <div className="flex flex-wrap gap-1 mb-3">
        {templates.map((tpl) => (
          <button key={tpl.id} type="button" onClick={() => pickTemplate(tpl.id)}
            title={lang === 'de' ? tpl.hint.de : tpl.hint.en}
            className={`rounded-lg border px-2 py-1 text-xs ${
              templateId === tpl.id ? 'border-teal-300 bg-teal-50 text-teal-800' : 'hover:bg-slate-50'}`}>
            {lang === 'de' ? tpl.title.de : tpl.title.en}
          </button>
        ))}
      </div>
      <p className="mb-3 text-xs text-slate-600">{activeHint}</p>

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

      <LabOutputPanel
        outputLabel={s.output}
        runError={runError}
        errorClassName="text-rose-300"
        result={result}
        noRunYetLabel={s.noRunYet}
        rcLabel={s.rc}
        durationLabel={s.duration}
        truncatedLabel={s.truncated}
        timedOutLabel={s.timedOut}
      />

      <ChallengeBox lang={lang} task={s.challenge} done={result !== null && result.rc === 0} />
    </div>
  )
}
