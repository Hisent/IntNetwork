import { useQuery } from '@tanstack/react-query'
import { useAuthStore } from '@/store/auth'
import { trainerApi } from '@/lib/trainerApi'

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

const THEMES = ['network', 'claude', 'infoblox', 'ansible', 'pki', 'nac']

// Trainer-Ansicht: ein per MCP angelegter Workshop trägt sein Theme selbst
// (Key != Theme-Name); gleicher Query wie TrainerPage (geteilter Cache), sonst Key-Heuristik.
export function useWorkshopTheme(workshopKey?: string | null): WorkshopThemeName {
  const loggedIn = useAuthStore((s) => s.role === 'trainer' && !!s.token)
  const { data } = useQuery({ queryKey: ['trainer-workshops'], queryFn: () => trainerApi.trainerWorkshops().then((r) => r.data), enabled: loggedIn })
  const t = data?.find((w) => w.key === workshopKey)?.theme
  return t && THEMES.includes(t) ? t : workshopTheme(workshopKey)
}
