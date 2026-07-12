import { create } from 'zustand'
import { createJSONStorage, persist } from 'zustand/middleware'

type Role = 'trainer' | 'participant' | null

interface AuthState {
  token: string | null
  role: Role
  displayName: string | null
  setAuth: (token: string, role: Role, displayName?: string) => void
  logout: () => void
}

// Entfernt einmalig Tokens aus Versionen vor 1.4, die dauerhaft im Local
// Storage lagen. Die aktuelle Sitzung wird ausschließlich im Session Storage
// gehalten.
if (typeof window !== 'undefined') window.localStorage.removeItem('intnetwork-auth')

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      role: null,
      displayName: null,
      setAuth: (token, role, displayName) => set({ token, role, displayName: displayName ?? null }),
      logout: () => set({ token: null, role: null, displayName: null }),
    }),
    {
      name: 'intnetwork-auth',
      // Sitzungsbezogen statt dauerhaft: beim Schließen des Tabs/Browsers
      // verschwindet das Bearer-Token und bleibt nicht wochenlang im Local Storage.
      storage: createJSONStorage(() => sessionStorage),
    },
  ),
)
