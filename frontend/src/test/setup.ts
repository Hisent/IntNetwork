import { vi } from 'vitest'

// Node 22+ bringt eigene localStorage/sessionStorage-Globals mit, die ohne
// --localstorage-file dauerhaft undefined bleiben. Vitest übernimmt sie beim
// Zusammenführen der jsdom-Environment-Globals nicht neu (Filter auf bekannte
// Schlüssel), sodass window.localStorage in jsdom-Tests kaputt bliebe. Simpler
// In-Memory-Ersatz vor jedem Testmodul — einzelne Tests dürfen das per
// vi.stubGlobal weiterhin gezielt überschreiben (z.B. für eigene Fälle).
function createMemoryStorage(): Storage {
  const store = new Map<string, string>()
  return {
    getItem: (key: string) => store.get(key) ?? null,
    setItem: (key: string, value: string) => { store.set(key, String(value)) },
    removeItem: (key: string) => { store.delete(key) },
    clear: () => store.clear(),
    key: (index: number) => Array.from(store.keys())[index] ?? null,
    get length() { return store.size },
  } as Storage
}

vi.stubGlobal('localStorage', createMemoryStorage())
vi.stubGlobal('sessionStorage', createMemoryStorage())
