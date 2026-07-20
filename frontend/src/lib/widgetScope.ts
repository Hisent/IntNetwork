import { createContext, useContext } from 'react'

// Teilnehmer-/Kurs-Präfix (`${participantId}-${courseId}`), von `Blocks`
// bereitgestellt. Widgets, die pro Teilnehmer speichern (z.B. die Live-CLI),
// lesen ihn hier — ohne dass alle Widgets eine extra Prop bekommen müssen.
// Leerer String = kein Teilnehmerkontext (Trainer-Vorschau, ausgeloggt) -> nicht speichern.
export const WidgetScopeContext = createContext<string>('')

export const useWidgetScope = () => useContext(WidgetScopeContext)
