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
