import { useWidgetScope } from '@/lib/widgetScope'
import { FileCommandLabConsole } from '@/widgets/lab/FileCommandLabConsole'
import { useFileCommandLab } from '@/widgets/lab/useFileCommandLab'
import { DEFAULT_TEMPLATE, GIT_TEMPLATES, templateById } from '@/widgets/gitlab/templates'
import type { Lang } from '@/lib/i18n'

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
  const scope = useWidgetScope()
  const storageKey = scope ? `intnetwork-gitlab-${scope}` : null

  const state = useFileCommandLab({
    kind: 'git', lang, storageKey, defaultTemplate: DEFAULT_TEMPLATE, templateById,
  })

  const activeTemplate = templateById(state.templateId)
  const activeHint = lang === 'de' ? activeTemplate.hint.de : activeTemplate.hint.en

  const banner = (
    <div className="mb-3 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-600">
      <p className="font-semibold">{s.noNetworkTitle}</p>
      <p>{s.noNetworkBody}</p>
    </div>
  )

  return (
    <FileCommandLabConsole
      lang={lang} s={s} templates={GIT_TEMPLATES} activeHint={activeHint} banner={banner} state={state}
    />
  )
}
