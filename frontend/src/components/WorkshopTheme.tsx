import type { ReactNode } from 'react'

export function WorkshopTheme({ theme = 'network', children }: { theme?: 'network' | 'claude'; children: ReactNode }) {
  return <div className={`workshop-theme workshop-theme--${theme}`}>{children}</div>
}
