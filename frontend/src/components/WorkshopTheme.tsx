import type { ReactNode } from 'react'

import type { WorkshopThemeName } from '@/lib/workshopTheme'

export function WorkshopTheme({ theme = 'network', children }: { theme?: WorkshopThemeName; children: ReactNode }) {
  return <div className={`workshop-theme workshop-theme--${theme}`}>{children}</div>
}
