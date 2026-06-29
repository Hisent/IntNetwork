import { create } from 'zustand'
import { persist } from 'zustand/middleware'

type Role = 'trainer' | 'participant' | null

interface AuthState {
  token: string | null
  role: Role
  displayName: string | null
  setAuth: (token: string, role: Role, displayName?: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      role: null,
      displayName: null,
      setAuth: (token, role, displayName) => set({ token, role, displayName: displayName ?? null }),
      logout: () => set({ token: null, role: null, displayName: null }),
    }),
    { name: 'intnetwork-auth' },
  ),
)
