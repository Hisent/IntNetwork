import type { ModuleMeta, Workshop } from '@/types'

export type ModuleSection = Workshop['sections'][number]

export interface ModuleGroup {
  key: string
  title_de: string
  title_en: string
  modules: ModuleMeta[]
}

const FALLBACK_SECTION: ModuleSection = { key: 'modules', from: -Infinity, to: Infinity, title_de: 'Module', title_en: 'Modules' }

// Gruppiert Module nach den Workshop-Sections (z.B. Tagesgruppen) — eine
// Stelle, die von der Kursübersicht (LearnPage) UND der Modul-Sidebar
// (ModulePage) genutzt wird, damit beide dieselbe Gliederung zeigen statt
// zweier leicht unterschiedlicher Ansichten derselben Daten. Reine Funktion,
// unabhängig von React/Sprache — die Sprachauswahl (title_de/title_en)
// passiert erst beim Rendern.
export function groupModulesBySection(modules: ModuleMeta[], sections?: ModuleSection[]): ModuleGroup[] {
  const sorted = [...modules].sort((a, b) => a.order - b.order)
  const list = sections && sections.length > 0 ? sections : [FALLBACK_SECTION]
  return list
    .map((section) => ({
      key: section.key,
      title_de: section.title_de,
      title_en: section.title_en,
      modules: sorted.filter((module) => module.order >= section.from && module.order <= section.to),
    }))
    .filter((group) => group.modules.length > 0)
}
