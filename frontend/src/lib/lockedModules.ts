export interface LockedInput { key: string; locked: boolean }
export interface LockedVisibility { key: string; locked: boolean; visible: boolean }

// Bestimmt, welche gesperrten Module direkt sichtbar bleiben (die nächsten
// `keepLockedCount` in Kursreihenfolge) und welche hinter "weitere anzeigen"
// verschwinden. Abgeschlossene und freigeschaltete Module sind immer
// sichtbar — das Zusammenklappen betrifft ausschließlich die Sperren
// dahinter, damit der erste Eindruck nach dem Beitritt nicht aus einer Wand
// aus "Voraussetzung offen"-Zeilen besteht.
export function markLockedVisibility(modules: LockedInput[], keepLockedCount = 3): LockedVisibility[] {
  let budget = keepLockedCount
  return modules.map(({ key, locked }) => {
    if (!locked) return { key, locked, visible: true }
    if (budget > 0) {
      budget -= 1
      return { key, locked, visible: true }
    }
    return { key, locked, visible: false }
  })
}

/** Voraussetzungen eines Moduls, die im Kurs aktiv sind. `GET /modules` liefert die rohen
 *  Voraussetzungen; ist eine davon im Kurs abgewählt, gibt es sie hier nicht zu bestehen
 *  und sie gilt als erfüllt (sonst bliebe das Modul dauerhaft ausgegraut). */
export function coursePrerequisites(module: { prerequisites: string[] }, courseModules: { key: string }[]): string[] {
  return module.prerequisites.filter((key) => courseModules.some((m) => m.key === key))
}

/** Noch nicht bestandene Voraussetzungen eines Moduls (Schlüssel, in Modul-Reihenfolge).
 *  Leer = freigeschaltet. Die „Sperre“ ist didaktische Führung, keine Zugriffskontrolle:
 *  Lernseite, Suche und Modulseite kennzeichnen damit nur, worauf ein Modul aufbaut. */
export function openPrerequisites(
  module: { prerequisites: string[] },
  progress: { module_key: string; done: boolean }[],
  courseModules: { key: string }[],
): string[] {
  return coursePrerequisites(module, courseModules).filter((key) => !progress.some((item) => item.module_key === key && item.done))
}
