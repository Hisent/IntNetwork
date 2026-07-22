import type { ReactNode } from 'react'

export type WorkshopThemeName = 'network' | 'claude' | 'infoblox' | 'ansible' | 'pki' | 'nac'

export function WorkshopTheme({ theme = 'network', children }: { theme?: WorkshopThemeName; children: ReactNode }) {
  return <div className={`workshop-theme workshop-theme--${theme}`}>{children}</div>
}
