export type WorkshopThemeName = 'network' | 'claude'

export function workshopTheme(workshopKey?: string | null): WorkshopThemeName {
  return workshopKey === 'claude-code' ? 'claude' : 'network'
}
