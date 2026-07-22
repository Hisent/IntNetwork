// Client-seitige Vorabprüfung für die Runner-Arten "openssl" und "git" (siehe
// docs/ideen/2026-07-22-lab-erweiterung.md, Änderung 2/3). Der Server prüft
// dieselben Grenzen unabhängig noch einmal — hier geht es nur darum, dass eine
// Verletzung sofort im Formular sichtbar wird statt erst nach einem
// Server-Fehlschlag. Bewusst der einzige Baustein, den OpensslLabWidget und
// GitLabWidget teilen: beide brauchen identische Grenzen, alles andere
// (Layout, Vorlagen, Zustand) bleibt je Widget eigenständig.
export const MAX_COMMANDS = 6
export const MAX_COMMAND_CHARS = 512
export const MAX_FILES = 10
export const MAX_FILE_BYTES = 32 * 1024
export const FILENAME_RE = /^[A-Za-z0-9._-]{1,64}$/

export interface LabFile {
  name: string
  content: string
}

export interface LimitViolation {
  de: string
  en: string
}

// Liefert die erste verletzte Regel (bilingual) oder null, wenn Dateien und
// Befehle innerhalb der Grenzen liegen. Eine Meldung reicht — nach der
// Korrektur greift die nächste Prüfung beim nächsten Tastendruck erneut.
export function validateLabRun(files: LabFile[], commands: string[]): LimitViolation | null {
  if (files.length > MAX_FILES) {
    return { de: `Höchstens ${MAX_FILES} Dateien pro Lauf.`, en: `At most ${MAX_FILES} files per run.` }
  }
  for (const f of files) {
    if (!FILENAME_RE.test(f.name)) {
      return {
        de: `Ungültiger Dateiname "${f.name}" (erlaubt: Buchstaben, Ziffern, Punkt, Unterstrich, Bindestrich; max. 64 Zeichen).`,
        en: `Invalid file name "${f.name}" (allowed: letters, digits, dot, underscore, hyphen; max 64 characters).`,
      }
    }
    if (new TextEncoder().encode(f.content).length > MAX_FILE_BYTES) {
      return {
        de: `Datei "${f.name}" ist größer als ${MAX_FILE_BYTES / 1024} KB.`,
        en: `File "${f.name}" is larger than ${MAX_FILE_BYTES / 1024} KB.`,
      }
    }
  }
  if (commands.length === 0) {
    return { de: 'Mindestens ein Befehl wird benötigt.', en: 'At least one command is required.' }
  }
  if (commands.length > MAX_COMMANDS) {
    return { de: `Höchstens ${MAX_COMMANDS} Befehle pro Lauf.`, en: `At most ${MAX_COMMANDS} commands per run.` }
  }
  for (const c of commands) {
    if (c.length > MAX_COMMAND_CHARS) {
      return {
        de: `Ein Befehl ist länger als ${MAX_COMMAND_CHARS} Zeichen.`,
        en: `A command is longer than ${MAX_COMMAND_CHARS} characters.`,
      }
    }
  }
  return null
}
