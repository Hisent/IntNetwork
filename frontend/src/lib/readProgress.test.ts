import { beforeEach, describe, expect, it, vi } from 'vitest'
import { pruneOtherParticipants } from '@/lib/readProgress'

// node-Testumgebung hat kein localStorage -> Stub mit echter length/key()-API
// (Object.keys funktioniert auf einem Storage-Objekt nicht verlässlich).
function stubLocalStorage() {
  const store = new Map<string, string>()
  vi.stubGlobal('localStorage', {
    getItem: (k: string) => store.get(k) ?? null,
    setItem: (k: string, v: string) => store.set(k, v),
    removeItem: (k: string) => store.delete(k),
    clear: () => store.clear(),
    key: (i: number) => Array.from(store.keys())[i] ?? null,
    get length() { return store.size },
  })
  return store
}

describe('pruneOtherParticipants (Aufräumen an geteilten Browsern)', () => {
  beforeEach(() => {
    stubLocalStorage()
  })

  it('entfernt Lese-/Reflexions-/CLI-Keys fremder Teilnehmer', () => {
    localStorage.setItem('intnetwork-read-2-9-arp', '[0,1]')
    localStorage.setItem('intnetwork-reflect-2-9-arp-3', 'fremder text')
    localStorage.setItem('intnetwork-cli-2-9', '{}')

    pruneOtherParticipants(1)

    expect(localStorage.getItem('intnetwork-read-2-9-arp')).toBeNull()
    expect(localStorage.getItem('intnetwork-reflect-2-9-arp-3')).toBeNull()
    expect(localStorage.getItem('intnetwork-cli-2-9')).toBeNull()
  })

  it('behält Keys der aktuellen participantId', () => {
    localStorage.setItem('intnetwork-read-1-9-arp', '[0]')
    localStorage.setItem('intnetwork-reflect-1-9-arp-3', 'eigener text')

    pruneOtherParticipants(1)

    expect(localStorage.getItem('intnetwork-read-1-9-arp')).toBe('[0]')
    expect(localStorage.getItem('intnetwork-reflect-1-9-arp-3')).toBe('eigener text')
  })

  it('lässt Nicht-App- und nicht zuordenbare App-Keys unberührt', () => {
    localStorage.setItem('intnetwork-theme', 'dark')
    localStorage.setItem('some-other-app-key', 'wert')

    pruneOtherParticipants(1)

    expect(localStorage.getItem('intnetwork-theme')).toBe('dark')
    expect(localStorage.getItem('some-other-app-key')).toBe('wert')
  })
})
