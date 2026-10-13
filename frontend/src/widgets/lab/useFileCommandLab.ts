import { useEffect, useState } from 'react'
import { labErrorMessage, runLabKind, type LabRunResult } from '@/lib/labApi'
import { filesFromRecord, validateLabRun, type LabFile, type LimitViolation } from '@/widgets/lab/limits'
import { readSnapshot } from '@/widgets/lab/snapshot'
import { useLabAvailability } from '@/widgets/lab/useLabAvailability'
import type { Lang } from '@/lib/i18n'

// Vorlagenform, die OpensslLabWidget und GitLabWidget teilen (siehe deren
// templates.ts): eine Kennung, Dateien fürs Arbeitsverzeichnis, eine
// Befehlsliste. Titel/Hinweistext gehören bewusst nicht zu diesem Typ — die
// braucht nur die Präsentationsschicht (FileCommandLabConsole), nicht die
// Zustandslogik hier.
export interface FileCommandTemplate {
  id: string
  files: Record<string, string>
  commands: string[]
}

interface Snapshot {
  templateId: string
  files: LabFile[]
  commands: string[]
}

// Streng: jedes Element wird geprüft. Ein Eintrag wie files: [null] oder
// commands: [42] (beschädigt/fremd) würde sonst erst beim Rendern bzw. in
// validateLabRun mit einem TypeError die Seite zerlegen.
export function isSnapshot(parsed: unknown): parsed is Snapshot {
  if (typeof parsed !== 'object' || parsed === null) return false
  const rec = parsed as Record<string, unknown>
  return typeof rec.templateId === 'string'
    && Array.isArray(rec.files)
    && rec.files.every((f: unknown) => typeof f === 'object' && f !== null
      && typeof (f as Record<string, unknown>).name === 'string'
      && typeof (f as Record<string, unknown>).content === 'string')
    && Array.isArray(rec.commands)
    && rec.commands.every((c: unknown) => typeof c === 'string')
}

export interface UseFileCommandLabArgs {
  kind: 'openssl' | 'git'
  lang: Lang
  storageKey: string | null
  defaultTemplate: FileCommandTemplate
  templateById: (id: string) => FileCommandTemplate
  // Vorlagen des aktuellen Moduls: Der Speicher gilt je Teilnehmer/Kurs, nicht
  // je Modul — ein gespeicherter Stand bleibt nur, wenn seine Vorlage hierzu
  // gehört, sonst startet das Widget mit defaultTemplate (wie im Ansible-Lab).
  moduleTemplateIds?: string[]
}

export interface FileCommandLabState {
  templateId: string
  files: LabFile[]
  commands: string[]
  labEnabled: boolean | null
  kindEnabled: boolean
  running: boolean
  result: LabRunResult | null
  runError: string | null
  violation: LimitViolation | null
  disabled: boolean
  pickTemplate: (id: string) => void
  addFile: () => void
  removeFile: (idx: number) => void
  updateFile: (idx: number, patch: Partial<LabFile>) => void
  addCommand: () => void
  removeCommand: (idx: number) => void
  updateCommand: (idx: number, value: string) => void
  handleRun: () => void
}

// Gemeinsame Zustands- und Lauf-Logik für OpensslLabWidget und GitLabWidget:
// beide arbeiten nach demselben Muster (Vorlage wählen -> Dateien/Befehle
// editieren -> serverseitig ausführen -> rohe Ausgabe zeigen). Absichtlich
// NICHT für AnsibleLabWidget gedacht: dort ist die Eingabe ein einzelnes
// Playbook plus Extra-Vars (keine Datei-/Befehlsliste), und es kommt die
// Idempotenz-Sonderlogik (zweiter-Lauf-Vergleich) dazu, die hier keine
// Entsprechung hat.
export function useFileCommandLab({
  kind, lang, storageKey, defaultTemplate, templateById, moduleTemplateIds,
}: UseFileCommandLabArgs): FileCommandLabState {
  const [snap] = useState<Snapshot>(() => {
    const fresh = () => ({
      templateId: defaultTemplate.id,
      files: filesFromRecord(defaultTemplate.files),
      commands: [...defaultTemplate.commands],
    })
    const stored = readSnapshot(storageKey, isSnapshot, fresh)
    return moduleTemplateIds && !moduleTemplateIds.includes(stored.templateId) ? fresh() : stored
  })
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

  const { labEnabled, kinds } = useLabAvailability()

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
  const kindEnabled = labEnabled === true && kinds.includes(kind)
  const disabled = !kindEnabled || running || violation !== null

  async function handleRun() {
    if (violation !== null) return
    setRunning(true)
    setRunError(null)
    try {
      // Doppelte Namen kommen hier nicht an: validateLabRun meldet sie als
      // Grenzverletzung (sonst überschriebe der spätere Eintrag still den früheren).
      const filesRecord: Record<string, string> = {}
      for (const f of files) filesRecord[f.name] = f.content
      const res = await runLabKind({ kind, files: filesRecord, commands })
      setResult(res)
    } catch (e) {
      setRunError(labErrorMessage(e, lang))
      setResult(null)
    } finally {
      setRunning(false)
    }
  }

  return {
    templateId, files, commands,
    labEnabled, kindEnabled, running, result, runError, violation, disabled,
    pickTemplate, addFile, removeFile, updateFile, addCommand, removeCommand, updateCommand, handleRun,
  }
}
