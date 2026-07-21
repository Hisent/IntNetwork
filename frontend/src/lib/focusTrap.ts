// Reine Hilfsfunktionen für den Fokus-Trap modaler Dialoge (z. B. GlossaryPanel).
// Ausgelagert, damit die Kernlogik – welche Geschwister-Elemente beim Öffnen
// eines Dialogs unerreichbar gemacht werden – ohne vollständiges
// Component-Rendering (Portal, React-Effekte) unit-getestet werden kann.

/** Liefert alle Kind-Elemente von `root`, außer `exclude` selbst. */
export function siblingsOf(root: ParentNode, exclude: Element): Element[] {
  return Array.from(root.children).filter((child) => child !== exclude)
}

/**
 * Macht die übergebenen Elemente per `inert`-Attribut für Fokus, Zeiger und
 * Screenreader unerreichbar. Damit zirkuliert Tab automatisch nur noch
 * innerhalb der verbleibenden (nicht-inerten) Elemente – ohne eigene
 * Tab-Zyklus-Logik.
 */
export function setInert(elements: Element[]): void {
  for (const element of elements) element.setAttribute('inert', '')
}

/** Macht zuvor per `setInert` gesperrte Elemente wieder erreichbar. */
export function clearInert(elements: Element[]): void {
  for (const element of elements) element.removeAttribute('inert')
}

const FOCUSABLE_SELECTOR = [
  'a[href]',
  'button:not([disabled])',
  'input:not([disabled])',
  'select:not([disabled])',
  'textarea:not([disabled])',
  '[tabindex]:not([tabindex="-1"])',
].join(', ')

/**
 * Liefert alle innerhalb `container` fokussierbaren Elemente in DOM-Reihenfolge.
 * `inert` allein reicht nicht als Tab-Zyklus: Chromium schickt den Fokus beim
 * Verlassen des letzten fokussierbaren Elements auf `<body>` statt zum ersten
 * Element zu springen (kein Browser-Chrome als nächstes Ziel). Diese Liste
 * dient daher als Grundlage für eine kleine, explizite Wrap-Logik.
 */
export function focusableElements(container: Element): HTMLElement[] {
  return Array.from(container.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR))
}
