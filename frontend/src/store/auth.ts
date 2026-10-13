import { create } from 'zustand'
import { createJSONStorage, persist } from 'zustand/middleware'

type Role = 'trainer' | 'participant' | null

interface AuthState {
  token: string | null
  role: Role
  displayName: string | null
  /** Die Teilnehmer-Sitzung wurde vom Server beendet (401: Token ungültig, Code
   *  zurückgesetzt, Kurs gelöscht) — Start- und Beitrittsseite zeigen dazu einmal
   *  einen Hinweis. Bewusstes Abmelden setzt es nicht. */
  sessionLost: boolean
  setAuth: (token: string, role: Role, displayName?: string) => void
  logout: () => void
  /** Erzwungenes Abmelden nach 401 (lib/api.ts). */
  expire: () => void
  dismissSessionLost: () => void
}

// Entfernt einmalig Tokens aus Versionen vor 1.4, die dauerhaft im Local
// Storage lagen. Die aktuelle Sitzung wird ausschließlich im Session Storage
// gehalten.
try {
  if (typeof window !== 'undefined') window.localStorage.removeItem('intnetwork-auth')
} catch {
  // localStorage blockiert (z.B. Cookies gesperrt) — darf den App-Start nicht verhindern.
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      role: null,
      displayName: null,
      sessionLost: false,
      setAuth: (token, role, displayName) => set({ token, role, displayName: displayName ?? null, sessionLost: false }),
      logout: () => set({ token: null, role: null, displayName: null, sessionLost: false }),
      // Der Hinweistext nennt Kurs-Code und Wiederaufnahme-Code — er gilt nur Teilnehmern;
      // Trainer landen ohnehin sichtbar auf dem Login.
      expire: () => set((state) => ({ token: null, role: null, displayName: null, sessionLost: state.role === 'participant' })),
      dismissSessionLost: () => set({ sessionLost: false }),
    }),
    {
      name: 'intnetwork-auth',
      // Sitzungsbezogen statt dauerhaft: beim Schließen des Tabs/Browsers
      // verschwindet das Bearer-Token und bleibt nicht wochenlang im Local Storage.
      storage: createJSONStorage(() => sessionStorage),
    },
  ),
)
