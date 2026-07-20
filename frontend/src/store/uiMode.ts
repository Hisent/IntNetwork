import { create } from 'zustand'

export type UiMode = 'classic' | 'workbench'

const STORAGE_KEY = 'intnetwork-ui-mode-v1'

export const parseUiMode = (value: string | null | undefined): UiMode | null =>
  value === 'classic' || value === 'workbench' ? value : null

export const resolveUiMode = (search = '', stored?: string | null): UiMode => {
  const preview = parseUiMode(new URLSearchParams(search).get('ui'))
  return preview ?? parseUiMode(stored) ?? 'workbench'
}

export const readUiMode = (search: string, readStored: () => string | null): UiMode => {
  try {
    return resolveUiMode(search, readStored())
  } catch {
    return resolveUiMode(search)
  }
}

const initialMode = typeof window === 'undefined'
  ? 'workbench'
  : readUiMode(window.location.search, () => window.localStorage.getItem(STORAGE_KEY))

interface UiModeState {
  mode: UiMode
  setMode: (mode: UiMode) => void
}

export const useUiModeStore = create<UiModeState>((set) => ({
  mode: initialMode,
  setMode: (mode) => {
    set({ mode })
    try {
      if (typeof window !== 'undefined') window.localStorage.setItem(STORAGE_KEY, mode)
    } catch {
      // Der Modus funktioniert für die aktuelle Seite auch ohne Browser-Persistenz.
    }
  },
}))
