import { create } from 'zustand'
import { storedLang, storeLang, tf, type Lang, type STRINGS } from '@/lib/i18n'

// Geteilte Sprachwahl der Trainer-Oberfläche. Dieselbe Browser-Wahl (localStorage)
// wie bei den öffentlichen Seiten, aber als Store, damit der Umschalter in der
// Kopfzeile alle gemounteten Komponenten sofort umstellt.
export const useLangStore = create<{ lang: Lang; setLang: (lang: Lang) => void }>((set) => ({
  lang: storedLang() ?? 'de',
  setLang: (lang) => { storeLang(lang); set({ lang }) },
}))

export type TrKey = keyof typeof STRINGS['de']

/** `tr('key', { n: 3 })` in der gewählten Sprache. */
export function useTr() {
  const lang = useLangStore((s) => s.lang)
  return { lang, tr: (key: TrKey, vars?: Record<string, string | number>) => tf(lang, key, vars) }
}
