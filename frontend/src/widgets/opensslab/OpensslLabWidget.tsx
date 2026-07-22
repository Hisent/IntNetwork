import { useWidgetScope } from '@/lib/widgetScope'
import { FileCommandLabConsole } from '@/widgets/lab/FileCommandLabConsole'
import { useFileCommandLab } from '@/widgets/lab/useFileCommandLab'
import { DEFAULT_TEMPLATE, OPENSSL_TEMPLATES, templateById } from '@/widgets/opensslab/templates'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'Openssl-Lab',
    hint: 'Echte openssl-Befehle tippen und die echte Ausgabe lesen — serverseitig in einem isolierten Container.',
    workspaceHint: 'Das Arbeitsverzeichnis bleibt zwischen Läufen erhalten: eine in Schritt 1 erzeugte CA ist in Schritt 3 noch da.',
    disabledTitle: 'Lab auf diesem Server nicht aktiviert',
    disabledBody: 'Auf diesem Server ist das Openssl-Lab nicht aktiviert; die Aufgaben lassen sich trotzdem als Denkaufgaben lösen.',
    statusChecking: 'Prüfe Verfügbarkeit…',
    templates: 'Vorlagen',
    filesLabel: 'Dateien',
    fileName: 'Dateiname',
    fileContent: 'Inhalt',
    addFile: '+ Datei', removeFile: 'Entfernen',
    commandsLabel: 'Befehle (ohne führendes „openssl“)',
    command: 'Befehl', addCommand: '+ Befehl', removeCommand: 'Entfernen',
    run: 'Ausführen', running: 'Läuft…',
    output: 'Ausgabe', noRunYet: 'Noch kein Lauf.',
    rc: 'Rückgabewert', duration: 'Dauer', truncated: 'Ausgabe gekürzt', timedOut: 'Zeitüberschreitung',
    challenge: 'Führe einen Lauf mit Rückgabewert 0 aus.',
  },
  en: {
    title: 'Openssl Lab',
    hint: 'Type real openssl commands and read the real output — server-side, in an isolated container.',
    workspaceHint: 'The workspace persists between runs: a CA created in step 1 is still there in step 3.',
    disabledTitle: 'Lab not enabled on this server',
    disabledBody: 'The openssl lab is not enabled on this server; the exercises can still be solved as thought exercises.',
    statusChecking: 'Checking availability…',
    templates: 'Templates',
    filesLabel: 'Files',
    fileName: 'File name',
    fileContent: 'Content',
    addFile: '+ File', removeFile: 'Remove',
    commandsLabel: 'Commands (without a leading "openssl")',
    command: 'Command', addCommand: '+ Command', removeCommand: 'Remove',
    run: 'Run', running: 'Running…',
    output: 'Output', noRunYet: 'No run yet.',
    rc: 'Return code', duration: 'Duration', truncated: 'Output truncated', timedOut: 'Timed out',
    challenge: 'Run a command batch that returns 0.',
  },
} as const

export function OpensslLab({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const scope = useWidgetScope()
  const storageKey = scope ? `intnetwork-opensslab-${scope}` : null

  const state = useFileCommandLab({
    kind: 'openssl', lang, storageKey, defaultTemplate: DEFAULT_TEMPLATE, templateById,
  })

  const activeTemplate = templateById(state.templateId)
  const activeHint = lang === 'de' ? activeTemplate.hint.de : activeTemplate.hint.en

  return (
    <FileCommandLabConsole
      lang={lang} s={s} templates={OPENSSL_TEMPLATES} activeHint={activeHint} state={state}
    />
  )
}
