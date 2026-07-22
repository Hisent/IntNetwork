export type WorkshopThemeName = 'network' | 'claude' | 'infoblox' | 'ansible' | 'pki' | 'nac'

// workshop_key (persistiert, z.B. aus dem Formular) -> visuelles Theme.
// Entspricht 1:1 dem `theme`-Feld in backend/app/content/workshops.py:
// key == Theme-Name, einzige Ausnahme ist 'claude-code' -> 'claude'.
export function workshopTheme(workshopKey?: string | null): WorkshopThemeName {
  if (workshopKey === 'claude-code') return 'claude'
  if (workshopKey === 'infoblox' || workshopKey === 'ansible' || workshopKey === 'pki'
      || workshopKey === 'nac') return workshopKey
  return 'network'
}
