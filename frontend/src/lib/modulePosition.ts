import type { ModuleMeta } from '@/types'

// `order` ist ein interner Sortierschlüssel, kein Anzeigewert: Der
// Claude-Code-Workshop nutzt bewusst Werte ab 100 (siehe `workshop_for_order`
// im Backend, `backend/app/content/workshops.py`), damit Module dort einem
// Workshop zugeordnet werden können. Roh angezeigt ("Modul 101") widerspricht
// sich mit "0/18 Module" für jeden neuen Teilnehmer. Diese Funktion bildet
// stattdessen die Position 1..n innerhalb der gegebenen Modulliste ab — die
// Liste kommt bereits kursscoped vom Backend (GET /api/modules), enthält für
// den Claude-Workshop also nur dessen 18 Module, nicht die Netzwerk-Module.
// Backend bewusst nicht angefasst (siehe Kommentar oben) — nur die Anzeige
// wird hier korrigiert, eine reine Funktion, damit Modulseite, deren Sidebar
// und Kursübersicht dieselbe Zahl zeigen.
export function modulePositions(modules: ModuleMeta[]): Map<string, number> {
  const sorted = [...modules].sort((a, b) => a.order - b.order)
  return new Map(sorted.map((module, index) => [module.key, index + 1]))
}
