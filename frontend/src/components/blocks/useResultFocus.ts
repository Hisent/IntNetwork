import { useEffect, useRef } from 'react'

const CONTROLS = 'button:not(:disabled), input:not(:disabled), select:not(:disabled)'

/** Tastaturfokus bei „Prüfen“/„Nochmal“: der ausgelöste Knopf wird dabei disabled oder
 * verschwindet, der Fokus fiele auf <body>. Stattdessen: Ergebnis erscheint -> Fokus auf
 * `[role="status"]` im Block; Ergebnis verschwindet -> erstes bedienbares Element im Block.
 * Nur bei einem WECHSEL — ein beim Laden bereits gezeigtes Ergebnis stiehlt keinen Fokus. */
export function useResultFocus<T extends HTMLElement = HTMLDivElement>(shown: boolean) {
  const root = useRef<T>(null)
  const was = useRef(shown)
  useEffect(() => {
    if (was.current === shown) return
    was.current = shown
    root.current?.querySelector<HTMLElement>(shown ? '[role="status"]' : CONTROLS)?.focus()
  }, [shown])
  return root
}
