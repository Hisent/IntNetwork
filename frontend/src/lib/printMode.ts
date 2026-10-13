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
    let theme: string | undefined
    const on = () => {
      theme = document.documentElement.dataset.theme
      document.documentElement.dataset.theme = 'light'
      flushSync(() => setPrinting(true))
    }
    const off = () => {
      if (theme) document.documentElement.dataset.theme = theme
      setPrinting(false)
    }
    window.addEventListener('beforeprint', on)
    window.addEventListener('afterprint', off)
    return () => { window.removeEventListener('beforeprint', on); window.removeEventListener('afterprint', off) }
  }, [])
  return printing
}
