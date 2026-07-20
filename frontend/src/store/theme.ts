import { create } from 'zustand'

export type Theme = 'light' | 'dark'
const STORAGE_KEY = 'intnetwork-theme'

const systemPrefersDark = () =>
  typeof window !== 'undefined' && window.matchMedia?.('(prefers-color-scheme: dark)').matches

// Gespeicherte Wahl gewinnt; sonst Systemeinstellung. Kein „system"-Drittzustand
// im Store — die Auto-Erkennung passiert nur beim ersten Laden.
const initialTheme = (): Theme => {
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY)
    if (stored === 'light' || stored === 'dark') return stored
  } catch {
    // localStorage kann blockiert sein — dann Systemwert.
  }
  return systemPrefersDark() ? 'dark' : 'light'
}

const apply = (theme: Theme) => {
  if (typeof document !== 'undefined') document.documentElement.dataset.theme = theme
}

const startTheme: Theme = typeof window === 'undefined' ? 'light' : initialTheme()
apply(startTheme)

interface ThemeState {
  theme: Theme
  toggle: () => void
}

export const useThemeStore = create<ThemeState>((set, get) => ({
  theme: startTheme,
  toggle: () => {
    const next: Theme = get().theme === 'dark' ? 'light' : 'dark'
    apply(next)
    try {
      window.localStorage.setItem(STORAGE_KEY, next)
    } catch {
      // Persistenz optional — Umschalten wirkt trotzdem für die Sitzung.
    }
    set({ theme: next })
  },
}))
