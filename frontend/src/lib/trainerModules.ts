// Gruppiert die Trainer-Modulliste nach Workshop, damit die Modulverwaltung
// bei vielen Modulen nicht als flache Pill-Wand mit 30+ Einträgen erscheint.
import type { ModuleMeta } from '@/types'

export interface ModuleGroup {
  key: string
  title: string
  modules: ModuleMeta[]
}

export function groupModulesByWorkshop(
  modules: ModuleMeta[],
  workshops: { key: string; title: { de: string } }[],
): ModuleGroup[] {
  const groups: ModuleGroup[] = workshops.map((w) => ({ key: w.key, title: w.title.de, modules: [] }))
  const rest: ModuleMeta[] = []
  for (const m of modules) {
    const group = m.workshop_key ? groups.find((g) => g.key === m.workshop_key) : undefined
    if (group) group.modules.push(m)
    else rest.push(m)
  }
  const nonEmpty = groups.filter((g) => g.modules.length > 0)
  if (rest.length > 0) nonEmpty.push({ key: '__sonstige', title: 'Sonstige', modules: rest })
  return nonEmpty
}
