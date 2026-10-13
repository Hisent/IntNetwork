/** Springt zum Block mit der Kennung `uid` (Suchtreffer, #b-<uid>) und setzt den
 *  Fokus darauf — Screenreader und Tab-Reihenfolge machen dort weiter.
 *  Blöcke darüber werden teils lazy geladen (Widgets, Diagramme) und schieben das
 *  Ziel nachträglich weg: solange sich die Seitenhöhe noch ändert, wird neu
 *  ausgerichtet — bis der Nutzer selbst scrollt/tippt, höchstens `settleMs`.
 *  Liefert die Aufräumfunktion. */
export function jumpToBlock(uid: string, settleMs = 4000): () => void {
  const target = [...document.querySelectorAll<HTMLElement>('[data-uid]')].find((el) => el.dataset.uid === uid)
  if (!target) return () => {}
  target.tabIndex = -1
  target.focus({ preventScroll: true })
  target.scrollIntoView()
  if (typeof ResizeObserver === 'undefined') return () => {}
  const observer = new ResizeObserver(() => target.scrollIntoView())
  const events = ['wheel', 'touchstart', 'keydown', 'mousedown'] as const
  const stop = () => {
    observer.disconnect()
    clearTimeout(timer)
    events.forEach((name) => window.removeEventListener(name, stop))
  }
  const timer = setTimeout(stop, settleMs)
  events.forEach((name) => window.addEventListener(name, stop, { passive: true }))
  observer.observe(document.body)
  return stop
}
