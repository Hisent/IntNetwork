// Tastatursteuerung des Beamer-Modus (TrainerPresentPage) als reine Funktion.
// Folien zeigen interaktive Widgets: deren Bedienelemente brauchen Pfeiltasten
// und Leertaste selbst — sonst blättert die Folie weiter, statt den Knopf
// auszulösen oder das <select> zu bedienen.
export type SlideKeyAction = 'next' | 'prev' | 'exit' | null

const EDITING = 'input, textarea, select, [contenteditable="true"], [role="slider"]'
const ACTIVATABLE = 'button, a[href], summary, [role="button"], [tabindex]:not([tabindex="-1"])'

export function slideKeyAction(key: string, target: EventTarget | null): SlideKeyAction {
  const el = target instanceof Element ? target : null
  if (el?.closest(EDITING)) return null
  if (key === 'Escape') return 'exit'
  if (key === 'ArrowRight' || key === 'PageDown') return 'next'
  if (key === 'ArrowLeft' || key === 'PageUp') return 'prev'
  // Leertaste gehört dem fokussierten Bedienelement; nur „im Leeren“ blättert sie.
  if (key === ' ') return el?.closest(ACTIVATABLE) ? null : 'next'
  return null
}
