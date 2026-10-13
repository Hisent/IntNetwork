import { createContext, useContext, useEffect, useState } from 'react'
import { flushSync } from 'react-dom'

// Druckansicht (Spickzettel): Was CSS allein nicht kann — Diagramme im
// Endzustand, aufgedeckte Reveal-Blöcke, Reflexionsnotizen als Text — rendern
// die Blöcke anhand dieses Flags. Alles andere regeln print:-Klassen.
export const PrintContext = createContext(false)
export const usePrinting = () => useContext(PrintContext)

/** true, solange der Browser druckt (Knopf ODER Strg+P/Browsermenü). */
export function usePrintState(): boolean {
  const [printing, setPrinting] = useState(false)
  useEffect(() => {
    // flushSync: der Browser nimmt das DOM direkt nach `beforeprint` auf.
    // Gedruckt wird immer hell: die Dunkel-Palette (helle Schrift) wäre auf Papier unlesbar.
    // `active`: ein zweites beforeprint (ohne afterprint) darf nicht „light“ als Ausgangsthema merken.
    let theme: string | undefined
    let active = false
    const on = () => {
      if (!active) {
        active = true
        theme = document.documentElement.dataset.theme
        document.documentElement.dataset.theme = 'light'
      }
      flushSync(() => setPrinting(true))
    }
    const restore = () => {
      if (!active) return
      active = false
      if (theme) document.documentElement.dataset.theme = theme
      else delete document.documentElement.dataset.theme
    }
    const off = () => { restore(); setPrinting(false) }
    window.addEventListener('beforeprint', on)
    window.addEventListener('afterprint', off)
    // Unmount mitten im Druck (Navigation): das Thema trotzdem zurückstellen.
    return () => { window.removeEventListener('beforeprint', on); window.removeEventListener('afterprint', off); restore() }
  }, [])
  return printing
}
